from enum import Enum


class BubbleEventTypeEnum(Enum):
    """
    需要冒泡的事件
    """
    left_click = "<Button-1>"
    right_click = "<Button-3>"


if __name__ == '__main__':
    for _, event_type in BubbleEventTypeEnum.__members__.items():
        print(_)
        print(event_type.value)
