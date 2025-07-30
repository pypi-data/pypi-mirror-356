import random
import re
import string
import time
from tkinter import Widget

from ttkplus.tkevents import BubbleEventTypeEnum


def unique_id(length=5) -> str:
    """
    生成随机ID
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def get_widget_size(widget):
    """
    获取组件的宽度和高度
    """
    widget.update_idletasks()

    width = widget.winfo_width()
    height = widget.winfo_height()
    return width, height


def camel_to_snake(camel_str):
    # 使用正则表达式找到所有大写字母，并在其前面插入下划线，然后将字符串转换为小写
    snake_str = re.sub(r'([A-Z])', r'_\1', camel_str).lower()
    # 移除字符串开头的多余下划线（如果有的话）
    if snake_str[0] == '_':
        snake_str = snake_str[1:]
    return snake_str


def bind_events(widget: Widget, handle_event):
    for _, enum in BubbleEventTypeEnum.__members__.items():
        widget.bind(enum.value, handle_event)


class Debounce:
    def __init__(self, func, wait_ms):
        self.func = func
        self.wait_ms = wait_ms  # 等待时间以毫秒为单位
        self.last_call_time = 0  # 上一次调用函数的时间戳
        self.args = None
        self.kwargs = None
        self.callback = None

    def call(self, *args, callback=None, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.callback = callback

        current_time = time.time()  # 获取当前时间戳（秒）
        elapsed_time = (current_time - self.last_call_time) * 1000  # 计算从上一次调用到现在经过的时间（毫秒）\
        if elapsed_time >= self.wait_ms:
            # 如果从上一次调用到现在的时间超过了等待时间，则立即执行函数
            self._execute_func()
        else:
            # 否则，重置上一次调用时间，但不执行函数
            self.last_call_time = current_time

    def _execute_func(self):
        result = self.func(*self.args, **self.kwargs)
        if self.callback:
            self.callback(result)  # 调用回调函数并传递结果
