import json
import re

def is_empty(value):
    """
    判断一个值是否为空。
    """
    if value is None:
        return True
    if isinstance(value, str) and str(value).strip() == "":
        return True
    if isinstance(value, (list, dict, tuple)) and len(value) == 0:
        return True
    if value in ["None", "null"]:
        return True
    return False



def safe_json_loads(json_str: str) -> dict:
    """
    处理 JSON 字符串，使其可以正确解析。
    """
    try:
        # 先尝试直接解析
        return json.loads(json_str)
    except json.JSONDecodeError:
        # 如果失败，预处理后再解析
        cleaned = preprocess_json_keys(json_str)
        return json.loads(cleaned)


def safe_get(data: dict, path: list, default=0.0):
    """
    安全地获取字典中的值，如果路径中的某个键不存在，则返回默认值。
    """
    if is_empty(data):
        return default
    current = data
    for key in path:
        try:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int) and 0 <= key < len(current):
                current = current[key]
            else:
                return default
        except Exception:
            return default
    return current



def preprocess_json_keys(json_str: str) -> str:
    """
    将 JSON 字符串中非字符串的 key 转换为字符串形式。

    例如：
        {6: "活期存款"} → {"6": "活期存款"}
    """
    # 使用正则匹配形如 `6:` 的键，并替换为 `"6":`
    processed = re.sub(r'([,{\s]+)(\d+)(\s*?:)', r'\1"\2"\3', json_str)
    return processed

def percent_to_float(s: str) -> float:
    """
    将百分比字符串如 '1,479%' 转换为浮点数（如 0.01479）
    """
    s = s.replace(',', '')   # 去除千分位逗号
    s = s.strip('%')         # 去除百分号
    return float(s) / 100
