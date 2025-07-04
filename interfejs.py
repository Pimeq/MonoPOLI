from constants import *
import pygame
import math
import sys

# Funkcja do rysowania zaokrąglonego prostokąta
def narysuj_zaokraglony_prostokat(powierzchnia, kolor, prostokat, promien):
    """Rysuje prostokąt z zaokrąglonymi rogami"""
    x, y, szer, wys = prostokat
    promien = min(promien, szer // 2, wys // 2)
    
    # Narysuj prostokąt
    pygame.draw.rect(powierzchnia, kolor, prostokat, border_radius=promien)

# Funkcja do tworzenia przycisku
def utworz_przycisk(ekran, tekst, x, y, szerokosc, wysokosc, kolor, kolor_tekstu, rozmiar_czcionki=24, glosnosc_efekty=None):
    """Tworzy przycisk i sprawdza czy został kliknięty"""
    czcionka = pygame.font.SysFont('Arial', rozmiar_czcionki)
    prostokat = pygame.Rect(x, y, szerokosc, wysokosc)
    myszka = pygame.mouse.get_pos()
    klikniecie = pygame.mouse.get_pressed()[0]
    
    # Rysuj przycisk
    narysuj_zaokraglony_prostokat(ekran, kolor, prostokat, 10)
    
    # Dodaj cień do przycisku
    pygame.draw.rect(ekran, KOLOR_PRZYCISK_CIEN2, (x+3, y+3, szerokosc, wysokosc), border_radius=10)
    
    # Renderuj tekst
    tekst_surface = czcionka.render(tekst, True, kolor_tekstu)
    tekst_rect = tekst_surface.get_rect(center=prostokat.center)
    ekran.blit(tekst_surface, tekst_rect)
    
    # Sprawdź czy przycisk został kliknięty
    if prostokat.collidepoint(myszka) and klikniecie:
        if hasattr(pygame, 'mixer') and hasattr(pygame.mixer, 'Sound'):
            try:
                sound = pygame.mixer.Sound("Audio/button.mp3")
                if glosnosc_efekty is not None:
                    sound.set_volume(glosnosc_efekty)
                sound.play()
            except Exception:
                pass
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
        pygame.draw.circle(ekran, CZARNY, (x + rozmiar//2, y + rozmiar//2), promien_oczka)
    
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
        pygame.draw.circle(ekran, CZARNY, (x + padding, y + rozmiar//2), promien_oczka)
        pygame.draw.circle(ekran, CZARNY, (x + rozmiar - padding, y + rozmiar//2), promien_oczka)

# Funkcja do rysowania logo Politechniki Łódzkiej
def narysuj_logo_pl(ekran, x, y, rozmiar):
    """Rysuje uproszczone logo Politechniki Łódzkiej"""
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
    pygame.draw.circle(ekran, BIALY, (int(x + rozmiar*0.5), int(y + rozmiar*0.5)), int(promien_kola), width=3)
    
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
        tekst = czcionka.render("?", True, CZARNY)
    # Dla pionka w lewym górnym rysujemy "c"
    else:
        tekst = czcionka.render("c", True, CZARNY)
    
    tekst_rect = tekst.get_rect(center=(x + rozmiar // 2, y + rozmiar // 2))
    ekran.blit(tekst, tekst_rect)

# Funkcja do rysowania karty gracza z informacjami
def narysuj_karte_gracza(ekran, gracz, x, y, szerokosc, wysokosc, aktywny=False):
    """Rysuje kartę informacyjną o graczu"""
    from pola import pobierz_nazwe_pola
    
    # Tło karty
    kolor_tla = gracz[KEY_KOLOR] if aktywny else KOLOR_KARTA_NIEAKTYWNA
    narysuj_zaokraglony_prostokat(ekran, kolor_tla, (x, y, szerokosc, wysokosc), 10)
    narysuj_zaokraglony_prostokat(ekran, KOLOR_KARTA_OBRAMOWANIE, (x+3, y+3, szerokosc-6, wysokosc-6), 8)
    
    # Nagłówek z nazwą gracza
    czcionka_nazwa = pygame.font.SysFont('Arial', 24, bold=True)
    tekst_nazwa = czcionka_nazwa.render(gracz[KEY_NAZWA], True, BIALY)
    tekst_nazwa_rect = tekst_nazwa.get_rect(center=(x + szerokosc//2, y + 25))
    ekran.blit(tekst_nazwa, tekst_nazwa_rect)
    
    # Linia oddzielająca
    pygame.draw.line(ekran, BIALY, (x + 10, y + 45), (x + szerokosc - 10, y + 45), 1)
    
    # Informacje o graczu
    czcionka_info = pygame.font.SysFont('Arial', 18)
    odst = 30  # Odstęp między wierszami
    
    # Pieniądze
    tekst_pieniadze = czcionka_info.render(f"Pieniądze: {gracz[KEY_PIENIADZE]} PLN", True, BIALY)
    ekran.blit(tekst_pieniadze, (x + 10, y + 55))
    
    # Pozycja
    nazwa_pola = pobierz_nazwe_pola(gracz[KEY_POZYCJA])
    if len(nazwa_pola) < 20:
        pole_str = nazwa_pola
    else:
        pole_str = nazwa_pola[:17] + "..."
    tekst_pozycja = czcionka_info.render(f"Pozycja: {pole_str}", True, BIALY)
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
def wyswietl_okno_karty(ekran, karta, tytul="KARTA", glosnosc_efekty=0.7):
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
                                        ZIELONY, BIALY, 18, glosnosc_efekty)
    
    pygame.display.flip()
    
    return przycisk_klikniety


def wyswietl_okno_platnosci(ekran, gracz_platnik, gracz_wlasciciel, pole, kwota, glosnosc_efekty=0.7):
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
                                        ZIELONY, BIALY, 18, glosnosc_efekty)
    
    pygame.display.flip()
    
    return przycisk_klikniety

def wyswietl_okno_kupna_domkow(ekran, pole, gracz, glosnosc_efekty=0.7):
    """Wyświetla okno do kupna domków na polu. Pozwala wybrać liczbę domków do kupienia (1-4, max 4 na polu). Zwraca liczbę domków do kupienia lub 0 jeśli anulowano."""
    szerokosc_okna = 550  # Zwiększono z 450
    wysokosc_okna = 520   # Zwiększono jeszcze bardziej z 500 na 520
    x_okna = (1200 - szerokosc_okna) // 2
    y_okna = (1000 - wysokosc_okna) // 2
    
    domki_aktualne = pole.get("domki", 0)
    domki_max = 4
    domki_mozna_kupic = domki_max - domki_aktualne
    if domki_mozna_kupic <= 0:
        return 0
    cena_domku = int(pole["cena"] * 0.5)
    wybrana_ilosc = 1
    
    # Zapisz aktualny stan ekranu
    background = ekran.copy()
    
    # Główna pętla okna modalnego
    running = True
    clock = pygame.time.Clock()
    
    while running:
        # Obsługa eventów
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0  # Anuluj
                elif event.key == pygame.K_RETURN:
                    # Kup wybrane domki
                    suma = wybrana_ilosc * cena_domku
                    if suma <= gracz['pieniadze']:
                        return wybrana_ilosc
                    else:
                        return 0
                elif event.key == pygame.K_LEFT or event.key == pygame.K_MINUS:
                    if wybrana_ilosc > 1:
                        wybrana_ilosc -= 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_PLUS:
                    if wybrana_ilosc < domki_mozna_kupic:
                        wybrana_ilosc += 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Sprawdź przyciski minus/plus
                btn_w = 50    # Zwiększono z 48
                btn_h = 50    # Zwiększono z 48  
                btn_y = y_okna + 365  # Dostosowane do y_info + 170 (gdzie y_info = ikona_y + 110 = y_okna + 85 + 110)
                btn_x_minus = x_okna + szerokosc_okna//2 - 120  # Więcej miejsca z lewej
                btn_x_plus = x_okna + szerokosc_okna//2 + 70    # Więcej miejsca z prawej
                
                btn_minus_rect = pygame.Rect(btn_x_minus, btn_y, btn_w, btn_h)
                btn_plus_rect = pygame.Rect(btn_x_plus, btn_y, btn_w, btn_h)
                
                if btn_minus_rect.collidepoint(mouse_pos):
                    if wybrana_ilosc > 1:
                        # Odtwórz dźwięk kliknięcia
                        if hasattr(pygame, 'mixer') and hasattr(pygame.mixer, 'Sound'):
                            try:
                                sound = pygame.mixer.Sound("Audio/button.mp3")
                                if glosnosc_efekty is not None:
                                    sound.set_volume(glosnosc_efekty)
                                sound.play()
                            except Exception:
                                pass
                        wybrana_ilosc -= 1
                elif btn_plus_rect.collidepoint(mouse_pos):
                    if wybrana_ilosc < domki_mozna_kupic:
                        # Odtwórz dźwięk kliknięcia
                        if hasattr(pygame, 'mixer') and hasattr(pygame.mixer, 'Sound'):
                            try:
                                sound = pygame.mixer.Sound("Audio/button.mp3")
                                if glosnosc_efekty is not None:
                                    sound.set_volume(glosnosc_efekty)
                                sound.play()
                            except Exception:
                                pass
                        wybrana_ilosc += 1
                
                # Sprawdź przyciski kup/anuluj - FIXED: dostosowane do pozycji w renderingu
                btn_kup_x = x_okna + szerokosc_okna//2 - 190   # Dopasowane do renderingu (-190)
                btn_anuluj_x = x_okna + szerokosc_okna//2 + 90  # Dopasowane do renderingu (+90)
                btn_y2 = y_okna + wysokosc_okna - 90            # Jeszcze więcej miejsca z dołu (90px od dołu)
                
                btn_kup_rect = pygame.Rect(btn_kup_x, btn_y2, 100, 50)    # Większe przyciski
                btn_anuluj_rect = pygame.Rect(btn_anuluj_x, btn_y2, 100, 50)  # Większe przyciski
                
                if btn_kup_rect.collidepoint(mouse_pos):
                    suma = wybrana_ilosc * cena_domku
                    if suma <= gracz['pieniadze']:
                        # Odtwórz dźwięk kliknięcia
                        if hasattr(pygame, 'mixer') and hasattr(pygame.mixer, 'Sound'):
                            try:
                                sound = pygame.mixer.Sound("Audio/button.mp3")
                                if glosnosc_efekty is not None:
                                    sound.set_volume(glosnosc_efekty)
                                sound.play()
                            except Exception:
                                pass
                        return wybrana_ilosc
                    else:
                        return 0
                elif btn_anuluj_rect.collidepoint(mouse_pos):
                    # Odtwórz dźwięk kliknięcia
                    if hasattr(pygame, 'mixer') and hasattr(pygame.mixer, 'Sound'):
                        try:
                            sound = pygame.mixer.Sound("Audio/button.mp3")
                            if glosnosc_efekty is not None:
                                sound.set_volume(glosnosc_efekty)
                            sound.play()
                        except Exception:
                            pass
                    return 0
        
        # Przywróć tło
        ekran.blit(background, (0, 0))
        
        # Półprzezroczyste tło - FIXED
        overlay = pygame.Surface((1200, 1000), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # RGBA format zamiast set_alpha
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
        ekran.blit(info1, (x_okna + 50, y_info))           # Więcej marginesu
        ekran.blit(info2, (x_okna + 50, y_info + 30))      # Większe odstępy
        ekran.blit(info3, (x_okna + 50, y_info + 60))      # Większe odstępy
        ekran.blit(info4, (x_okna + 50, y_info + 90))      # Większe odstępy
        
        # Wybór ilości domków
        czcionka_wyb = pygame.font.SysFont('Arial', 22, bold=True)
        ekran.blit(czcionka_wyb.render("Wybierz liczbę domków do kupienia:", True, CZARNY), (x_okna + 50, y_info + 130))  # Więcej miejsca
        
        # Strzałki i liczba - FIXED buttons with better spacing
        btn_w = 50
        btn_h = 50
        btn_y = y_info + 170  # Więcej miejsca od góry - musi pasować do pozycji w obsłudze zdarzeń
        btn_x_minus = x_okna + szerokosc_okna//2 - 120  # Więcej miejsca z lewej
        btn_x_plus = x_okna + szerokosc_okna//2 + 70    # Więcej miejsca z prawej
        
        # Sprawdź hover dla przycisków
        mouse_pos = pygame.mouse.get_pos()
        btn_minus_rect = pygame.Rect(btn_x_minus, btn_y, btn_w, btn_h)
        btn_plus_rect = pygame.Rect(btn_x_plus, btn_y, btn_w, btn_h)
        
        # Przycisk minus
        minus_color = (70, 120, 170) if btn_minus_rect.collidepoint(mouse_pos) else NIEBIESKI_POLE
        narysuj_zaokraglony_prostokat(ekran, minus_color, btn_minus_rect, 12)
        czcionka_btn = pygame.font.SysFont('Arial', 32, bold=True)
        tekst_minus = czcionka_btn.render("-", True, BIALY)
        minus_text_rect = tekst_minus.get_rect(center=btn_minus_rect.center)
        ekran.blit(tekst_minus, minus_text_rect)
        
        # Przycisk plus
        plus_color = (70, 120, 170) if btn_plus_rect.collidepoint(mouse_pos) else NIEBIESKI_POLE
        narysuj_zaokraglony_prostokat(ekran, plus_color, btn_plus_rect, 12)
        tekst_plus = czcionka_btn.render("+", True, BIALY)
        plus_text_rect = tekst_plus.get_rect(center=btn_plus_rect.center)
        ekran.blit(tekst_plus, plus_text_rect)
        
        # Liczba - wyśrodkowana między przyciskami
        liczba_rect = pygame.Rect(x_okna + szerokosc_okna//2 - 30, btn_y, 60, btn_h)
        pygame.draw.rect(ekran, ZIELONY, liczba_rect, border_radius=12)
        liczba_txt = czcionka_wyb.render(str(wybrana_ilosc), True, BIALY)
        liczba_text_rect = liczba_txt.get_rect(center=liczba_rect.center)
        ekran.blit(liczba_txt, liczba_text_rect)
        
        # Suma - więcej miejsca między cenę a przyciskami
        suma = wybrana_ilosc * cena_domku
        czcionka_kwota = pygame.font.SysFont('Arial', 36, bold=True)
        tekst_kwota = czcionka_kwota.render(f"{suma} PLN", True, CZERWONY)
        kwota_rect = tekst_kwota.get_rect(centerx=x_okna + szerokosc_okna//2, y=y_info + 240)
        tlo_kwota = pygame.Rect(kwota_rect.x - 20, kwota_rect.y - 5, kwota_rect.width + 40, kwota_rect.height + 10)
        narysuj_zaokraglony_prostokat(ekran, (255, 230, 230), tlo_kwota, 5)
        ekran.blit(tekst_kwota, kwota_rect)
        
        # Przyciski kup i anuluj - pozycje z większym odstępem
        btn_kup_x = x_okna + szerokosc_okna//2 - 190   # Więcej w lewo dla lepszego rozłożenia
        btn_anuluj_x = x_okna + szerokosc_okna//2 + 90  # Więcej w prawo dla lepszego rozłożenia
        btn_y2 = y_okna + wysokosc_okna - 90            # Jeszcze więcej miejsca z dołu (90px od dołu - więcej miejsca od ceny)
        
        btn_kup_rect = pygame.Rect(btn_kup_x, btn_y2, 100, 50)    # Większe przyciski
        btn_anuluj_rect = pygame.Rect(btn_anuluj_x, btn_y2, 100, 50)  # Większe przyciski
        
        # Sprawdź hover
        kup_hover = btn_kup_rect.collidepoint(mouse_pos)
        anuluj_hover = btn_anuluj_rect.collidepoint(mouse_pos)
        
        # Przycisk Kup
        kup_color = (50, 180, 50) if kup_hover else ZIELONY
        if suma > gracz['pieniadze']:
            kup_color = (150, 150, 150)  # Szary jeśli nie stać
        narysuj_zaokraglony_prostokat(ekran, kup_color, btn_kup_rect, 10)
        czcionka_btn_text = pygame.font.SysFont('Arial', 20, bold=True)  # Większa czcionka
        tekst_kup = czcionka_btn_text.render("Kup", True, BIALY)
        kup_text_rect = tekst_kup.get_rect(center=btn_kup_rect.center)
        ekran.blit(tekst_kup, kup_text_rect)
        
        # Przycisk Anuluj
        anuluj_color = (220, 50, 50) if anuluj_hover else CZERWONY
        narysuj_zaokraglony_prostokat(ekran, anuluj_color, btn_anuluj_rect, 10)
        tekst_anuluj = czcionka_btn_text.render("Anuluj", True, BIALY)
        anuluj_text_rect = tekst_anuluj.get_rect(center=btn_anuluj_rect.center)
        ekran.blit(tekst_anuluj, anuluj_text_rect)
        
        # Instrukcje - dostosowane do nowej pozycji przycisków
        czcionka_instr = pygame.font.SysFont('Arial', 12)
        tekst_instr = czcionka_instr.render("ENTER=Kup, ESC=Anuluj, ←→=Zmień ilość", True, (100, 100, 100))
        instr_rect = tekst_instr.get_rect(centerx=x_okna + szerokosc_okna//2, y=y_okna + wysokosc_okna - 30)
        ekran.blit(tekst_instr, instr_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return 0

# Funkcja do wyświetlania ekranu wygranej
def wyswietl_ekran_wygranej(ekran, zwyciezca, glosnosc_efekty=0.7):
    """Wyświetla ekran wygranej gdy gracz osiągnie 30 ECTS"""
    clock = pygame.time.Clock()
    
    # Załaduj dźwięk wygranej (jeśli istnieje)
    try:
        dzwiek_wygrana = pygame.mixer.Sound("Audio/victory.mp3")
        dzwiek_wygrana.set_volume(glosnosc_efekty)
        dzwiek_wygrana.play()
    except:
        pass
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "new_game"
                elif event.key == pygame.K_ESCAPE:
                    return "menu"
        
        # Gradient tło
        for y in range(1000):
            color_ratio = y / 1000
            r = int(30 + (100 - 30) * color_ratio)
            g = int(50 + (150 - 50) * color_ratio)
            b = int(80 + (200 - 80) * color_ratio)
            pygame.draw.line(ekran, (r, g, b), (0, y), (1200, y))
        
        # Fajerwerki (animowane koła)
        import time
        current_time = time.time()
        for i in range(10):
            x = (i * 120 + 100) + int(50 * math.sin(current_time * 2 + i))
            y = (i * 80 + 150) + int(30 * math.cos(current_time * 3 + i))
            radius = int(20 + 15 * math.sin(current_time * 4 + i))
            color = [
                int(255 * abs(math.sin(current_time + i))),
                int(255 * abs(math.sin(current_time + i + 2))),
                int(255 * abs(math.sin(current_time + i + 4)))
            ]
            pygame.draw.circle(ekran, color, (x % 1200, y % 1000), radius)
        
        # Główny tytuł
        czcionka_tytul = pygame.font.SysFont('Arial', 72, bold=True)
        tekst_gratulacje = czcionka_tytul.render("GRATULACJE!", True, ZLOTY)
        gratulacje_rect = tekst_gratulacje.get_rect(center=(600, 200))
        
        # Cień tytułu
        tekst_cien = czcionka_tytul.render("GRATULACJE!", True, CZARNY)
        cien_rect = tekst_cien.get_rect(center=(605, 205))
        ekran.blit(tekst_cien, cien_rect)
        ekran.blit(tekst_gratulacje, gratulacje_rect)
        
        # Nazwa zwycięzcy
        czcionka_zwyciezca = pygame.font.SysFont('Arial', 48, bold=True)
        tekst_zwyciezca = czcionka_zwyciezca.render(f"{zwyciezca[KEY_NAZWA]} WYGRYWA!", True, zwyciezca[KEY_KOLOR])
        zwyciezca_rect = tekst_zwyciezca.get_rect(center=(600, 300))
        
        # Tło za nazwą zwycięzcy
        tlo_zwyciezca = pygame.Rect(zwyciezca_rect.x - 20, zwyciezca_rect.y - 10, 
                                   zwyciezca_rect.width + 40, zwyciezca_rect.height + 20)
        narysuj_zaokraglony_prostokat(ekran, BIALY, tlo_zwyciezca, 15)
        pygame.draw.rect(ekran, CZARNY, tlo_zwyciezca, 3, border_radius=15)
        ekran.blit(tekst_zwyciezca, zwyciezca_rect)
        
        # Informacje o ECTS
        czcionka_info = pygame.font.SysFont('Arial', 36)
        tekst_ects = czcionka_info.render(f"Zdobyte ECTS: {zwyciezca[KEY_ECTS]}/30", True, ZLOTY)
        ects_rect = tekst_ects.get_rect(center=(600, 380))
        ekran.blit(tekst_ects, ects_rect)
        
        # Statystyki zwycięzcy
        czcionka_stats = pygame.font.SysFont('Arial', 24)
        stats_y = 450
        stats = [
            f"Pieniądze: {zwyciezca[KEY_PIENIADZE]} PLN",
            f"Budynki: {zwyciezca[KEY_BUDYNKI]}"
        ]
        
        for i, stat in enumerate(stats):
            tekst_stat = czcionka_stats.render(stat, True, BIALY)
            stat_rect = tekst_stat.get_rect(center=(600, stats_y + i * 35))
            ekran.blit(tekst_stat, stat_rect)
        
        # Trofeum (uproszczone)
        trofeum_x, trofeum_y = 600, 600
        # Puchar
        pygame.draw.ellipse(ekran, ZLOTY, (trofeum_x - 40, trofeum_y - 30, 80, 50))
        pygame.draw.rect(ekran, ZLOTY, (trofeum_x - 5, trofeum_y + 10, 10, 30))
        pygame.draw.ellipse(ekran, ZLOTY, (trofeum_x - 20, trofeum_y + 35, 40, 15))
        
        # Uchwyty pucharu
        pygame.draw.arc(ekran, ZLOTY, (trofeum_x - 60, trofeum_y - 20, 30, 40), 0, math.pi, 5)
        pygame.draw.arc(ekran, ZLOTY, (trofeum_x + 30, trofeum_y - 20, 30, 40), 0, math.pi, 5)
        
        # Instrukcje
        czcionka_instr = pygame.font.SysFont('Arial', 28)
        instrukcje = [
            "SPACJA - Nowa gra",
            "ESC - Powrót do menu"
        ]
        
        for i, instr in enumerate(instrukcje):
            tekst_instr = czcionka_instr.render(instr, True, SZARY_JASNY)
            instr_rect = tekst_instr.get_rect(center=(600, 750 + i * 40))
            ekran.blit(tekst_instr, instr_rect)
        
        pygame.display.flip()
        clock.tick(60)

# ...existing code...