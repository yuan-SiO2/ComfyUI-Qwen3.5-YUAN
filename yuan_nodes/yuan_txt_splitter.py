import re

class YUAN_TXTParagraphSplitter:
    """
    文本段落分割 - 复刻终极修复版 V9
    1. 标题智能识别升级：支持规律性前缀+序号模式（如 XX1, XX2, XXX一, XXX二, XXX1XX, XXX2XX）。
    2. 数字提取修复：严格从原文提取。
    3. 输出模式稳定：解决卡死并优化逻辑。
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "", "placeholder": "输入需要分割段落的文本..."}),
                "分段方式": (["端口", "空行", "序号", "段落", "标题", "数字", "地址"], {"default": "空行"}),
                "段落优化": ("BOOLEAN", {"default": True, "label_on": "开启", "label_off": "关闭"}),
                "输出模式": ("BOOLEAN", {"default": False, "label_on": "开启", "label_off": "关闭"}),
                "输出段落": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1}),
                "输入端口": ("INT", {"default": 1, "min": 1, "max": 64, "step": 1}),
                "选取段落": ("STRING", {"default": "0", "placeholder": "例如: 1,3,5 (0或留空表示保留所有)"}),
                "筛选段落": ("INT", {"default": 0, "min": 0, "max": 1000, "step": 1}),
            },
            "optional": {
                **{f"any_{i}": ("*",) for i in range(1, 65)}
            }
        }

    RETURN_TYPES = ("INT", "STRING", *["STRING"] * 100)
    RETURN_NAMES = ("数", "总段", *[f"段落{i+1}" for i in range(100)])
    OUTPUT_IS_LIST = (False, True, *[False] * 100)
    
    FUNCTION = "process_text"
    CATEGORY = "YUAN_ALL"

    def process_text(self, text, 分段方式, 段落优化, 输出模式, 输出段落, 输入端口, 选取段落, 筛选段落, **kwargs):
        # --- 步骤 1: 基础分段 ---
        paragraphs = []
        
        # 合并所有输入源
        full_text = text if text else ""
        for i in range(1, 输入端口 + 1):
            val = kwargs.get(f"any_{i}")
            if val is not None:
                if 分段方式 == "端口":
                    if isinstance(val, list):
                        paragraphs.extend([str(x) for x in val])
                    else:
                        paragraphs.append(str(val))
                else:
                    if full_text and not full_text.endswith('\n'): full_text += "\n"
                    full_text += str(val)

        if 分段方式 != "端口":
            if 分段方式 == "空行":
                paragraphs = re.split(r'\n\s*\n', full_text)
            elif 分段方式 == "序号":
                # 识别常见的列表序号：1. / (1) / A. / 一、
                pattern = r'^(?:\d+[\.、]|[\(\（]\d+[\)\）]|[A-Za-z][\.、]|[一二三四五六七八九十百千万]+[、\.])'
                parts = re.split(f'({pattern})', full_text, flags=re.MULTILINE)
                if len(parts) > 1:
                    if parts[0].strip(): paragraphs.append(parts[0])
                    for i in range(1, len(parts), 2):
                        paragraphs.append(parts[i] + (parts[i+1] if i+1 < len(parts) else ""))
                else:
                    paragraphs = [full_text]
            elif 分段方式 == "段落":
                paragraphs = full_text.splitlines()
            elif 分段方式 == "标题":
                # 增强型标题智能识别：
                # 1. 经典章节：第x章/节/回/部分/单元
                # 2. 层级标题：1.1, 1.2.1, 一.1
                # 3. Markdown：# ## ###
                # 4. 规律性重复前缀+序号模式：
                #    - XX1, XX2, XX3 (前缀+阿拉伯数字)
                #    - XXX一, XXX二, XXX三 (前缀+中文数字)
                #    - XXX1XX, XXX2XX (中间嵌入数字)
                
                # 定义正则组件
                cn_nums = "一二三四五六七八九十百千万"
                # 捕捉行首出现的：(任意字符)+(数字或中文数字)+(可选的任意字符)
                # 限制：前缀长度1-10，防止整行被误判；数字后接标点或空格或直接换行
                # 这里使用组合正则：
                title_pattern = rf'^(?:' \
                                rf'第[{cn_nums}\d]+[章节回部分单元].*|' \
                                rf'(?:\d+\.)+\d+.*|' \
                                rf'#+\s+.*|' \
                                rf'.{{1,10}}[{cn_nums}\d]+(?:[\.、\s].*|(?:\s|$))' \
                                rf')'
                
                parts = re.split(f'({title_pattern})', full_text, flags=re.MULTILINE)
                if len(parts) > 1:
                    if parts[0].strip(): paragraphs.append(parts[0])
                    for i in range(1, len(parts), 2):
                        paragraphs.append(parts[i] + (parts[i+1] if i+1 < len(parts) else ""))
                else:
                    paragraphs = [full_text]
            elif 分段方式 == "数字":
                paragraphs = re.findall(r'\d+', full_text)
            elif 分段方式 == "地址":
                pattern = r'[a-zA-Z]:\\[^ \n\u4e00-\u9fa5]+'
                paragraphs = re.findall(pattern, full_text)
            else:
                paragraphs = [full_text]

        # --- 步骤 2: 段落优化 (文本清洗) ---
        if 段落优化:
            paragraphs = [p.strip() for p in paragraphs if p and p.strip()]
        else:
            paragraphs = [p for p in paragraphs if p is not None]

        # --- 步骤 3: 选取段落 (大过滤器) ---
        final_paragraphs = paragraphs
        is_select_all = (选取段落 == "0" or not 选取段落.strip())
        if not is_select_all:
            try:
                indices = []
                for part in 选取段落.replace('，', ',').split(','):
                    if part.strip().isdigit():
                        idx = int(part.strip()) - 1
                        if 0 <= idx < len(paragraphs):
                            indices.append(idx)
                if indices:
                    final_paragraphs = [paragraphs[i] for i in indices]
            except:
                pass

        # --- 步骤 4: 筛选段落 (小过滤器) ---
        if 筛选段落 == 0:
            filtered_paragraphs = final_paragraphs
        else:
            idx = 筛选段落 - 1
            if 0 <= idx < len(final_paragraphs):
                filtered_paragraphs = [final_paragraphs[idx]]
            else:
                filtered_paragraphs = []

        # --- 步骤 5: 输出模式控制 [总段] ---
        if 输出模式:
            main_output = filtered_paragraphs
        else:
            combined_text = "\n\n".join(filtered_paragraphs)
            main_output = [combined_text]

        # --- 步骤 6: 返回元组 ---
        results = [len(filtered_paragraphs), main_output]
        for i in range(100):
            if i < len(filtered_paragraphs):
                results.append(filtered_paragraphs[i])
            else:
                results.append("")
                
        return tuple(results)

NODE_CLASS_MAPPINGS = {
    "YUAN_TXTParagraphSplitter": YUAN_TXTParagraphSplitter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YUAN_TXTParagraphSplitter": "文本段落分割"
}
