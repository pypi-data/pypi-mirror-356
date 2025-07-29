import json
from typing import Any, Optional
from sslib.base.entity import Entity


class JsonUtil:
    @staticmethod
    def to_json(src: Any) -> Any:
        if src is None:
            return None

        if isinstance(src, list):
            elements = [JsonUtil.__to_json(item) for item in src]
            if not elements:
                return None
            return elements

        return JsonUtil.__to_json(src=src)

    @staticmethod
    def json_dumps(src: Any) -> Optional[str]:
        return json.dumps(obj=JsonUtil.to_json(src=src), ensure_ascii=False)

    @staticmethod
    def print_json(src: Any, indent: int | None = None):
        print(json.dumps(JsonUtil.to_json(src=src), indent=indent, ensure_ascii=False))

    @staticmethod
    def __to_json(src: Any):
        if isinstance(src, Entity):
            return src.to_dict()
        return src

    @staticmethod
    def from_json(src: Any, fallback: str = '[]') -> Any:
        if src is None:
            src = fallback
        return json.loads(src)
