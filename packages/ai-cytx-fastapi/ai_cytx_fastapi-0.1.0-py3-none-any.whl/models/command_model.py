from pydantic import BaseModel, validator
from typing import Optional, Dict, Any,Union

class CommandModel(BaseModel):
    """命令模型类

    CommandModel
    """
    command: str  # 操作类型：add|update|delete
    ownerType: Optional[Union[int, str]] = None
    type: str  # 数据类型
    id: Optional[Union[int, str]] = None  # 数据 ID（可选）
    data: Optional[Dict[str, Any]] = None
    
    @validator('ownerType', pre=True)
    def convert_owner_type(cls, value):
        if value is None:
            return value
        return str(value)
    
    @validator('id', pre=True)
    def convert_id(cls, value):
        if value is None:
            return value
        return str(value)
    