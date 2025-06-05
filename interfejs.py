import pygame
import sys
import math
from kolory import *

# Funkcja do rysowania zaokrąglonego prostokąta
def narysuj_zaokraglony_prostokat(powierzchnia, kolor, prostokat, promien):
    """Rysuje prostokąt z zaokrąglonymi rogami"""
    x, y, szer, wys = prostokat
    promien = min(promien, szer // 2, wys // 2)
    
    # Narysuj prostokąt
    pygame.draw.rect(powierzchnia, kolor, prostokat, border_radius=promien)

# Funkcja do tworzenia przycisku
def utworz_przycisk(ekran, tekst, x, y, szerokosc, wysokosc, kolor, kolor_tekstu, rozmiar_czcionki=24):
    """Tworzy przycisk i sprawdza czy został kliknięty"""
    czcionka = pygame.font.SysFont('Arial', rozmiar_czcionki)
    prostokat = pygame.Rect(x, y, szerokosc, wysokosc)
    myszka = pygame.mouse.get_pos()
    klikniecie = pygame.mouse.get_pressed()[0]
    
    # Rysuj przycisk
    narysuj_zaokraglony_prostokat(ekran, kolor, prostokat, 10)
    
    # Dodaj cień do przycisku
    pygame.draw.rect(ekran, (0, 0, 0, 50), (x+3, y+3, szerokosc, wysokosc), border_radius=10)
    
    # Renderuj tekst
    tekst_surface = czcionka.render(tekst, True, kolor_tekstu)
    tekst_rect = tekst_surface.get_rect(center=prostokat.center)
    ekran.blit(tekst_surface, tekst_rect)
    
    # Sprawdź czy przycisk został kliknięty
    if prostokat.collidepoint(myszka) and klikniecie:
        return True
    return False

# Funkcja do rysowania kostek
def narysuj_kostke(ekran, x, y, rozmiar, liczba_oczek):
    """Rysuje kostkę do gry z określoną liczbą oczek"""
    # Tło kostki
    pygame.draw.rect(ekran, BIALY, (x, y, rozmiar, rozmiar), border_radius=rozmiar//5)
    pygame.draw.rect(ekran, CZARNY, (x, y, rozmiar, rozmiar), 1, border_radius=rozmiar//5)
    
    # Oczka
    promien_oczka = rozmiar // 10
    padding = rozmiar // 4
    
    # Pozycje oczek zależnie od liczby
    if liczba_oczek == 1 or liczba_oczek == 3 or liczba_oczek == 5:
        # Środkowe oczko
        pygame.draw.circle(ekran, CZARNY, (x + rozmiar // 2, y + rozmiar // 2), promien_oczka)
    
    if liczba_oczek >= 2:
        # Lewy górny i prawy dolny
        pygame.draw.circle(ekran, CZARNY, (x + padding, y + padding), promien_oczka)
        pygame.draw.circle(ekran, CZARNY, (x + rozmiar - padding, y + rozmiar - padding), promien_oczka)
    
    if liczba_oczek >= 4:
        # Prawy górny i lewy dolny
        pygame.draw.circle(ekran, CZARNY, (x + rozmiar - padding, y + padding), promien_oczka)
        pygame.draw.circle(ekran, CZARNY, (x + padding, y + rozmiar - padding), promien_oczka)
    
    if liczba_oczek == 6:
        # Środkowe lewe i prawe
        pygame.draw.circle(ekran, CZARNY, (x + padding, y + rozmiar // 2), promien_oczka)
        pygame.draw.circle(ekran, CZARNY, (x + rozmiar - padding, y + rozmiar // 2), promien_oczka)

# Funkcja do rysowania logo Politechniki Łódzkiej
def narysuj_logo_pl(ekran, x, y, rozmiar):
    """Rysuje uproszczone logo Politechniki Łódzkiej"""
    import math
    # Tarcza
    pygame.draw.polygon(ekran, BIALY, [
        (x, y + rozmiar*0.5),
        (x + rozmiar*0.4, y),
        (x + rozmiar*0.6, y),
        (x + rozmiar, y + rozmiar*0.5),
        (x + rozmiar*0.6, y + rozmiar),
        (x + rozmiar*0.4, y + rozmiar)
    ])
    
    # Litery P i Ł
    czcionka = pygame.font.SysFont('Arial', int(rozmiar*0.4), bold=True)
    p_text = czcionka.render("P", True, BIALY)
    l_text = czcionka.render("Ł", True, BIALY)
    ekran.blit(p_text, (x + rozmiar*0.3, y + rozmiar*0.3))
    ekran.blit(l_text, (x + rozmiar*0.5, y + rozmiar*0.3))
    
    # Koło zębate
    promien_kola = rozmiar * 0.6
    pygame.draw.circle(ekran, BIALY, (x + rozmiar*0.5, y + rozmiar*0.5), promien_kola, width=3)
    
    for i in range(8):
        kat = i * math.pi / 4
        pygame.draw.line(ekran, BIALY, 
                        (x + rozmiar*0.5 + promien_kola * math.cos(kat), 
                         y + rozmiar*0.5 + promien_kola * math.sin(kat)),
                        (x + rozmiar*0.5 + (promien_kola+rozmiar*0.15) * math.cos(kat), 
                         y + rozmiar*0.5 + (promien_kola+rozmiar*0.15) * math.sin(kat)), 
                        3)
    
    # Skrzydło na górze
    pygame.draw.arc(ekran, BIALY, 
                   (x + rozmiar*0.25, y - rozmiar*0.1, rozmiar*0.5, rozmiar*0.3), 
                   0, math.pi, 3)
    
    for i in range(3):
        pygame.draw.arc(ekran, BIALY, 
                       (x + rozmiar*0.25, y - rozmiar*0.1 - i*6, rozmiar*0.5, rozmiar*0.3), 
                       0, math.pi, 2)

# Funkcja do rysowania pionka/znacznika monopoly
def narysuj_pionek(ekran, x, y, rozmiar):
    """Rysuje znacznik/pionek monopoly"""
    pygame.draw.rect(ekran, SZARY, (x, y, rozmiar, rozmiar), border_radius=5)
    przekatna_dlugosc = math.sqrt(2) * rozmiar / 2
    grubosc = rozmiar // 10
    
    # Rysuj symbol "?" lub "c" na pionku
    czcionka = pygame.font.SysFont('Arial', rozmiar // 2)
    
    # Dla pionka w prawym dolnym rogu rysujemy "?"
    if x > 400:  # Zmieniono z SZEROKOSC // 2 na stałą wartość, ponieważ SZEROKOSC nie jest dostępna
        tekst = czcionka.render("?", True, (100, 100, 100))
    # Dla pionka w lewym górnym rysujemy "c"
    else:
        tekst = czcionka.render("c", True, (100, 100, 100))
    
    tekst_rect = tekst.get_rect(center=(x + rozmiar // 2, y + rozmiar // 2))
    ekran.blit(tekst, tekst_rect)

# Funkcja do rysowania karty gracza z informacjami
def narysuj_karte_gracza(ekran, gracz, x, y, szerokosc, wysokosc, aktywny=False):
    """Rysuje kartę informacyjną o graczu"""
    from pola import pobierz_nazwe_pola
    
    # Tło karty
    kolor_tla = gracz["kolor"] if aktywny else (100, 100, 100)
    narysuj_zaokraglony_prostokat(ekran, kolor_tla, (x, y, szerokosc, wysokosc), 10)
    narysuj_zaokraglony_prostokat(ekran, (40, 40, 40), (x+3, y+3, szerokosc-6, wysokosc-6), 8)
    
    # Nagłówek z nazwą gracza
    czcionka_nazwa = pygame.font.SysFont('Arial', 24, bold=True)
    tekst_nazwa = czcionka_nazwa.render(gracz["nazwa"], True, BIALY)
    tekst_nazwa_rect = tekst_nazwa.get_rect(center=(x + szerokosc//2, y + 25))
    ekran.blit(tekst_nazwa, tekst_nazwa_rect)
    
    # Linia oddzielająca
    pygame.draw.line(ekran, BIALY, (x + 10, y + 45), (x + szerokosc - 10, y + 45), 1)
    
    # Informacje o graczu
    czcionka_info = pygame.font.SysFont('Arial', 18)
    odst = 30  # Odstęp między wierszami
    
    # Pieniądze
    tekst_pieniadze = czcionka_info.render(f"Pieniądze: {gracz['pieniadze']} PLN", True, BIALY)
    ekran.blit(tekst_pieniadze, (x + 10, y + 55))
    
    # Pozycja
    nazwa_pola = pobierz_nazwe_pola(gracz["pozycja"]) if len(pobierz_nazwe_pola(gracz["pozycja"])) < 20 else pobierz_nazwe_pola(gracz["pozycja"])[:17] + "..."
    tekst_pozycja = czcionka_info.render(f"Pozycja: {nazwa_pola}", True, BIALY)
    ekran.blit(tekst_pozycja, (x + 10, y + 55 + odst))
    
    # Budynki
    tekst_budynki = czcionka_info.render(f"Budynki: {gracz['budynki']}", True, BIALY)
    ekran.blit(tekst_budynki, (x + 10, y + 55 + 2*odst))
    
    # ECTS
    tekst_ects = czcionka_info.render(f"ECTS: {gracz['ects']}", True, ZLOTY)
    ekran.blit(tekst_ects, (x + 10, y + 55 + 3*odst))
    
    # Znacznik aktywnego gracza
    if aktywny:
        pygame.draw.circle(ekran, ZLOTY, (x + szerokosc - 20, y + 20), 10)
        pygame.draw.circle(ekran, (200, 150, 0), (x + szerokosc - 20, y + 20), 8)

# Funkcja do wyświetlania okna z kartą
def wyswietl_okno_karty(ekran, karta, tytul="KARTA"):
    """Wyświetla okno z kartą i czeka na reakcję gracza"""
    # Wymiary okna karty
    szerokosc_okna = 400
    wysokosc_okna = 350
    x_okna = (1200 - szerokosc_okna) // 2
    y_okna = (1000 - wysokosc_okna) // 2
    
    # Półprzezroczyste tło
    overlay = pygame.Surface((1200, 1000))
    overlay.set_alpha(128)
    overlay.fill(CZARNY)
    ekran.blit(overlay, (0, 0))
    
    # Okno karty
    narysuj_zaokraglony_prostokat(ekran, BIALY, (x_okna, y_okna, szerokosc_okna, wysokosc_okna), 15)
    pygame.draw.rect(ekran, CZARNY, (x_okna, y_okna, szerokosc_okna, wysokosc_okna), 3, border_radius=15)
    
    # Tytuł karty
    czcionka_tytul = pygame.font.SysFont('Arial', 24, bold=True)
    kolor_tytulu = CZERWONY if tytul == "SZANSA" else NIEBIESKI_POLE
    
    tekst_tytul = czcionka_tytul.render(tytul, True, kolor_tytulu)
    tytul_rect = tekst_tytul.get_rect(centerx=x_okna + szerokosc_okna//2, y=y_okna + 20)
    ekran.blit(tekst_tytul, tytul_rect)
    
    # Linia pod tytułem
    pygame.draw.line(ekran, kolor_tytulu, 
                     (x_okna + 30, y_okna + 60), 
                     (x_okna + szerokosc_okna - 30, y_okna + 60), 2)
    
    # Tekst karty
    czcionka_tekst = pygame.font.SysFont('Arial', 16)
    linie = karta["tekst"].split('\n')
    
    # Wyśrodkuj tekst
    start_y = y_okna + 80
    for i, linia in enumerate(linie):
        if linia.strip():  # Pomiń puste linie
            tekst_surface = czcionka_tekst.render(linia, True, CZARNY)
            tekst_rect = tekst_surface.get_rect(centerx=x_okna + szerokosc_okna//2, 
                                               y=start_y + i * 25)
            ekran.blit(tekst_surface, tekst_rect)
    
    # Przycisk OK
    przycisk_y = y_okna + wysokosc_okna - 70
    przycisk_klikniety = utworz_przycisk(ekran, "OK", x_okna + szerokosc_okna//2 - 60, 
                                        przycisk_y, 120, 40, 
                                        ZIELONY, BIALY, 18)
    
    pygame.display.flip()
    
    return przycisk_klikniety


def wyswietl_okno_platnosci(ekran, gracz_platnik, gracz_wlasciciel, pole, kwota):
    """Wyświetla okno informujące o płatności czynszu"""
    # Wymiary okna
    szerokosc_okna = 450
    wysokosc_okna = 400
    x_okna = (1200 - szerokosc_okna) // 2
    y_okna = (1000 - wysokosc_okna) // 2
    
    # Półprzezroczyste tło
    overlay = pygame.Surface((1200, 1000))
    overlay.set_alpha(128)
    overlay.fill(CZARNY)
    ekran.blit(overlay, (0, 0))
    
    # Okno płatności
    narysuj_zaokraglony_prostokat(ekran, BIALY, (x_okna, y_okna, szerokosc_okna, wysokosc_okna), 15)
    pygame.draw.rect(ekran, CZARNY, (x_okna, y_okna, szerokosc_okna, wysokosc_okna), 3, border_radius=15)
    
    # Nagłówek - PŁATNOŚĆ CZYNSZU
    czcionka_tytul = pygame.font.SysFont('Arial', 28, bold=True)
    tekst_tytul = czcionka_tytul.render("PŁATNOŚĆ CZYNSZU", True, CZERWONY)
    tytul_rect = tekst_tytul.get_rect(centerx=x_okna + szerokosc_okna//2, y=y_okna + 25)
    ekran.blit(tekst_tytul, tytul_rect)
    
    # Linia pod tytułem
    pygame.draw.line(ekran, CZERWONY, 
                     (x_okna + 30, y_okna + 65), 
                     (x_okna + szerokosc_okna - 30, y_okna + 65), 2)
    
    # Ikona domu/pola
    ikona_y = y_okna + 85
    pygame.draw.rect(ekran, pole.get("kolor", SZARY), 
                     (x_okna + szerokosc_okna//2 - 40, ikona_y, 80, 60), 
                     border_radius=5)
    pygame.draw.rect(ekran, CZARNY, 
                     (x_okna + szerokosc_okna//2 - 40, ikona_y, 80, 60), 
                     2, border_radius=5)
    
    # Nazwa pola
    czcionka_pole = pygame.font.SysFont('Arial', 20, bold=True)
    tekst_pole = czcionka_pole.render(pole["nazwa"], True, CZARNY)
    pole_rect = tekst_pole.get_rect(centerx=x_okna + szerokosc_okna//2, y=ikona_y + 70)
    ekran.blit(tekst_pole, pole_rect)
    
    # Informacje o transakcji
    czcionka_info = pygame.font.SysFont('Arial', 18)
    y_info = ikona_y + 110
    
    # Kto płaci
    tekst_platnik = czcionka_info.render(f"{gracz_platnik['nazwa']} płaci czynsz", True, CZARNY)
    platnik_rect = tekst_platnik.get_rect(centerx=x_okna + szerokosc_okna//2, y=y_info)
    ekran.blit(tekst_platnik, platnik_rect)
    
    # Właściciel
    tekst_wlasciciel = czcionka_info.render(f"właścicielowi: {gracz_wlasciciel['nazwa']}", True, CZARNY)
    wlasciciel_rect = tekst_wlasciciel.get_rect(centerx=x_okna + szerokosc_okna//2, y=y_info + 30)
    ekran.blit(tekst_wlasciciel, wlasciciel_rect)
    
    # Kwota z dużą czcionką
    czcionka_kwota = pygame.font.SysFont('Arial', 36, bold=True)
    tekst_kwota = czcionka_kwota.render(f"{kwota} PLN", True, CZERWONY)
    kwota_rect = tekst_kwota.get_rect(centerx=x_okna + szerokosc_okna//2, y=y_info + 70)
    
    # Tło dla kwoty
    tlo_kwota = pygame.Rect(kwota_rect.x - 20, kwota_rect.y - 5, kwota_rect.width + 40, kwota_rect.height + 10)
    narysuj_zaokraglony_prostokat(ekran, (255, 230, 230), tlo_kwota, 5)
    
    ekran.blit(tekst_kwota, kwota_rect)
    
    # Stan konta po transakcji
    czcionka_stan = pygame.font.SysFont('Arial', 14)
    tekst_stan = czcionka_stan.render(
        f"Stan konta {gracz_platnik['nazwa']}: {gracz_platnik['pieniadze']} PLN", 
        True, (100, 100, 100)
    )
    stan_rect = tekst_stan.get_rect(centerx=x_okna + szerokosc_okna//2, y=y_info + 120)
    ekran.blit(tekst_stan, stan_rect)
    
    # Przycisk OK
    przycisk_y = y_okna + wysokosc_okna - 60
    przycisk_klikniety = utworz_przycisk(ekran, "OK", x_okna + szerokosc_okna//2 - 60, 
                                        przycisk_y, 120, 40, 
                                        ZIELONY, BIALY, 18)
    
    pygame.display.flip()
    
    return przycisk_klikniety

def wyswietl_okno_kupna_domkow(ekran, pole, gracz):
    """Wyświetla okno do kupna domków na polu. Pozwala wybrać liczbę domków do kupienia (1-4, max 4 na polu). Zwraca liczbę domków do kupienia lub 0 jeśli anulowano."""
    szerokosc_okna = 450
    wysokosc_okna = 400
    x_okna = (1200 - szerokosc_okna) // 2
    y_okna = (1000 - wysokosc_okna) // 2
    
    domki_aktualne = pole.get("domki", 0)
    domki_max = 4
    domki_mozna_kupic = domki_max - domki_aktualne
    if domki_mozna_kupic <= 0:
        return 0
    cena_domku = int(pole["cena"] * 0.5)
    wybrana_ilosc = 1
    running = True
    while running:
        # Półprzezroczyste tło - mocniej przezroczyste
        overlay = pygame.Surface((1200, 1000))
        overlay.set_alpha(70)  # Było 128, teraz mocniej przezroczyste
        overlay.fill(CZARNY)
        ekran.blit(overlay, (0, 0))
        # Okno
        narysuj_zaokraglony_prostokat(ekran, BIALY, (x_okna, y_okna, szerokosc_okna, wysokosc_okna), 15)
        pygame.draw.rect(ekran, CZARNY, (x_okna, y_okna, szerokosc_okna, wysokosc_okna), 3, border_radius=15)
        # Nagłówek
        czcionka_tytul = pygame.font.SysFont('Arial', 28, bold=True)
        tekst_tytul = czcionka_tytul.render("KUPNO DOMKÓW", True, ZIELONY)
        tytul_rect = tekst_tytul.get_rect(centerx=x_okna + szerokosc_okna//2, y=y_okna + 25)
        ekran.blit(tekst_tytul, tytul_rect)
        # Linia pod tytułem
        pygame.draw.line(ekran, ZIELONY, (x_okna + 30, y_okna + 65), (x_okna + szerokosc_okna - 30, y_okna + 65), 2)
        # Ikona domu/pola
        ikona_y = y_okna + 85
        pygame.draw.rect(ekran, pole.get("kolor", SZARY), (x_okna + szerokosc_okna//2 - 40, ikona_y, 80, 60), border_radius=5)
        pygame.draw.rect(ekran, CZARNY, (x_okna + szerokosc_okna//2 - 40, ikona_y, 80, 60), 2, border_radius=5)
        # Nazwa pola
        czcionka_pole = pygame.font.SysFont('Arial', 20, bold=True)
        tekst_pole = czcionka_pole.render(pole["nazwa"], True, CZARNY)
        pole_rect = tekst_pole.get_rect(centerx=x_okna + szerokosc_okna//2, y=ikona_y + 70)
        ekran.blit(tekst_pole, pole_rect)
        # Info o domkach
        czcionka_info = pygame.font.SysFont('Arial', 18)
        y_info = ikona_y + 110
        info1 = czcionka_info.render(f"Masz już: {domki_aktualne} domków", True, CZARNY)
        info2 = czcionka_info.render(f"Możesz dokupić: {domki_mozna_kupic} (max 4)", True, CZARNY)
        info3 = czcionka_info.render(f"Cena za domek: {cena_domku} PLN", True, CZARNY)
        info4 = czcionka_info.render(f"Twój stan konta: {gracz['pieniadze']} PLN", True, (40, 100, 40))
        ekran.blit(info1, (x_okna + 40, y_info))
        ekran.blit(info2, (x_okna + 40, y_info + 28))
        ekran.blit(info3, (x_okna + 40, y_info + 56))
        ekran.blit(info4, (x_okna + 40, y_info + 84))
        # Wybór ilości domków
        czcionka_wyb = pygame.font.SysFont('Arial', 22, bold=True)
        ekran.blit(czcionka_wyb.render("Wybierz liczbę domków do kupienia:", True, CZARNY), (x_okna + 40, y_info + 120))
        # Strzałki i liczba
        btn_w = 48
        btn_h = 48
        btn_y = y_info + 155 + y_okna  # RELATYWNA POZYCJA Y względem okna
        btn_x_minus = x_okna + szerokosc_okna//2 - 90  # RELATYWNA POZYCJA X względem okna
        btn_x_plus = x_okna + szerokosc_okna//2 + 42   # RELATYWNA POZYCJA X względem okna
        # -
        if utworz_przycisk(ekran, "-", btn_x_minus, btn_y, btn_w, btn_h, NIEBIESKI_POLE, BIALY, 32):
            if wybrana_ilosc > 1:
                wybrana_ilosc -= 1
        # +
        if utworz_przycisk(ekran, "+", btn_x_plus, btn_y, btn_w, btn_h, NIEBIESKI_POLE, BIALY, 32):
            if wybrana_ilosc < domki_mozna_kupic:
                wybrana_ilosc += 1
        # Liczba
        liczba_rect = pygame.Rect(x_okna + szerokosc_okna//2 - 30, btn_y, 60, btn_h)
        pygame.draw.rect(ekran, ZIELONY, liczba_rect, border_radius=12)
        liczba_txt = czcionka_wyb.render(str(wybrana_ilosc), True, BIALY)
        ekran.blit(liczba_txt, liczba_txt.get_rect(center=liczba_rect.center))
        # Suma
        suma = wybrana_ilosc * cena_domku
        czcionka_kwota = pygame.font.SysFont('Arial', 36, bold=True)
        tekst_kwota = czcionka_kwota.render(f"{suma} PLN", True, CZERWONY)
        kwota_rect = tekst_kwota.get_rect(centerx=x_okna + szerokosc_okna//2, y=y_info + 230 + y_okna)
        tlo_kwota = pygame.Rect(kwota_rect.x - 20, kwota_rect.y - 5, kwota_rect.width + 40, kwota_rect.height + 10)
        narysuj_zaokraglony_prostokat(ekran, (255, 230, 230), tlo_kwota, 5)
        ekran.blit(tekst_kwota, kwota_rect)
        # Przycisk kup i anuluj - wyśrodkowane względem okna, przesunięte niżej
        btn_kup_x = x_okna + szerokosc_okna//2 - 110
        btn_anuluj_x = x_okna + szerokosc_okna//2 + 20
        btn_y2 = y_okna + wysokosc_okna - 48  # było -62, przesunięcie o 14px w dół
        kup = utworz_przycisk(ekran, "Kup", btn_kup_x, btn_y2, 90, 44, ZIELONY, BIALY, 22)
        anuluj = utworz_przycisk(ekran, "Anuluj", btn_anuluj_x, btn_y2, 90, 44, CZERWONY, BIALY, 22)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if kup:
                    if suma <= gracz['pieniadze']:
                        return wybrana_ilosc
                if anuluj:
                    return 0
    return 0