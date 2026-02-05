from enum import Enum

mwst_brutto = 1.19
mwst_netto = 0.19


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
    return (num / num2) * 100

def calculate_percentage_mwst_brutto(num: float):
    return num * mwst_brutto

def calculate_percentage_mwst_netto(num:float):
    value = (num / mwst_netto)
    num -= value
    return num

class Unit(Enum):
    davon = 1
    dazu = 2
    weg = 3
    satz = 4
    brutto = 5
    netto = 6

    # ENUM nutzen um Optionen durchzurotieren für UI Anpassung