from constants import *

# pola.py - definicje pól na planszy MonoPOLI

# Definicje pól na planszy
pola = [
    {KEY_NAZWA: "START", KEY_TYP: "narozne", KEY_CENA: 0},
    {KEY_NAZWA: "WEEIA CTI", KEY_TYP: "wydzial", KEY_CENA: 60, KEY_KOLOR: (150, 80, 40), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "KASA STUDENCKA", KEY_TYP: "specjalne", KEY_CENA: 0},
    {KEY_NAZWA: "WEEIA A10", KEY_TYP: "wydzial", KEY_CENA: 60, KEY_KOLOR: (150, 80, 40), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "CZESNE", KEY_TYP: "podatek", KEY_CENA: 200},
    {KEY_NAZWA: "AKADEMIK V", KEY_TYP: "akademik", KEY_CENA: 200, KEY_WLASCICIEL: None},
    {KEY_NAZWA: "FTIMS B10", KEY_TYP: "wydzial", KEY_CENA: 100, KEY_KOLOR: (42, 150, 148), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "SZANSA", KEY_TYP: "specjalne", KEY_CENA: 0},
    {KEY_NAZWA: "FTIMS B14", KEY_TYP: "wydzial", KEY_CENA: 100, KEY_KOLOR: (42, 150, 148), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "DZIEKANAT", KEY_TYP: "narozne", KEY_CENA: 0},
    {KEY_NAZWA: "TEMP", KEY_TYP: "wydzial", KEY_CENA: 140, KEY_KOLOR: (180, 50, 120), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "INTERNET", KEY_TYP: "uslugi", KEY_CENA: 150, KEY_WLASCICIEL: None},
    {KEY_NAZWA: "WEEIA DMCS", KEY_TYP: "wydzial", KEY_CENA: 140, KEY_KOLOR: (180, 50, 120), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "AKWARIUM", KEY_TYP: "wydzial", KEY_CENA: 160, KEY_KOLOR: (180, 50, 120), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "AKADEMIK I", KEY_TYP: "akademik", KEY_CENA: 200, KEY_WLASCICIEL: None},
    {KEY_NAZWA: "CHEMICZNY ALCHEMIUM", KEY_TYP: "wydzial", KEY_CENA: 180, KEY_KOLOR: (255, 140, 0), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "KASA STUDENCKA", KEY_TYP: "specjalne", KEY_CENA: 0},
    {KEY_NAZWA: "CHEMICZNY IŁ7", KEY_TYP: "wydzial", KEY_CENA: 180, KEY_KOLOR: (255, 140, 0), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "PARKING", KEY_TYP: "narozne", KEY_CENA: 0},
    {KEY_NAZWA: "BINOZ A3", KEY_TYP: "wydzial", KEY_CENA: 220, KEY_KOLOR: (255, 0, 0), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "SZANSA", KEY_TYP: "specjalne", KEY_CENA: 0},
    {KEY_NAZWA: "BINOZ IŁ4", KEY_TYP: "wydzial", KEY_CENA: 220, KEY_KOLOR: (255, 0, 0), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "DZIAŁ WYDAWNICTW", KEY_TYP: "wydzial", KEY_CENA: 240, KEY_KOLOR: (255, 0, 0), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "AKADEMIK II", KEY_TYP: "akademik", KEY_CENA: 200, KEY_WLASCICIEL: None},
    {KEY_NAZWA: "TEMP", KEY_TYP: "wydzial", KEY_CENA: 260, KEY_KOLOR: (255, 255, 0), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "KOLOKWIUM", KEY_TYP: "wydzial", KEY_CENA: 260, KEY_KOLOR: (255, 255, 0), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "KSERO", KEY_TYP: "uslugi", KEY_CENA: 150, KEY_WLASCICIEL: None},
    {KEY_NAZWA: "IDŹ NA POPRAWKĘ", KEY_TYP: "narozne", KEY_CENA: 0},
    {KEY_NAZWA: "MECHANICZNY A22", KEY_TYP: "wydzial", KEY_CENA: 300, KEY_KOLOR: (0, 255, 0), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "MECHANICZNY A20", KEY_TYP: "wydzial", KEY_CENA: 300, KEY_KOLOR: (0, 255, 0), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "KASA STUDENCKA", KEY_TYP: "specjalne", KEY_CENA: 0},
    {KEY_NAZWA: "OIZ LODEX", KEY_TYP: "wydzial", KEY_CENA: 320, KEY_KOLOR: (0, 255, 0), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "AKADEMIK III", KEY_TYP: "akademik", KEY_CENA: 200, KEY_WLASCICIEL: None},
    {KEY_NAZWA: "SZANSA", KEY_TYP: "specjalne", KEY_CENA: 0},
    {KEY_NAZWA: "DZIAŁ REKRUTACJI", KEY_TYP: "wydzial", KEY_CENA: 350, KEY_KOLOR: (0, 0, 255), KEY_WLASCICIEL: None},
    {KEY_NAZWA: "OPŁATA ZA OBRONĘ", KEY_TYP: "podatek", KEY_CENA: 100},
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
