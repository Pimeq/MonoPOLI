import random
from pola import pobierz_pole, pola
from constants import *
from karty import pobierz_karte_szansa, pobierz_karte_kasa_studencka, wykonaj_karte

def utworz_liste_graczy():
    """Creates new player list with current names from settings"""
    try:
        from ustawienia import nazwy_graczy
    except ImportError:
        nazwy_graczy = ["Gracz 1", "Gracz 2", "Gracz 3", "Gracz 4"]
    
    return [
        {KEY_NAZWA: nazwy_graczy[0], KEY_POZYCJA: 0, KEY_PIENIADZE: START_MONEY, KEY_KOLOR: CZERWONY_GRACZ, KEY_BUDYNKI: 0, KEY_ECTS: 0, KEY_JAIL_FREE: 0},
        {KEY_NAZWA: nazwy_graczy[1], KEY_POZYCJA: 0, KEY_PIENIADZE: START_MONEY, KEY_KOLOR: ZIELONY_GRACZ, KEY_BUDYNKI: 0, KEY_ECTS: 0, KEY_JAIL_FREE: 0},
        {KEY_NAZWA: nazwy_graczy[2], KEY_POZYCJA: 0, KEY_PIENIADZE: START_MONEY, KEY_KOLOR: NIEBIESKI_GRACZ, KEY_BUDYNKI: 0, KEY_ECTS: 0, KEY_JAIL_FREE: 0},
        {KEY_NAZWA: nazwy_graczy[3], KEY_POZYCJA: 0, KEY_PIENIADZE: START_MONEY, KEY_KOLOR: ZOLTY_GRACZ, KEY_BUDYNKI: 0, KEY_ECTS: 0, KEY_JAIL_FREE: 0}
    ]

# Domyślna lista graczy (będzie nadpisana w ekranie gry)
gracze = utworz_liste_graczy()

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
    """Moves player by specified number of fields on board"""
    global gracze, historia_ruchow
    
    stara_pozycja = gracze[gracz_index][KEY_POZYCJA]
    nowa_pozycja = (stara_pozycja + liczba_pol) % BOARD_SIZE

    # Add START bonus when passing START
    if nowa_pozycja < stara_pozycja:
        gracze[gracz_index][KEY_PIENIADZE] += START_BONUS
        gracze[gracz_index][KEY_ECTS] += 1
        print(f"Gracz {gracze[gracz_index][KEY_NAZWA]} przeszedł przez START i otrzymuje {START_BONUS} PLN oraz 1 ECTS")

    gracze[gracz_index][KEY_POZYCJA] = nowa_pozycja
    
    # Zapisz ruch w historii
    historia_ruchow.append({
        "gracz": gracz_index,
        "z_pozycji": stara_pozycja,
        "na_pozycje": nowa_pozycja,
        "rzut": liczba_pol
    })
    
    # Zwróć nową pozycję i nazwę pola
    pole = pobierz_pole(nowa_pozycja)
    print(f"Gracz {gracze[gracz_index][KEY_NAZWA]} przesunął się na pole {pole['nazwa']}")
      # Logika pól specjalnych
    if pole["typ"] == "podatek":
        # Pobierz opłatę
        gracze[gracz_index][KEY_PIENIADZE] -= pole["cena"]
        print(f"Gracz {gracze[gracz_index][KEY_NAZWA]} płaci {pole['cena']} PLN podatku")
    
    elif pole["typ"] == "narozne" and pole["nazwa"] == "IDŹ NA POPRAWKĘ":
        # Idź do więzienia
        if(gracze[gracz_index][KEY_JAIL_FREE] == 0):
            gracze[gracz_index][KEY_POZYCJA] = 9  # Dostosuj do nowego indeksu DZIEKANAT jeśli trzeba
            print(f"Gracz {gracze[gracz_index][KEY_NAZWA]} idzie na poprawkę (dziekanat)")
        else:
            gracze[gracz_index][KEY_JAIL_FREE] = 0;
    
    elif pole["typ"] == "specjalne" and pole["nazwa"] == "SZANSA":
        karta = pobierz_karte_szansa()
        print(f"Gracz {gracze[gracz_index][KEY_NAZWA]} wyciągnął kartę Szansa: {karta['tekst']}")
        wykonaj_karte(karta, gracz_index, gracze)
        return karta
    
    elif pole["typ"] == "specjalne" and pole["nazwa"] == "KASA STUDENCKA":
        karta = pobierz_karte_kasa_studencka()
        print(f"Gracz {gracze[gracz_index][KEY_NAZWA]} wyciągnął kartę Kasa Studencka: {karta['tekst']}")
        wykonaj_karte(karta, gracz_index, gracze)
        return karta
    
    return None

