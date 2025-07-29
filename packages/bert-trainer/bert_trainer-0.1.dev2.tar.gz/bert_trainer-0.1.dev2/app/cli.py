import os

import typer

from app.core.trainer import bert_trainer

app = typer.Typer(
    name="bert-trainer",
    no_args_is_help=True
)


@app.command()
def train(
        china_mirror: bool = typer.Option(True, help="是否使用中国镜像"),
        MODEL_NAME: str = typer.Option("hfl/chinese-bert-wwm-ext", help="模型名称"),
        BATCH_SIZE: int = typer.Option(16, help="批处理大小"),
        NUM_EPOCHS: int = typer.Option(12, help="训练轮数"),
        MODEL_SAVE_PATH: str = typer.Option("./bert_topic_classifier", help="模型保存路径"),
        TRAIN_PARQUET: str = typer.Option('input.parquet', help="训练数据的Parquet文件路径"),
        OUTPUT_DIR: str = typer.Option("./results", help="输出目录"),
        MAX_LENGTH: int = typer.Option(128, help="最大序列长度"),
        x_dim_label: str = typer.Option("topic", help="特征标签"),
        y_dim_label: str = typer.Option("result", help="预测标签")
):
    if china_mirror:
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
    bertTrainer = bert_trainer(
        MODEL_NAME=MODEL_NAME,
        BATCH_SIZE=BATCH_SIZE,
        NUM_EPOCHS=NUM_EPOCHS,
        MODEL_SAVE_PATH=MODEL_SAVE_PATH,
        TRAIN_PARQUET=TRAIN_PARQUET,
        OUTPUT_DIR=OUTPUT_DIR,
        MAX_LENGTH=MAX_LENGTH,
    )
    bertTrainer.train(
        x_dim_label=x_dim_label,
        y_dim_label=y_dim_label
    )


@app.command()
def predict(
        china_mirror: bool = typer.Option(True, help="是否使用中国镜像"),
        MODEL_NAME: str = typer.Option("hfl/chinese-bert-wwm-ext", help="模型名称"),
        BATCH_SIZE: int = typer.Option(16, help="批处理大小"),
        NUM_EPOCHS: int = typer.Option(12, help="训练轮数"),
        MODEL_SAVE_PATH: str = typer.Option("./bert_topic_classifier", help="模型保存路径"),
        TRAIN_PARQUET: str = typer.Option('input.parquet', help="训练数据的Parquet文件路径"),
        OUTPUT_DIR: str = typer.Option("./results", help="输出目录"),
        MAX_LENGTH: int = typer.Option(128, help="最大序列长度"),
        texts: str = typer.Argument(..., help="待预测文本")
):
    if china_mirror:
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
    bertTrainer = bert_trainer(
        MODEL_NAME=MODEL_NAME,
        BATCH_SIZE=BATCH_SIZE,
        NUM_EPOCHS=NUM_EPOCHS,
        MODEL_SAVE_PATH=MODEL_SAVE_PATH,
        TRAIN_PARQUET=TRAIN_PARQUET,
        OUTPUT_DIR=OUTPUT_DIR,
        MAX_LENGTH=MAX_LENGTH,
    )
    bertTrainer.predict(
        texts=texts
    )


@app.command()
def predict_parquet(
        china_mirror: bool = typer.Option(True, help="是否使用中国镜像"),
        MODEL_NAME: str = typer.Option("hfl/chinese-bert-wwm-ext", help="模型名称"),
        BATCH_SIZE: int = typer.Option(16, help="批处理大小"),
        NUM_EPOCHS: int = typer.Option(12, help="训练轮数"),
        MODEL_SAVE_PATH: str = typer.Option("./bert_topic_classifier", help="模型保存路径"),
        TRAIN_PARQUET: str = typer.Option('input.parquet', help="训练数据的Parquet文件路径"),
        OUTPUT_DIR: str = typer.Option("./results", help="输出目录"),
        MAX_LENGTH: int = typer.Option(128, help="最大序列长度"),
        input_path: str = typer.Argument(..., help="输入的Parquet文件路径"),
        output_path: str = typer.Argument("output.parquet", help="输出的Parquet文件路径"),
        x_dim_label: str = typer.Option("topic", help="特征标签"),
        y_dim_label: str = typer.Option("result", help="预测标签")
):
    assert os.path.exists(input_path), f"输入的Parquet文件不存在: {input_path}"
    assert input_path.endswith('.parquet'), "输入文件必须是Parquet格式"
    assert output_path.endswith('.parquet'), "输出文件必须是Parquet格式"

    if china_mirror:
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
    bertTrainer = bert_trainer(
        MODEL_NAME=MODEL_NAME,
        BATCH_SIZE=BATCH_SIZE,
        NUM_EPOCHS=NUM_EPOCHS,
        MODEL_SAVE_PATH=MODEL_SAVE_PATH,
        TRAIN_PARQUET=TRAIN_PARQUET,
        OUTPUT_DIR=OUTPUT_DIR,
        MAX_LENGTH=MAX_LENGTH,
    )
    bertTrainer.predict_parquet(
        input_path=input_path,
        output_path=output_path,
        x_dim_label=x_dim_label,
        y_dim_label=y_dim_label
    )


def main():
    app()
