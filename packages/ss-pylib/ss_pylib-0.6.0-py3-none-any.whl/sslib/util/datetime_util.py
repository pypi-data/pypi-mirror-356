import re
from datetime import datetime
from typing import Optional


class DatetimeUtil:
    @staticmethod
    def format_date(src: str, date_format: str = '%Y-%m-%d') -> Optional[str]:
        '''문자열 날짜를 형식화된(기본:YYYY-MM-DD) 문자열로 변경'''
        if not src:
            return None
        parts = [d for d in re.split(r'[^\d]', src) if d]
        if len(parts) < 3:
            return None
        year, month, day = parts[0], parts[1].zfill(2), parts[2].zfill(2)
        try:
            return datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').strftime(date_format)
        except ValueError:
            return None
