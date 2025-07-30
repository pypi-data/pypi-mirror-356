# 文件名：time.py
# 作者：nairoads
# 日期：2025-06-18 15:22:37
# 描述：时间相关工具类，便于时间处理

from datetime import datetime, timedelta

class TimeUtils:
    """
    时间工具类
    """
    @staticmethod
    def current_time_ymd() -> str:
        """
        返回当前日期字符串，格式为20230420
        :return: 20230420
        """
        return datetime.now().strftime('%Y%m%d')

    @staticmethod
    def current_time_ymd_n(n: int) -> str:
        """
        当前时间往前推n天的日期
        :param n: 往前推的天数
        :return: 前n天的年月日
        """
        today = datetime.now()
        n_day = timedelta(days=n)
        result = (today - n_day).strftime('%Y%m%d')
        return result

__all__ = ["TimeUtils"] 