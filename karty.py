import random
import pygame
from kolory import *

# Definicje kart Szansa
karty_szansa = [
    {
        "tekst": "Przechodź na START\n(Zbierz 200 PLN)",
        "typ": "ruch",
        "pozycja": 0,
        "nagroda": 200
    },
    {
        "tekst": "Idź do DZIEKANATU\nJeśli przejdziesz przez START,\nzbierz 200 PLN",
        "typ": "ruch",
        "pozycja": 9
    },
    {
        "tekst": "Plagiat!!!\nZostałeś złapany na plagiacie\nIdziesz do dziekanatu\nNie przechodź przez START",
        "typ": "ruch",
        "pozycja": 9
    },
    {
        "tekst": "Nie wiesz jak działają ECTS\n Placisz:200 PLN",
        "typ": "platnosc",
        "kwota": -50
    },
    {
        "tekst": "Otrzymujesz stypendium\n150 PLN",
        "typ": "platnosc",
        "kwota": 150
    },
    {
        "tekst": "Oto Bilecik\nPłacisz od każdego budynku:\n- 25 PLN za każdy dom\n- 100 PLN za każdy hotel",
        "typ": "platnosc_budynki",
        "dom": -25,
        "hotel": -100
    },
    {
        "tekst": "Otrzymujesz nagrodę\nza udany projekt\n200 PLN",
        "typ": "platnosc",
        "kwota": 200
    },
    {
        "tekst": "ROśnijcie kwaitki zdrowe\nNatura przykuła twoją uwagę\nCofaj się o 3 pola",
        "typ": "ruch_relatywny",
        "pozycja": -3
    },
    {
        "tekst": "Idź do najbliższego\nAKADEMIKU\nJeśli jest własnością innego\ngracza, zapłać dwukrotność\nnormalnego czynszu",
        "typ": "ruch_specjalny",
        "cel": "akademik"
    },
    {
        "tekst": "Zostałeś wybrany na\nstarostę roku\nOtrzymaj od każdego\ngracza 50 PLN",
        "typ": "platnosc_od_graczy",
        "kwota": 50
    },
    {
        "tekst": "Otrzymujesz dodatkowe\nECTS za aktywność\n+3 ECTS",
        "typ": "ects",
        "kwota": 3
    },
    {
        "tekst": "Karta 'Wyjście z Poprawki'\nNastępny raz, gdy\nbędziesz w Poprawce,\nmożesz użyć tej karty,\naby wyjść",
        "typ": "wyjscie_z_wiezienia"
    }
]

# Definicje kart Kasa Studencka
karty_kasa_studencka = [
    {
        "tekst": "Przechodź na START\n(Zbierz 200 PLN)",
        "typ": "ruch",
        "pozycja": 0,
        "nagroda": 200
    },
    {
        "tekst": "Błąd banku na twoją korzyść\nZbierz 200 PLN",
        "typ": "platnosc",
        "kwota": 200
    },
    {
        "tekst": "Rachunek za mieszkanie\nw akademiku\nZapłać 50 PLN",
        "typ": "platnosc",
        "kwota": -50
    },
    {
        "tekst": "Otrzymujesz zwrot\nza ubezpieczenie zdrowotne\n20 PLN",
        "typ": "platnosc",
        "kwota": 20
    },
    {
        "tekst": "Idź na POPRAWKĘ\nIdź prosto na POPRAWKĘ\nNie przechodź przez START",
        "typ": "ruch",
        "pozycja": 27
    },
    {
        "tekst": "Otrzymujesz spadek\n100 PLN",
        "typ": "platnosc",
        "kwota": 100
    },
    {
        "tekst": "Zapłać składki na koło naukowe\n100 PLN lub 10% majątku\n(wybierz mniejszą kwotę)",
        "typ": "platnosc_procent",
        "kwota_stala": 100,
        "procent": 0.10
    },
    {
        "tekst": "Zbierasz środki\nna wyjazd integracyjny\nOtrzymaj od każdego\ngracza 10 PLN",
        "typ": "platnosc_od_graczy",
        "kwota": 10
    },
    {
        "tekst": "Płacisz za książki\n100 PLN",
        "typ": "platnosc",
        "kwota": -100
    },
    {
        "tekst": "Wygrywasz konkurs\nna najlepszy projekt\n25 PLN",
        "typ": "platnosc",
        "kwota": 25
    },
    {
        "tekst": "To są twoje urodziny\nKażdy gracz daje ci\n10 PLN",
        "typ": "platnosc_od_graczy",
        "kwota": 10
    },
    {
        "tekst": "Karta 'Wyjście z Poprawki'\nMożesz zatrzymać tę kartę\nlub sprzedać",
        "typ": "wyjscie_z_wiezienia"
    }
]

# Przetasowane talię kart
talia_szansa = karty_szansa.copy()
talia_kasa_studencka = karty_kasa_studencka.copy()

# Przetasuj karty na początku gry
random.shuffle(talia_szansa)
random.shuffle(talia_kasa_studencka)

# Karty specjalne w posiadaniu graczy

def przetasuj_karty():
    """Przetasowuje obie talie kart"""
    global talia_szansa, talia_kasa_studencka
    random.shuffle(talia_szansa)
    random.shuffle(talia_kasa_studencka)

def pobierz_karte_szansa():
    """Pobiera kartę z talii Szansa"""
    global talia_szansa
    if not talia_szansa:
        talia_szansa = karty_szansa.copy()
        random.shuffle(talia_szansa)
    return talia_szansa.pop()

