from constants import *
import pygame
import pygame.gfxdraw
import pygame.mixer
import sys
import math
import random
import time

# Paleta kolorów graczy
KOLORY_GRACZY = [
    CZERWONY_GRACZ,    # Czerwony
    NIEBIESKI_GRACZ,   # Niebieski
    ZIELONY_GRACZ,     # Zielony
    ZOLTY_GRACZ,       # Żółty
    FIOLETOWY_GRACZ,   # Fioletowy
    POMARANCZOWY_GRACZ,# Pomarańczowy
    CYJAN_GRACZ,       # Cyjan
    ROZOWY_GRACZ,      # Różowy
]

# Rozmiar okna
SZEROKOSC, WYSOKOSC = SCREEN_WIDTH, SCREEN_HEIGHT

# Global player names for editing in settings
nazwy_graczy = [f"Gracz {i+1}" for i in range(4)]

# Klasa animowanego tła (skopiowana z landing page)
class AnimowaneTlo:
    def __init__(self, szerokosc, wysokosc):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.punkty = []
        self.linie = []
        self.czas = 0
        
        # Utwórz losowe punkty
        for _ in range(ANIMATION_POINTS_COUNT):
            self.punkty.append([random.randint(0, szerokosc), random.randint(0, wysokosc), 
                              random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)])
        
        # Utwórz linie łączące punkty
        self.przelicz_linie()
    
    def przelicz_linie(self):
        self.linie = []
        for i in range(len(self.punkty)):
            for j in range(i+1, len(self.punkty)):
                odleglosc = math.sqrt((self.punkty[i][0] - self.punkty[j][0])**2 + 
                                    (self.punkty[i][1] - self.punkty[j][1])**2)
                if odleglosc < ANIMATION_MAX_DISTANCE:
                    alpha = int(255 * (1 - odleglosc / ANIMATION_MAX_DISTANCE))
                    self.linie.append((i, j, alpha))
    
    def aktualizuj(self):
        self.czas += 0.01
        
        # Aktualizuj pozycje punktów
        for punkt in self.punkty:
            punkt[0] += punkt[2]
            punkt[1] += punkt[3]
            
            # Dodaj delikatną sinusoidalną animację
            punkt[0] += math.sin(self.czas + punkt[0] * 0.01) * 0.2
            punkt[1] += math.cos(self.czas + punkt[1] * 0.01) * 0.2
            
            # Odbicie od krawędzi
            if punkt[0] < 0:
                punkt[0] = 0
                punkt[2] *= -1
            if punkt[0] > self.szerokosc:
                punkt[0] = self.szerokosc
                punkt[2] *= -1
            if punkt[1] < 0:
                punkt[1] = 0
                punkt[3] *= -1
            if punkt[1] > self.wysokosc:
                punkt[1] = self.wysokosc
                punkt[3] *= -1
        
        # Przeliczaj linie co 10 klatek
        if int(self.czas * ANIMATION_TIMER_MULTIPLIER) % ANIMATION_TIMER_MODULO == 0:
            self.przelicz_linie()
    
    def rysuj(self, ekran):
        # Rysuj linie
        for i, j, alpha in self.linie:
            kolor = (100, 150, 255, alpha // ANIMATION_ALPHA_DIVISOR)
            pygame.gfxdraw.line(ekran, int(self.punkty[i][0]), int(self.punkty[i][1]), 
                              int(self.punkty[j][0]), int(self.punkty[j][1]), kolor)
        
        # Rysuj punkty
        for punkt in self.punkty:
            pygame.gfxdraw.filled_circle(ekran, int(punkt[0]), int(punkt[1]), ANIMATION_CIRCLE_RADIUS, (150, 200, 255, 100))
            pygame.gfxdraw.aacircle(ekran, int(punkt[0]), int(punkt[1]), ANIMATION_CIRCLE_RADIUS, (200, 230, 255, 150))

class KoloKolorow:
    def __init__(self, x, y, promien, kolor_gracza):
        self.x = x
        self.y = y
        self.promien = promien
        self.kolor = kolor_gracza
        
    def rysuj(self, surface):
        """Rysuje koło z wybranym kolorem gracza z antyaliasingiem"""
        # Zewnętrzny pierścień (cień) - używamy gfxdraw dla antyaliasingu
        pygame.gfxdraw.filled_circle(surface, self.x + ANIMATION_CIRCLE_SHADOW_OFFSET, self.y + ANIMATION_CIRCLE_SHADOW_OFFSET, 
                                   self.promien + ANIMATION_CIRCLE_SHADOW_OFFSET, (0, 0, 0, SHADOW_ALPHA))
        pygame.gfxdraw.aacircle(surface, self.x + ANIMATION_CIRCLE_SHADOW_OFFSET, self.y + ANIMATION_CIRCLE_SHADOW_OFFSET, 
                              self.promien + ANIMATION_CIRCLE_SHADOW_OFFSET, (0, 0, 0, SHADOW_ALPHA))
        
        # Główne koło z antyaliasingiem
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, self.promien, self.kolor)
        pygame.gfxdraw.aacircle(surface, self.x, self.y, self.promien, self.kolor)
        
        # Wewnętrzny błysk
        kolor_jasny = tuple(min(255, c + ANIMATION_COLOR_BOOST) for c in self.kolor)
        pygame.gfxdraw.filled_circle(surface, self.x - 3, self.y - 3, self.promien - 5, kolor_jasny)
        pygame.gfxdraw.aacircle(surface, self.x - 3, self.y - 3, self.promien - 5, kolor_jasny)

