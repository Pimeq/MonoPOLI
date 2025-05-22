import pygame
import sys
import math

# Inicjalizacja Pygame
pygame.init()

# Kolory
NIEBIESKI_TLO = (39, 72, 98)
ZIELONY_TLO = (123, 175, 157)
CIEMNY_FIOLET = (30, 20, 50)
CZERWONY = (230, 30, 30)
BIALY = (255, 255, 255)
SZARY = (220, 220, 220)
SZARY_JASNY = (235, 235, 235)

# Rozmiar okna
SZEROKOSC, WYSOKOSC = 800, 600

class KoloKolorow:
    def __init__(self, x, y, promien):
        self.x = x
        self.y = y
        self.promien = promien
        self.powierzchnia = pygame.Surface((promien*2, promien*2), pygame.SRCALPHA)
        self._generuj_kolo_kolorow()
        
    def _generuj_kolo_kolorow(self):
        """Generuje koło kolorów jako tęczę"""
        for x in range(self.promien*2):
            for y in range(self.promien*2):
                # Oblicz odległość od środka
                odl_x = x - self.promien
                odl_y = y - self.promien
                odleglosc = math.sqrt(odl_x**2 + odl_y**2)
                
                if odleglosc <= self.promien:
                    # Oblicz kąt w stosunku do środka (w radianach)
                    kat = math.atan2(odl_y, odl_x)
                    
                    # Przekształć kąt na kolor HSV i potem na RGB
                    h = (kat / (2 * math.pi) + 0.5) % 1.0
                    s = min(odleglosc / self.promien, 1.0)
                    v = 1.0
                    
                    # Konwersja HSV do RGB
                    h_i = int(h * 6)
                    f = h * 6 - h_i
                    p = v * (1 - s)
                    q = v * (1 - f * s)
                    t = v * (1 - (1 - f) * s)
                    
                    if h_i == 0:
                        r, g, b = v, t, p
                    elif h_i == 1:
                        r, g, b = q, v, p
                    elif h_i == 2:
                        r, g, b = p, v, t
                    elif h_i == 3:
                        r, g, b = p, q, v
                    elif h_i == 4:
                        r, g, b = t, p, v
                    else:
                        r, g, b = v, p, q
                    
                    # Ustaw kolor piksela
                    self.powierzchnia.set_at((x, y), (int(r*255), int(g*255), int(b*255)))
    
    def rysuj(self, ekran):
        """Rysuje koło kolorów na ekranie"""
        ekran.blit(self.powierzchnia, (self.x - self.promien, self.y - self.promien))

