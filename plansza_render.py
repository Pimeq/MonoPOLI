import pygame
import sys
import math  # Dodany import math dla funkcji trygonometrycznych
from kolory import *
from pola import pobierz_pole
from interfejs import narysuj_zaokraglony_prostokat, narysuj_logo_pl

# Funkcja do rysowania pojedynczego pola planszy - ulepszona wersja
def narysuj_pole(ekran, x, y, szerokosc, wysokosc, pole_id):
    """Rysuje pojedyncze pole planszy z uwzględnieniem jego typu - ulepszona wersja"""
    pole = pobierz_pole(pole_id)
    kolor_pola = BIALY
    
    # Rysuj tło pola z zaokrąglonymi rogami
    narysuj_zaokraglony_prostokat(ekran, kolor_pola, (x, y, szerokosc, wysokosc), 5)
    # Dla obramowania używamy natywnej funkcji pygame
    pygame.draw.rect(ekran, CZARNY, (x, y, szerokosc, wysokosc), 2, border_radius=5)
    
    # Dodaj kolorowy pasek dla wydziałów
    if pole["typ"] == "wydzial":
        kolor_wydzialu = pole["kolor"]
        pasek_wysokosc = wysokosc // 5  # Zmniejszony rozmiar paska kolorowego
        # Używamy zwykłego prostokąta dla paska wydziału
        pygame.draw.rect(
            ekran, 
            kolor_wydzialu, 
            (x + 1, y + 1, szerokosc - 2, pasek_wysokosc),
            border_radius=4
        )
    
    # Dodaj ikony dla akademików - ładniejszy domek
    if pole["typ"] == "akademik":
        # Tło ikony
        ikona_padding = 4  # Zmniejszony padding ikony
        pygame.draw.rect(
            ekran, 
            (220, 250, 220), 
            (x + ikona_padding, y + ikona_padding, szerokosc - 2*ikona_padding, wysokosc//4),
            border_radius=2
        )
        
        # Domek
        pygame.draw.polygon(
            ekran, 
            (40, 140, 40), 
            [
                (x + szerokosc//2, y + ikona_padding),
                (x + szerokosc - ikona_padding - 2, y + wysokosc//5),
                (x + ikona_padding + 2, y + wysokosc//5)
            ]
        )
        # Podstawa domku
        pygame.draw.rect(
            ekran, 
            (40, 120, 40), 
            (x + szerokosc//4, y + wysokosc//5, szerokosc//2, wysokosc//8),
            border_radius=2
        )
        # Drzwi
        pygame.draw.rect(
            ekran, 
            (120, 80, 40), 
            (x + szerokosc//2 - 4, y + wysokosc//5 + 2, 6, 8),
            border_radius=1
        )
    
    # Dodaj ikony dla usług - ładniejsza ikona usług
    if pole["typ"] == "uslugi":
        ikona_padding = 4  # Zmniejszony padding ikony
        # Tło ikony
        pygame.draw.rect(
            ekran, 
            (220, 220, 250), 
            (x + ikona_padding, y + ikona_padding, szerokosc - 2*ikona_padding, wysokosc//4),
            border_radius=2
        )
        
        # Ikona narzędzi
        pygame.draw.circle(
            ekran, 
            (40, 40, 140), 
            (x + szerokosc//2, y + wysokosc//6), 
            szerokosc//8
        )
        pygame.draw.circle(
            ekran, 
            (220, 220, 250), 
            (x + szerokosc//2, y + wysokosc//6), 
            szerokosc//12
        )
        
        # Prosty symbol narzędzia
        grubosc = 2  # Zmniejszona grubość linii
        dlugosc = szerokosc//5  # Zmniejszona długość linii
        pygame.draw.line(
            ekran, 
            (40, 40, 140), 
            (x + szerokosc//2 - dlugosc//2, y + wysokosc//6), 
            (x + szerokosc//2 + dlugosc//2, y + wysokosc//6), 
            grubosc
        )
        pygame.draw.line(
            ekran, 
            (40, 40, 140), 
            (x + szerokosc//2, y + wysokosc//6 - dlugosc//2), 
            (x + szerokosc//2, y + wysokosc//6 + dlugosc//2), 
            grubosc
        )
    
    # Dodaj tekst nazwy pola z lepszym formatowaniem
    nazwa = pole["nazwa"]
    
    # Dostosuj rozmiar czcionki w zależności od długości nazwy i typu pola
    rozmiar_czcionki = 11  # Zmniejszony domyślny rozmiar czcionki
    if len(nazwa) > 12:
        rozmiar_czcionki = 9
    if len(nazwa) > 16:
        rozmiar_czcionki = 7
    
    # Użyj pogrubionej czcionki dla lepszej czytelności
    czcionka_nazwa = pygame.font.SysFont('Arial', rozmiar_czcionki, bold=True)
    
    # Dostosuj pozycję tekstu w zależności od typu pola
    tekst_y_offset = 0
    if pole["typ"] == "wydzial":
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
    if pole["typ"] in ["wydzial", "akademik", "uslugi"]:
        czcionka_cena = pygame.font.SysFont('Arial', 10, bold=True)  # Zmniejszony rozmiar czcionki
        tekst_cena = czcionka_cena.render(f"{pole['cena']} PLN", True, CZARNY)
        
        # Tło dla ceny
        tekst_szerokosc = tekst_cena.get_width() + 6  # Zmniejszony padding
        tekst_wysokosc = tekst_cena.get_height() + 2  # Zmniejszony padding
        narysuj_zaokraglony_prostokat(
            ekran, 
            (245, 245, 245), 
            (x + (szerokosc - tekst_szerokosc)//2, y + wysokosc - tekst_wysokosc - 3, 
             tekst_szerokosc, tekst_wysokosc), 
            3  # Mniejszy promień zaokrąglenia
        )
        
        # Tekst ceny wycentrowany
        ekran.blit(
            tekst_cena, 
            (x + (szerokosc - tekst_cena.get_width())//2, y + wysokosc - tekst_wysokosc - 2)
        )

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

# Funkcja do rysowania planszy MonoPOLI - ulepszona wersja
def narysuj_plansze(ekran, gracze):
    """Rysuje planszę do gry MonoPOLI - ulepszona wersja"""
    # Math został już zaimportowany na górze pliku
    
    # Wielkość planszy
    plansza_rozmiar = 800
    plansza_x = 50
    plansza_y = 50
    
    # Tło planszy z cieniem
    # Cień
    pygame.draw.rect(ekran, (30, 30, 60), (plansza_x + 8, plansza_y + 8, plansza_rozmiar, plansza_rozmiar), border_radius=12)
    # Główna plansza
    narysuj_zaokraglony_prostokat(ekran, NIEBIESKI_POLE, (plansza_x, plansza_y, plansza_rozmiar, plansza_rozmiar), 10)
    
    # Ustawienia pól
    rozmiar_pola_naroza = 120  # Zmniejszony rozmiar pól narożnych
    rozmiar_pola_bok_szer = 70  # Zmniejszona szerokość pól bocznych
    rozmiar_pola_bok_wys = 120  # Zmniejszona wysokość pól bocznych
    
    # Środek planszy z ładniejszym tłem - dostosowany do nowych rozmiarów pól
    narysuj_zaokraglony_prostokat(
        ekran, 
        CZERWONY_TLO, 
        (plansza_x + rozmiar_pola_bok_wys, plansza_y + rozmiar_pola_bok_wys, 
         plansza_rozmiar - 2*rozmiar_pola_bok_wys, plansza_rozmiar - 2*rozmiar_pola_bok_wys), 
        8
    )
    
    # Efekt 3D dla środka planszy - cienki biały pasek na górze
    pygame.draw.rect(
        ekran, 
        (250, 180, 180), 
        (plansza_x + rozmiar_pola_bok_wys, plansza_y + rozmiar_pola_bok_wys, 
         plansza_rozmiar - 2*rozmiar_pola_bok_wys, 4), 
        border_radius=8
    )
    
    # Efekt 3D dla środka planszy - cienki biały pasek po lewej
    pygame.draw.rect(
        ekran, 
        (250, 180, 180), 
        (plansza_x + rozmiar_pola_bok_wys, plansza_y + rozmiar_pola_bok_wys, 
         4, plansza_rozmiar - 2*rozmiar_pola_bok_wys), 
        border_radius=8
    )
    
    # Delikatny gradient na środku
    srodek_szer = plansza_rozmiar - 2*rozmiar_pola_bok_wys
    for i in range(20):  # Zmniejszona liczba iteracji
        alpha = 200 - i * 8  # Zmniejszająca się przezroczystość
        if alpha < 0:
            alpha = 0
        s = pygame.Surface((srodek_szer - i*2, srodek_szer - i*2), pygame.SRCALPHA)
        s.fill((255, 255, 255, alpha))
        ekran.blit(s, (plansza_x + rozmiar_pola_bok_wys + i, plansza_y + rozmiar_pola_bok_wys + i))
    
    # Logo i tytuł w środku
    logo_rozmiar = 120  # Zmniejszony rozmiar logo
    narysuj_logo_pl(
        ekran, 
        plansza_x + plansza_rozmiar//2 - logo_rozmiar//2, 
        plansza_y + plansza_rozmiar//2 - logo_rozmiar//2, 
        logo_rozmiar
    )
    
    # Tytuł gry z cieniem
    czcionka_tytul = pygame.font.SysFont('Arial', 56, bold=True)  # Zmniejszony rozmiar czcionki
    # Cień
    tekst_mono_cien = czcionka_tytul.render("Mono", True, (100, 100, 100))
    tekst_poli_cien = czcionka_tytul.render("POLI", True, (100, 100, 100))
    ekran.blit(tekst_mono_cien, (plansza_x + plansza_rozmiar//2 - 120 + 3, plansza_y + plansza_rozmiar//2 - 140 + 3))
    ekran.blit(tekst_poli_cien, (plansza_x + plansza_rozmiar//2 - 5 + 3, plansza_y + plansza_rozmiar//2 - 140 + 3))
    
    # Tekst główny
    tekst_mono = czcionka_tytul.render("Mono", True, BIALY)
    tekst_poli = czcionka_tytul.render("POLI", True, CZERWONY)
    ekran.blit(tekst_mono, (plansza_x + plansza_rozmiar//2 - 120, plansza_y + plansza_rozmiar//2 - 140))
    ekran.blit(tekst_poli, (plansza_x + plansza_rozmiar//2 - 5, plansza_y + plansza_rozmiar//2 - 140))
    
    # Podtytuł z lepszym formatowaniem
    czcionka_podtytul = pygame.font.SysFont('Arial', 32, bold=True)  # Zmniejszony rozmiar czcionki
    # Cień
    tekst_politechnika_cien = czcionka_podtytul.render("Politechnika", True, (100, 100, 100))
    tekst_lodzka_cien = czcionka_podtytul.render("Łódzka", True, (100, 100, 100))
    ekran.blit(tekst_politechnika_cien, (plansza_x + plansza_rozmiar//2 - 80 + 2, plansza_y + plansza_rozmiar//2 + 70 + 2))
    ekran.blit(tekst_lodzka_cien, (plansza_x + plansza_rozmiar//2 - 35 + 2, plansza_y + plansza_rozmiar//2 + 105 + 2))
    
    # Tekst główny
    tekst_politechnika = czcionka_podtytul.render("Politechnika", True, BIALY)
    tekst_lodzka = czcionka_podtytul.render("Łódzka", True, BIALY)
    ekran.blit(tekst_politechnika, (plansza_x + plansza_rozmiar//2 - 80, plansza_y + plansza_rozmiar//2 + 70))
    ekran.blit(tekst_lodzka, (plansza_x + plansza_rozmiar//2 - 35, plansza_y + plansza_rozmiar//2 + 105))
    
    # Ładniejsze pionki kart pytań - dostosowane do nowych wymiarów planszy
    # Pierwsza karta
    karta_szer = 60  # Zmniejszona szerokość karty
    karta_wys = 75   # Zmniejszona wysokość karty
    
    # Pozycje kart dopasowane do rozmiarów planszy - symetrycznie rozmieszczone
    karta1_x = plansza_x + rozmiar_pola_bok_wys + 50
    karta1_y = plansza_y + plansza_rozmiar//2 - 20
    
    narysuj_zaokraglony_prostokat(ekran, SZARY, (karta1_x, karta1_y, karta_szer, karta_wys), 6)
    # Górny jaśniejszy pasek karty (efekt 3D)
    pygame.draw.rect(ekran, (180, 180, 180), (karta1_x, karta1_y, karta_szer, 4), border_radius=6)
    # Lewy jaśniejszy pasek karty (efekt 3D)
    pygame.draw.rect(ekran, (180, 180, 180), (karta1_x, karta1_y, 4, karta_wys), border_radius=6)
    
    pygame.draw.rect(ekran, (240, 240, 240), (karta1_x + 8, karta1_y + 8, karta_szer - 16, 15), border_radius=2)
    pygame.draw.rect(ekran, (240, 240, 240), (karta1_x + 8, karta1_y + 30, karta_szer - 16, 15), border_radius=2)
    
    # Ikona znaku zapytania
    pygame.draw.circle(ekran, CZARNY, (karta1_x + karta_szer//2, karta1_y + karta_wys - 15), 10)
    pygame.draw.circle(ekran, SZARY, (karta1_x + karta_szer//2, karta1_y + karta_wys - 15), 8)
    czcionka_znakzap = pygame.font.SysFont('Arial', 16, bold=True)
    tekst_znakzap = czcionka_znakzap.render("?", True, CZARNY)
    ekran.blit(tekst_znakzap, (karta1_x + karta_szer//2 - 4, karta1_y + karta_wys - 22))
    
    # Druga karta
    karta2_x = plansza_x + plansza_rozmiar - rozmiar_pola_bok_wys - karta_szer - 50
    karta2_y = plansza_y + plansza_rozmiar//2 - 20
    
    narysuj_zaokraglony_prostokat(ekran, SZARY, (karta2_x, karta2_y, karta_szer, karta_wys), 6)
    # Górny jaśniejszy pasek karty (efekt 3D)
    pygame.draw.rect(ekran, (180, 180, 180), (karta2_x, karta2_y, karta_szer, 4), border_radius=6)
    # Lewy jaśniejszy pasek karty (efekt 3D)
    pygame.draw.rect(ekran, (180, 180, 180), (karta2_x, karta2_y, 4, karta_wys), border_radius=6)
    
    pygame.draw.rect(ekran, (240, 240, 240), (karta2_x + 8, karta2_y + 8, karta_szer - 16, 15), border_radius=2)
    pygame.draw.rect(ekran, (240, 240, 240), (karta2_x + 8, karta2_y + 30, karta_szer - 16, 15), border_radius=2)
    
    # Ikona znaku zapytania
    pygame.draw.circle(ekran, CZARNY, (karta2_x + karta_szer//2, karta2_y + karta_wys - 15), 10)
    pygame.draw.circle(ekran, SZARY, (karta2_x + karta_szer//2, karta2_y + karta_wys - 15), 8)
    tekst_znakzap = czcionka_znakzap.render("?", True, CZARNY)
    ekran.blit(tekst_znakzap, (karta2_x + karta_szer//2 - 4, karta2_y + karta_wys - 22))
    
    # Rysowanie pól na planszy
    # Narożniki
    narysuj_pole(ekran, plansza_x, plansza_y + plansza_rozmiar - rozmiar_pola_naroza, rozmiar_pola_naroza, rozmiar_pola_naroza, 0)  # START (lewy dolny róg)
    narysuj_pole(ekran, plansza_x, plansza_y, rozmiar_pola_naroza, rozmiar_pola_naroza, 9)  # DZIEKANAT (lewy górny róg)
    narysuj_pole(ekran, plansza_x + plansza_rozmiar - rozmiar_pola_naroza, plansza_y, rozmiar_pola_naroza, rozmiar_pola_naroza, 18)  # PARKING (prawy górny róg)
    narysuj_pole(ekran, plansza_x + plansza_rozmiar - rozmiar_pola_naroza, plansza_y + plansza_rozmiar - rozmiar_pola_naroza, rozmiar_pola_naroza, rozmiar_pola_naroza, 27)  # IDŹ NA POPRAWKĘ (prawy dolny róg)

    # Lewa krawędź (pola 1-8) - od dołu do góry
    for i in range(1, 9):
        narysuj_pole(
            ekran,
            plansza_x,
            plansza_y + plansza_rozmiar - rozmiar_pola_naroza - i * rozmiar_pola_bok_szer,
            rozmiar_pola_naroza,
            rozmiar_pola_bok_szer,
            i
        )

    # Górna krawędź (pola 10-17) - od lewej do prawej
    for i in range(10, 18):
        narysuj_pole(
            ekran,
            plansza_x + rozmiar_pola_naroza + (i - 10) * rozmiar_pola_bok_szer,
            plansza_y,
            rozmiar_pola_bok_szer,
            rozmiar_pola_naroza,
            i
        )

    # Prawa krawędź (pola 19-26) - od góry do dołu
    for i in range(19, 27):
        narysuj_pole(
            ekran,
            plansza_x + plansza_rozmiar - rozmiar_pola_naroza,
            plansza_y + rozmiar_pola_naroza + (i - 19) * rozmiar_pola_bok_szer,
            rozmiar_pola_naroza,
            rozmiar_pola_bok_szer,
            i
        )

    # Dolna krawędź (pola 28-35) - od prawej do lewej
    for i in range(28, 36):
        narysuj_pole(
            ekran,
            plansza_x + plansza_rozmiar - rozmiar_pola_naroza - (i - 27) * rozmiar_pola_bok_szer,
            plansza_y + plansza_rozmiar - rozmiar_pola_naroza,
            rozmiar_pola_bok_szer,
            rozmiar_pola_naroza,
            i
        )

    # Pozycje graczy na planszy
    gracze_count = len(gracze)
    for i, gracz in enumerate(gracze):
        pozycja = gracz["pozycja"]
        x, y = oblicz_pozycje_gracza(plansza_x, plansza_y, plansza_rozmiar, pozycja, i, gracze_count)
        
        # Rysuj ładniejszy pionek gracza z efektem 3D
        # Cień
        pygame.draw.circle(ekran, (50, 50, 50), (x + 2, y + 2), 12)  # Zmniejszony rozmiar pionka
        # Główna część pionka
        pygame.draw.circle(ekran, gracz["kolor"], (x, y), 12)
        # Odblaski
        pygame.draw.circle(ekran, CZARNY, (x, y), 12, 1)  # Obramowanie
        # Wewnętrzny krąg
        pygame.draw.circle(ekran, mix_color(gracz["kolor"], BIALY, 0.3), (x, y), 8)
        # Odblask
        pygame.draw.circle(ekran, BIALY, (x - 3, y - 3), 3)
    
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