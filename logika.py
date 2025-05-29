import random
from pola import pobierz_pole, pola
from karty import pobierz_karte_szansa, pobierz_karte_kasa_studencka, wykonaj_karte

# Dane graczy (przykładowe)
gracze = [
    {"nazwa": "Jan", "pozycja": 0, "pieniadze": 1500, "kolor": (255, 50, 50), "budynki": 0, "ects": 0},
    {"nazwa": "Sołtys", "pozycja": 0, "pieniadze": 1500, "kolor": (50, 255, 50), "budynki": 0, "ects": 0},
    {"nazwa": "Doktor", "pozycja": 0, "pieniadze": 1500, "kolor": (50, 50, 255), "budynki": 0, "ects": 0},
    {"nazwa": "Analizator", "pozycja": 0, "pieniadze": 1500, "kolor": (255, 255, 50), "budynki": 0, "ects": 0}
]

# Aktualna tura gracza
aktualny_gracz = 0

# Stan wyrzuconych kostek
ostatni_rzut = [1, 1]
tura_wykonana = False

# Historia ruchów (dla statystyk)
historia_ruchow = []

# Funkcja do rzutu kostką
def rzut_kostka():
    """Symuluje rzut dwoma kostkami"""
    return [random.randint(1, 6), random.randint(1, 6)]

# Funkcja do przesunięcia gracza
def przesun_gracza(gracz_index, liczba_pol):
    """Przesuwa gracza o określoną liczbę pól"""
    global gracze, historia_ruchow
    
    stara_pozycja = gracze[gracz_index]["pozycja"]
    nowa_pozycja = (stara_pozycja + liczba_pol) % 40
    
    # Jeśli przekroczył START, dodaj 200 PLN
    if nowa_pozycja < stara_pozycja:
        gracze[gracz_index]["pieniadze"] += 200
        print(f"Gracz {gracze[gracz_index]['nazwa']} przeszedł przez START i otrzymuje 200 PLN")
    
    gracze[gracz_index]["pozycja"] = nowa_pozycja
    
    # Zapisz ruch w historii
    historia_ruchow.append({
        "gracz": gracz_index,
        "z_pozycji": stara_pozycja,
        "na_pozycje": nowa_pozycja,
        "rzut": liczba_pol
    })
    
    # Zwróć nową pozycję i nazwę pola
    pole = pobierz_pole(nowa_pozycja)
    print(f"Gracz {gracze[gracz_index]['nazwa']} przesunął się na pole {pole['nazwa']}")
      # Logika pól specjalnych
    if pole["typ"] == "podatek":
        # Pobierz opłatę
        gracze[gracz_index]["pieniadze"] -= pole["cena"]
        print(f"Gracz {gracze[gracz_index]['nazwa']} płaci {pole['cena']} PLN podatku")
    
    elif pole["typ"] == "specjalne" and pole["nazwa"] == "IDŹ NA POPRAWKĘ":
        # Idź do więzienia
        gracze[gracz_index]["pozycja"] = 10
        print(f"Gracz {gracze[gracz_index]['nazwa']} idzie na poprawkę (dziekanat)")
    
    elif pole["typ"] == "specjalne" and pole["nazwa"] == "SZANSA":
        # Wyciągnij kartę Szansa
        karta = pobierz_karte_szansa()
        print(f"Gracz {gracze[gracz_index]['nazwa']} wyciągnął kartę Szansa: {karta['tekst']}")
        wykonaj_karte(karta, gracz_index, gracze)
        return karta  # Zwróć kartę do wyświetlenia
    
    elif pole["typ"] == "specjalne" and pole["nazwa"] == "KASA STUDENCKA":
        # Wyciągnij kartę Kasa Studencka
        karta = pobierz_karte_kasa_studencka()
        print(f"Gracz {gracze[gracz_index]['nazwa']} wyciągnął kartę Kasa Studencka: {karta['tekst']}")
        wykonaj_karte(karta, gracz_index, gracze)
        return karta  # Zwróć kartę do wyświetlenia
      # Za każdy ruch dodaj ECTS
    gracze[gracz_index]["ects"] += 1
    
    # Zwróć nową pozycję (i kartę jeśli została wyciągnięta)
    return None  # Domyślnie brak karty

# Funkcja do zmiany tury
def nastepny_gracz():
    """Przełącza turę na następnego gracza"""
    global aktualny_gracz, tura_wykonana
    aktualny_gracz = (aktualny_gracz + 1) % len(gracze)
    tura_wykonana = False
    print(f"Tura gracza: {gracze[aktualny_gracz]['nazwa']}")
    return aktualny_gracz

# Funkcja do kupowania pola
def kup_pole(gracz_index, pozycja_pola):
    """Kupuje pole dla gracza"""
    global gracze
    
    pole = pobierz_pole(pozycja_pola)
    
    # Sprawdź czy pole można kupić
    if pole["typ"] not in ["wydzial", "akademik", "uslugi"] or pole["wlasciciel"] is not None:
        return False
        
    # Sprawdź czy gracz ma wystarczająco pieniędzy
    if gracze[gracz_index]["pieniadze"] < pole["cena"]:
        return False
        
    # Kup pole
    gracze[gracz_index]["pieniadze"] -= pole["cena"]
    pole["wlasciciel"] = gracz_index
    
    # Dodaj budynek do statystyk gracza
    gracze[gracz_index]["budynki"] += 1
    
    print(f"Gracz {gracze[gracz_index]['nazwa']} kupił {pole['nazwa']} za {pole['cena']} PLN")
    return True

# Funkcja do pobierania statystyk graczy
def pobierz_statystyki():
    """Zwraca statystyki graczy do wyświetlenia"""
    statystyki = []
    
    for i, gracz in enumerate(gracze):
        posiadane_pola = [p["nazwa"] for p in pola if p.get("wlasciciel") == i]
        
        statystyki.append({
            "nazwa": gracz["nazwa"],
            "pieniadze": gracz["pieniadze"],
            "ects": gracz["ects"],
            "budynki": gracz["budynki"],
            "pozycja": gracz["pozycja"],
            "pole": pobierz_pole(gracz["pozycja"])["nazwa"],
            "posiadane_pola": posiadane_pola
        })
    
    return statystyki

# Funkcja do resetowania gry
def resetuj_gre():
    """Resetuje stan gry do początkowego"""
    global gracze, aktualny_gracz, ostatni_rzut, tura_wykonana, historia_ruchow
    
    # Zresetuj graczy
    for gracz in gracze:
        gracz["pozycja"] = 0
        gracz["pieniadze"] = 1500
        gracz["budynki"] = 0
        gracz["ects"] = 0
    
    # Zresetuj pola
    for pole in pola:
        pole["wlasciciel"] = None
    
    # Zresetuj pozostałe zmienne stanu
    aktualny_gracz = 0
    ostatni_rzut = [1, 1]
    tura_wykonana = False
    historia_ruchow = []
    
    print("Gra została zresetowana")