def pobierz_karte_kasa_studencka():
    """Pobiera kartę z talii Kasa Studencka"""
    global talia_kasa_studencka
    if not talia_kasa_studencka:
        talia_kasa_studencka = karty_kasa_studencka.copy()
        random.shuffle(talia_kasa_studencka)
    return talia_kasa_studencka.pop()

def wykonaj_karte(karta, gracz_index, gracze):
    """Wykonuje akcję opisaną na karcie"""
    gracz = gracze[gracz_index]
    
    if karta["typ"] == "ruch":
        # Przesuń gracza na określoną pozycję
        stara_pozycja = gracz["pozycja"]
        nowa_pozycja = karta["pozycja"]
        
        # Sprawdź czy gracz przeszedł przez START
        if nowa_pozycja < stara_pozycja or karta.get("nagroda", 0) > 0:
            gracz["pieniadze"] += karta.get("nagroda", 200)
            
        gracz["pozycja"] = nowa_pozycja
        
    elif karta["typ"] == "ruch_relatywny":
        # Przesuń gracza o określoną liczbę pól
        stara_pozycja = gracz["pozycja"]
        nowa_pozycja = (stara_pozycja + karta["pozycja"]) % 40
        
        # Sprawdź czy gracz przeszedł przez START (tylko do przodu)
        if karta["pozycja"] > 0 and nowa_pozycja < stara_pozycja:
            gracz["pieniadze"] += 200
            
        gracz["pozycja"] = nowa_pozycja
        
    elif karta["typ"] == "platnosc":
        # Dodaj lub odejmij pieniądze
        gracz["pieniadze"] += karta["kwota"]
        
    elif karta["typ"] == "platnosc_procent":
        # Zapłać mniejszą z dwóch kwot
        kwota_procent = int(gracz["pieniadze"] * karta["procent"])
        kwota_do_zaplaty = min(karta["kwota_stala"], kwota_procent)
        gracz["pieniadze"] -= kwota_do_zaplaty
        
    elif karta["typ"] == "platnosc_od_graczy":
        # Otrzymaj pieniądze od innych graczy
        for i, inny_gracz in enumerate(gracze):
            if i != gracz_index:
                kwota = min(karta["kwota"], inny_gracz["pieniadze"])
                inny_gracz["pieniadze"] -= kwota
                gracz["pieniadze"] += kwota
                
    elif karta["typ"] == "platnosc_budynki":
        # Zapłać za budynki (implementacja zależy od systemu budynków)
        koszt = gracz.get("budynki", 0) * abs(karta["dom"])
        gracz["pieniadze"] += koszt  # koszt jest ujemny
        
    elif karta["typ"] == "ects":
        # Dodaj ECTS
        gracz["ects"] += karta["kwota"]
        
    elif karta["typ"] == "wyjscie_z_wiezienia":
        # Dodaj kartę do posiadanych przez gracza
        gracz['jail_free'] = 1;
        
    elif karta["typ"] == "ruch_specjalny":
        # Logika dla specjalnych ruchów (np. do najbliższego akademika)
        if karta["cel"] == "akademik":
            # Znajdź najbliższy akademik
            pozycja_gracza = gracz["pozycja"]
            najblizsza_pozycja = znajdz_najblizszy_akademik(pozycja_gracza)
            print(f"Gracz {gracz_index} przesuwa się do najbliższego akademika na pozycji {najblizsza_pozycja}")
            stara_pozycja = gracz["pozycja"]
            gracz["pozycja"] = najblizsza_pozycja
            
            # Sprawdź czy przeszedł przez START
            if najblizsza_pozycja < stara_pozycja:
                gracz["pieniadze"] += 200

def znajdz_najblizszy_akademik(pozycja_gracza):
    """Znajduje pozycję najbliższego akademika"""
    from pola import pola
    
    # Akademiki są na pozycjach: 5, 15, 25, 35
    pozycje_akademikow = []
    for i, pole in enumerate(pola):
        if pole["typ"] == "akademik":
            pozycje_akademikow.append(i)
    
    # Znajdź najbliższy akademik
    najblizszy = None
    najmniejsza_odleglosc = float('inf')
    
    for pos in pozycje_akademikow:
        odleglosc = (pos - pozycja_gracza) % 40
        if odleglosc < najmniejsza_odleglosc:
            najmniejsza_odleglosc = odleglosc
            najblizszy = pos
    
    return najblizszy

def narysuj_karte(ekran, karta, x, y, szerokosc, wysokosc):
    """Rysuje kartę na ekranie"""
    # Tło karty
    pygame.draw.rect(ekran, BIALY, (x, y, szerokosc, wysokosc), border_radius=10)
    pygame.draw.rect(ekran, CZARNY, (x, y, szerokosc, wysokosc), 3, border_radius=10)
    
    # Tytuł karty
    czcionka_tytul = pygame.font.SysFont('Arial', 20, bold=True)
    tytul = "SZANSA" if karta in karty_szansa else "KASA STUDENCKA"
    kolor_tytulu = CZERWONY if karta in karty_szansa else NIEBIESKI_TLO
    
    tekst_tytul = czcionka_tytul.render(tytul, True, kolor_tytulu)
    tytul_rect = tekst_tytul.get_rect(centerx=x + szerokosc//2, y=y + 10)
    ekran.blit(tekst_tytul, tytul_rect)
    
    # Tekst karty
    czcionka_tekst = pygame.font.SysFont('Arial', 14)
    linie = karta["tekst"].split('\n')
    
    for i, linia in enumerate(linie):
        tekst_surface = czcionka_tekst.render(linia, True, CZARNY)
        tekst_rect = tekst_surface.get_rect(centerx=x + szerokosc//2, y=y + 50 + i * 20)
        ekran.blit(tekst_surface, tekst_rect)


