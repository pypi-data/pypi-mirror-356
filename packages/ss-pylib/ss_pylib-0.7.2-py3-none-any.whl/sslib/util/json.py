import json
from typing import Any, Optional
from sslib.base.entity import Entity


class JsonUtil:
    @staticmethod
    def dumps(src: Any) -> str:
        return json.dumps(obj=JsonUtil.to_json(src), ensure_ascii=False)

    @staticmethod
    def to_json(src: Any) -> Any:
        if src is None:
            return None
        if isinstance(src, list):
            return [JsonUtil.__to_json(item) for item in src]
        return JsonUtil.__to_json(src)

    @staticmethod
    def from_json(src: Optional[str], fallback: str = '[]') -> Any:
        try:
            return json.loads(src or fallback)
        except (TypeError, json.JSONDecodeError):
            return json.loads(fallback)

    @staticmethod
    def print_json(src: Any, indent: int | None = 2):
        print(json.dumps(JsonUtil.to_json(src), indent=indent, ensure_ascii=False))

    @staticmethod
    def __to_json(src: Any):
        return src.to_dict() if isinstance(src, Entity) else src
