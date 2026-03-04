来源于B站：【Qwen3.5 图片反推提示词支持ComfyUI. 全新TE-llama反推节点高速版,再提速20%】https://www.bilibili.com/video/BV1viPvzJEha?vd_source=88bb58bee6e1773cd3c34354ab4ead37
在此我修复了模型卸载后无法重新加载问题。
# ComfyUI Qwen3.5 GGUF 本地图片推理插件 (Qwen VL)

这是一个专为 ComfyUI 设计的自定义节点，用于在本地运行 **Qwen3-VL** 和 **Qwen3.5-VL** (GGUF 格式) 多模态大模型，实现图片理解、视频帧分析和视觉问答功能。

## ✨ 主要特性

- **支持模型**: Qwen3-VL, Qwen3.5-VL (GGUF 格式)。
- **多模态能力**: 支持加载视觉投影模型 (mmproj)，实现图文混合输入。
- **灵活模式**:
  - **图片模式**: 分析单张图片。
  - **逐帧模式**: 对视频序列的每一帧单独进行描述。
  - **视频模式**: 抽取关键帧，作为整体上下文进行视频内容理解。
- **智能显存管理**: 
  - 提供独立的“卸载模型”节点，手动释放显存。
  - **自动重加载机制**: 模型卸载后，再次运行推理节点时，会自动检测并重新加载模型，无需手动重新连接或运行加载器节点（修复了旧版本的报错问题）。
- **参数微调**: 支持温度 (Temperature), Top-P, Top-K, 重复惩罚等完整生成参数控制。

## 📦 安装步骤

### 1. 安装插件
将本插件文件夹复制到 ComfyUI 的自定义节点目录：
`ComfyUI/custom_nodes/ComfyUI-Qwen3.5-llama-YUAN/`

### 2. 安装依赖 (重要)
进入插件目录，运行以下命令安装必要的 Python 库：

```bash
cd ComfyUI/custom_nodes/ComfyUI-Qwen3.5-llama-YUAN

pip install -r requirements.txt
