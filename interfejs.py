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