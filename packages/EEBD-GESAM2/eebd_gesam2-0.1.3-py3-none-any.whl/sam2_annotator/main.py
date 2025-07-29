# src/sam2_annotator/main.py

import os
import sys
import torch
import traceback
import urllib.request
from appdirs import user_cache_dir
from importlib import resources


# 关键函数1: 安全地获取包内资源（如配置文件）的路径
def get_config_path(config_filename="sam2_hiera_l.yaml"):
    """使用 importlib.resources 安全地获取包内配置文件的路径"""
    try:
        # For Python 3.9+
        return resources.files('sam2_annotator').joinpath('configs').joinpath(config_filename)
    except (ImportError, AttributeError):
        # Fallback for Python 3.8
        with resources.path('sam2_annotator.configs', config_filename) as p:
            return p


# 关键函数2: 自动下载并缓存模型文件
def get_model_weights_path(model_name="sam2_hiera_large.pt"):
    """检查模型是否存在于用户缓存中，如果不存在则下载，并返回其路径。"""
    # !!重要!!: 你需要将你的 .pt 文件上传到某处，并在这里提供一个真实、稳定的直接下载链接
    # 例如，可以上传到 Hugging Face, GitHub Releases, 或其他云存储
    MODEL_URL = "https://dl.fbaipublicfiles.com/segment_anything_2/072824/sam2_hiera_large.pt"  # <<< 务必替换成你的模型链接

    cache_directory = user_cache_dir("EEBD_SAM2_Annotator", "EEBD-GESAM2")
    os.makedirs(cache_directory, exist_ok=True)
    model_path = os.path.join(cache_directory, model_name)

    if not os.path.exists(model_path):
        print(f"模型文件未找到。正在从以下链接下载 '{model_name}'...")
        print(f"URL: {MODEL_URL}")
        print(f"将保存到: {model_path}")
        try:
            with urllib.request.urlopen(MODEL_URL) as response, open(model_path, 'wb') as out_file:
                total_length = response.getheader('content-length')
                if total_length:
                    total_length = int(total_length)
                    dl = 0
                    block_sz = 8192
                    while True:
                        buffer = response.read(block_sz)
                        if not buffer: break
                        dl += len(buffer)
                        out_file.write(buffer)
                        done = int(50 * dl / total_length)
                        sys.stdout.write(
                            f"\r下载进度: [{'=' * done}{' ' * (50 - done)}] {dl / 1024 / 1024:.2f}MB / {total_length / 1024 / 1024:.2f}MB")
                        sys.stdout.flush()
                else:
                    out_file.write(response.read())
            print("\n模型下载完成！")
        except Exception as e:
            print(f"\n下载模型失败: {e}")
            if os.path.exists(model_path): os.remove(model_path)
            sys.exit(1)
    else:
        print(f"在缓存中找到模型: {model_path}")
    return model_path


# 程序的总入口点
def start():
    """此函数将作为命令行的入口点被调用"""
    print("--- EEBD-GESAM2 交互式标注工具 ---")

    # 确保使用CUDA（如果可用）
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"检测到设备: {device}")
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    try:
        # 从我们的包中相对导入主应用类
        from .app import InteractiveSAM2Annotator

        # 动态获取模型和配置的路径
        model_path = get_model_weights_path()
        config_path = str(get_config_path())

        # 创建并运行应用实例
        annotator = InteractiveSAM2Annotator(
            model_path=model_path,
            config_path=config_path,
            device=device,
            output_dir="./annotations_sam2_tool"  # 输出目录可以保持为当前工作目录下的子文件夹
        )
        print("UI界面已启动。")
        annotator.mainloop()

    except Exception as e:
        print(f"程序启动失败: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    start()