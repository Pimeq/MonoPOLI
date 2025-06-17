from constants import *
import pygame
import sys
import math
import random
from pygame import gfxdraw
import time
from pygame.locals import *
from interfejs import utworz_przycisk, narysuj_zaokraglony_prostokat, narysuj_kostke, narysuj_pionek
from plansza import *

# Import stron gry
try:
    from ustawienia import strona_ustawien
except ImportError:
    def strona_ustawien(ekran=None):
        print("Moduł ustawień nie został znaleziony!")
        return False

try:
    from plansza import ekran_gry
except ImportError:
    def ekran_gry(ekran=None):
        print("Moduł planszy gry nie został znaleziony!")
        return False

# Inicjalizacja Pygame
pygame.init()

# Rozmiar okna
SZEROKOSC, WYSOKOSC = 1200, 1000

# Utworzenie okna z obsługą przezroczystości
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC), HWSURFACE)
pygame.display.set_caption("MonoPOLI")

# Audio setup
pygame.mixer.init()
SOUND_BUTTON = pygame.mixer.Sound("Audio/button.mp3")
SOUND_DICE = pygame.mixer.Sound("Audio/dice.mp3")
SOUND_PLAYERMOVE = pygame.mixer.Sound("Audio/playermove.mp3")
pygame.mixer.music.load("Audio/music.mp3")

