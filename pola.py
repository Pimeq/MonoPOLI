# pola.py - definicje pól na planszy MonoPOLI

# Definicje pól na planszy
pola = [
    {"nazwa": "START", "typ": "narozne", "cena": 0},
    {"nazwa": "WEEIA CTI", "typ": "wydzial", "cena": 60, "kolor": (150, 80, 40), "wlasciciel": None},
    {"nazwa": "KASA STUDENCKA", "typ": "specjalne", "cena": 0},
    {"nazwa": "WEEIA A10", "typ": "wydzial", "cena": 60, "kolor": (150, 80, 40), "wlasciciel": None},
    {"nazwa": "CZESNE", "typ": "podatek", "cena": 200},
    {"nazwa": "AKADEMIK V", "typ": "akademik", "cena": 200, "wlasciciel": None},
    {"nazwa": "FTIMS B10", "typ": "wydzial", "cena": 100, "kolor": (42, 150, 148), "wlasciciel": None},
    {"nazwa": "SZANSA", "typ": "specjalne", "cena": 0},
    {"nazwa": "FTIMS B14", "typ": "wydzial", "cena": 100, "kolor": (42, 150, 148), "wlasciciel": None},
    {"nazwa": "DZIEKANAT", "typ": "narozne", "cena": 0},
    {"nazwa": "TEMP", "typ": "wydzial", "cena": 140, "kolor": (180, 50, 120), "wlasciciel": None},
    {"nazwa": "INTERNET", "typ": "uslugi", "cena": 150, "wlasciciel": None},
    {"nazwa": "WEEIA DMCS", "typ": "wydzial", "cena": 140, "kolor": (180, 50, 120), "wlasciciel": None},
    {"nazwa": "AKWARIUM", "typ": "wydzial", "cena": 160, "kolor": (180, 50, 120), "wlasciciel": None},
    {"nazwa": "AKADEMIK I", "typ": "akademik", "cena": 200, "wlasciciel": None},
    {"nazwa": "CHEMICZNY ALCHEMIUM", "typ": "wydzial", "cena": 180, "kolor": (255, 140, 0), "wlasciciel": None},
    {"nazwa": "KASA STUDENCKA", "typ": "specjalne", "cena": 0},
    {"nazwa": "CHEMICZNY IŁ7", "typ": "wydzial", "cena": 180, "kolor": (255, 140, 0), "wlasciciel": None},
    {"nazwa": "PARKING", "typ": "narozne", "cena": 0},
    {"nazwa": "BINOZ A3", "typ": "wydzial", "cena": 220, "kolor": (255, 0, 0), "wlasciciel": None},
    {"nazwa": "SZANSA", "typ": "specjalne", "cena": 0},
    {"nazwa": "BINOZ IŁ4", "typ": "wydzial", "cena": 220, "kolor": (255, 0, 0), "wlasciciel": None},
    {"nazwa": "DZIAŁ WYDAWNICTW", "typ": "wydzial", "cena": 240, "kolor": (255, 0, 0), "wlasciciel": None},
    {"nazwa": "AKADEMIK II", "typ": "akademik", "cena": 200, "wlasciciel": None},
    {"nazwa": "TEMP", "typ": "wydzial", "cena": 260, "kolor": (255, 255, 0), "wlasciciel": None},
    {"nazwa": "KOLOKWIUM", "typ": "wydzial", "cena": 260, "kolor": (255, 255, 0), "wlasciciel": None},
    {"nazwa": "KSERO", "typ": "uslugi", "cena": 150, "wlasciciel": None},
    {"nazwa": "IDŹ NA POPRAWKĘ", "typ": "narozne", "cena": 0},
    {"nazwa": "MECHANICZNY A22", "typ": "wydzial", "cena": 300, "kolor": (0, 255, 0), "wlasciciel": None},
    {"nazwa": "MECHANICZNY A20", "typ": "wydzial", "cena": 300, "kolor": (0, 255, 0), "wlasciciel": None},
    {"nazwa": "KASA STUDENCKA", "typ": "specjalne", "cena": 0},
    {"nazwa": "OIZ LODEX", "typ": "wydzial", "cena": 320, "kolor": (0, 255, 0), "wlasciciel": None},
    {"nazwa": "AKADEMIK III", "typ": "akademik", "cena": 200, "wlasciciel": None},
    {"nazwa": "SZANSA", "typ": "specjalne", "cena": 0},
    {"nazwa": "DZIAŁ REKRUTACJI", "typ": "wydzial", "cena": 350, "kolor": (0, 0, 255), "wlasciciel": None},
    {"nazwa": "OPŁATA ZA OBRONĘ", "typ": "podatek", "cena": 100},
]

# Funkcja do pobierania pola na podstawie pozycji
def pobierz_pole(pozycja):
    """Pobiera informacje o polu o danej pozycji"""
    return pola[pozycja % len(pola)]

# Funkcja do pobierania nazwy pola
def pobierz_nazwe_pola(pozycja):
    """Pobiera nazwę pola o danej pozycji"""
    return pola[pozycja % len(pola)]["nazwa"]

# Funkcja do pobierania koloru pola (dla wydziałów)
def pobierz_kolor_pola(pozycja):
    """Pobiera kolor pola lub None jeśli pole nie ma koloru"""
    pole = pola[pozycja % len(pola)]
    return pole.get("kolor", None)

# Funkcja do pobierania typu pola
def pobierz_typ_pola(pozycja):
    """Pobiera typ pola o danej pozycji"""
    return pola[pozycja % len(pola)]["typ"]