# Funkcja do zmiany tury
def nastepny_gracz():
    """Przełącza turę na następnego gracza"""
    global aktualny_gracz, tura_wykonana
    aktualny_gracz = (aktualny_gracz + 1) % len(gracze)
    tura_wykonana = False
    print(f"Tura gracza: {gracze[aktualny_gracz][KEY_NAZWA]}")
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
    if gracze[gracz_index][KEY_PIENIADZE] < pole["cena"]:
        return False
        
    # Kup pole
    gracze[gracz_index][KEY_PIENIADZE] -= pole["cena"]
    pole["wlasciciel"] = gracz_index
    
    # Dodaj budynek do statystyk gracza
    gracze[gracz_index][KEY_BUDYNKI] += 1
    
    print(f"Gracz {gracze[gracz_index][KEY_NAZWA]} kupił {pole['nazwa']} za {pole['cena']} PLN")
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
    """Resets game state to initial values"""
    global gracze, aktualny_gracz, ostatni_rzut, tura_wykonana, historia_ruchow
    
    for gracz in gracze:
        gracz[KEY_POZYCJA] = 0
        gracz[KEY_PIENIADZE] = START_MONEY
        gracz[KEY_BUDYNKI] = 0
        gracz[KEY_ECTS] = 0
    
    for pole in pola:
        pole[KEY_WLASCICIEL] = None
    
    aktualny_gracz = 0
    ostatni_rzut = [1, 1]
    tura_wykonana = False
    historia_ruchow = []
    
    print("Gra została zresetowana")


# Funkcja do liczenia czynszu za pole

def oblicz_czynsz(pole):
    """Oblicza wysokość czynszu za pole, uwzględniając domki"""
    base_rent = 0
    if pole["typ"] == "wydzial":
        base_rent = int(pole["cena"] * 0.4)
    elif pole["typ"] == "akademik":
        base_rent = 50
    elif pole["typ"] == "uslugi":
        base_rent = 75
    # Dodaj czynsz za domki (każdy domek +150% bazowego czynszu)
    domki = pole.get("domki", 0)
    if domki > 0:
        base_rent += int(base_rent * 1.5 * domki)
    return base_rent

# Funkcja do sprawdzania płatności czynszu

def sprawdz_platnosc(gracz_index, pozycja, gracze):
    """Sprawdza czy gracz musi zapłacić czynsz i wykonuje płatność"""
    pole = pobierz_pole(pozycja)
    
    # Sprawdź czy pole ma właściciela i czy to nie jest aktualny gracz
    if pole.get("wlasciciel") is not None and pole["wlasciciel"] != gracz_index:
        czynsz = oblicz_czynsz(pole)
        
        # Pobierz pieniądze od gracza
        if gracze[gracz_index]["pieniadze"] >= czynsz:
            gracze[gracz_index]["pieniadze"] -= czynsz
            gracze[pole["wlasciciel"]]["pieniadze"] += czynsz
            print(f"Gracz {gracze[gracz_index][KEY_NAZWA]} płaci {czynsz} PLN czynszu graczowi {gracze[pole['wlasciciel']][KEY_NAZWA]}")
            
            # Zwróć informacje potrzebne do wyświetlenia okna
            return {
                "kwota": czynsz,
                "platnik": gracz_index,
                "wlasciciel": pole["wlasciciel"],
                "pole": pole
            }
        else:
            # Gracz nie ma wystarczająco pieniędzy - zapłaci ile może
            kwota = gracze[gracz_index]["pieniadze"]
            gracze[gracz_index]["pieniadze"] = 0
            gracze[pole["wlasciciel"]]["pieniadze"] += kwota
            print(f"Gracz {gracze[gracz_index][KEY_NAZWA]} nie ma wystarczająco pieniędzy! Płaci tylko {kwota} PLN")
            
            # Zwróć informacje potrzebne do wyświetlenia okna
            return {
                "kwota": kwota,
                "platnik": gracz_index,
                "wlasciciel": pole["wlasciciel"],
                "pole": pole,
                "brak_pieniedzy": True
            }
    
    return None  # Brak płatności

# Victory checking function
def sprawdz_zwyciezce(gracze_lista):
    """Checks if any player reached ECTS win condition"""
    for gracz in gracze_lista:
        if gracz[KEY_ECTS] >= ECTS_TO_WIN:
            return gracz
    return None

# Funkcja do dodawania ECTS za kupno działki
def dodaj_ects_za_dzialke(gracz_index, gracze_lista):
    """Dodaje 1 ECTS za kupioną działkę"""
    gracze_lista[gracz_index][KEY_ECTS] += 1
    print(f"Gracz {gracze_lista[gracz_index][KEY_NAZWA]} otrzymuje 1 ECTS za kupioną działkę (łącznie: {gracze_lista[gracz_index][KEY_ECTS]})")

# Funkcja do dodawania ECTS za kupno domków
def dodaj_ects_za_domki(gracz_index, liczba_domkow, gracze_lista):
    """Dodaje ECTS za kupione domki (1 ECTS za każdy domek)"""
    gracze_lista[gracz_index][KEY_ECTS] += liczba_domkow
    print(f"Gracz {gracze_lista[gracz_index][KEY_NAZWA]} otrzymuje {liczba_domkow} ECTS za kupione domki (łącznie: {gracze_lista[gracz_index][KEY_ECTS]})")

# Funkcja debugująca - ustawia 30 ECTS dla aktualnego gracza
