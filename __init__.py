# -*- coding: utf-8 -*-
"""
ComfyUI  Qwen3/Qwen3.5 (llama-cpp-python) 插件
"""

from .nodes import (
    QwenVL模型加载器,
    QwenVL图像推理,
    QwenVL卸载模型,
)

NODE_CLASS_MAPPINGS = {
    "QwenVL_ModelLoader": QwenVL模型加载器,
    "QwenVL_ImageInfer": QwenVL图像推理,
    "QwenVL_Unload": QwenVL卸载模型,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QwenVL_ModelLoader": "Qwen VL 模型加载器",
    "QwenVL_ImageInfer": "Qwen VL 图像推理",
    "QwenVL_Unload": "Qwen VL 卸载模型",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
