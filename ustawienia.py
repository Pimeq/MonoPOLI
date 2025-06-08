from kolory import *
import pygame
import pygame.gfxdraw
import sys
import math

# Inicjalizacja Pygame
pygame.init()

# Paleta kolorów graczy
KOLORY_GRACZY = [
    KOLOR_GRACZ_CZERWONY,    # Czerwony
    KOLOR_GRACZ_NIEBIESKI,   # Niebieski
    KOLOR_GRACZ_ZIELONY,     # Zielony
    KOLOR_GRACZ_ZOLTY,       # Żółty
    KOLOR_GRACZ_FIOLETOWY,   # Fioletowy
    KOLOR_GRACZ_POMARANCZOWY,# Pomarańczowy
    KOLOR_GRACZ_CYJAN,       # Cyjan
    KOLOR_GRACZ_ROZOWY,      # Różowy
]

# Rozmiar okna
SZEROKOSC, WYSOKOSC = 1200, 1000

class KoloKolorow:
    def __init__(self, x, y, promien, kolor_gracza):
        self.x = x
        self.y = y
        self.promien = promien
        self.kolor = kolor_gracza
        
    def rysuj(self, surface):
        """Rysuje koło z wybranym kolorem gracza z antyaliasingiem"""
        # Zewnętrzny pierścień (cień) - używamy gfxdraw dla antyaliasingu
        pygame.gfxdraw.filled_circle(surface, self.x + 2, self.y + 2, self.promien + 2, (0, 0, 0, 80))
        pygame.gfxdraw.aacircle(surface, self.x + 2, self.y + 2, self.promien + 2, (0, 0, 0, 80))
        
        # Główne koło z antyaliasingiem
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, self.promien, self.kolor)
        pygame.gfxdraw.aacircle(surface, self.x, self.y, self.promien, self.kolor)
        
        # Wewnętrzny błysk
        kolor_jasny = tuple(min(255, c + 40) for c in self.kolor)
        pygame.gfxdraw.filled_circle(surface, self.x - 3, self.y - 3, self.promien - 5, kolor_jasny)
        pygame.gfxdraw.aacircle(surface, self.x - 3, self.y - 3, self.promien - 5, kolor_jasny)

