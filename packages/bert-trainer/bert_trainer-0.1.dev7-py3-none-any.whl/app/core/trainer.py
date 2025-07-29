import os

import loguru
from tqdm import tqdm

import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    pipeline
)
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split


def compute_metrics(p):
    """自定义评估指标"""
    preds = np.argmax(p.predictions, axis=1)
    return {
        "accuracy": accuracy_score(p.label_ids, preds),
        "f1": f1_score(p.label_ids, preds)
    }


class TopicDataset(Dataset):
    """自定义数据集处理类"""

    def __init__(self, texts, labels, tokenizer, MAX_LENGTH):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.MAX_LENGTH = MAX_LENGTH

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        content = str(self.texts[idx])
        label = self.labels[idx]

        encoding = self.tokenizer(
            content,
            max_length=self.MAX_LENGTH,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].flatten(),
            "attention_mask": encoding["attention_mask"].flatten(),
            "labels": torch.tensor(label, dtype=torch.long)
        }


class bert_trainer:
    def __init__(self, MODEL_NAME="hfl/chinese-bert-wwm-ext",
                 BATCH_SIZE=16,
                 NUM_EPOCHS=12,
                 MODEL_SAVE_PATH="./bert_topic_classifier",
                 TRAIN_PARQUET='../datasets/topic_raw_data.parquet',
                 OUTPUT_DIR="./results",
                 MAX_LENGTH=128
                 ):
        loguru.logger.info("Initializing BERT Trainer...")
        self.MODEL_NAME = MODEL_NAME
        self.BATCH_SIZE = BATCH_SIZE
        self.NUM_EPOCHS = NUM_EPOCHS
        self.MODEL_SAVE_PATH = MODEL_SAVE_PATH
        self.TRAIN_PARQUET = TRAIN_PARQUET
        self.OUTPUT_DIR = OUTPUT_DIR
        self.MAX_LENGTH = MAX_LENGTH

        assert os.path.exists(self.TRAIN_PARQUET), f"训练数据集文件不存在: {self.TRAIN_PARQUET}"

        loguru.logger.info(f"BERT Trainer initialized with model: {self.MODEL_NAME}")

    def read_dataset(self):
        """
        读取训练数据集
        :return:
        """
        df = pd.read_parquet(self.TRAIN_PARQUET)
        return df

    def train(self,
              x_dim_label: str = "topic",
              y_dim_label: str = "is_topic_meet_instructions"
              ):
        """训练函数"""
        # 加载数据
        df = self.read_dataset()
        texts = df[x_dim_label].tolist()
        labels = df[y_dim_label].tolist()

        # 划分训练集和验证集
        train_texts, val_texts, train_labels, val_labels = train_test_split(
            texts, labels, test_size=0.2, random_state=42
        )

        # 初始化分词器
        tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)

        # 创建数据集
        train_dataset = TopicDataset(train_texts, train_labels, tokenizer, self.MAX_LENGTH)
        val_dataset = TopicDataset(val_texts, val_labels, tokenizer, self.MAX_LENGTH)

        # 加载预训练模型
        model = AutoModelForSequenceClassification.from_pretrained(
            self.MODEL_NAME,
            num_labels=2
        )

        # 训练参数设置
        training_args = TrainingArguments(
            output_dir=self.OUTPUT_DIR,
            num_train_epochs=self.NUM_EPOCHS,
            per_device_train_batch_size=self.BATCH_SIZE,
            per_device_eval_batch_size=self.BATCH_SIZE,
            eval_strategy="epoch",
            save_strategy="epoch",
            logging_steps=50,
            load_best_model_at_end=True,
            metric_for_best_model="f1",
            greater_is_better=True,
            seed=42,
            fp16=torch.cuda.is_available(),
        )

        # 创建Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=compute_metrics
        )

        # 开始训练
        trainer.train()

        # 保存模型
        model.save_pretrained(self.MODEL_SAVE_PATH)
        tokenizer.save_pretrained(self.MODEL_SAVE_PATH)
        loguru.logger.success(f"模型已保存至 {self.MODEL_SAVE_PATH}")

    def predict(self, texts: list):
        """
        批量预测文本分类结果
        :param texts:
        :return:
        """
        model_path = self.MODEL_SAVE_PATH
        predict_batch_size = self.BATCH_SIZE
        # 加载模型和分词器
        tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)

        # 设备配置
        main_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        model = model.to(main_device)

        # 多GPU处理 (兼容属性传递)
        if torch.cuda.device_count() > 1:
            print(f"使用 {torch.cuda.device_count()} 块GPU")
            original_model = model  # 保存原始模型引用
            model = torch.nn.DataParallel(model)
            # 动态属性转发（关键修复）
            model.config = original_model.config
            model.device = main_device
            model.can_generate = getattr(original_model, "can_generate", False)

        # 创建pipeline
        classifier = pipeline(
            "text-classification",
            model=model,
            tokenizer=tokenizer,
            device=0 if torch.cuda.is_available() else -1,
            batch_size=predict_batch_size
        )

        # 转换数据为生成器以支持流式处理
        def text_generator():
            for text in texts:
                yield text

        # 实时进度显示
        results = []
        with tqdm(total=len(texts), desc="预测进度", unit="样本", dynamic_ncols=True) as pbar:
            for text in texts:
                try:
                    out = classifier(text, padding=True, truncation=True, max_length=self.MAX_LENGTH)
                    results.append(out[0])
                except Exception as e:
                    print(f"预测错误: 文本 {text[:50]}... 发生异常: {str(e)}")
                    loguru.logger.trace(e)
                finally:
                    pbar.update(1)
        return [{
            "label": int(res["label"].split("_")[-1]),
            "confidence": res["score"]
        } for res in results]

    def predict_parquet(
            self,
            input_path: str,
            output_path: str,
            x_dim_label: str = "topic",
            y_dim_label: str = "is_topic_meet_instructions",
    ) -> pd.DataFrame:
        """
        批量预测parquet文件并覆盖标签列

        Args:
            input_path (str): 输入parquet文件路径
            output_path (str): 输出parquet文件路径
            x_dim_label (str): 文本列名，默认'topic'
            y_dim_label (str): 待覆盖的标签列名，默认'is_topic_meet_instructions'

        Returns:
            pd.DataFrame: 包含预测结果的DataFrame
        """
        df = pd.read_parquet(input_path)
        texts = df[x_dim_label].tolist()
        predictions = self.predict(texts)
        df[y_dim_label] = [pred["label"] for pred in predictions]
        df["pred_confidence"] = [pred["confidence"] for pred in predictions]  # 新增置信度列

        # 保存结果
        df.to_parquet(output_path, index=False)
        print(f"预测结果已保存至 {output_path}")

        return df

    def predict_parquet_with_knowledgebase_questions(
            self,
            input_path: str,
            output_path: str,
            x_dim_label: str = "questions",
            y_dim_label: str = "is_topic_meet_instructions",
            batch_size: int = 256
    ) -> pd.DataFrame:
        # 读取数据
        df = pd.read_parquet(input_path)
        texts = df[x_dim_label].tolist()

        # 多GPU预测
        predictions = self.predict(texts)

        # 处理结果
        df[y_dim_label] = [pred["label"] for pred in predictions]
        df["pred_confidence"] = [pred["confidence"] for pred in predictions]
        df = df[df[y_dim_label] != 0]

        # 保存结果
        df.to_parquet(output_path, index=False)
        print(f"预测结果已保存至 {output_path}")
        return df


if __name__ == "__main__":
    # 训练模型
    # train_model()

    # 测试预测
    test_texts = [
        "如何配置SSL证书来提高网站安全性？",
        "请说明网络钓鱼攻击的基本原理",
        "Python编程基础教学"
    ]

    BT = bert_trainer()

    predictions = BT.predict(test_texts)
    for text, pred in zip(test_texts, predictions):
        print(f"文本：{text}")
        print(f"预测结果：{pred}\n")

    # predict_parquet('../datasets/input.parquet', '../datasets/output.parquet')
    BT.predict_parquet_with_knowledgebase_questions('../datasets/seed_prompts_20250416120441.parquet',
                                                    '../datasets/output.parquet')
