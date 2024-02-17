from datetime import datetime


def timeDiff(time: str):
    givenTime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    currentTime = datetime.now()
    timeDiff = currentTime - givenTime

    seconds = int(timeDiff.total_seconds())
    minutes = int(seconds // 60)
    hours = int(minutes // 60)
    days = int(hours // 24)

    if days > 0:
        return f"{days}일 전"
    elif hours > 0:
        return f"{hours}시간 전"
    elif minutes > 0:
        return f"{minutes}분 전"
    elif seconds > 0:
        return f"{seconds}초 전"
    else:
        return "방금 전"
