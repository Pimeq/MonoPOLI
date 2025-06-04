import pygame
import sys
from kolory import *
from pola import *
from logika import *
from interfejs import *
from plansza_render import narysuj_plansze

# Inicjalizacja Pygame
pygame.init()

# Rozmiar okna
SZEROKOSC, WYSOKOSC = 1200, 1000

# Funkcja główna dla ekranu gry
def ekran_gry(ekran_zewnetrzny=None):
    """Główna funkcja obsługująca rozgrywkę"""
    global gracze, aktualny_gracz, ostatni_rzut, tura_wykonana
      # Używaj przekazanego ekranu lub utwórz własny jeśli nie został przekazany
    if ekran_zewnetrzny:
        ekran = ekran_zewnetrzny
    else:
        ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
        pygame.display.set_caption("MonoPOLI - Politechnika Łódzka")
    
    # Główna pętla gry
    zegar = pygame.time.Clock()
    running = True
      # Zmienna do przechowywania informacji o kupowaniu pola
    kupowanie_pola = False
    
    # Zmienna do przechowywania informacji o karcie do wyświetlenia
    karta_do_wyswietlenia = None
    
    # Animacja ruchu gracza
    platnosc_do_wyswietlenia = None

    animacja_aktywna = False
    animacja_krok = 0
    animacja_docelowa_pozycja = 0
    animacja_start_pozycja = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Obsługa klawiszy
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not tura_wykonana and not animacja_aktywna:
                    # Rzut kostką po naciśnięciu spacji
                    ostatni_rzut = rzut_kostka()
                    suma_oczek = ostatni_rzut[0] + ostatni_rzut[1]
                    
                    # Zapisz pozycję początkową i docelową dla animacji
                    animacja_start_pozycja = gracze[aktualny_gracz]["pozycja"]
                    animacja_docelowa_pozycja = (animacja_start_pozycja + suma_oczek) % 40
                    
                    # Rozpocznij animację
                    animacja_aktywna = True
                    animacja_krok = 0
                
        # Wypełnij tło
        ekran.fill(CIEMNY_NIEBIESKI)
        
        # Animacja ruchu gracza
        if animacja_aktywna:
            if animacja_krok < ostatni_rzut[0] + ostatni_rzut[1]:
                # Przesuń gracza o jeden krok
                gracze[aktualny_gracz]["pozycja"] = (animacja_start_pozycja + animacja_krok + 1) % 40
                
                # Sprawdź czy gracz przekroczył START (tylko podczas animacji)
                if gracze[aktualny_gracz]["pozycja"] == 0 and animacja_krok > 0:
                    gracze[aktualny_gracz]["pieniadze"] += 200
                    print(f"Gracz {gracze[aktualny_gracz]['nazwa']} przeszedł przez START i otrzymuje 200 PLN")
                
                animacja_krok += 1
                
                # Opóźnienie dla animacji
                pygame.time.delay(300)
            else:
                # Zakończ animację i aktualizuj logikę
                animacja_aktywna = False
                tura_wykonana = True
                
                # Sprawdzenie końcowej pozycji (pola specjalne, podatki itp.)
                pozycja = gracze[aktualny_gracz]["pozycja"]
                pole = pobierz_pole(pozycja)

                # Sprawdź czy gracz musi zapłacić czynsz
                info_platnosci = sprawdz_platnosc(aktualny_gracz, pozycja, gracze)
                if info_platnosci:
                    # Ustaw flagę do wyświetlenia okna płatności
                    platnosc_do_wyswietlenia = info_platnosci
                
                # Dodaj wpis do historii
                historia_ruchow.append({
                    "gracz": aktualny_gracz,
                    "z_pozycji": animacja_start_pozycja,
                    "na_pozycje": pozycja,
                    "rzut": ostatni_rzut[0] + ostatni_rzut[1]
                })
                  # Logika pól specjalnych
                if pole["typ"] == "podatek":
                    # Pobierz opłatę
                    gracze[aktualny_gracz]["pieniadze"] -= pole["cena"]
                    print(f"Gracz {gracze[aktualny_gracz]['nazwa']} płaci {pole['cena']} PLN podatku")
                
                elif pole["typ"] == "specjalne" and pole["nazwa"] == "IDŹ NA POPRAWKĘ":
                    # Idź do dziekanatu
                    gracze[aktualny_gracz]["pozycja"] = 10
                    print(f"Gracz {gracze[aktualny_gracz]['nazwa']} idzie na poprawkę (dziekanat)")
                
                elif pole["typ"] == "specjalne" and pole["nazwa"] == "SZANSA":
                    # Wyciągnij kartę Szansa
                    from karty import pobierz_karte_szansa, wykonaj_karte
                    karta = pobierz_karte_szansa()
                    print(f"Gracz {gracze[aktualny_gracz]['nazwa']} wyciągnął kartę Szansa")
                    karta_do_wyswietlenia = ("SZANSA", karta)
                    wykonaj_karte(karta, aktualny_gracz, gracze)
                
                elif pole["typ"] == "specjalne" and pole["nazwa"] == "KASA STUDENCKA":
                    # Wyciągnij kartę Kasa Studencka
                    from karty import pobierz_karte_kasa_studencka, wykonaj_karte
                    karta = pobierz_karte_kasa_studencka()
                    print(f"Gracz {gracze[aktualny_gracz]['nazwa']} wyciągnął kartę Kasa Studencka")
                    karta_do_wyswietlenia = ("KASA STUDENCKA", karta)
                    wykonaj_karte(karta, aktualny_gracz, gracze)
                
                # Za każdy ruch dodaj ECTS
                gracze[aktualny_gracz]["ects"] += 1
                
                # Sprawdzenie, czy może kupić pole
                if pole["typ"] in ["wydzial", "akademik", "uslugi"] and pole.get("wlasciciel") is None:
                    kupowanie_pola = True
        
        # Rysuj planszę i pobierz jej wymiary
        plansza_x, plansza_y, plansza_rozmiar = narysuj_plansze(ekran, gracze)
        
        # Panel boczny z informacjami o graczach
        panel_x = plansza_x + plansza_rozmiar + 20
        
        # Obszar panelu bocznego
        pygame.draw.rect(ekran, NIEBIESKI_POLE, (panel_x, plansza_y, SZEROKOSC - panel_x - 20, plansza_rozmiar), border_radius=10)
        
        # Nagłówek panelu
        czcionka_naglowek = pygame.font.SysFont('Arial', 30, bold=True)
        tekst_naglowek = czcionka_naglowek.render("Status graczy", True, BIALY)
        ekran.blit(tekst_naglowek, (panel_x + 20, plansza_y + 20))
        
        # Karty graczy
        for i, gracz in enumerate(gracze):
            karta_wysokosc = 180
            karta_y = plansza_y + 70 + i * (karta_wysokosc + 10)
            narysuj_karte_gracza(ekran, gracz, panel_x + 20, karta_y, SZEROKOSC - panel_x - 60, karta_wysokosc, i == aktualny_gracz)
        
        # Panel kontrolny na dole ekranu
        panel_dol_y = plansza_y + plansza_rozmiar + 20
        pygame.draw.rect(ekran, NIEBIESKI_POLE, (50, panel_dol_y, SZEROKOSC - 100, WYSOKOSC - panel_dol_y - 20), border_radius=10)
        
        # Kostki
        narysuj_kostke(ekran, 80, panel_dol_y + 20, 50, ostatni_rzut[0])
        narysuj_kostke(ekran, 150, panel_dol_y + 20, 50, ostatni_rzut[1])
        
        # Suma
        czcionka_suma = pygame.font.SysFont('Arial', 24, bold=True)
        suma_tekst = czcionka_suma.render(f"Suma: {ostatni_rzut[0] + ostatni_rzut[1]}", True, BIALY)
        ekran.blit(suma_tekst, (230, panel_dol_y + 35))
        
        # Instrukcje
        czcionka_instr = pygame.font.SysFont('Arial', 20)
        instr_tekst1 = czcionka_instr.render("Spacja = rzut kostką", True, BIALY)
        ekran.blit(instr_tekst1, (80, panel_dol_y + 80))
        
        # Status tury
        status_tekst = f"Tura gracza: {gracze[aktualny_gracz]['nazwa']}"
        status_render = czcionka_suma.render(status_tekst, True, ZLOTY)
        ekran.blit(status_render, (400, panel_dol_y + 35))
        
        # Przycisk kupowania pola
        if kupowanie_pola and tura_wykonana and not animacja_aktywna:
            pozycja = gracze[aktualny_gracz]["pozycja"]
            pole = pobierz_pole(pozycja)
            if utworz_przycisk(ekran, f"Kup {pole['nazwa']} za {pole['cena']} PLN", 400, panel_dol_y + 80, 350, 40, ZIELONY, BIALY, 18):
                if gracze[aktualny_gracz]["pieniadze"] >= pole["cena"]:
                    gracze[aktualny_gracz]["pieniadze"] -= pole["cena"]
                    pole["wlasciciel"] = aktualny_gracz
                    gracze[aktualny_gracz]["budynki"] += 1
                    print(f"Gracz {gracze[aktualny_gracz]['nazwa']} kupił {pole['nazwa']} za {pole['cena']} PLN")
                    kupowanie_pola = False
                else:
                    print(f"Gracz {gracze[aktualny_gracz]['nazwa']} nie ma wystarczająco pieniędzy, aby kupić {pole['nazwa']}")
        
        # Przycisk następnego gracza
        if tura_wykonana and not animacja_aktywna:
            if utworz_przycisk(ekran, "Następny gracz", 800, panel_dol_y + 35, 200, 40, ZIELONY, BIALY, 20):
                aktualny_gracz = (aktualny_gracz + 1) % len(gracze)
                tura_wykonana = False
                kupowanie_pola = False
                print(f"Tura gracza: {gracze[aktualny_gracz]['nazwa']}")
          
        # Wyświetl okno płatności jeśli była transakcja
        if platnosc_do_wyswietlenia:
            from interfejs import wyswietl_okno_platnosci
            gracz_platnik = gracze[platnosc_do_wyswietlenia["platnik"]]
            gracz_wlasciciel = gracze[platnosc_do_wyswietlenia["wlasciciel"]]
            pole_info = platnosc_do_wyswietlenia["pole"]
            kwota = platnosc_do_wyswietlenia["kwota"]
            
            if wyswietl_okno_platnosci(ekran, gracz_platnik, gracz_wlasciciel, pole_info, kwota):
                platnosc_do_wyswietlenia = None
          
          # Wyświetl kartę jeśli została wyciągnięta
        if karta_do_wyswietlenia:
            tytul, karta = karta_do_wyswietlenia
            if wyswietl_okno_karty(ekran, karta, tytul):
                karta_do_wyswietlenia = None
          # Przycisk powrotu
        if not animacja_aktywna and utworz_przycisk(ekran, "Powrót do menu", 800, panel_dol_y + 80, 200, 40, CZERWONY_TLO, BIALY, 20):
            running = False
            return True
        
        # Aktualizuj ekran
        pygame.display.flip()
        zegar.tick(60)
    
    return False
    
    return False

# Uruchom samodzielnie jeśli skrypt jest wywoływany bezpośrednio
if __name__ == "__main__":
    ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
    pygame.display.set_caption("MonoPOLI - Politechnika Łódzka")
    ekran_gry()
    pygame.quit()