class KostkaTrojwymiarowa:
    def __init__(self, x, y, rozmiar):
        self.x = x
        self.y = y
        self.rozmiar = rozmiar
        self.wartosc = random.randint(1, 6)
        
        # Kąty obrotu (w zakresie 0-360)
        self.obrot_x = 0
        self.obrot_y = 0
        self.obrot_z = 0
        
        # Stałe prędkości obrotu
        self.predkosc_x = 20  # stopni na sekundę
        self.predkosc_y = 30   # stopni na sekundę
        self.predkosc_z = 15
    
    def aktualizuj(self, delta_czas):
        # Stały, ciągły obrót
        self.obrot_x = (self.obrot_x + self.predkosc_x * delta_czas) % 360
        self.obrot_y = (self.obrot_y + self.predkosc_y * delta_czas) % 360
        self.obrot_z = (self.obrot_z + self.predkosc_z * delta_czas) % 360
        
    def rysuj(self, ekran):
        self._rysuj_3d(ekran)
    
    def _rysuj_3d(self, ekran):
        centrum_x = self.x
        centrum_y = self.y
        polowa = self.rozmiar / 2.0

        # 1) Wierzchołki kostki w lokalnym układzie
        local_verts = [
            (-polowa, -polowa, -polowa),
            ( polowa, -polowa, -polowa),
            ( polowa,  polowa, -polowa),
            (-polowa,  polowa, -polowa),
            (-polowa, -polowa,  polowa),
            ( polowa, -polowa,  polowa),
            ( polowa,  polowa,  polowa),
            (-polowa,  polowa,  polowa),
        ]

        # 2) Ściany i indeksy wierzchołków + wartość oczek
        faces = [
            ([0,1,2,3], 1),  # tył
            ([4,5,6,7], 6),  # przód
            ([0,4,7,3], 2),  # lewa
            ([1,5,6,2], 5),  # prawa
            ([0,1,5,4], 3),  # dół
            ([3,2,6,7], 4),  # góra
        ]
        base_colors = [
            (220,220,220), (255,255,255), (200,200,200),
            (240,240,240), (180,180,180), (230,230,230),
        ]

        # 3) Obrót + rzut ortogonalny
        transformed = []
        for vx, vy, vz in local_verts:
            # rotacja X
            ay = math.radians(self.obrot_x)
            ry = vy*math.cos(ay) - vz*math.sin(ay)
            rz = vy*math.sin(ay) + vz*math.cos(ay)
            rx = vx
            # rotacja Y
            by = math.radians(self.obrot_y)
            rz2 = rz*math.cos(by) - rx*math.sin(by)
            rx2 = rz*math.sin(by) + rx*math.cos(by)
            ry2 = ry
            # rotacja Z
            cy = math.radians(self.obrot_z)
            rx3 = rx2*math.cos(cy) - ry2*math.sin(cy)
            ry3 = rx2*math.sin(cy) + ry2*math.cos(cy)
            rz3 = rz2
            # rzut orto
            x2 = centrum_x + rx3
            y2 = centrum_y + ry3
            transformed.append((rx3, ry3, rz3, x2, y2))

        # 4) Sortowanie ścian wg głębokości
        face_order = []
        for idx, (inds, _) in enumerate(faces):
            avg_z = sum(transformed[i][2] for i in inds)/4.0
            face_order.append((idx, avg_z))
        face_order.sort(key=lambda x: x[1], reverse=True)

        # 5) przygotowanie źródła światła (wektor znormalizowany)
        # np. światło nad i przed widzem:
        L = (1, 1, -0.5)
        l_len = math.sqrt(L[0]*L[0] + L[1]*L[1] + L[2]*L[2])
        L = (L[0]/l_len, L[1]/l_len, L[2]/l_len)

        # 6) Pip–patterns
        pip_patterns = {
            1: [(0,0)],
            2: [(-.5,-.5),(.5,.5)],
            3: [(-.5,-.5),(0,0),(.5,.5)],
            4: [(-.5,-.5),(-.5,.5),(.5,-.5),(.5,.5)],
            5: [(-.5,-.5),(-.5,.5),(0,0),(.5,-.5),(.5,.5)],
            6: [(-.5,-.5),(-.5,0),(-.5,.5),(.5,-.5),(.5,0),(.5,.5)],
        }
        offset = polowa * 0.7
        pip_r = max(3, int(offset * 0.15))

        # 7) Rysowanie ścian i pipów
        for face_idx, _ in face_order:
            inds, val = faces[face_idx]
            base_col = base_colors[face_idx]

            # oblicz normalną ściany przez iloczyn wektorowy:
            p0 = transformed[inds[0]][:3]
            p1 = transformed[inds[1]][:3]
            p3 = transformed[inds[3]][:3]
            # u = p1-p0, v = p3-p0
            u = (p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2])
            v = (p3[0]-p0[0], p3[1]-p0[1], p3[2]-p0[2])
            # n = u × v
            nx = u[1]*v[2] - u[2]*v[1]
            ny = u[2]*v[0] - u[0]*v[2]
            nz = u[0]*v[1] - u[1]*v[0]
            n_len = math.sqrt(nx*nx + ny*ny + nz*nz)
            n = (nx/n_len, ny/n_len, nz/n_len)

            # jasność = max(0, n·L)
            brightness = max(0.0,
            n[0]*L[0] + n[1]*L[1] + n[2]*L[2]
            )
            # skalowanie do [0.5…1.0] dla delikatnego cienia
            factor = 0.8 + 0.3 * brightness
            col = (
                min(255, int(base_col[0] * factor)),
                min(255, int(base_col[1] * factor)),
                min(255, int(base_col[2] * factor))
            )

            # punkty 2D
            poly2d = [(transformed[i][3], transformed[i][4]) for i in inds]
            # wypełnienie + AA krawędzi
            pygame.gfxdraw.filled_polygon(ekran, poly2d, col)
            pygame.gfxdraw.aapolygon(ekran, poly2d, (0,0,0))

            # środek ściany 3D
            cx3 = sum(transformed[i][0] for i in inds)/4.0
            cy3 = sum(transformed[i][1] for i in inds)/4.0
            cz3 = sum(transformed[i][2] for i in inds)/4.0

            # u,v znormalizowane
            ul = math.sqrt(u[0]*u[0]+u[1]*u[1]+u[2]*u[2])
            vl = math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
            u = (u[0]/ul, u[1]/ul, u[2]/ul)
            v = (v[0]/vl, v[1]/vl, v[2]/vl)

            # rysuj pipy
            for pu, pv in pip_patterns[val]:
                # pozycja 3D
                px3 = cx3 + u[0]*(pu*offset) + v[0]*(pv*offset)
                py3 = cy3 + u[1]*(pu*offset) + v[1]*(pv*offset)
                # projekcja orto
                sx = int(centrum_x + px3)
                sy = int(centrum_y + py3)
                # pip: wypełniony + AA obrys
                pygame.gfxdraw.filled_circle(ekran, sx, sy, pip_r, (0,0,0))
                pygame.gfxdraw.aacircle(ekran, sx, sy, pip_r, (0,0,0))
    
    def _rysuj_kropki(self, ekran, x, y, wartosc, promien):
        # Układy kropek dla każdej wartości kostki
        kropki_pozycje = {
            1: [(0, 0)],
            2: [(-0.5, -0.5), (0.5, 0.5)],
            3: [(-0.5, -0.5), (0, 0), (0.5, 0.5)],
            4: [(-0.5, -0.5), (-0.5, 0.5), (0.5, -0.5), (0.5, 0.5)],
            5: [(-0.5, -0.5), (-0.5, 0.5), (0, 0), (0.5, -0.5), (0.5, 0.5)],
            6: [(-0.5, -0.5), (-0.5, 0), (-0.5, 0.5), (0.5, -0.5), (0.5, 0), (0.5, 0.5)]
        }
        
        rozmiar_kropki = max(3, promien * 0.15)
        
        for px, py in kropki_pozycje[wartosc]:
            pygame.draw.circle(
                ekran,
                (0, 0, 0),  # Czarne kropki
                (int(x + px * promien * 0.7), int(y + py * promien * 0.7)),
                int(rozmiar_kropki)
            )

