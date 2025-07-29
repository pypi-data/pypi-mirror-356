import click

from .pan import Pan123openAPI


@click.group()
def cli():
    """Pan123 CLI 工具"""
    pass


@cli.command()
@click.argument("filename", type=click.Path(exists=False))
@click.option("--onlyurl", is_flag=True, help="只获取下载链接")
@click.option("--overwrite", is_flag=True, help="覆盖已有文件")
def download(filename, onlyurl, overwrite):
    """下载文件"""
    pan = Pan123openAPI()
    try:
        result = pan.download(filename, onlyurl=onlyurl, overwrite=overwrite)
        if onlyurl:
            click.echo(result)
    except Exception as e:
        click.echo(f"下载失败: {e}", err=True)


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--upload-name", type=str, help="上传到云端的文件名")
@click.option("--parent-id", type=int, default=0, help="上传到哪个云端目录 ID")
@click.option("--overwrite", is_flag=True, help="是否覆盖云端同名文件")
@click.option(
    "--duplicate", type=int, default=None, help="同名文件策略（1保留, 2覆盖）"
)
@click.option("--contain-dir", is_flag=True, help="是否包含目录结构上传")
def upload(filename, upload_name, parent_id, overwrite, duplicate, contain_dir):
    """上传文件"""
    pan = Pan123openAPI()
    try:
        file_id = pan.upload(
            filename, upload_name, parent_id, overwrite, duplicate, contain_dir
        )
        click.echo(f"上传完成，文件 ID: {file_id}")
    except Exception as e:
        click.echo(f"上传失败: {e}", err=True)


if __name__ == "__main__":
    cli()
