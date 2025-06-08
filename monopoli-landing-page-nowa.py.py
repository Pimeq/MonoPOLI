from kolory import *
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

        # 1) Definiujemy 8 wierzchołków kostki w lokalnym układzie
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

        # 2) Ściany - indeksy wierzchołków i odpowiadające im wartości oczek
        faces = [
            ( [0,1,2,3], 1 ),  # tył
            ( [4,5,6,7], 6 ),  # przód
            ( [0,4,7,3], 2 ),  # lewa
            ( [1,5,6,2], 5 ),  # prawa
            ( [0,1,5,4], 3 ),  # dół
            ( [3,2,6,7], 4 ),  # góra
        ]
        kolory_scian = [
                (220, 220, 220),  # tył
                (255, 255, 255),  # przód
                (200, 200, 200),  # lewa
                (240, 240, 240),  # prawa
                (180, 180, 180),  # dół
                (230, 230, 230),  # góra
            ]
        # 3) Obrót wszystkich wierzchołków i zapis w postaci (x3d,y3d,z3d,x2d,y2d)
        transformed = []
        for vx, vy, vz in local_verts:
            # obrót X
            ry = vy * math.cos(math.radians(self.obrot_x)) \
                 - vz * math.sin(math.radians(self.obrot_x))
            rz = vy * math.sin(math.radians(self.obrot_x)) \
                 + vz * math.cos(math.radians(self.obrot_x))
            rx = vx
            # obrót Y
            rz2 = rz * math.cos(math.radians(self.obrot_y)) \
                  - rx * math.sin(math.radians(self.obrot_y))
            rx2 = rz * math.sin(math.radians(self.obrot_y)) \
                  + rx * math.cos(math.radians(self.obrot_y))
            ry2 = ry
            # obrót Z
            rx3 = rx2 * math.cos(math.radians(self.obrot_z)) \
                  - ry2 * math.sin(math.radians(self.obrot_z))
            ry3 = rx2 * math.sin(math.radians(self.obrot_z)) \
                  + ry2 * math.cos(math.radians(self.obrot_z))
            rz3 = rz2

            # rzutowanie ortogonalne
            x2 = centrum_x + rx3
            y2 = centrum_y + ry3
            transformed.append((rx3, ry3, rz3, x2, y2))

        # 4) Sortujemy ściany po głębokości (średnie z >0 z wierzchołków)
        face_order = []
        for idx, (inds, val) in enumerate(faces):
            avg_z = sum(transformed[i][2] for i in inds) / 4.0
            face_order.append((idx, avg_z))
        face_order.sort(key=lambda x: x[1], reverse=True)

        # 5) Rysujemy ściany i pipsy
        for face_idx, _ in face_order:
            inds, val = faces[face_idx]

            # punkty 2D do polygonu
            poly2d = [(transformed[i][3], transformed[i][4]) for i in inds]
            pygame.draw.polygon(ekran, kolory_scian[face_idx], poly2d)
            pygame.draw.polygon(ekran, (0,0,0), poly2d, 2)

            # --- tutaj ustalamy ramkę ściany w 3D ---
            # weź trzy wierzchołki, zrób bazę u,v na 3D
            p0 = transformed[inds[0]][:3]
            p1 = transformed[inds[1]][:3]
            p3 = transformed[inds[3]][:3]
            # wektor u wzdłuż pierwszej krawędzi
            ux, uy, uz = (p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2])
            # wektor v wzdłuż trzeciej krawędzi
            vx, vy, vz = (p3[0]-p0[0], p3[1]-p0[1], p3[2]-p0[2])
            # normalizacja u i v
            ul = math.sqrt(ux*ux + uy*uy + uz*uz)
            vl = math.sqrt(vx*vx + vy*vy + vz*vz)
            ux, uy, uz = ux/ul, uy/ul, uz/ul
            vx, vy, vz = vx/vl, vy/vl, vz/vl

            # środek ściany w 3D
            cx3 = sum(transformed[i][0] for i in inds) / 4.0
            cy3 = sum(transformed[i][1] for i in inds) / 4.0
            cz3 = sum(transformed[i][2] for i in inds) / 4.0

            # promień rozstawu pipsów w lokalnych współrzędnych [0..1]
            offset = polowa * 0.7

            # pozycje pipsów w lokalnych współrzędnych u,v
            pip_patterns = {
                1: [(0,0)],
                2: [(-.5,-.5),(.5,.5)],
                3: [(-.5,-.5),(0,0),(.5,.5)],
                4: [(-.5,-.5),(-.5,.5),(.5,-.5),(.5,.5)],
                5: [(-.5,-.5),(-.5,.5),(0,0),(.5,-.5),(.5,.5)],
                6: [(-.5,-.5),(-.5,0),(-.5,.5),(.5,-.5),(.5,0),(.5,.5)],
            }

            # rysujemy każdy pips jako punkt 3D → projektujemy
            for pu, pv in pip_patterns[val]:
                # punkt 3D
                px3 = cx3 + ux * (pu * offset) + vx * (pv * offset)
                py3 = cy3 + uy * (pu * offset) + vy * (pv * offset)
                # pomijamy z3 (rzut orto)
                sx = int(centrum_x + px3)
                sy = int(centrum_y + py3)
                # promień kropki w pikselach
                r = max(3, int(offset * 0.15))
                pygame.gfxdraw.filled_circle(ekran, sx, sy, r, (0,0,0))
    
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
def narysuj_przycisk_3d(ekran, tekst, x, y, szerokosc, wysokosc, kolor, kolor_tekstu, animacja=0):
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

# Główna pętla gry z efektami
def main():
    zegar = pygame.time.Clock()
    ostatni_czas = time.time()
    animowane_tlo = AnimowaneTlo(SZEROKOSC, WYSOKOSC)
    czasteczki = []
    
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
        animuj_pionek(ekran, 80, 80, 100)
        animuj_pionek(ekran, 1100, 80, 100)
        animuj_pionek(ekran, 80, 900, 100)
        animuj_pionek(ekran, 1100, 900, 100)
        
        # Rysuj tytuł z animacją
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
                            CZERWONY_CIEMNY, BIALY, animacja_przycisku_graj):
            animacja_przycisku_graj = 1.0
            
            # Dodaj efekt cząsteczek przy kliknięciu
            for _ in range(30):
                czasteczki.append(Czasteczka(SZEROKOSC // 2, 250 + 35, CZERWONY_CIEMNY))
            
            # Wywołanie ekranu gry z efektem przejścia
            print("Kliknięto przycisk GRAJ!")
            efekt_przejscia(ekran, ekran_gry, "slide")
        
        if narysuj_przycisk_3d(ekran, "Ustawienia", SZEROKOSC // 2 - 150, 350, 300, 70, 
                            CZERWONY_CIEMNY, BIALY, animacja_przycisku_ustawienia):
            animacja_przycisku_ustawienia = 1.0
            
            # Dodaj efekt cząsteczek przy kliknięciu
            for _ in range(30):
                czasteczki.append(Czasteczka(SZEROKOSC // 2, 350 + 35, CZERWONY_CIEMNY))
            
            # Wywołanie strony ustawień z efektem przejścia
            print("Kliknięto przycisk Ustawienia!")
            efekt_przejscia(ekran, strona_ustawien, "fade")
        
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