import pyfiglet
from typing import Dict, List, Union
from .core import Colors

def custom_print(text: str) -> None:
    """Печатает текст в виде ASCII-арта"""
    ascii_art = pyfiglet.figlet_format(text)
    print(ascii_art)

def color_print(text: str, color: str) -> None:
    """Печатает цветной текст"""
    color_code = getattr(Colors, color.upper(), Colors.RESET)
    print(f"{color_code}{text}{Colors.RESET}")

def calculate(print_of_val: int, *nums: float) -> None:
    """Выполняет вычисления с числами"""
    if not nums:
        print("Нет чисел для вычислений!")
        return
    if print_of_val == 1:
        print(f"Сумма: {sum(nums)}")
    elif print_of_val == 2:
        print(f"Сумма: {sum(nums)}")
        print(f"Среднее: {sum(nums)/len(nums):.2f}")

def print_menu(valueOfvar: int, *descriptions: str) -> None:
    """Печатает меню с заданными опциями"""
    max_length = max(len(desc) for desc in descriptions) if descriptions else 10
    menu_width = max(max_length + 8, 20)
    menu = f"╔{'═' * menu_width}╗\n"
    menu += f"║{'МЕНЮ'.center(menu_width)}║\n"
    menu += f"╠{'═' * menu_width}╣\n"
    for i in range(valueOfvar):
        desc = descriptions[i] if i < len(descriptions) else "..."
        menu_line = f"║ {i+1}. {desc.ljust(menu_width - 6)}  ║"
        menu += menu_line + "\n"
    menu += f"╚{'═' * menu_width}╝"
    print(menu)

def plot_bar(data: Dict[str, Union[int, float]], width: int = 50) -> None:
    """Рисует гистограмму в консоли"""
    max_val = max(data.values())
    for key, val in data.items():
        bar = '█' * int(val / max_val * width)
        print(f"{key:10} | {Colors.CYAN}{bar}{Colors.RESET} {val}")

def plot_pie(values: List[float], labels: List[str]) -> None:
    """Рисует круговую диаграмму в консоли"""
    total = sum(values)
    for label, val in zip(labels, values):
        percent = val / total * 100
        print(f"{label}: {'▣' * int(percent // 10)} {percent:.1f}%")