from enum import Enum

def calculate_percentage_davon(num: float, percentage: float):
    return percentage * num / 100
    # wie viel sind X % von Y

def calculate_percentage_dazu(num:float, percentage:float):
    return (percentage * num / 100) + num

def calculate_percentage_weg(num:float, percentage:float):
    value = (percentage * num / 100)
    num -= value
    return num

def calculate_percentage_satz(num:float, num2:float):
    pass


class Unit(Enum):
    davon = 1
    dazu = 2
    weg = 3
    satz = 4

    # ENUM nutzen um Optionen durchzurotieren für UI Anpassung