class Czasteczka:
    def __init__(self, x, y, kolor):
        self.x = x
        self.y = y
        self.kolor = kolor
        self.rozmiar = random.randint(3, 8)
        self.predkosc_x = random.uniform(-3, 3)
        self.predkosc_y = random.uniform(-5, -1)
        self.grawitacja = 0.1
        self.czas_zycia = random.randint(30, 90)
        
    def aktualizuj(self):
        self.x += self.predkosc_x
        self.y += self.predkosc_y
        self.predkosc_y += self.grawitacja
        self.czas_zycia -= 1
        self.rozmiar = max(0, self.rozmiar - 0.1)
    
    def rysuj(self, ekran):
        alpha = int(255 * (self.czas_zycia / 90))
        kolor_z_alpha = (self.kolor[0], self.kolor[1], self.kolor[2], alpha)
        pygame.gfxdraw.filled_circle(ekran, int(self.x), int(self.y), int(self.rozmiar), kolor_z_alpha)

# Klasa animowanego tła
class AnimowaneTlo:
    def __init__(self, szerokosc, wysokosc):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.punkty = []
        self.linie = []
        self.czas = 0
        
        # Utwórz 20 losowych punktów
        for _ in range(20):
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
                if odleglosc < 300:  # Łącz tylko punkty w odległości mniejszej niż 300
                    alpha = int(255 * (1 - odleglosc / 300))
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
        if int(self.czas * 100) % 10 == 0:
            self.przelicz_linie()
    
    def rysuj(self, ekran):
        # Rysuj linie
        for i, j, alpha in self.linie:
            kolor = (100, 150, 255, alpha // 3)
            pygame.gfxdraw.line(ekran, int(self.punkty[i][0]), int(self.punkty[i][1]), 
                              int(self.punkty[j][0]), int(self.punkty[j][1]), kolor)
        
        # Rysuj punkty
        for punkt in self.punkty:
            pygame.gfxdraw.filled_circle(ekran, int(punkt[0]), int(punkt[1]), 3, (150, 200, 255, 100))
            pygame.gfxdraw.aacircle(ekran, int(punkt[0]), int(punkt[1]), 3, (200, 230, 255, 150))

# Poprawiona funkcja do rysowania przycisków - jednoznacznie czerwone
def narysuj_przycisk_3d(ekran, tekst, x, y, szerokosc, wysokosc, kolor, kolor_tekstu, animacja=0, glosnosc_efekty=None):
    # Sprawdź hover
    myszka_x, myszka_y = pygame.mouse.get_pos()
    hover = (x <= myszka_x <= x + szerokosc and y <= myszka_y <= y + wysokosc)
    
    # Określ kolor przycisku
    if hover:
        # Lekko jaśniejszy czerwony przy hover
        kolor_przycisku = (min(kolor[0] + 30, 255), min(kolor[1] + 20, 255), min(kolor[2] + 20, 255))
    else:
        kolor_przycisku = kolor
    
    # Pozycja z animacją wciśnięcia
    pozycja_y = y + animacja * 3
    
    # Narysuj cień
    pygame.draw.rect(ekran, (0, 0, 0, 80), (x + 3, pozycja_y + 3, szerokosc, wysokosc))
    
    # Narysuj główny prostokąt
    pygame.draw.rect(ekran, kolor_przycisku, (x, pozycja_y, szerokosc, wysokosc))
    
    # Dodaj subtelny gradient tylko na górze (bez białego koloru)
    for i in range(15):
        alpha = 50 - i * 3
        if alpha > 0:
            # Używamy tego samego koloru co przycisk, tylko jaśniejszego
            gradient_kolor = (
                min(kolor_przycisku[0] + 20, 255),
                min(kolor_przycisku[1] + 15, 255),
                min(kolor_przycisku[2] + 15, 255)
            )
            powierzchnia = pygame.Surface((szerokosc, 1), pygame.SRCALPHA)
            powierzchnia.fill((*gradient_kolor, alpha))
            ekran.blit(powierzchnia, (x, pozycja_y + i))
    
    # Dodaj tekst
    czcionka = pygame.font.SysFont('Arial', 30, bold=True)
    tekst_powierzchnia = czcionka.render(tekst, True, kolor_tekstu)
    tekst_rect = tekst_powierzchnia.get_rect(center=(x + szerokosc // 2, pozycja_y + wysokosc // 2))
    ekran.blit(tekst_powierzchnia, tekst_rect)
    
    # Sprawdź kliknięcie
    kliknieto = False
    if hover and pygame.mouse.get_pressed()[0]:
        kliknieto = True
        if glosnosc_efekty is not None:
            SOUND_BUTTON.set_volume(glosnosc_efekty)
        SOUND_BUTTON.play()
    return kliknieto

# Reszta kodu pozostaje bez zmian...

# Efekt przejścia
def efekt_przejscia(ekran, funkcja_docelowa, typ="fade"):
    szerokosc, wysokosc = ekran.get_size()
    
    if typ == "fade":
        # Zapisz aktualny ekran
        kopia_ekranu = ekran.copy()
        
        # Animacja fade out (przyspieszona)
        for alpha in range(0, 256, 24):  # Większy krok (było 8)
            ekran.blit(kopia_ekranu, (0, 0))
            powierzchnia = pygame.Surface((szerokosc, wysokosc), pygame.SRCALPHA)
            powierzchnia.fill((0, 0, 0, alpha))
            ekran.blit(powierzchnia, (0, 0))
            pygame.display.flip()
            pygame.time.delay(5)  # Zmniejszone opóźnienie (było 10)
        
        # Wywołaj funkcję docelową
        rezultat = funkcja_docelowa(ekran)
        
        # Zapisz nowy ekran
        nowy_ekran = ekran.copy()
        
        # Animacja fade in (przyspieszona)
        for alpha in range(255, -1, -24):  # Większy krok (było -8)
            ekran.blit(nowy_ekran, (0, 0))
            powierzchnia = pygame.Surface((szerokosc, wysokosc), pygame.SRCALPHA)
            powierzchnia.fill((0, 0, 0, alpha))
            ekran.blit(powierzchnia, (0, 0))
            pygame.display.flip()
            pygame.time.delay(5)  # Zmniejszone opóźnienie (było 10)
    
    elif typ == "slide":
        # Zapisz aktualny ekran
        kopia_ekranu = ekran.copy()
        
        # Animacja slide out (przyspieszona)
        for i in range(0, szerokosc, 80):  # Większy krok (było 40)
            ekran.fill(NIEBIESKI_TLO)
            ekran.blit(kopia_ekranu, (-i, 0))
            pygame.display.flip()
            pygame.time.delay(2)  # Zmniejszone opóźnienie (było 5)
        
        # Wywołaj funkcję docelową
        rezultat = funkcja_docelowa(ekran)
        
        # Zapisz nowy ekran
        nowy_ekran = ekran.copy()
        
        # Animacja slide in (przyspieszona)
        for i in range(szerokosc, 0, -80):  # Większy krok (było -40)
            ekran.fill(NIEBIESKI_TLO)
            ekran.blit(nowy_ekran, (i, 0))
            pygame.display.flip()
            pygame.time.delay(2)  # Zmniejszone opóźnienie (było 5)
        
        ekran.blit(nowy_ekran, (0, 0))
    
    return rezultat


# Funkcja do animacji świecącego tytułu
def animuj_tytul(ekran, x, y):
    czcionka_tytul = pygame.font.SysFont('Arial', 100, bold=True)
    
    czas = pygame.time.get_ticks() / 1000
    
    # Animowany kolor dla "POLI" (pulsujący)
    czerwony_pulsujacy = (
        min(255, max(200, int(220 + 35 * math.sin(czas * 3)))),
        min(100, max(20, int(60 + 40 * math.sin(czas * 3.5)))),
        min(100, max(20, int(60 + 40 * math.cos(czas * 4))))
    )
    
    # Renderowanie tekstu
    tekst_mono = czcionka_tytul.render("Mono", True, BIALY)
    tekst_poli = czcionka_tytul.render("POLI", True, czerwony_pulsujacy)
    
    # Efekt świecenia dla "POLI"
    for i in range(6, 0, -2):
        alpha = 50 - i * 5
        if alpha > 0:
            powierzchnia = pygame.Surface((tekst_poli.get_width() + i*2, tekst_poli.get_height() + i*2), pygame.SRCALPHA)
            powierzchnia.fill((0, 0, 0, 0))
            pygame.gfxdraw.filled_ellipse(powierzchnia, powierzchnia.get_width()//2, powierzchnia.get_height()//2, 
                                       powierzchnia.get_width()//2, powierzchnia.get_height()//2, 
                                       (czerwony_pulsujacy[0], czerwony_pulsujacy[1], czerwony_pulsujacy[2], alpha))
            ekran.blit(powierzchnia, (x - 20 + i + tekst_mono.get_width() - i, y - i))
    
    # Blask pod "Mono"
    for i in range(6, 0, -2):
        alpha = 20 - i * 2
        if alpha > 0:
            powierzchnia = pygame.Surface((tekst_mono.get_width() + i*2, tekst_mono.get_height() + i*2), pygame.SRCALPHA)
            powierzchnia.fill((0, 0, 0, 0))
            pygame.gfxdraw.filled_ellipse(powierzchnia, powierzchnia.get_width()//2, powierzchnia.get_height()//2, 
                                       powierzchnia.get_width()//2, powierzchnia.get_height()//2, 
                                       (100, 150, 255, alpha))
            ekran.blit(powierzchnia, (x - i, y - i))
    
    # Rysowanie tekstu
    ekran.blit(tekst_mono, (x, y))
    ekran.blit(tekst_poli, (x + tekst_mono.get_width() - 20, y))  # Lekkie nachodzenie
    
    # Dodaj delikatny efekt blasku na literach (zmniejszony)
    blask_powierzchnia = pygame.Surface((SZEROKOSC, WYSOKOSC), pygame.SRCALPHA)
    for i in range(5):  # Zmniejszono z 10 na 5
        offset_x = int(math.sin(czas * 4 + i * 0.2) * 10)
        offset_y = int(math.cos(czas * 3 + i * 0.3) * 5)
        pygame.gfxdraw.line(blask_powierzchnia, 
                         x + tekst_mono.get_width() // 2 + offset_x, 
                         y - 20 + offset_y, 
                         x + tekst_mono.get_width() + tekst_poli.get_width() // 2 + offset_x, 
                         y + tekst_poli.get_height() + 20 + offset_y, 
                         (255, 255, 255, 3))
    
    ekran.blit(blask_powierzchnia, (0, 0))

# Funkcja do animowanego pionka
def animuj_pionek(ekran, x, y, rozmiar):
    czas = pygame.time.get_ticks() / 1000
    
    # Animacja skakania
    offset_y = int(math.sin(czas * 3) * 10)
    skala = 1.0 + 0.05 * math.sin(czas * 4)
    
    # Dodaj cień pod pionkiem
    pygame.gfxdraw.filled_ellipse(ekran, x, y + rozmiar//2 - offset_y//2, 
                               int(rozmiar * 0.6), int(rozmiar * 0.2), (0, 0, 0, 100))
    
    # Rysuj pionek z animacją
    narysuj_pionek(ekran, x, y - offset_y, int(rozmiar * skala))
    
    # Dodaj błysk na pionku
    kat_blasku = czas * 2 % (2 * math.pi)
    x_blask = x + int(math.cos(kat_blasku) * rozmiar * 0.3)
    y_blask = y - offset_y + int(math.sin(kat_blasku) * rozmiar * 0.3)
    
    pygame.gfxdraw.filled_circle(ekran, x_blask, y_blask, 5, (255, 255, 255, 150))
def make_card_surface(w, h, border_color, blur_scale=0.1,
                      border_thickness=4, fill_alpha=255):
    """
    Tworzy pojedynczą kartę:
    - biały podkład z alpha=fill_alpha,
    - grubsze obramowanie o szer. border_thickness,
    - rozmycie przez skalowanie w dół i do góry,
    - znak zapytania na środku.
    """
    # 1) Rysujemy podkład
    surf = pygame.Surface((w, h), flags=pygame.SRCALPHA)
    pygame.gfxdraw.box(surf, (0, 0, w, h), (255, 255, 255, fill_alpha))
    # 2) Grube obramowanie
    for i in range(border_thickness):
        rect = (i, i, w - 1 - 2*i, h - 1 - 2*i)
        pygame.gfxdraw.rectangle(surf, rect, border_color + (255,))

    # 3) Rozmycie (scale down/up)
    sw = max(1, int(w * blur_scale))
    sh = max(1, int(h * blur_scale))
    tiny = pygame.transform.smoothscale(surf, (sw, sh))
    blurred = pygame.transform.smoothscale(tiny, (w, h))

    # 4) Znak zapytania
    font = pygame.font.SysFont(None, int(min(w, h) * 0.6))
    txt = font.render("?", True, border_color)
    tw, th = txt.get_size()
    blurred.blit(txt, ((w - tw)//2, (h - th)//2))

    return blurred


class Card:
    def __init__(self, pos, size, border_color, phase):
        self.cx, self.cy = pos
        self.w, self.h = size
        self.phase = phase
        # bielszy fill_alpha=255, grubsza ramka=4px:
        self.base = make_card_surface(self.w, self.h,
                                      border_color,
                                      blur_scale=0.08,
                                      border_thickness=4,
                                      fill_alpha=240)

    def draw(self, screen, t):
        # wolniejszy obrót: 0.2 rad/s
        angle = t * 0.5 + self.phase
        ws = abs(math.cos(angle))
        new_w = max(1, int(self.w * ws))
        scaled = pygame.transform.smoothscale(self.base, (new_w, self.h))
        tilt = math.sin(angle) * 30
        final = pygame.transform.rotate(scaled, tilt)
        rect = final.get_rect(center=(self.cx, self.cy))
        screen.blit(final, rect)
# Główna pętla gry z efektami
def main():
    zegar = pygame.time.Clock()
    ostatni_czas = time.time()
    animowane_tlo = AnimowaneTlo(SZEROKOSC, WYSOKOSC)
    czasteczki = []
    glosnosc_efekty = 0.7
    
    # Animacja wstępna - przyspieszona (max 2-3 sekundy)
    alfa_ekranu = 0
    
    # Utwórz animowane kostki 3D
    kostka1 = KostkaTrojwymiarowa(250, 700, 100)
    kostka2 = KostkaTrojwymiarowa(750, 700, 100)
    
    while alfa_ekranu < 255:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Wypełnij ekran kolorem tła z gradientem
        ekran.fill((0, 0, 0))
        
        # Narysuj animowane tło
        animowane_tlo.aktualizuj()
        animowane_tlo.rysuj(ekran)
        
        # Rysuj półprzezroczysty gradient
        for i in range(0, WYSOKOSC, 2):  # Przyspieszenie przez rysowanie co drugiej linii
            alpha = 150 - i * 0.15
            if alpha > 0:
                pygame.gfxdraw.hline(ekran, 0, SZEROKOSC, i, 
                                  (0, int(30 + i * 0.05), int(80 + i * 0.15), int(alpha)))
        
        # Narysuj logo z efektem pojawiania
        powierzchnia_logo = pygame.Surface((SZEROKOSC, WYSOKOSC), pygame.SRCALPHA)
        powierzchnia_logo.fill((0, 0, 0, 0))
        
        animuj_tytul(powierzchnia_logo, SZEROKOSC // 2 - 220, 100)
        
        # Zastosuj alfa dla całej powierzchni (uproszczone dla szybkości)
        powierzchnia_alpha = pygame.Surface((SZEROKOSC, WYSOKOSC), pygame.SRCALPHA)
        powierzchnia_alpha.fill((255, 255, 255, alfa_ekranu))
        powierzchnia_logo.blit(powierzchnia_alpha, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        ekran.blit(powierzchnia_logo, (0, 0))
        
        # Zwiększ alfa (szybciej)
        alfa_ekranu += 15  # Zmieniono z 5 na 15
        
        pygame.display.flip()
        zegar.tick(60)
    
    # Główna pętla gry
    animacja_przycisku_graj = 0
    animacja_przycisku_ustawienia = 0
    
    # Start background music
    pygame.mixer.music.play(-1)  # Loop background music
    
    
    card_w = 100
    card_h = int(card_w * 1.4)
    positions = [(90, 90), (1100, 80), (80, 900), (1100, 900)]
    colors = [
    (200,   0,   0),
    (  0, 200,   0),
    (200, 150,   0),  # cieplejsze, bardziej widoczne
    (  0,   0, 200),
    ]
    phases = [0, math.pi/2, math.pi, 3*math.pi/2]

    cards = [Card(pos, (card_w, card_h), col, ph)
             for pos, col, ph in zip(positions, colors, phases)]
    
    while True:
        obecny_czas = time.time()
        delta_czas = obecny_czas - ostatni_czas
        ostatni_czas = obecny_czas
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Wypełnij ekran kolorem tła z gradientem
        ekran.fill((0, 0, 20))
        
        # Narysuj animowane tło
        animowane_tlo.aktualizuj()
        animowane_tlo.rysuj(ekran)
        
        # Rysuj półprzezroczysty gradient (zoptymalizowany)
        for i in range(0, WYSOKOSC, 2):  # Rysuj co drugą linię dla szybkości
            alpha = 150 - i * 0.15
            if alpha > 0:
                pygame.gfxdraw.hline(ekran, 0, SZEROKOSC, i, 
                                  (0, int(30 + i * 0.05), int(80 + i * 0.15), int(alpha)))
        
        # Aktualizuj i rysuj cząsteczki
        for c in czasteczki[:]:
            c.aktualizuj()
            if c.czas_zycia <= 0:
                czasteczki.remove(c)
            else:
                c.rysuj(ekran)
        
        # Rysuj animowane pionki
        
        t = pygame.time.get_ticks() / 1000.0
        for c in cards:
            c.draw(ekran, t)
   
        animuj_tytul(ekran, SZEROKOSC // 2 - 220, 100)
        
        # Zarządzanie animacją przycisków
        if animacja_przycisku_graj > 0:
            animacja_przycisku_graj -= 0.05
            if animacja_przycisku_graj < 0:
                animacja_przycisku_graj = 0
        
        if animacja_przycisku_ustawienia > 0:
            animacja_przycisku_ustawienia -= 0.05
            if animacja_przycisku_ustawienia < 0:
                animacja_przycisku_ustawienia = 0
        
        # Rysuj przyciski
        if narysuj_przycisk_3d(ekran, "GRAJ", SZEROKOSC // 2 - 150, 250, 300, 70, 
                            CZERWONY_CIEMNY, BIALY, animacja_przycisku_graj, glosnosc_efekty):
            animacja_przycisku_graj = 1.0
            for _ in range(30):
                czasteczki.append(Czasteczka(SZEROKOSC // 2, 250 + 35, CZERWONY_CIEMNY))
            print("Kliknięto przycisk GRAJ!")
            efekt_przejscia(ekran, lambda e: ekran_gry(e, 1, glosnosc_efekty), "slide")
        
        if narysuj_przycisk_3d(ekran, "Ustawienia", SZEROKOSC // 2 - 150, 350, 300, 70, 
                            CZERWONY_CIEMNY, BIALY, animacja_przycisku_ustawienia, glosnosc_efekty):
            animacja_przycisku_ustawienia = 1.0
            for _ in range(30):
                czasteczki.append(Czasteczka(SZEROKOSC // 2, 350 + 35, CZERWONY_CIEMNY))
            print("Kliknięto przycisk Ustawienia!")
            # Przechwyć głośność efektów z ustawień
            def ustawienia_wrapper(ekran):
                wynik = strona_ustawien(ekran)
                # Po powrocie z ustawień pobierz aktualną głośność efektów
                try:
                    return getattr(strona_ustawien, 'glosnosc_efekty', glosnosc_efekty)
                except Exception:
                    return glosnosc_efekty
            nowa_glosnosc_efekty = efekt_przejscia(ekran, ustawienia_wrapper, "fade")
            if nowa_glosnosc_efekty is not None:
                glosnosc_efekty = nowa_glosnosc_efekty
            main.glosnosc_efekty = glosnosc_efekty
        
        # Aktualizuj animowane kostki
        kostka1.aktualizuj(delta_czas)
        kostka2.aktualizuj(delta_czas)
        
        # Rysuj animowane kostki zamiast statycznych
        kostka1.rysuj(ekran)
        kostka2.rysuj(ekran)
        
        # Aktualizuj ekran
        pygame.display.flip()
        zegar.tick(60)

if __name__ == "__main__":
    main()