# Funkcja do rysowania zaokrąglonego prostokąta z antyaliasingiem
def narysuj_zaokraglony_prostokat(powierzchnia, kolor, prostokat, promien):
    """Rysuje prostokąt z zaokrąglonymi rogami i antyaliasingiem"""
    x, y, szer, wys = prostokat
    promien = min(promien, szer // 2, wys // 2)
    
    # Użyj wbudowanej funkcji z antyaliasingiem
    pygame.draw.rect(powierzchnia, kolor, prostokat, border_radius=promien)

def utworz_przycisk(surface, tekst, x, y, szerokosc, wysokosc, kolor, kolor_tekstu, rozmiar_czcionki=INFO_FONT_SIZE, glosnosc_efekty=None):
    czcionka = pygame.font.SysFont('Arial', rozmiar_czcionki, bold=True)
    prostokat = pygame.Rect(x, y, szerokosc, wysokosc)
    myszka = pygame.mouse.get_pos()
    klikniecie = pygame.mouse.get_pressed()[0]
    
    # Efekt hover
    if prostokat.collidepoint(myszka):
        kolor_hover = tuple(min(255, c + ANIMATION_HOVER_COLOR_BOOST) for c in kolor)
        kolor = kolor_hover
    
    # Cień
    pygame.draw.rect(surface, (0, 0, 0), (x+3, y+3, szerokosc, wysokosc), border_radius=0)
    
    # Rysuj przycisk
    narysuj_zaokraglony_prostokat(surface, kolor, prostokat, 0)
    
    # Renderuj tekst z antyaliasingiem
    tekst_surface = czcionka.render(tekst, True, kolor_tekstu)
    tekst_rect = tekst_surface.get_rect(center=prostokat.center)
    surface.blit(tekst_surface, tekst_rect)
    
    # Sprawdź czy przycisk został kliknięty
    if prostokat.collidepoint(myszka) and klikniecie:
        try:
            sound = pygame.mixer.Sound("Audio/button.mp3")
            if glosnosc_efekty is not None:
                sound.set_volume(glosnosc_efekty)
            sound.play()
        except Exception:
            pass
        return True
    return False

# Funkcja do rysowania pionka szachowego z antyaliasingiem
def narysuj_pionek(surface, x, y, szerokosc, wysokosc, kolor_pionka=KOLOR_KOSTKA_PIONEK):
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
    pygame.draw.rect(surface, (0, 0, 0), (x+2, y+2, szerokosc, wysokosc), border_radius=25)
    pygame.draw.rect(surface, SZARY_JASNY, tlo_rect, border_radius=25)
    pygame.draw.rect(surface, SZARY_CIEMNY, tlo_rect, width=2, border_radius=25)
    
    # Ikona głośnika - lepsza wersja
    ikona_x = x + 15
    ikona_y = y + wysokosc // 2
    
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

# Funkcja do animacji tytułu dla strony ustawień
def animuj_tytul_ustawienia(ekran, x, y):
    czcionka_tytul = pygame.font.SysFont('Arial', 48, bold=True)
    
    czas = pygame.time.get_ticks() / 1000
    
    # Animowany kolor (pulsujący)
    kolor_pulsujacy = (
        min(255, max(200, int(255 + 35 * math.sin(czas * 2)))),
        min(255, max(200, int(255 + 35 * math.sin(czas * 2.5)))),
        min(255, max(200, int(255 + 35 * math.cos(czas * 2))))
    )
    
    # Renderowanie tekstu z efektem świecenia
    tekst = czcionka_tytul.render("USTAWIENIA GRY", True, kolor_pulsujacy)
    
    # Efekt świecenia
    for i in range(6, 0, -2):
        alpha = 30 - i * 3
        if alpha > 0:
            powierzchnia = pygame.Surface((tekst.get_width() + i*2, tekst.get_height() + i*2), pygame.SRCALPHA)
            powierzchnia.fill((0, 0, 0, 0))
            pygame.gfxdraw.filled_ellipse(powierzchnia, powierzchnia.get_width()//2, powierzchnia.get_height()//2, 
                                       powierzchnia.get_width()//2, powierzchnia.get_height()//2, 
                                       (kolor_pulsujacy[0], kolor_pulsujacy[1], kolor_pulsujacy[2], alpha))
            ekran.blit(powierzchnia, (x - i, y - i))
    
    # Cień tekstu
    tekst_cien = czcionka_tytul.render("USTAWIENIA GRY", True, (0, 0, 0, 100))
    ekran.blit(tekst_cien, (x + 3, y + 3))
    
    # Główny tekst
    ekran.blit(tekst, (x, y))

# Funkcja do animowanego pionka dla strony ustawień
def animuj_pionek_ustawienia(ekran, x, y, rozmiar, kolor_pionka):
    czas = pygame.time.get_ticks() / 1000
    
    # Animacja skakania
    offset_y = int(math.sin(czas * 2 + x * 0.01) * 8)
    skala = 1.0 + 0.03 * math.sin(czas * 3 + y * 0.01)
    
    # Dodaj cień pod pionkiem
    pygame.gfxdraw.filled_ellipse(ekran, x, y + rozmiar//2 - offset_y//2, 
                               int(rozmiar * 0.6), int(rozmiar * 0.2), (0, 0, 0, 80))
    
    # Rysuj pionek z animacją
    narysuj_pionek(ekran, x - int(rozmiar * skala)//2, y - offset_y, 
                  int(rozmiar * skala), int(rozmiar * skala), kolor_pionka)

# Funkcja główna dla strony ustawień z animowanym tłem
def strona_ustawien(ekran_zewnetrzny=None, skala_interfejsu=1):
    """
    Wyświetla ekran ustawień gry z animowanym tłem jak na landing page
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
    
    # Utwórz animowane tło
    animowane_tlo = AnimowaneTlo(bazowa_szerokosc, bazowa_wysokosc)
    
    # Utwórz surface dla interfejsu o bazowym rozmiarze
    interface_surface = pygame.Surface((bazowa_szerokosc, bazowa_wysokosc), pygame.SRCALPHA)
    
    # Oblicz docelowe wymiary po skalowaniu
    skalowana_szerokosc = int(bazowa_szerokosc * skala_interfejsu)
    skalowana_wysokosc = int(bazowa_wysokosc * skala_interfejsu)
    
    # Pozycja interfejsu na ekranie (centrowanie)
    interface_x = (screen_width - skalowana_szerokosc) // 2
    interface_y = (screen_height - skalowana_wysokosc) // 2
    
    # Wartość suwaka głośności
    try:
        glosnosc = pygame.mixer.music.get_volume()
    except Exception:
        glosnosc = 0.7
    glosnosc_efekty = getattr(strona_ustawien, 'glosnosc_efekty', 0.7)
    
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
        ekran.fill((0, 0, 20))
        
        # ===== ANIMOWANE TŁO (tak samo jak na landing page) =====
        # Narysuj animowane tło punktów i linii
        animowane_tlo.aktualizuj()
        animowane_tlo.rysuj(ekran)
        
        # Rysuj półprzezroczysty gradient (tak samo jak na landing page)
        for i in range(0, WYSOKOSC, 2):  # Rysuj co drugą linię dla szybkości
            alpha = 150 - i * 0.15
            if alpha > 0:
                pygame.gfxdraw.hline(ekran, 0, SZEROKOSC, i, 
                                  (0, int(30 + i * 0.05), int(80 + i * 0.15), int(alpha)))
        
        # Wyczyść powierzchnię interfejsu (przezroczysta)
        interface_surface.fill((0, 0, 0, 0))
        
        # ===== ZAWARTOŚĆ STRONY USTAWIEŃ =====
        
        # Oblicz pozycje dla idealnego wyśrodkowania pionowego
        total_content_height = 80 + 200 + 60 + 80 + 60 + 100  # tytuł + karty + odstęp + głośność + odstęp + przycisk
        start_y = (WYSOKOSC - total_content_height) // 2
        
        # Tytuł główny z animacją
        tytul_x = SZEROKOSC//2 - 200
        tytul_y = start_y + 40
        animuj_tytul_ustawienia(interface_surface, tytul_x, tytul_y)
        
        # Animowane pionki w rogach
        animuj_pionek_ustawienia(interface_surface, 80, 80, 60, KOLORY_GRACZY[0])
        animuj_pionek_ustawienia(interface_surface, SZEROKOSC - 80, 80, 60, KOLORY_GRACZY[1])
        animuj_pionek_ustawienia(interface_surface, 80, WYSOKOSC - 80, 60, KOLORY_GRACZY[2])
        animuj_pionek_ustawienia(interface_surface, SZEROKOSC - 80, WYSOKOSC - 80, 60, KOLORY_GRACZY[3])
        
        # Sekcja graczy - wyśrodkowana
        sekcja_y = start_y + 120
        karta_szerokosc = 180
        karta_wysokosc = 200
        odstepy = 40
        
        # Oblicz całkowitą szerokość sekcji graczy
        calkowita_szerokosc = 4 * karta_szerokosc + 3 * odstepy
        start_x = (SZEROKOSC - calkowita_szerokosc) // 2
        
        # Rysuj karty graczy i pola edycji nazw
        global nazwy_graczy
        aktywne_pole = getattr(strona_ustawien, 'aktywne_pole', None)
        for i in range(4):
            x_pozycja = start_x + i * (karta_szerokosc + odstepy)
            narysuj_karte_gracza(interface_surface, x_pozycja, sekcja_y, karta_szerokosc, karta_wysokosc, nazwy_graczy[i], i + 1)
            # Pole edycji nazwy
            pole_rect = pygame.Rect(x_pozycja + 15, sekcja_y + 75, karta_szerokosc - 30, 35)
            kolor_pola = (255,255,255) if aktywne_pole == i else (230,230,230)
            pygame.draw.rect(interface_surface, kolor_pola, pole_rect, border_radius=8)
            pygame.draw.rect(interface_surface, (120,120,120), pole_rect, 2, border_radius=8)
            czcionka = pygame.font.SysFont('Arial', 18)
            tekst = czcionka.render(nazwy_graczy[i], True, (40,40,40))
            interface_surface.blit(tekst, (pole_rect.x+8, pole_rect.y+6))
            # Obsługa kliknięcia
            if pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                if pole_rect.collidepoint(mx, my):
                    strona_ustawien.aktywne_pole = i
        # Obsługa wpisywania znaków
        for event in pygame.event.get():
            if hasattr(strona_ustawien, 'aktywne_pole') and strona_ustawien.aktywne_pole is not None:
                if event.type == pygame.KEYDOWN:
                    idx = strona_ustawien.aktywne_pole
                    if event.key == pygame.K_BACKSPACE:
                        nazwy_graczy[idx] = nazwy_graczy[idx][:-1]
                    elif event.key == pygame.K_RETURN:
                        strona_ustawien.aktywne_pole = None
                    elif len(nazwy_graczy[idx]) < 16 and event.unicode.isprintable():
                        nazwy_graczy[idx] += event.unicode
        
        # Sekcja głośności - wyśrodkowana
        glosnosc_y = sekcja_y + karta_wysokosc + 80
        glosnosc_szerokosc = 550
        glosnosc_wysokosc = 80
        glosnosc_x = (SZEROKOSC - glosnosc_szerokosc) // 2
        
        # Nagłówek głośności muzyki
        czcionka_naglowek = pygame.font.SysFont('Arial', 32, bold=True)
        czas = pygame.time.get_ticks() / 1000
        kolor_naglowka = (
            min(255, max(200, int(255 + 25 * math.sin(czas * 1.5)))),
            min(255, max(200, int(255 + 25 * math.sin(czas * 1.8)))),
            min(255, max(200, int(255 + 25 * math.cos(czas * 1.2))))
        )
        tekst_glosnosc = czcionka_naglowek.render("GŁOŚNOŚĆ MUZYKI", True, kolor_naglowka)
        glosnosc_naglowek_rect = tekst_glosnosc.get_rect(center=(SZEROKOSC//2, glosnosc_y - 40))
        tekst_glosnosc_cien = czcionka_naglowek.render("GŁOŚNOŚĆ MUZYKI", True, (0, 0, 0))
        interface_surface.blit(tekst_glosnosc_cien, (glosnosc_naglowek_rect.x + 2, glosnosc_naglowek_rect.y + 2))
        interface_surface.blit(tekst_glosnosc, glosnosc_naglowek_rect)
        
        # Suwak muzyki
        nowa_glosnosc = narysuj_suwak_glosnosci(interface_surface, glosnosc_x, glosnosc_y, glosnosc_szerokosc, glosnosc_wysokosc, glosnosc)
        if nowa_glosnosc != glosnosc:
            glosnosc = nowa_glosnosc
            try:
                pygame.mixer.music.set_volume(glosnosc)
            except:
                pass
            print(f"Ustawiono głośność muzyki: {glosnosc*100:.0f}%")
        
        # Suwak efektów dźwiękowych
        efekty_y = glosnosc_y + glosnosc_wysokosc + 60
        tekst_efekty = czcionka_naglowek.render("GŁOŚNOŚĆ EFEKTÓW", True, kolor_naglowka)
        efekty_naglowek_rect = tekst_efekty.get_rect(center=(SZEROKOSC//2, efekty_y - 40))
        tekst_efekty_cien = czcionka_naglowek.render("GŁOŚNOŚĆ EFEKTÓW", True, (0, 0, 0))
        interface_surface.blit(tekst_efekty_cien, (efekty_naglowek_rect.x + 2, efekty_naglowek_rect.y + 2))
        interface_surface.blit(tekst_efekty, efekty_naglowek_rect)
        
        nowa_glosnosc_efekty = narysuj_suwak_glosnosci(interface_surface, glosnosc_x, efekty_y, glosnosc_szerokosc, glosnosc_wysokosc, glosnosc_efekty)
        if nowa_glosnosc_efekty != glosnosc_efekty:
            glosnosc_efekty = nowa_glosnosc_efekty
            print(f"Ustawiono głośność efektów: {glosnosc_efekty*100:.0f}%")
        strona_ustawien.glosnosc_efekty = glosnosc_efekty
        
        # Przycisk powrotu - wyśrodkowany, przesunięty pod suwak efektów
        przycisk_szerokosc = 300
        przycisk_wysokosc = 80
        przycisk_x = (SZEROKOSC - przycisk_szerokosc) // 2
        przycisk_y = efekty_y + glosnosc_wysokosc + 60  # Teraz pod suwakiem efektów
        
        if utworz_przycisk(interface_surface, "POWRÓT DO MENU", przycisk_x, przycisk_y, przycisk_szerokosc, przycisk_wysokosc, CZERWONY_CIEMNY, BIALY, 32, glosnosc_efekty):
            running = False
            # Przywróć oryginalną funkcję myszy
            pygame.mouse.get_pos = original_mouse_get_pos
            return True
        
        # Przywróć oryginalną funkcję myszy
        pygame.mouse.get_pos = original_mouse_get_pos
        
        # Narysuj interface_surface na głównym ekranie (z animowanym tłem)
        if skala_interfejsu != 1.0:
            scaled_surface = pygame.transform.scale(interface_surface, (skalowana_szerokosc, skalowana_wysokosc))
            ekran.blit(scaled_surface, (interface_x, interface_y))
        else:
            ekran.blit(interface_surface, (interface_x, interface_y))
        
        # Aktualizuj ekran
        pygame.display.flip()
        zegar.tick(60)
    
    return False

# Test funkcji (jeśli uruchomiony bezpośrednio)
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
    pygame.display.set_caption("MonoPOLI - Ustawienia Test")
    strona_ustawien(ekran)
    pygame.quit()