# Funkcja do rysowania zaokrąglonego prostokąta
def narysuj_zaokraglony_prostokat(powierzchnia, kolor, prostokat, promien):
    """Rysuje prostokąt z zaokrąglonymi rogami"""
    x, y, szer, wys = prostokat
    promien = min(promien, szer // 2, wys // 2)
    
    # Narysuj prostokąt
    pygame.draw.rect(powierzchnia, kolor, prostokat, border_radius=promien)

# Funkcja do tworzenia przycisku
def utworz_przycisk(tekst, x, y, szerokosc, wysokosc, kolor, kolor_tekstu, rozmiar_czcionki=36):
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

# Funkcja do rysowania pionka szachowego
def narysuj_pionek(x, y, szerokosc, wysokosc):
    """Rysuje pionek szachowy"""
    # Kolor pionka
    kolor_pionka = (40, 60, 100)
    
    # Rysuj podstawę pionka
    pygame.draw.ellipse(ekran, kolor_pionka, (x + szerokosc/4, y + wysokosc*0.75, szerokosc/2, wysokosc/8))
    
    # Rysuj trzon pionka
    pygame.draw.rect(ekran, kolor_pionka, (x + szerokosc*0.4, y + wysokosc*0.5, szerokosc*0.2, wysokosc*0.3))
    
    # Rysuj główkę pionka
    pygame.draw.circle(ekran, kolor_pionka, (x + szerokosc/2, y + wysokosc*0.4), szerokosc*0.15)
    
    # Dodaj efekt 3D
    pygame.draw.ellipse(ekran, (60, 80, 120), (x + szerokosc/4 + 2, y + wysokosc*0.75 + 2, szerokosc/2 - 4, wysokosc/8 - 2))

# Funkcja do rysowania suwaka głośności
def narysuj_suwak_glosnosci(x, y, szerokosc, wysokosc, wartosc=0.5):
    """Rysuje suwak głośności z wartością od 0 do 1"""
    # Rysuj tło suwaka
    pygame.draw.rect(ekran, NIEBIESKI_TLO, (x, y, szerokosc, wysokosc), border_radius=5)
    pygame.draw.rect(ekran, (0, 0, 0, 50), (x+2, y+2, szerokosc, wysokosc), border_radius=5)
    
    # Rysuj ikonę głośnika
    ikona_glosnika_x = x + 30
    ikona_glosnika_y = y + wysokosc/2
    
    # Główny kształt głośnika
    pygame.draw.polygon(ekran, BIALY, [
        (ikona_glosnika_x, ikona_glosnika_y - 10),
        (ikona_glosnika_x + 10, ikona_glosnika_y - 10),
        (ikona_glosnika_x + 20, ikona_glosnika_y - 15),
        (ikona_glosnika_x + 20, ikona_glosnika_y + 15),
        (ikona_glosnika_x + 10, ikona_glosnika_y + 10),
        (ikona_glosnika_x, ikona_glosnika_y + 10)
    ])
    
    # Fale dźwiękowe
    pygame.draw.arc(ekran, (255, 80, 80), 
                    (ikona_glosnika_x + 25, ikona_glosnika_y - 15, 10, 30), 
                    math.pi * 1.5, math.pi * 0.5, 2)
    pygame.draw.arc(ekran, (255, 80, 80), 
                    (ikona_glosnika_x + 30, ikona_glosnika_y - 20, 15, 40), 
                    math.pi * 1.5, math.pi * 0.5, 2)
    
    # Rysuj pasek wypełnienia
    pasek_szerokosc = int((szerokosc - 80) * wartosc)
    pygame.draw.rect(ekran, (100, 230, 100), (x + 70, y + 5, pasek_szerokosc, wysokosc - 10), border_radius=5)
    
    # Rysuj uchwyt suwaka
    uchwyt_x = x + 70 + pasek_szerokosc
    pygame.draw.circle(ekran, BIALY, (uchwyt_x, y + wysokosc/2), 12)
    pygame.draw.circle(ekran, (220, 220, 220), (uchwyt_x, y + wysokosc/2), 10)
    
    # Obsługa kliknięcia i przeciągania
    myszka = pygame.mouse.get_pos()
    klikniecie = pygame.mouse.get_pressed()[0]
    
    if klikniecie and y <= myszka[1] <= y + wysokosc and x + 70 <= myszka[0] <= x + szerokosc - 10:
        nowa_wartosc = (myszka[0] - (x + 70)) / (szerokosc - 80)
        return max(0, min(1, nowa_wartosc))
    
    return wartosc

# Funkcja do rysowania karty gracza
def narysuj_karte_gracza(x, y, szerokosc, wysokosc, nazwa="Gracz", nr_gracza=1):
    """Rysuje kartę gracza z kolorem, nazwą i pionkiem"""
    # Tło karty
    pygame.draw.rect(ekran, SZARY_JASNY, (x, y, szerokosc, wysokosc), border_radius=5)
    
    # Pole koloru
    kolo_kolorow = KoloKolorow(x + szerokosc//2, y + wysokosc//6, 20)
    kolo_kolorow.rysuj(ekran)
    
    # Pole nazwy
    pygame.draw.rect(ekran, CIEMNY_FIOLET, (x, y + wysokosc//3, szerokosc, wysokosc//6), border_radius=2)
    czcionka = pygame.font.SysFont('Arial', 20)
    tekst_nazwa = czcionka.render(nazwa, True, BIALY)
    tekst_nazwa_rect = tekst_nazwa.get_rect(center=(x + szerokosc//2, y + wysokosc//3 + wysokosc//12))
    ekran.blit(tekst_nazwa, tekst_nazwa_rect)
    
    # Pionek
    narysuj_pionek(x + szerokosc//4, y + wysokosc//2 + 5, szerokosc//2, wysokosc//3)
    
    # Numer gracza
    czcionka_nr = pygame.font.SysFont('Arial', 18)
    tekst_nr = czcionka_nr.render(f"Gracz {nr_gracza}", True, BIALY)
    tekst_nr_rect = tekst_nr.get_rect(center=(x + szerokosc//2, y + wysokosc + 20))
    ekran.blit(tekst_nr, tekst_nr_rect)

# Funkcja główna dla strony ustawień
def strona_ustawien(ekran_zewnetrzny=None):
    """
    Wyświetla ekran ustawień gry
    Parametr ekran_zewnetrzny: Istniejący ekran Pygame do użycia (z landing page)
    """
    global ekran
    
    # Używaj przekazanego ekranu lub utwórz własny jeśli nie został przekazany
    if ekran_zewnetrzny:
        ekran = ekran_zewnetrzny
    elif 'ekran' not in globals():
        ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
        pygame.display.set_caption("MonoPOLI - Ustawienia")
    
    # Wartość suwaka głośności
    glosnosc = 0.7
    
    # Główna pętla
    zegar = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Wypełnij tło
        ekran.fill(ZIELONY_TLO)
        
        # Rysuj nagłówki kolumn
        czcionka_naglowek = pygame.font.SysFont('Arial', 24, bold=True)
        
        pygame.draw.rect(ekran, CIEMNY_FIOLET, (80, 90, 140, 40))
        tekst_kolor = czcionka_naglowek.render("Kolor", True, BIALY)
        ekran.blit(tekst_kolor, (120, 95))
        
        pygame.draw.rect(ekran, CIEMNY_FIOLET, (80, 140, 140, 40))
        tekst_nazwa = czcionka_naglowek.render("Nazwa", True, BIALY)
        ekran.blit(tekst_nazwa, (120, 145))
        
        pygame.draw.rect(ekran, CIEMNY_FIOLET, (80, 190, 140, 40))
        tekst_pionek = czcionka_naglowek.render("Pionek", True, BIALY)
        ekran.blit(tekst_pionek, (120, 195))
        
        # Rysuj karty graczy
        narysuj_karte_gracza(230, 70, 120, 170, "Jan", 1)
        narysuj_karte_gracza(370, 70, 120, 170, "Sołtys", 2)
        narysuj_karte_gracza(510, 70, 120, 170, "Doktor", 3)
        narysuj_karte_gracza(650, 70, 120, 170, "Analizator", 4)
        
        # Rysuj suwak głośności
        nowa_glosnosc = narysuj_suwak_glosnosci(230, 350, 350, 50, glosnosc)
        if nowa_glosnosc != glosnosc:
            glosnosc = nowa_glosnosc
            print(f"Ustawiono głośność: {glosnosc*100:.0f}%")
        
        # Rysuj przycisk powrotu
        if utworz_przycisk("Powrót do menu", SZEROKOSC // 2 - 150, 450, 300, 70, NIEBIESKI_TLO, BIALY):
            running = False
            return True  # Informacja o powrocie do menu
        
        # Aktualizuj ekran
        pygame.display.flip()
        zegar.tick(60)
    
    return False  # Normalnie nie powinno się tu dotrzeć
