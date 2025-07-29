# SAM2 交互式图像标注工具

[![PyPI version](https://img.shields.io/pypi/v/interactive-sam2-annotator.svg)](https://pypi.org/project/interactive-sam2-annotator/)
[![Python versions](https://img.shields.io/pypi/pyversions/interactive-sam2-annotator.svg)](https://pypi.org/project/interactive-sam2-annotator/)
[![License](https://img.shields.io/pypi/l/interactive-sam2-annotator.svg)](https://pypi.org/project/interactive-sam2-annotator/)

一个基于 Meta 的 **Segment Anything Model 2 (SAM2)** 和 Tkinter 构建的图形化、交互式图像分割与标注工具。它旨在提供一个简单易用、开箱即用的方式，利用强大的AI模型来辅助进行高精度的图像标注工作。

*(注意：上面的徽章在你将包成功发布到 PyPI 后才会生效。请将 `interactive-sam2-annotator` 替换为你在 `pyproject.toml` 中设定的最终包名)*

## 软件截图

*(强烈建议您将下方占位符替换为一张或多张实际的软件运行截图，这能极大地帮助用户理解工具的功能)*

![软件运行截图](https://user-images.githubusercontent.com/your-github-id/your-repo/assets/screenshot.png)

## 主要功能

* **✨ 智能分割**: 集成强大的 SAM2 模型，通过点击正/负点进行高质量的掩码预测，极大提升标注效率。
* **✏️ 手动微调**: 支持手动绘制多边形进行精确标注，或对AI生成的掩码进行补充和修正。
* **📝 标签编辑**: 方便地对已完成的标注区域进行标签修改、删除和管理。
* **🖱️ 多模式操作**: 在 "SAM标注"、"多边形" 和 "编辑标签" 模式间自由切换，应对不同标注场景。
* **🖼️ 便捷的视图控制**: 支持图像的无级缩放与平移，轻松处理高分辨率大图。
* **💾 会话管理**: 自动保存和加载上一次的标注会话，方便随时中断和继续工作。
* **📄 格式兼容**: 以与 [LabelMe](https://github.com/wkentaro/labelme) 兼容的 JSON 格式保存标注结果，便于下游任务处理。
* **🚀 自动下载**: 首次运行时自动从网络下载所需的模型权重，无需手动配置。

## 安装

安装过程分为**两个必要步骤**。请务必按顺序执行。

### ⚠️ 步骤 1: 安装前提依赖 `segment-anything-2`

本工具依赖于 Meta 官方的 `segment-anything-2` 库，它需要从其 GitHub 仓库直接安装。请打开你的终端（命令行/CMD/PowerShell）并运行以下命令：

```bash
pip install git+[https://github.com/facebookresearch/segment-anything-2.git](https://github.com/facebookresearch/segment-anything-2.git)
```

### 步骤 2: 安装本工具

完成上一步后，你可以通过 PyPI 直接安装本工具：

```bash
pip install interactive-sam2-annotator
```
*(请将 `interactive-sam2-annotator` 替换为你在 PyPI 上发布的实际包名)*

**注意**：在首次启动本工具时，程序会自动从网络下载所需的 SAM2 模型权重文件（大小可能为几GB），此过程可能需要一些时间，具体取决于你的网络状况。下载完成后，模型将被缓存，未来启动时将不再需要下载。

## 快速开始

安装完成后，你的系统中就有了一个新的命令行指令。直接在终端中运行它即可启动程序：

```bash
sam2-annotator
```
*(同样，请将 `sam2-annotator` 替换为你在 `pyproject.toml` 中定义的 `[project.scripts]` 命令名)*

程序启动后，会显示图形界面。你可以通过点击 "加载图像" 按钮来选择一个包含多张图片的文件夹，然后开始你的标注工作。

## 许可证

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。

## 致谢

本项目的开发离不开以下这些优秀的项目和社区：

* **[Segment Anything Model (SAM)](https://github.com/facebookresearch/segment-anything)** by Meta AI
* **[PyTorch](https://pytorch.org/)**
* **[OpenCV](https://opencv.org/)**
* **[Tkinter](https://docs.python.org/3/library/tkinter.html)**

---