# Funkcja do rysowania zaokrąglonego prostokąta z antyaliasingiem
def narysuj_zaokraglony_prostokat(powierzchnia, kolor, prostokat, promien):
    """Rysuje prostokąt z zaokrąglonymi rogami i antyaliasingiem"""
    x, y, szer, wys = prostokat
    promien = min(promien, szer // 2, wys // 2)
    
    # Użyj wbudowanej funkcji z antyaliasingiem
    pygame.draw.rect(powierzchnia, kolor, prostokat, border_radius=promien)

# Funkcja do tworzenia przycisku z lepszym wyglądem
def utworz_przycisk(surface, tekst, x, y, szerokosc, wysokosc, kolor, kolor_tekstu, rozmiar_czcionki=32):
    """Tworzy przycisk z lepszym designem i antyaliasingiem"""
    czcionka = pygame.font.SysFont('Arial', rozmiar_czcionki, bold=True)
    prostokat = pygame.Rect(x, y, szerokosc, wysokosc)
    myszka = pygame.mouse.get_pos()
    klikniecie = pygame.mouse.get_pressed()[0]
    
    # Efekt hover
    if prostokat.collidepoint(myszka):
        kolor_hover = tuple(min(255, c + 20) for c in kolor)
        kolor = kolor_hover
    
    # Cień
    pygame.draw.rect(surface, (0, 0, 0, 60), (x+3, y+3, szerokosc, wysokosc), border_radius=15)
    
    # Rysuj przycisk
    narysuj_zaokraglony_prostokat(surface, kolor, prostokat, 15)
    
    # Renderuj tekst z antyaliasingiem
    tekst_surface = czcionka.render(tekst, True, kolor_tekstu)
    tekst_rect = tekst_surface.get_rect(center=prostokat.center)
    surface.blit(tekst_surface, tekst_rect)
    
    # Sprawdź czy przycisk został kliknięty
    if prostokat.collidepoint(myszka) and klikniecie:
        return True
    return False

# Funkcja do rysowania pionka szachowego z antyaliasingiem
def narysuj_pionek(surface, x, y, szerokosc, wysokosc, kolor_pionka=(40, 60, 100)):
    """Rysuje pionek szachowy z antyaliasingiem"""
    center_x = x + szerokosc // 2
    
    # Cień pionka - elipsa
    cien_x = x + szerokosc//4 + 2
    cien_y = int(y + wysokosc*0.75 + 2)
    cien_w = szerokosc//2
    cien_h = wysokosc//8
    
    # Rysuj podstawę pionka z antyaliasingiem
    base_x = x + szerokosc//4
    base_y = int(y + wysokosc*0.75)
    base_w = szerokosc//2
    base_h = wysokosc//8
    
    pygame.draw.ellipse(surface, kolor_pionka, (base_x, base_y, base_w, base_h))
    
    # Rysuj trzon pionka
    trzon_rect = (center_x - szerokosc//10, y + wysokosc*0.5, szerokosc//5, wysokosc*0.3)
    pygame.draw.rect(surface, kolor_pionka, trzon_rect)
    
    # Rysuj główkę pionka z antyaliasingiem
    glowka_x = center_x
    glowka_y = int(y + wysokosc*0.4)
    glowka_r = int(szerokosc*0.15)
    
    pygame.gfxdraw.filled_circle(surface, glowka_x, glowka_y, glowka_r, kolor_pionka)
    pygame.gfxdraw.aacircle(surface, glowka_x, glowka_y, glowka_r, kolor_pionka)
    
    # Dodaj efekt 3D - highlight z antyaliasingiem
    kolor_jasny = tuple(min(255, c + 40) for c in kolor_pionka)
    highlight_x = glowka_x - 2
    highlight_y = glowka_y - 2
    highlight_r = int(szerokosc*0.12)
    
    pygame.gfxdraw.filled_circle(surface, highlight_x, highlight_y, highlight_r, kolor_jasny)
    pygame.gfxdraw.aacircle(surface, highlight_x, highlight_y, highlight_r, kolor_jasny)

# Funkcja do rysowania nowoczesnego suwaka głośności
def narysuj_suwak_glosnosci(surface, x, y, szerokosc, wysokosc, wartosc=0.5):
    """Rysuje nowoczesny suwak głośności"""
    # Tło suwaka
    tlo_rect = pygame.Rect(x, y, szerokosc, wysokosc)
    pygame.draw.rect(surface, (0, 0, 0, 30), (x+2, y+2, szerokosc, wysokosc), border_radius=25)
    pygame.draw.rect(surface, SZARY_JASNY, tlo_rect, border_radius=25)
    pygame.draw.rect(surface, SZARY_CIEMNY, tlo_rect, width=2, border_radius=25)
    
    # Ikona głośnika - lepsza wersja
    ikona_x = x + 15
    ikona_y = y + wysokosc // 2
    ikona_rozmiar = 16
    
    # Główny kształt głośnika
    punkty_glosnika = [
        (ikona_x, ikona_y - 6),
        (ikona_x + 8, ikona_y - 6),
        (ikona_x + 16, ikona_y - 10),
        (ikona_x + 16, ikona_y + 10),
        (ikona_x + 8, ikona_y + 6),
        (ikona_x, ikona_y + 6)
    ]
    pygame.draw.polygon(surface, CIEMNY_FIOLET, punkty_glosnika)
    
    # Fale dźwiękowe - bardziej eleganckie
    if wartosc > 0.3:
        pygame.draw.arc(surface, CIEMNY_FIOLET, 
                       (ikona_x + 20, ikona_y - 8, 12, 16), 
                       -math.pi/3, math.pi/3, 2)
    if wartosc > 0.6:
        pygame.draw.arc(surface, CIEMNY_FIOLET, 
                       (ikona_x + 25, ikona_y - 12, 16, 24), 
                       -math.pi/3, math.pi/3, 2)
    if wartosc > 0.8:
        pygame.draw.arc(surface, CIEMNY_FIOLET, 
                       (ikona_x + 30, ikona_y - 16, 20, 32), 
                       -math.pi/3, math.pi/3, 2)
    
    # Ścieżka suwaka
    sciezka_x = x + 65
    sciezka_y = y + wysokosc // 2
    sciezka_szerokosc = szerokosc - 120
    sciezka_wysokosc = 6
    
    # Tło ścieżki
    pygame.draw.rect(surface, SZARY_CIEMNY, 
                    (sciezka_x, sciezka_y - sciezka_wysokosc//2, sciezka_szerokosc, sciezka_wysokosc), 
                    border_radius=3)
    
    # Wypełnienie ścieżki
    wypelnienie_szerokosc = int(sciezka_szerokosc * wartosc)
    if wypelnienie_szerokosc > 0:
        # Gradient effect - symulacja
        for i in range(wypelnienie_szerokosc):
            alpha = i / wypelnienie_szerokosc
            kolor_r = int(100 + alpha * 120)  # Od ciemnego do jasnego zielonego
            kolor_g = int(200 + alpha * 55)
            kolor_b = int(100 + alpha * 50)
            pygame.draw.line(surface, (kolor_r, kolor_g, kolor_b), 
                           (sciezka_x + i, sciezka_y - sciezka_wysokosc//2), 
                           (sciezka_x + i, sciezka_y + sciezka_wysokosc//2))
    
    # Uchwyt suwaka z antyaliasingiem
    uchwyt_x = sciezka_x + wypelnienie_szerokosc
    uchwyt_promien = 12
    
    # Cień uchwytu
    pygame.gfxdraw.filled_circle(surface, uchwyt_x + 2, sciezka_y + 2, uchwyt_promien, (0, 0, 0, 40))
    pygame.gfxdraw.aacircle(surface, uchwyt_x + 2, sciezka_y + 2, uchwyt_promien, (0, 0, 0, 40))
    
    # Główny uchwyt z antyaliasingiem
    pygame.gfxdraw.filled_circle(surface, uchwyt_x, sciezka_y, uchwyt_promien, BIALY)
    pygame.gfxdraw.aacircle(surface, uchwyt_x, sciezka_y, uchwyt_promien, BIALY)
    pygame.gfxdraw.aacircle(surface, uchwyt_x, sciezka_y, uchwyt_promien, SZARY_CIEMNY)
    
    # Wewnętrzny punkt z antyaliasingiem
    pygame.gfxdraw.filled_circle(surface, uchwyt_x, sciezka_y, 4, CIEMNY_FIOLET)
    pygame.gfxdraw.aacircle(surface, uchwyt_x, sciezka_y, 4, CIEMNY_FIOLET)
    
    # Tekst procentowy
    czcionka_procent = pygame.font.SysFont('Arial', 18, bold=True)
    tekst_procent = f"{int(wartosc * 100)}%"
    surface_procent = czcionka_procent.render(tekst_procent, True, CIEMNY_FIOLET)
    surface.blit(surface_procent, (x + szerokosc - 45, y + wysokosc // 2 - 10))
    
    # Obsługa kliknięcia i przeciągania
    myszka = pygame.mouse.get_pos()
    klikniecie = pygame.mouse.get_pressed()[0]
    
    if klikniecie and (sciezka_y - 20) <= myszka[1] <= (sciezka_y + 20) and sciezka_x <= myszka[0] <= (sciezka_x + sciezka_szerokosc):
        nowa_wartosc = (myszka[0] - sciezka_x) / sciezka_szerokosc
        return max(0, min(1, nowa_wartosc))
    
    return wartosc

# Funkcja do rysowania karty gracza
def narysuj_karte_gracza(surface, x, y, szerokosc, wysokosc, nazwa="Gracz", nr_gracza=1):
    """Rysuje kartę gracza z lepszym designem"""
    # Cień karty
    pygame.draw.rect(surface, (0, 0, 0, 40), (x+3, y+3, szerokosc, wysokosc), border_radius=12)
    
    # Tło karty
    pygame.draw.rect(surface, SZARY_JASNY, (x, y, szerokosc, wysokosc), border_radius=12)
    pygame.draw.rect(surface, SZARY_CIEMNY, (x, y, szerokosc, wysokosc), width=2, border_radius=12)
    
    # Kolor gracza
    kolor_gracza = KOLORY_GRACZY[(nr_gracza - 1) % len(KOLORY_GRACZY)]
    kolo_kolorow = KoloKolorow(x + szerokosc//2, y + 40, 25, kolor_gracza)
    kolo_kolorow.rysuj(surface)
    
    # Pole nazwy
    nazwa_rect = pygame.Rect(x + 15, y + 75, szerokosc - 30, 35)
    pygame.draw.rect(surface, CIEMNY_FIOLET, nazwa_rect, border_radius=8)
    
    czcionka = pygame.font.SysFont('Arial', 20, bold=True)
    tekst_nazwa = czcionka.render(nazwa, True, BIALY)
    tekst_nazwa_rect = tekst_nazwa.get_rect(center=nazwa_rect.center)
    surface.blit(tekst_nazwa, tekst_nazwa_rect)
    
    # Pionek
    narysuj_pionek(surface, x + szerokosc//4, y + 125, szerokosc//2, wysokosc - 150, kolor_gracza)


# Funkcja pomocnicza do skalowania pozycji myszy
def skaluj_pozycje_myszy(event, interface_x, interface_y, skala_interfejsu, bazowa_szerokosc, bazowa_wysokosc):
    """Skaluje pozycję myszy do współrzędnych interface_surface"""
    if hasattr(event, 'pos'):
        mouse_x, mouse_y = event.pos
        # Przelicz pozycję myszy na współrzędne względem interface_surface
        scaled_mouse_x = int((mouse_x - interface_x) / skala_interfejsu)
        scaled_mouse_y = int((mouse_y - interface_y) / skala_interfejsu)
        # Sprawdź czy pozycja jest w granicach interface_surface
        if 0 <= scaled_mouse_x < bazowa_szerokosc and 0 <= scaled_mouse_y < bazowa_wysokosc:
            event.pos = (scaled_mouse_x, scaled_mouse_y)
            return True
    return False

# Funkcja główna dla strony ustawień
def strona_ustawien(ekran_zewnetrzny=None, skala_interfejsu=1):
    """
    Wyświetla ekran ustawień gry z wyśrodkowanymi elementami i obsługą skalowania
    """
    global ekran
    
    # Bazowe wymiary interfejsu
    bazowa_szerokosc = SZEROKOSC
    bazowa_wysokosc = WYSOKOSC
      # Używaj przekazanego ekranu lub utwórz własny
    if ekran_zewnetrzny:
        ekran = ekran_zewnetrzny
        screen_width, screen_height = ekran.get_size()
    else:
        ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
        pygame.display.set_caption("MonoPOLI - Ustawienia")
        screen_width, screen_height = SZEROKOSC, WYSOKOSC
    
    # Utwórz surface dla interfejsu o bazowym rozmiarze
    interface_surface = pygame.Surface((bazowa_szerokosc, bazowa_wysokosc), pygame.SRCALPHA)
    
    # Oblicz docelowe wymiary po skalowaniu
    skalowana_szerokosc = int(bazowa_szerokosc * skala_interfejsu)
    skalowana_wysokosc = int(bazowa_wysokosc * skala_interfejsu)
    
    # Pozycja interfejsu na ekranie (centrowanie)
    interface_x = (screen_width - skalowana_szerokosc) // 2
    interface_y = (screen_height - skalowana_wysokosc) // 2
    
    # Wartość suwaka głośności
    glosnosc = 0.7
      # Główna pętla
    zegar = pygame.time.Clock()
    running = True
    
    while running:
        # Oblicz aktualną pozycję myszy względem interface_surface
        mouse_pos = pygame.mouse.get_pos()
        scaled_mouse_x = int((mouse_pos[0] - interface_x) / skala_interfejsu)
        scaled_mouse_y = int((mouse_pos[1] - interface_y) / skala_interfejsu)
        
        # Tymczasowo nadpisz pozycję myszy dla funkcji rysujących
        original_mouse_get_pos = pygame.mouse.get_pos
        def get_scaled_mouse_pos():
            return (scaled_mouse_x, scaled_mouse_y)
        pygame.mouse.get_pos = get_scaled_mouse_pos
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return False
        
        # Wyczyść główny ekran
        ekran.fill(NIEBIESKI_TLO)
        
        # Wyczyść powierzchnię interfejsu gradientem
        for y in range(bazowa_wysokosc):
            ratio = y / bazowa_wysokosc
            r = int(ZIELONY_TLO[0] * (1 - ratio) + NIEBIESKI_TLO[0] * ratio)
            g = int(ZIELONY_TLO[1] * (1 - ratio) + NIEBIESKI_TLO[1] * ratio)
            b = int(ZIELONY_TLO[2] * (1 - ratio) + NIEBIESKI_TLO[2] * ratio)
            pygame.draw.line(interface_surface, (r, g, b), (0, y), (bazowa_szerokosc, y))
        
        # Wyśrodkowanie wszystkich elementów w pionie i poziomie
          # Oblicz pozycje dla idealnego wyśrodkowania pionowego
        total_content_height = 80 + 200 + 60 + 80 + 60 + 100  # tytuł + karty + odstęp + głośność + odstęp + przycisk
        start_y = (WYSOKOSC - total_content_height) // 2
        
        # Tytuł główny
        czcionka_tytul = pygame.font.SysFont('Arial', 48, bold=True)
        tekst_tytul = czcionka_tytul.render("USTAWIENIA GRY", True, BIALY)
        tytul_rect = tekst_tytul.get_rect(center=(SZEROKOSC//2, start_y + 40))
        # Cień tytułu
        tekst_tytul_cien = czcionka_tytul.render("USTAWIENIA GRY", True, (0, 0, 0, 100))
        interface_surface.blit(tekst_tytul_cien, (tytul_rect.x + 3, tytul_rect.y + 3))
        interface_surface.blit(tekst_tytul, tytul_rect)
        
        # Sekcja graczy - wyśrodkowana
        sekcja_y = start_y + 120
        karta_szerokosc = 180
        karta_wysokosc = 200
        odstepy = 40
        
        # Oblicz całkowitą szerokość sekcji graczy
        calkowita_szerokosc = 4 * karta_szerokosc + 3 * odstepy
        start_x = (SZEROKOSC - calkowita_szerokosc) // 2
        
        # Rysuj karty graczy
        for i in range(4):
            x_pozycja = start_x + i * (karta_szerokosc + odstepy)
            nazwy_graczy = ["Gracz 1", "Gracz 2", "Gracz 3", "Gracz 4"]
            narysuj_karte_gracza(interface_surface, x_pozycja, sekcja_y, karta_szerokosc, karta_wysokosc, nazwy_graczy[i], i + 1)
        
        # Sekcja głośności - wyśrodkowana
        glosnosc_y = sekcja_y + karta_wysokosc + 80
        glosnosc_szerokosc = 550
        glosnosc_wysokosc = 80
        glosnosc_x = (SZEROKOSC - glosnosc_szerokosc) // 2
        
        # Nagłówek głośności
        czcionka_naglowek = pygame.font.SysFont('Arial', 32, bold=True)
        tekst_glosnosc = czcionka_naglowek.render("GŁOŚNOŚĆ", True, BIALY)
        glosnosc_naglowek_rect = tekst_glosnosc.get_rect(center=(SZEROKOSC//2, glosnosc_y - 40))
        # Cień nagłówka
        tekst_glosnosc_cien = czcionka_naglowek.render("GŁOŚNOŚĆ", True, (0, 0, 0, 100))
        interface_surface.blit(tekst_glosnosc_cien, (glosnosc_naglowek_rect.x + 2, glosnosc_naglowek_rect.y + 2))
        interface_surface.blit(tekst_glosnosc, glosnosc_naglowek_rect)
        
        # Suwak głośności
        nowa_glosnosc = narysuj_suwak_glosnosci(interface_surface, glosnosc_x, glosnosc_y, glosnosc_szerokosc, glosnosc_wysokosc, glosnosc)
        if nowa_glosnosc != glosnosc:
            glosnosc = nowa_glosnosc
            print(f"Ustawiono głośność: {glosnosc*100:.0f}%")
          # Przycisk powrotu - wyśrodkowany
        przycisk_szerokosc = 300
        przycisk_wysokosc = 80
        przycisk_x = (SZEROKOSC - przycisk_szerokosc) // 2
        przycisk_y = glosnosc_y + glosnosc_wysokosc + 60
        
        if utworz_przycisk(interface_surface, "POWRÓT DO MENU", przycisk_x, przycisk_y, przycisk_szerokosc, przycisk_wysokosc, NIEBIESKI_TLO, BIALY):
            running = False
            # Przywróć oryginalną funkcję myszy
            pygame.mouse.get_pos = original_mouse_get_pos
            return True
        
        # Przywróć oryginalną funkcję myszy
        pygame.mouse.get_pos = original_mouse_get_pos
        
        # Skaluj i wyrysuj interface_surface na głównym ekranie
        if skala_interfejsu != 1.0:
            scaled_surface = pygame.transform.scale(interface_surface, (skalowana_szerokosc, skalowana_wysokosc))
            ekran.blit(scaled_surface, (interface_x, interface_y))
        else:
            ekran.blit(interface_surface, (interface_x, interface_y))
        
        # Aktualizuj ekran
        pygame.display.flip()
        zegar.tick(60)
    
    return False