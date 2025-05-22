import pygame
import sys
import math
import random
from pygame import gfxdraw
import time
from kolory import *
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
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
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
        
        # Wolne stałe prędkości obrotu (bez docelowych wartości)
        # Użycie różnych wartości dla każdej osi daje ciekawszy efekt
        self.predkosc_x = 35  # stopni na sekundę
        self.predkosc_y = 25   # stopni na sekundę
        self.predkosc_z = 10
    
    def aktualizuj(self, delta_czas):
        # Stały, ciągły obrót bez przeskoków
        self.obrot_x = (self.obrot_x + self.predkosc_x * delta_czas) % 360
        self.obrot_y = (self.obrot_y + self.predkosc_y * delta_czas) % 360
        self.obrot_z = (self.obrot_z + self.predkosc_z * delta_czas) % 360
        
    def rysuj(self, ekran):
        # Zawsze rysuj kostkę 3D w animacji
        self._rysuj_3d(ekran)
    
    def _rysuj_3d(self, ekran):
        # Przygotowanie parametrów rysowania idealnie kwadratowej kostki
        centrum_x = self.x
        centrum_y = self.y
        polowa_rozmiaru = self.rozmiar // 2
        
        # Definiuj wierzchołki kostki 3D - idealny sześcian
        wierzcholki = [
            [-polowa_rozmiaru, -polowa_rozmiaru, -polowa_rozmiaru],  # 0: tylny dolny lewy
            [polowa_rozmiaru, -polowa_rozmiaru, -polowa_rozmiaru],   # 1: tylny dolny prawy
            [polowa_rozmiaru, polowa_rozmiaru, -polowa_rozmiaru],    # 2: tylny górny prawy
            [-polowa_rozmiaru, polowa_rozmiaru, -polowa_rozmiaru],   # 3: tylny górny lewy
            [-polowa_rozmiaru, -polowa_rozmiaru, polowa_rozmiaru],   # 4: przedni dolny lewy
            [polowa_rozmiaru, -polowa_rozmiaru, polowa_rozmiaru],    # 5: przedni dolny prawy
            [polowa_rozmiaru, polowa_rozmiaru, polowa_rozmiaru],     # 6: przedni górny prawy
            [-polowa_rozmiaru, polowa_rozmiaru, polowa_rozmiaru]     # 7: przedni górny lewy
        ]
        
        # Definiuj ściany kostki (indeksy wierzchołków)
        sciany = [
            [0, 1, 2, 3],  # Tył
            [4, 5, 6, 7],  # Przód
            [0, 4, 7, 3],  # Lewa
            [1, 5, 6, 2],  # Prawa
            [0, 1, 5, 4],  # Dół
            [3, 2, 6, 7]   # Góra
        ]
        
        # Wartości na ścianach - ZMIANA: wszystkie ściany mają tę samą wartość
        stala_wartosc = 6  # Możesz ustawić dowolną wartość od 1 do 6
        wartosci_scian = [stala_wartosc, stala_wartosc, stala_wartosc, stala_wartosc, stala_wartosc, stala_wartosc]
        
        # Kolory ścian - bardziej kontrastowe i wyraziste
        kolory_scian = [
            (230, 50, 50),     # Czerwony
            (180, 40, 40),    # Ciemno czerwony
            (230, 50, 50),  # Jasny czerwony
            (230, 50, 50),     # Ciemny czerwony
            (180, 40, 40),   # Bardzo jasny czerwony
            (230, 50, 50)      # Bardzo ciemny czerwony
        ]
        
        # Obrót wierzchołków
        obrocone_wierzcholki = []
        for v in wierzcholki:
            # Obroty w 3D
            # Obrót X
            x = v[0]
            y = v[1] * math.cos(math.radians(self.obrot_x)) - v[2] * math.sin(math.radians(self.obrot_x))
            z = v[1] * math.sin(math.radians(self.obrot_x)) + v[2] * math.cos(math.radians(self.obrot_x))
            
            # Obrót Y
            x2 = x * math.cos(math.radians(self.obrot_y)) + z * math.sin(math.radians(self.obrot_y))
            y2 = y
            z2 = -x * math.sin(math.radians(self.obrot_y)) + z * math.cos(math.radians(self.obrot_y))
            
            # Obrót Z
            x3 = x2 * math.cos(math.radians(self.obrot_z)) - y2 * math.sin(math.radians(self.obrot_z))
            y3 = x2 * math.sin(math.radians(self.obrot_z)) + y2 * math.cos(math.radians(self.obrot_z))
            z3 = z2
            
            # ZMIANA: Usunięcie efektu perspektywy dla idealnie kwadratowego wyglądu
            # Teraz używamy ortogonalnej projekcji zamiast perspektywicznej
            x_proj = x3
            y_proj = y3
            
            obrocone_wierzcholki.append([centrum_x + x_proj, centrum_y + y_proj, z3])
        
        # Sortuj ściany według głębokości (aby najpierw rysować te z tyłu)
        sortowane_sciany = []
        for i, s in enumerate(sciany):
            # Oblicz średnią wartość Z dla ściany
            srednia_z = sum([obrocone_wierzcholki[j][2] for j in s]) / 4
            sortowane_sciany.append((i, srednia_z))
        
        sortowane_sciany.sort(key=lambda x: x[1], reverse=True)
        
        # Rysuj ściany
        for i, _ in sortowane_sciany:
            punkty = [(obrocone_wierzcholki[j][0], obrocone_wierzcholki[j][1]) for j in sciany[i]]
            
            # Rysuj ścianę jako wielokąt z większym obramowaniem dla lepszej widoczności krawędzi
            pygame.draw.polygon(ekran, kolory_scian[i], punkty)
            pygame.draw.polygon(ekran, (0, 0, 0), punkty, 3)  # Grubszy czarny obrys (3px)
            
            # Dodaj kropki dla numeru na ścianie
            wartosc = wartosci_scian[i]
            
            # Środek ściany
            sr_x = sum([p[0] for p in punkty]) / 4
            sr_y = sum([p[1] for p in punkty]) / 4
            
            # Oblicz rozmiar ściany dla odpowiedniego skalowania kropek
            max_x = max([p[0] for p in punkty])
            min_x = min([p[0] for p in punkty])
            max_y = max([p[1] for p in punkty])
            min_y = min([p[1] for p in punkty])
            
            # Oblicz odpowiedni promień kropek na podstawie rozmiaru ściany
            rozmiar_sciany = min(max_x - min_x, max_y - min_y)
            promien = rozmiar_sciany * 0.35  # Zwiększony promień dla lepszej widoczności
            
            # Dodaj kropki w zależności od wartości
            self._rysuj_kropki(ekran, sr_x, sr_y, wartosc, promien)
    
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
        
        rozmiar_kropki = promien * 0.2  # Większe kropki
        
        for px, py in kropki_pozycje[wartosc]:
            # ZMIANA: Rysuj białe kropki zamiast czarnych
            pygame.draw.circle(
                ekran,
                (255, 255, 255),  # Biały kolor
                (int(x + px * promien * 0.8), int(y + py * promien * 0.8)),  # Pozycja kropki
                int(rozmiar_kropki)  # Rozmiar kropki
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

# Funkcja do rysowania pięknych przycisków
def narysuj_przycisk_3d(ekran, tekst, x, y, szerokosc, wysokosc, kolor, kolor_tekstu, animacja=0):
    # Przygotowanie kolorów
    kolor_jasny = (min(kolor[0] + 50, 255), min(kolor[1] + 50, 255), min(kolor[2] + 50, 255))
    kolor_ciemny = (max(kolor[0] - 50, 0), max(kolor[1] - 50, 0), max(kolor[2] - 50, 0))
    
    # Zastosuj animację (dla efektu wciśnięcia przycisku)
    pozycja_y = y + animacja * 5
    
    # Narysuj cień
    pygame.draw.rect(ekran, (0, 0, 0, 50), (x + 5, pozycja_y + 5, szerokosc, wysokosc))
    
    # Narysuj prostokąt główny - używając prostego pygame.draw.rect zamiast narysuj_zaokraglony_prostokat
    pygame.draw.rect(ekran, kolor, (x, pozycja_y, szerokosc, wysokosc))
    
    # Narysuj gradient na górze (efekt światła)
    for i in range(20):
        alpha = 120 - i * 6
        if alpha > 0:
            pygame.draw.rect(ekran, (255, 255, 255, alpha), (x, pozycja_y, szerokosc, i))
    
    # Dodaj błyszczący efekt na przycisku
    if animacja > 0:
        for i in range(int(wysokosc * 0.7)):
            alpha = int(20 - i * 0.3)
            if alpha > 0:
                pygame.draw.rect(ekran, (255, 255, 255, alpha), 
                              (x + 10, pozycja_y + i + int(wysokosc * 0.3), szerokosc - 20, 1))
    
    # Dodaj tekst
    czcionka = pygame.font.SysFont('Arial', 30, bold=True)
    tekst_powierzchnia = czcionka.render(tekst, True, kolor_tekstu)
    tekst_rect = tekst_powierzchnia.get_rect(center=(x + szerokosc // 2, pozycja_y + wysokosc // 2))
    ekran.blit(tekst_powierzchnia, tekst_rect)
    
    # Sprawdź kliknięcie
    myszka_x, myszka_y = pygame.mouse.get_pos()
    kliknieto = False
    
    if (x <= myszka_x <= x + szerokosc and 
        pozycja_y <= myszka_y <= pozycja_y + wysokosc):
        # Dodaj delikatną poświatę przy najechaniu
        for i in range(10):
            alpha = 20 - i * 2
            if alpha > 0:
                pygame.draw.rect(ekran, (255, 255, 255, alpha), 
                              (x - i, pozycja_y - i, szerokosc + i*2, wysokosc + i*2))
        
        if pygame.mouse.get_pressed()[0]:
            kliknieto = True
            
    return kliknieto

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
        
        # Kostki obracają się cały czas, nie ma potrzeby rzucać ich ponownie
        
        # Aktualizuj ekran
        pygame.display.flip()
        zegar.tick(60)
if __name__ == "__main__":
    main()