import pygame
import sys
import math 
from constants import *
from pola import pobierz_pole
from interfejs import narysuj_zaokraglony_prostokat, narysuj_logo_pl

# Funkcja do rysowania pojedynczego pola planszy - ulepszona wersja
def narysuj_pole(ekran, x, y, szerokosc, wysokosc, pole_id):
    """Rysuje pojedyncze pole planszy z uwzględnieniem jego typu - ulepszona wersja"""
    pole = pobierz_pole(pole_id)
    if pole_id%9 == 0:
        kolor_pola = SZARY_CIEMNY_POLE
    else:
        kolor_pola = BIALY
    # Rysuj tło pola z zaokrąglonymi rogami
    narysuj_zaokraglony_prostokat(ekran, kolor_pola, (x, y, szerokosc, wysokosc), 5)
    # Dla obramowania używamy natywnej funkcji pygame
    pygame.draw.rect(ekran, CZARNY, (x, y, szerokosc, wysokosc), 2, border_radius=5)
    # Dodaj kolorowy pasek dla wydziałów
    if pole[KEY_TYP] == "wydzial":
        kolor_wydzialu = pole[KEY_KOLOR]
        pasek_wysokosc = wysokosc // 5  # Zmniejszony rozmiar paska kolorowego
        # Używamy zwykłego prostokąta dla paska wydziału
        pygame.draw.rect(
            ekran, 
            kolor_wydzialu, 
            (x + 1, y + 1, szerokosc - 2, pasek_wysokosc),
            border_radius=4
        )
    # Dodaj ikony dla usług - ładniejsza ikona usług
    if pole[KEY_TYP] == "uslugi":
        ikona_padding = 4  # Zmniejszony padding ikony
        # Tło ikony
        pygame.draw.rect(
            ekran, 
            KOLOR_USLUGI_TLO, 
            (x + ikona_padding, y + ikona_padding, szerokosc - 2*ikona_padding, wysokosc//4),
            border_radius=2
        )
        # Ikona narzędzi
        pygame.draw.circle(
            ekran, 
            KOLOR_USLUGI_KOLO, 
            (x + szerokosc//2, y + wysokosc//6), 
            szerokosc//8
        )
        pygame.draw.circle(
            ekran, 
            KOLOR_USLUGI_KOLO_TLO, 
            (x + szerokosc//2, y + wysokosc//6), 
            szerokosc//12
        )
        # Prosty symbol narzędzia
        grubosc = 2  # Zmniejszona grubość linii
        dlugosc = szerokosc//5  # Zmniejszona długość linii
        pygame.draw.line(
            ekran, 
            KOLOR_USLUGI_KOLO, 
            (x + szerokosc//2 - dlugosc//2, y + wysokosc//6), 
            (x + szerokosc//2 + dlugosc//2, y + wysokosc//6), 
            grubosc
        )
        pygame.draw.line(
            ekran, 
            KOLOR_USLUGI_KOLO, 
            (x + szerokosc//2, y + wysokosc//6 - dlugosc//2), 
            (x + szerokosc//2, y + wysokosc//6 + dlugosc//2), 
            grubosc
        )
    # Dodaj tekst nazwy pola z lepszym formatowaniem
    nazwa = pole[KEY_NAZWA]
    rozmiar_czcionki = 11  # Zmniejszony domyślny rozmiar czcionki
    if len(nazwa) > 12:
        rozmiar_czcionki = 9
    if len(nazwa) > 16:
        rozmiar_czcionki = 7
    czcionka_nazwa = pygame.font.SysFont('Arial', rozmiar_czcionki, bold=True)
    tekst_y_offset = 0
    if pole[KEY_TYP] == "wydzial":
        tekst_y_offset = wysokosc // 10  # Zmniejszone przesunięcie
    max_linia_dlugosc = 10  # Zmniejszona maksymalna długość linii
    # Podziel długie nazwy na kilka linii bardziej inteligentnie
    if len(nazwa) > max_linia_dlugosc:
        slowa = nazwa.split()
        linii = []
        aktualna_linia = ""
        for slowo in slowa:
            if len(aktualna_linia + " " + slowo) <= max_linia_dlugosc:
                aktualna_linia += " " + slowo if aktualna_linia else slowo
            else:
                linii.append(aktualna_linia)
                aktualna_linia = slowo
        if aktualna_linia:
            linii.append(aktualna_linia)
        for i, linia in enumerate(linii):
            tekst = czcionka_nazwa.render(linia, True, CZARNY)
            tekst_rect = tekst.get_rect(center=(
                x + szerokosc//2, 
                y + wysokosc//2 + tekst_y_offset + (i - len(linii)//2) * (rozmiar_czcionki + 1)
            ))
            ekran.blit(tekst, tekst_rect)
    else:
        tekst = czcionka_nazwa.render(nazwa, True, CZARNY)
        tekst_rect = tekst.get_rect(center=(x + szerokosc//2, y + wysokosc//2 + tekst_y_offset))
        ekran.blit(tekst, tekst_rect)
    # Dodaj cenę dla wydziałów, akademików i usług z lepszym formatowaniem
    if pole[KEY_TYP] in ["wydzial", "akademik", "uslugi"]:
        czcionka_cena = pygame.font.SysFont('Arial', 10, bold=True)  # Zmniejszony rozmiar czcionki
        tekst_cena = czcionka_cena.render(f"{pole[KEY_CENA]} PLN", True, CZARNY)
        # Tło dla ceny
        tekst_szerokosc = tekst_cena.get_width() + 6  # Zmniejszony padding
        tekst_wysokosc = tekst_cena.get_height() + 2  # Zmniejszony padding
        narysuj_zaokraglony_prostokat(
            ekran, 
            KOLOR_CENA_TLO, 
            (x + (szerokosc - tekst_szerokosc)//2, y + wysokosc - tekst_wysokosc - 3, 
             tekst_szerokosc, tekst_wysokosc), 
            3  # Mniejszy promień zaokrąglenia
        )
        # Tekst ceny wycentrowany
        ekran.blit(
            tekst_cena, 
            (x + (szerokosc - tekst_cena.get_width())//2, y + wysokosc - tekst_wysokosc - 2)
        )
    # Rysuj domki na nieruchomości, jeśli są
    if pole[KEY_TYP] in ["wydzial", "akademik", "uslugi"] and pole.get(KEY_DOMKI, 0) > 0:
        max_houses_inline = 4
        domki = pole[KEY_DOMKI]
        for i in range(min(domki, max_houses_inline)):
            house_width = szerokosc // 8
            house_height = wysokosc // 10
            house_x = x + 5 + i * (house_width + 2)
            house_y = y + wysokosc - house_height - 5
            pygame.draw.rect(ekran, KOLOR_DOMKU, (house_x, house_y, house_width, house_height), border_radius=2)
            pygame.draw.rect(ekran, CZARNY, (house_x, house_y, house_width, house_height), 1, border_radius=2)
        # Jeśli domków jest więcej niż 4, pokaż liczbę
        if domki > max_houses_inline:
            czcionka_domki = pygame.font.SysFont('Arial', 14, bold=True)
            tekst_domki = czcionka_domki.render(f"x{domki}", True, KOLOR_DOMKI_TEKST)
            ekran.blit(tekst_domki, (x + szerokosc//2 - tekst_domki.get_width()//2, y + wysokosc - house_height - 22))
# Poprawiona funkcja oblicz_pozycje_gracza
# Funkcja do obliczania współrzędnych pozycji gracza na planszy - ulepszona
def oblicz_pozycje_gracza(plansza_x, plansza_y, plansza_rozmiar, pozycja, i, gracze_count=4):
    """
    Oblicza współrzędne gracza na planszy na podstawie pozycji - wersja klasyczna Monopoly
    i - indeks gracza (potrzebny do przesunięcia, by pionki się nie nakładały)
    gracze_count - całkowita liczba graczy (wpływa na rozmieszczenie)
    """
    rozmiar_pola_naroza = 120
    rozmiar_pola_bok_szer = 70
    rozmiar_pola_bok_wys = 120
    
    pozycja = pozycja % 36

    # Rozmieszczenie pionków graczy na polu (żeby się nie nakładały)
    if gracze_count <= 4:
        kat = (i / gracze_count) * 6.28
        promien = min(15, 25 - gracze_count * 3)
        przesun_x = int(promien * math.cos(kat))
        przesun_y = int(promien * math.sin(kat))
    else:
        przesun_x = ((i % 3) - 1) * 15
        przesun_y = ((i // 3) - 1) * 15

    # Narożniki: 0, 9, 18, 27
    if pozycja == 0:  # START (lewy dolny róg)
        x = plansza_x + rozmiar_pola_naroza // 2 + przesun_x
        y = plansza_y + plansza_rozmiar - rozmiar_pola_naroza // 2 + przesun_y
    elif pozycja == 9:  # DZIEKANAT (lewy górny róg)
        x = plansza_x + rozmiar_pola_naroza // 2 + przesun_x
        y = plansza_y + rozmiar_pola_naroza // 2 + przesun_y
    elif pozycja == 18:  # PARKING (prawy górny róg)
        x = plansza_x + plansza_rozmiar - rozmiar_pola_naroza // 2 + przesun_x
        y = plansza_y + rozmiar_pola_naroza // 2 + przesun_y
    elif pozycja == 27:  # IDŹ NA POPRAWKĘ (prawy dolny róg)
        x = plansza_x + plansza_rozmiar - rozmiar_pola_naroza // 2 + przesun_x
        y = plansza_y + plansza_rozmiar - rozmiar_pola_naroza // 2 + przesun_y
    # Lewa krawędź (1-8)
    elif 1 <= pozycja <= 8:
        x = plansza_x + rozmiar_pola_naroza // 2 + przesun_x
        y = plansza_y + plansza_rozmiar - rozmiar_pola_naroza - (pozycja - 1) * rozmiar_pola_bok_szer - rozmiar_pola_bok_szer // 2 + przesun_y
    # Górna krawędź (10-17)
    elif 10 <= pozycja <= 17:
        x = plansza_x + rozmiar_pola_naroza + (pozycja - 10) * rozmiar_pola_bok_szer + rozmiar_pola_bok_szer // 2 + przesun_x
        y = plansza_y + rozmiar_pola_naroza // 2 + przesun_y
    # Prawa krawędź (19-26)
    elif 19 <= pozycja <= 26:
        x = plansza_x + plansza_rozmiar - rozmiar_pola_naroza // 2 + przesun_x
        y = plansza_y + rozmiar_pola_naroza + (pozycja - 19) * rozmiar_pola_bok_szer + rozmiar_pola_bok_szer // 2 + przesun_y
    # Dolna krawędź (28-35)
    elif 28 <= pozycja <= 35:
        x = plansza_x + plansza_rozmiar - rozmiar_pola_naroza - (pozycja - 28) * rozmiar_pola_bok_szer - rozmiar_pola_bok_szer // 2 + przesun_x
        y = plansza_y + plansza_rozmiar - rozmiar_pola_naroza // 2 + przesun_y
    else:
        x, y = plansza_x + plansza_rozmiar // 2, plansza_y + plansza_rozmiar // 2
    return x, y

# Funkcja do rysowania planszy MonoPOLI - ulepszona wersja z obsługą skalowalności
def narysuj_plansze(ekran, gracze, skala=1):
    """Rysuje planszę do gry MonoPOLI - ulepszona wersja z obsługą skalowalności"""
    # Bazowy rozmiar planszy (zawsze ten sam, niezależnie od skali)
    bazowy_rozmiar = 800
    
    # Utwórz surface planszy o bazowym rozmiarze
    plansza_surface = pygame.Surface((bazowy_rozmiar, bazowy_rozmiar), pygame.SRCALPHA)
    
    # Wszystkie rysowanie odbywa się na surface z bazowymi współrzędnymi
    surface_x = 0
    surface_y = 0
    surface_rozmiar = bazowy_rozmiar
    
    # Tło planszy z cieniem na surface
    # Cień
    pygame.draw.rect(plansza_surface, (30, 30, 60), (surface_x + 8, surface_y + 8, surface_rozmiar, surface_rozmiar), border_radius=12)
    # Główna plansza
    narysuj_zaokraglony_prostokat(plansza_surface, NIEBIESKI_POLE, (surface_x, surface_y, surface_rozmiar, surface_rozmiar), 10)
    
    # Ustawienia pól
    rozmiar_pola_naroza = 120  # Zmniejszony rozmiar pól narożnych
    rozmiar_pola_bok_szer = 70  # Zmniejszona szerokość pól bocznych
    rozmiar_pola_bok_wys = 120  # Zmniejszona wysokość pól bocznych
    
    # Środek planszy z ładniejszym tłem - dostosowany do nowych rozmiarów pól
    narysuj_zaokraglony_prostokat(
        plansza_surface, 
        CZERWONY_TLO, 
        (surface_x + rozmiar_pola_bok_wys, surface_y + rozmiar_pola_bok_wys, 
         surface_rozmiar - 2*rozmiar_pola_bok_wys, surface_rozmiar - 2*rozmiar_pola_bok_wys), 
        8
    )
    
    

    # Jednolity kolor na środku planszy z czarnym obramowaniem
    srodek_szer = surface_rozmiar - 2 * rozmiar_pola_bok_wys

    ss = pygame.Surface((srodek_szer, srodek_szer))
    ss.fill((139, 35, 29))  # Stały czerwony kolor
    ekran.blit(ss, (surface_x + rozmiar_pola_bok_wys, surface_y + rozmiar_pola_bok_wys))

    
    # Tytuł gry z cieniem
    czcionka_tytul = pygame.font.SysFont('Arial', 70, bold=True)
    # Cień

    tekst_mono_cien = czcionka_tytul.render("Mono", True, (119, 25, 19))
    tekst_poli_cien = czcionka_tytul.render("POLI", True, (119, 25, 19))
    plansza_surface.blit(tekst_mono_cien, (surface_x + surface_rozmiar//2 - 150 + 3, surface_y + surface_rozmiar//2 - 240 + 3))
    plansza_surface.blit(tekst_poli_cien, (surface_x + surface_rozmiar//2 + 25 + 3, surface_y + surface_rozmiar//2 - 200 + 3))

    
    # Tekst główny
    tekst_mono = czcionka_tytul.render("Mono", True, BIALY)
    tekst_poli = czcionka_tytul.render("POLI", True, CZERWONY)

    plansza_surface.blit(tekst_mono, (surface_x + surface_rozmiar//2 - 150, surface_y + surface_rozmiar//2 - 240))
    plansza_surface.blit(tekst_poli, (surface_x + surface_rozmiar//2 + 25, surface_y + surface_rozmiar//2 - 200))
    


    
    # Ładniejsze pionki kart pytań - dostosowane do nowych wymiarów planszy
    # Pierwsza karta
    karta_szer = 100  # Zmniejszona szerokość karty
    karta_wys = 160   # Zmniejszona wysokość karty
    

    # KARTA SZANSY (lewa)
    karta1_x = surface_x  + rozmiar_pola_bok_wys + 50
    karta1_y = surface_y  + surface_rozmiar//2 - 60

    # Jasno pomarańczowy środek i biała obramówka
    narysuj_zaokraglony_prostokat(plansza_surface, (255, 200, 100), (karta1_x, karta1_y, karta_szer, karta_wys), 6)
    pygame.draw.rect(plansza_surface, BIALY, (karta1_x, karta1_y, karta_szer, karta_wys), 4, border_radius=6)

    # Znak zapytania poziomo na środku karty
    czcionka_szansa = pygame.font.SysFont('Arial', 80, bold=True)
    tekst_szansa = czcionka_szansa.render("?", True, (255, 120, 0))
    tekst_szansa = pygame.transform.rotate(tekst_szansa, 0)  # poziomo
    tekst_rect = tekst_szansa.get_rect(center=(karta1_x + karta_szer // 2, karta1_y + karta_wys // 2))
    plansza_surface.blit(tekst_szansa, tekst_rect)

    # KARTA SZANSY (prawa)
    karta2_x = surface_x + surface_rozmiar  - rozmiar_pola_bok_wys - karta_szer - 50
    karta2_y = surface_y  + surface_rozmiar //2 - 60

    narysuj_zaokraglony_prostokat(plansza_surface, (255, 200, 100), (karta2_x, karta2_y, karta_szer, karta_wys), 6)
    pygame.draw.rect(plansza_surface, BIALY, (karta2_x, karta2_y, karta_szer, karta_wys), 4, border_radius=6)

    tekst_szansa2 = czcionka_szansa.render("?", True, (255, 120, 0))
    tekst_szansa2 = pygame.transform.rotate(tekst_szansa2, 0)
    tekst_rect2 = tekst_szansa2.get_rect(center=(karta2_x + karta_szer // 2, karta2_y + karta_wys // 2))
    plansza_surface.blit(tekst_szansa2, tekst_rect2)
    

    
    # Rysowanie pól na planszy - na surface
    # Narożniki
    narysuj_pole(plansza_surface, surface_x, surface_y + surface_rozmiar - rozmiar_pola_naroza, rozmiar_pola_naroza, rozmiar_pola_naroza, 0)  # START (lewy dolny róg)
    narysuj_pole(plansza_surface, surface_x, surface_y, rozmiar_pola_naroza, rozmiar_pola_naroza, 9)  # DZIEKANAT (lewy górny róg)
    narysuj_pole(plansza_surface, surface_x + surface_rozmiar - rozmiar_pola_naroza, surface_y, rozmiar_pola_naroza, rozmiar_pola_naroza, 18)  # PARKING (prawy górny róg)
    narysuj_pole(plansza_surface, surface_x + surface_rozmiar - rozmiar_pola_naroza, surface_y + surface_rozmiar - rozmiar_pola_naroza, rozmiar_pola_naroza, rozmiar_pola_naroza, 27)  # IDŹ NA POPRAWKĘ (prawy dolny róg)

    # Lewa krawędź (pola 1-8) - od dołu do góry
    for i in range(1, 9):
        narysuj_pole(
            plansza_surface,
            surface_x,
            surface_y + surface_rozmiar - rozmiar_pola_naroza - i * rozmiar_pola_bok_szer,
            rozmiar_pola_naroza,
            rozmiar_pola_bok_szer,
            i
        )

    # Górna krawędź (pola 10-17) - od lewej do prawej
    for i in range(10, 18):
        narysuj_pole(
            plansza_surface,
            surface_x + rozmiar_pola_naroza + (i - 10) * rozmiar_pola_bok_szer,
            surface_y,
            rozmiar_pola_bok_szer,
            rozmiar_pola_naroza,
            i
        )

    # Prawa krawędź (pola 19-26) - od góry do dołu
    for i in range(19, 27):
        narysuj_pole(
            plansza_surface,
            surface_x + surface_rozmiar - rozmiar_pola_naroza,
            surface_y + rozmiar_pola_naroza + (i - 19) * rozmiar_pola_bok_szer,
            rozmiar_pola_naroza,
            rozmiar_pola_bok_szer,
            i
        )

    # Dolna krawędź (pola 28-35) - od prawej do lewej
    for i in range(28, 36):
        narysuj_pole(
            plansza_surface,
            surface_x + surface_rozmiar - rozmiar_pola_naroza - (i - 27) * rozmiar_pola_bok_szer,
            surface_y + surface_rozmiar - rozmiar_pola_naroza,
            rozmiar_pola_bok_szer,
            rozmiar_pola_naroza,
            i
        )

    # Pozycje graczy na planszy - na surface z bazowymi współrzędnymi
    gracze_count = len(gracze)
    for i, gracz in enumerate(gracze):
        pozycja = gracz["pozycja"]
        x, y = oblicz_pozycje_gracza(surface_x, surface_y, surface_rozmiar, pozycja, i, gracze_count)
        
        # Rysuj ładniejszy pionek gracza z efektem 3D
        # Cień
        pygame.draw.circle(plansza_surface, (50, 50, 50), (x + 2, y + 2), 12)  # Zmniejszony rozmiar pionka
        # Główna część pionka
        pygame.draw.circle(plansza_surface, gracz["kolor"], (x, y), 12)
        # Odblaski
        pygame.draw.circle(plansza_surface, CZARNY, (x, y), 12, 1)  # Obramowanie
        # Wewnętrzny krąg
        pygame.draw.circle(plansza_surface, mix_color(gracz["kolor"], BIALY, 0.3), (x, y), 8)
        # Odblask
        pygame.draw.circle(plansza_surface, BIALY, (x - 3, y - 3), 3)
    
    # Skalowanie i blitowanie na główny ekran
    plansza_rozmiar = int(bazowy_rozmiar * skala)
    if skala != 1.0:
        plansza_surface = pygame.transform.scale(plansza_surface, (plansza_rozmiar, plansza_rozmiar))
    
    # Pozycja planszy na ekranie (wycentrowana)
    plansza_x = 50
    plansza_y = 50
    
    # Blituj przeskalowaną planszę na główny ekran
    ekran.blit(plansza_surface, (plansza_x, plansza_y))
    
    return plansza_x, plansza_y, plansza_rozmiar  # Zwracamy wymiary planszy do późniejszego użycia

# Funkcja do mieszania kolorów
def mix_color(color1, color2, factor):
    """Miesza dwa kolory z określonym współczynnikiem (0.0 - 1.0)"""
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = int(r1 * (1 - factor) + r2 * factor)
    g = int(g1 * (1 - factor) + g2 * factor)
    b = int(b1 * (1 - factor) + b2 * factor)
    return (r, g, b)