import time
import sys
from tqdm import tqdm
from .core import Colors

def tqdm_use(rangeValue: int, desc: str, timeWait: float) -> None:
    """Использует tqdm для отображения прогресса"""
    for _ in tqdm(range(rangeValue), desc=desc):
        time.sleep(timeWait)

def progress_bar(iterations: int, desc: str = "Progress", color: str = "GREEN") -> None:
    """Отображает кастомный прогресс-бар"""
    color_code = getattr(Colors, color.upper(), Colors.GREEN)
    for i in range(iterations + 1):
        percent = i / iterations * 100
        bar = '▓' * int(percent // 2) + '░' * (50 - int(percent // 2))
        sys.stdout.write(f"\r{desc}: {color_code}{bar}{Colors.RESET} {percent:.1f}%")
        sys.stdout.flush()
        time.sleep(0.05)
    print()