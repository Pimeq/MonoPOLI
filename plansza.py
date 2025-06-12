import pygame
import sys
from constants import *
from pola import *
from logika import *
from interfejs import *
from plansza_render import narysuj_plansze

# Inicjalizacja Pygame
pygame.init()

# Rozmiar okna
SZEROKOSC, WYSOKOSC = 1200, 1000

# Funkcja główna dla ekranu gry
def ekran_gry(ekran_zewnetrzny=None, skala_interfejsu=1, glosnosc_efekty=0.7):
    """Główna funkcja obsługująca rozgrywkę z obsługą skalowania"""
    global gracze, aktualny_gracz, ostatni_rzut, tura_wykonana
    
    # Bazowe wymiary interfejsu
    bazowa_szerokosc = SZEROKOSC
    bazowa_wysokosc = WYSOKOSC
    
    # Używaj przekazanego ekranu lub utwórz własny jeśli nie został przekazany
    if ekran_zewnetrzny:
        ekran = ekran_zewnetrzny
        screen_width, screen_height = ekran.get_size()
    else:
        ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
        pygame.display.set_caption("MonoPOLI - Politechnika Łódzka")
        screen_width, screen_height = SZEROKOSC, WYSOKOSC
    
    # Utwórz surface dla interfejsu o bazowym rozmiarze
    interface_surface = pygame.Surface((bazowa_szerokosc, bazowa_wysokosc), pygame.SRCALPHA)
    
    # Oblicz docelowe wymiary po skalowaniu
    skalowana_szerokosc = int(bazowa_szerokosc * skala_interfejsu)
    skalowana_wysokosc = int(bazowa_wysokosc * skala_interfejsu)
    
    # Pozycja interfejsu na ekranie (centrowanie)
    interface_x = (screen_width - skalowana_szerokosc) // 2
    interface_y = (screen_height - skalowana_wysokosc) // 2
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
    
    original_get_pos = pygame.mouse.get_pos


    while running:
        # Temporarne nadpisanie pygame.mouse.get_pos dla skalowania
        
        def scaled_get_pos():
            pos = original_get_pos()
            # Przelicz pozycję myszy z ekranu na współrzędne interface_surface
            scaled_x = (pos[0] - interface_x) / skala_interfejsu
            scaled_y = (pos[1] - interface_y) / skala_interfejsu
            return (int(scaled_x), int(scaled_y))
        
        pygame.mouse.get_pos = scaled_get_pos
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Obsługa klawiszy
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not tura_wykonana and not platnosc_do_wyswietlenia and not animacja_aktywna and not karta_do_wyswietlenia:
                    # Play dice sound
                    try:
                        d = pygame.mixer.Sound("Audio/dice.mp3")
                        d.set_volume(glosnosc_efekty)
                        d.play()
                    except Exception:
                        pass
                    # Rzut kostką po naciśnięciu spacji
                    ostatni_rzut = rzut_kostka()
                    suma_oczek = ostatni_rzut[0] + ostatni_rzut[1]
                    
                    # Zapisz pozycję początkową i docelową dla animacji
                    animacja_start_pozycja = gracze[aktualny_gracz][KEY_POZYCJA]
                    animacja_docelowa_pozycja = (animacja_start_pozycja + suma_oczek) % 36
                    
                    # Rozpocznij animację
                    animacja_aktywna = True
                    animacja_krok = 0

                if event.key == pygame.K_SPACE and karta_do_wyswietlenia and not platnosc_do_wyswietlenia and not animacja_aktywna:
                    karta_do_wyswietlenia = False
                    tura_wykonana = True
                    
                if event.key == pygame.K_SPACE and platnosc_do_wyswietlenia and not animacja_aktywna and not karta_do_wyswietlenia:
                    platnosc_do_wyswietlenia = False
                    tura_wykonana = True

                if event.key == pygame.K_SPACE and tura_wykonana and not animacja_aktywna:
                    aktualny_gracz = (aktualny_gracz + 1) % len(gracze)
                    tura_wykonana = False
                    kupowanie_pola = False
                    print(f"Tura gracza: {gracze[aktualny_gracz][KEY_NAZWA]}")

                
                # DEBUG: Dodaj domek na aktualnym polu po wciśnięciu D
                if event.key == pygame.K_d:
                    pozycja = gracze[aktualny_gracz][KEY_POZYCJA]
                    pole = pobierz_pole(pozycja)
                    if pole[KEY_TYP] in ["wydzial", "akademik", "uslugi"]:
                        if pole.get(KEY_DOMKI, 0) < 4:
                            pole[KEY_DOMKI] = pole.get(KEY_DOMKI, 0) + 1
                            print(f"[DEBUG] Dodano domek na {pole[KEY_NAZWA]} (liczba domków: {pole[KEY_DOMKI]})")
                        else:
                            print(f"[DEBUG] Na polu {pole[KEY_NAZWA]} nie można mieć więcej niż 4 domki!")
                
                # DEBUG: Przekaż wszystkie posiadłości graczowi z tury po wciśnięciu F
                if event.key == pygame.K_f:
                    for idx, pole in enumerate(pola):
                        if pole[KEY_TYP] in ["wydzial", "akademik", "uslugi"]:
                            pole[KEY_WLASCICIEL] = aktualny_gracz
                            pole[KEY_DOMKI] = 0  # opcjonalnie zeruj domki
                    print(f"[DEBUG] Wszystkie posiadłości zostały przekazane graczowi {gracze[aktualny_gracz][KEY_NAZWA]}")
                
        # Wypełnij tło
        interface_surface.fill(CIEMNY_NIEBIESKI)
        
        # Animacja ruchu gracza
        if animacja_aktywna:
            # Play player move sound on every animation step, including the last
            try:
                m = pygame.mixer.Sound("Audio/playermove.mp3")
                m.set_volume(glosnosc_efekty)
                m.play()
            except Exception:
                pass
            if animacja_krok < ostatni_rzut[0] + ostatni_rzut[1]:
                # Przesuń gracza o jeden krok
                gracze[aktualny_gracz][KEY_POZYCJA] = (animacja_start_pozycja + animacja_krok + 1) % 36
                
                # Sprawdź czy gracz przekroczył START (tylko podczas animacji)
                if gracze[aktualny_gracz][KEY_POZYCJA] == 0 and animacja_krok > 0:
                    gracze[aktualny_gracz][KEY_PIENIADZE] += 200
                    print(f"Gracz {gracze[aktualny_gracz][KEY_NAZWA]} przeszedł przez START i otrzymuje 200 PLN")
                
                animacja_krok += 1
                
                # Opóźnienie dla animacji
                pygame.time.delay(300)
            else:
                # Zakończ animację i aktualizuj logikę
                animacja_aktywna = False
                tura_wykonana = True
                
                # Sprawdzenie końcowej pozycji (pola specjalne, podatki itp.)
                pozycja = gracze[aktualny_gracz][KEY_POZYCJA]
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
                if pole[KEY_TYP] == "podatek":
                    gracze[aktualny_gracz][KEY_PIENIADZE] -= pole[KEY_CENA]
                    print(f"Gracz {gracze[aktualny_gracz][KEY_NAZWA]} płaci {pole['cena']} PLN podatku")
                
                elif pole[KEY_TYP] == "narozne" and pole[KEY_NAZWA] == "IDŹ NA POPRAWKĘ":
                    gracze[aktualny_gracz][KEY_POZYCJA] = 9
                    print(f"Gracz {gracze[aktualny_gracz][KEY_NAZWA]} idzie na poprawkę (dziekanat)")
                
                elif pole[KEY_TYP] == "specjalne" and pole[KEY_NAZWA] == "SZANSA":
                    # Wyciągnij kartę Szansa
                    from karty import pobierz_karte_szansa, wykonaj_karte
                    karta = pobierz_karte_szansa()
                    print(f"Gracz {gracze[aktualny_gracz][KEY_NAZWA]} wyciągnął kartę Szansa")
                    karta_do_wyswietlenia = ("SZANSA", karta)
                    wykonaj_karte(karta, aktualny_gracz, gracze)
                
                elif pole[KEY_TYP] == "specjalne" and pole[KEY_NAZWA] == "KASA STUDENCKA":
                    # Wyciągnij kartę Kasa Studencka
                    from karty import pobierz_karte_kasa_studencka, wykonaj_karte
                    karta = pobierz_karte_kasa_studencka()
                    print(f"Gracz {gracze[aktualny_gracz][KEY_NAZWA]} wyciągnął kartę Kasa Studencka")
                    karta_do_wyswietlenia = ("KASA STUDENCKA", karta)
                    wykonaj_karte(karta, aktualny_gracz, gracze)
                
                # Za każdy ruch dodaj ECTS
                gracze[aktualny_gracz][KEY_ECTS] += 1
                
                # Sprawdzenie, czy może kupić pole
                if pole[KEY_TYP] in ["wydzial", "akademik", "uslugi"] and pole.get(KEY_WLASCICIEL) is None:
                    kupowanie_pola = True
          # Rysuj planszę i pobierz jej wymiary
        plansza_x, plansza_y, plansza_rozmiar = narysuj_plansze(interface_surface, gracze)
        
        # Panel boczny z informacjami o graczach
        panel_x = plansza_x + plansza_rozmiar + 20
        
        # Obszar panelu bocznego
        pygame.draw.rect(interface_surface, NIEBIESKI_POLE, (panel_x, plansza_y, bazowa_szerokosc - panel_x - 20, plansza_rozmiar + 120), border_radius=10)

        
        # Nagłówek panelu
        czcionka_naglowek = pygame.font.SysFont('Arial', 30, bold=True)
        tekst_naglowek = czcionka_naglowek.render("Status graczy", True, BIALY)
        interface_surface.blit(tekst_naglowek, (panel_x + 20, plansza_y + 20))
        
        # Karty graczy
        for i, gracz in enumerate(gracze):
            karta_wysokosc = 180
            karta_y = plansza_y + 70 + i * (karta_wysokosc + 10)
            narysuj_karte_gracza(interface_surface, gracz, panel_x + 20, karta_y, bazowa_szerokosc - panel_x - 60, karta_wysokosc, i == aktualny_gracz)
        
        # Panel kontrolny na dole ekranu
        panel_dol_y = plansza_y + plansza_rozmiar + 20

        pygame.draw.rect(interface_surface, NIEBIESKI_POLE, (50, panel_dol_y, bazowa_szerokosc - 70, bazowa_wysokosc - panel_dol_y - 20), border_radius=10)

        
        # Kostki
        narysuj_kostke(interface_surface, 80, panel_dol_y + 20, 50, ostatni_rzut[0])
        narysuj_kostke(interface_surface, 150, panel_dol_y + 20, 50, ostatni_rzut[1])
        
        # Suma
        czcionka_suma = pygame.font.SysFont('Arial', 24, bold=True)
        suma_tekst = czcionka_suma.render(f"Suma: {ostatni_rzut[0] + ostatni_rzut[1]}", True, BIALY)
        interface_surface.blit(suma_tekst, (230, panel_dol_y + 35))
        
        # Instrukcje
        czcionka_instr = pygame.font.SysFont('Arial', 20)
        instr_tekst1 = czcionka_instr.render("Spacja = rzut kostką", True, BIALY)
        interface_surface.blit(instr_tekst1, (80, panel_dol_y + 80))
        
        # Status tury

        status_tekst = f"Tura gracza: {gracze[aktualny_gracz][KEY_NAZWA]}"
        status_render = czcionka_suma.render(status_tekst, True, ZLOTY)
        interface_surface.blit(status_render, (400, panel_dol_y + 35))
          # Przycisk kupowania pola
        if kupowanie_pola and tura_wykonana and not animacja_aktywna:
            pozycja = gracze[aktualny_gracz][KEY_POZYCJA]
            pole = pobierz_pole(pozycja)
            if utworz_przycisk(interface_surface, f"Kup {pole[KEY_NAZWA]} za {pole[KEY_CENA]} PLN", 350, panel_dol_y + 30, 350, 40, ZIELONY, BIALY, 18, glosnosc_efekty=glosnosc_efekty):

                if gracze[aktualny_gracz][KEY_PIENIADZE] >= pole[KEY_CENA]:
                    gracze[aktualny_gracz][KEY_PIENIADZE] -= pole[KEY_CENA]
                    pole[KEY_WLASCICIEL] = aktualny_gracz
                    gracze[aktualny_gracz][KEY_BUDYNKI] += 1
                    print(f"Gracz {gracze[aktualny_gracz][KEY_NAZWA]} kupił {pole[KEY_NAZWA]} za {pole[KEY_CENA]} PLN")
                    kupowanie_pola = False
                    tura_wykonana = False
                    aktualny_gracz = (aktualny_gracz + 1) % len(gracze)
                    continue

                else:
                    print(f"Gracz {gracze[aktualny_gracz][KEY_NAZWA]} nie ma wystarczająco pieniędzy, aby kupić {pole[KEY_NAZWA]}")
        
        # Przycisk kupowania domku na swoim polu (otwiera okno po kliknięciu)
        if (
            tura_wykonana and not animacja_aktywna and not kupowanie_pola
        ):
            pozycja = gracze[aktualny_gracz][KEY_POZYCJA]
            pole = pobierz_pole(pozycja)
            if (
                pole[KEY_TYP] in ["wydzial", "akademik", "uslugi"]
                and pole.get(KEY_WLASCICIEL) == aktualny_gracz
                and pole.get(KEY_DOMKI, 0) < 4
            ):
                cena_domku = int(pole[KEY_CENA] * 0.5)
                if utworz_przycisk(interface_surface, f"Kup domek na {pole[KEY_NAZWA]} za {cena_domku} PLN", 400, panel_dol_y + 80, 350, 40, ZIELONY, BIALY, 18, glosnosc_efekty=glosnosc_efekty):
                    ilosc = wyswietl_okno_kupna_domkow(ekran, pole, gracze[aktualny_gracz])
                    interface_surface.fill(CIEMNY_NIEBIESKI)
                    plansza_x, plansza_y, plansza_rozmiar = narysuj_plansze(interface_surface, gracze)
                    panel_x = plansza_x + plansza_rozmiar + 20
                    pygame.draw.rect(interface_surface, NIEBIESKI_POLE, (panel_x, plansza_y, bazowa_szerokosc - panel_x - 20, plansza_rozmiar + 120), border_radius=10)
                    czcionka_naglowek = pygame.font.SysFont('Arial', 30, bold=True)
                    tekst_naglowek = czcionka_naglowek.render("Status graczy", True, BIALY)
                    interface_surface.blit(tekst_naglowek, (panel_x + 20, plansza_y + 20))
                    for i, gracz in enumerate(gracze):
                        karta_wysokosc = 180
                        karta_y = plansza_y + 70 + i * (karta_wysokosc + 10)
                        narysuj_karte_gracza(interface_surface, gracz, panel_x + 20, karta_y, bazowa_szerokosc - panel_x - 60, karta_wysokosc, i == aktualny_gracz)
                    pygame.draw.rect(interface_surface, NIEBIESKI_POLE, (50, panel_dol_y, bazowa_szerokosc - 70, bazowa_wysokosc - panel_dol_y - 20), border_radius=10)
                    narysuj_kostke(interface_surface, 80, panel_dol_y + 20, 50, ostatni_rzut[0])
                    narysuj_kostke(interface_surface, 150, panel_dol_y + 20, 50, ostatni_rzut[1])
                    czcionka_suma = pygame.font.SysFont('Arial', 24, bold=True)
                    suma_tekst = czcionka_suma.render(f"Suma: {ostatni_rzut[0] + ostatni_rzut[1]}", True, BIALY)
                    interface_surface.blit(suma_tekst, (230, panel_dol_y + 35))
                    czcionka_instr = pygame.font.SysFont('Arial', 20)
                    instr_tekst1 = czcionka_instr.render("Spacja = rzut kostką", True, BIALY)
                    interface_surface.blit(instr_tekst1, (80, panel_dol_y + 80))
                    status_tekst = f"Tura gracza: {gracze[aktualny_gracz][KEY_NAZWA]}"
                    status_render = czcionka_suma.render(status_tekst, True, ZLOTY)
                    interface_surface.blit(status_render, (400, panel_dol_y + 35))
                    if ilosc > 0:
                        suma = ilosc * cena_domku
                        if gracze[aktualny_gracz][KEY_PIENIADZE] >= suma:
                            gracze[aktualny_gracz][KEY_PIENIADZE] -= suma
                            pole[KEY_DOMKI] = pole.get(KEY_DOMKI, 0) + ilosc
                            print(f"Gracz {gracze[aktualny_gracz][KEY_NAZWA]} kupił {ilosc} domków na {pole[KEY_NAZWA]} (razem: {pole[KEY_DOMKI]})")
                        else:
                            print(f"Gracz {gracze[aktualny_gracz][KEY_NAZWA]} nie ma wystarczająco pieniędzy na {ilosc} domków na {pole[KEY_NAZWA]}")
        
        # Przycisk następnego gracza
        if tura_wykonana and not animacja_aktywna:

            if utworz_przycisk(interface_surface, "Następny gracz", 740, panel_dol_y + 30, 200, 40, ZIELONY, BIALY, 20, glosnosc_efekty=glosnosc_efekty):

                aktualny_gracz = (aktualny_gracz + 1) % len(gracze)
                tura_wykonana = False
                kupowanie_pola = False
                print(f"Tura gracza: {gracze[aktualny_gracz][KEY_NAZWA]}")
            # Wyświetl okno płatności jeśli była transakcja
        if platnosc_do_wyswietlenia:
            from interfejs import wyswietl_okno_platnosci
            gracz_platnik = gracze[platnosc_do_wyswietlenia["platnik"]]
            gracz_wlasciciel = gracze[platnosc_do_wyswietlenia["wlasciciel"]]
            pole_info = platnosc_do_wyswietlenia["pole"]
            kwota = platnosc_do_wyswietlenia["kwota"]
            
            if wyswietl_okno_platnosci(interface_surface, gracz_platnik, gracz_wlasciciel, pole_info, kwota):
                platnosc_do_wyswietlenia = None
          
          # Wyświetl kartę jeśli została wyciągnięta
        if karta_do_wyswietlenia:
            tytul, karta = karta_do_wyswietlenia
            if wyswietl_okno_karty(interface_surface, karta, tytul):
                karta_do_wyswietlenia = None
          # Przycisk powrotu

        if not animacja_aktywna and utworz_przycisk(interface_surface, "Powrót do menu", 950, panel_dol_y + 30, 200, 40, CZERWONY_TLO, BIALY, 20):

            running = False
            # Przywróć oryginalną funkcję mouse.get_pos
            pygame.mouse.get_pos = original_get_pos
            return True
        
        
        
        # Skaluj interface_surface i narysuj na głównym ekranie
        if skala_interfejsu != 1.0:
            scaled_surface = pygame.transform.scale(interface_surface, (skalowana_szerokosc, skalowana_wysokosc))
        else:
            scaled_surface = interface_surface
        
        # Wyczyść główny ekran
        ekran.fill(CZARNY)
        
        # Narysuj skalowany interfejs na głównym ekranie
        ekran.blit(scaled_surface, (interface_x, interface_y))
          # Aktualizuj ekran
        pygame.display.flip()
        zegar.tick(60)
    
    return False

# Uruchom samodzielnie jeśli skrypt jest wywoływany bezpośrednio
if __name__ == "__main__":
    ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
    pygame.display.set_caption("MonoPOLI - Politechnika Łódzka")
    ekran_gry()
    pygame.quit()