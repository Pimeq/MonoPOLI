import pygame
from constants import *
from pola import pola, pobierz_pole
from interfejs import narysuj_zaokraglony_prostokat, utworz_przycisk

# Funkcje debugujące
def debug_wygraj_gre(gracze, gracz_index):
    """DEBUG: Sets ECTS to win condition for selected player"""
    gracze[gracz_index][KEY_ECTS] = ECTS_TO_WIN
    print(f"DEBUG: Gracz {gracze[gracz_index][KEY_NAZWA]} otrzymał {ECTS_TO_WIN} ECTS i wygrywa!")

def debug_dodaj_domek(gracze, gracz_index, pozycja=None):
    """DEBUG: Dodaje domek na polu gracza lub określonej pozycji"""
    if pozycja is None:
        pozycja = gracze[gracz_index][KEY_POZYCJA]
    
    pole = pobierz_pole(pozycja)
    if pole[KEY_TYP] in ["wydzial", "akademik", "uslugi"]:
        if pole.get(KEY_DOMKI, 0) < 4:
            pole[KEY_DOMKI] = pole.get(KEY_DOMKI, 0) + 1
            print(f"[DEBUG] Dodano domek na {pole[KEY_NAZWA]} (liczba domków: {pole[KEY_DOMKI]})")
            return True
        else:
            print(f"[DEBUG] Na polu {pole[KEY_NAZWA]} nie można mieć więcej niż 4 domki!")
            return False
    else:
        print(f"[DEBUG] Nie można dodać domku na polu {pole[KEY_NAZWA]} - zły typ pola")
        return False

def debug_przekaz_posiadlosci(gracze, gracz_index):
    """DEBUG: Przekazuje wszystkie posiadłości wybranemu graczowi"""
    for idx, pole in enumerate(pola):
        if pole[KEY_TYP] in ["wydzial", "akademik", "uslugi"]:
            pole[KEY_WLASCICIEL] = gracz_index
            pole[KEY_DOMKI] = 0  # Zeruj domki
    print(f"[DEBUG] Wszystkie posiadłości zostały przekazane graczowi {gracze[gracz_index][KEY_NAZWA]}")

def debug_przenies_gracza(gracze, gracz_index, pozycja):
    """DEBUG: Przenosi gracza na określoną pozycję"""
    if 0 <= pozycja < len(pola):
        gracze[gracz_index][KEY_POZYCJA] = pozycja
        pole = pobierz_pole(pozycja)
        print(f"[DEBUG] Gracz {gracze[gracz_index][KEY_NAZWA]} przeniesiony na pole {pole[KEY_NAZWA]} (pozycja {pozycja})")
        return True
    else:
        print(f"[DEBUG] Nieprawidłowa pozycja: {pozycja}")
        return False

def debug_dodaj_pieniadze(gracze, gracz_index, kwota):
    """DEBUG: Dodaje pieniądze graczowi"""
    gracze[gracz_index][KEY_PIENIADZE] += kwota
    print(f"[DEBUG] Gracz {gracze[gracz_index][KEY_NAZWA]} otrzymał {kwota} PLN (łącznie: {gracze[gracz_index][KEY_PIENIADZE]})")

def debug_dodaj_ects(gracze, gracz_index, ects):
    """DEBUG: Dodaje ECTS graczowi"""
    gracze[gracz_index][KEY_ECTS] += ects
    print(f"[DEBUG] Gracz {gracze[gracz_index][KEY_NAZWA]} otrzymał {ects} ECTS (łącznie: {gracze[gracz_index][KEY_ECTS]})")

def debug_ustaw_ture(aktualny_gracz_index, nowy_gracz_index):
    """DEBUG: Ustawia turę na wybranego gracza"""
    print(f"[DEBUG] Tura zmieniona z gracza {aktualny_gracz_index} na gracza {nowy_gracz_index}")
    return nowy_gracz_index

# Menu debugowania
def wyswietl_menu_debug(ekran, gracze, aktualny_gracz, glosnosc_efekty=0.7):
    """Wyświetla menu debugowania z opcjami dla każdego gracza"""
    clock = pygame.time.Clock()
    wybrany_gracz = 0
    wybrany_akcja = 0
    pozycja_input = ""
    kwota_input = ""
    ects_input = ""
    input_aktywny = None
    
    akcje = [
        "Instant Win (30 ECTS)",
        "Dodaj domek na aktualnej pozycji",
        "Przekaż wszystkie posiadłości",
        "Przenies gracza (pozycja)",
        "Dodaj pieniądze (kwota)",
        "Dodaj ECTS (ilość)",
        "Ustaw turę na tego gracza"
    ]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return aktualny_gracz, "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return aktualny_gracz, "close"
                elif event.key == pygame.K_UP:
                    wybrany_akcja = (wybrany_akcja - 1) % len(akcje)
                elif event.key == pygame.K_DOWN:
                    wybrany_akcja = (wybrany_akcja + 1) % len(akcje)
                elif event.key == pygame.K_LEFT:
                    wybrany_gracz = (wybrany_gracz - 1) % len(gracze)
                elif event.key == pygame.K_RIGHT:
                    wybrany_gracz = (wybrany_gracz + 1) % len(gracze)
                elif event.key == pygame.K_RETURN:
                    # Wykonaj wybraną akcję
                    if wybrany_akcja == 0:  # Instant Win
                        debug_wygraj_gre(gracze, wybrany_gracz)
                        return aktualny_gracz, "close"
                    elif wybrany_akcja == 1:  # Dodaj domek
                        debug_dodaj_domek(gracze, wybrany_gracz)
                    elif wybrany_akcja == 2:  # Przekaż posiadłości
                        debug_przekaz_posiadlosci(gracze, wybrany_gracz)
                    elif wybrany_akcja == 3:  # Przenies gracza
                        if pozycja_input.isdigit():
                            pozycja = int(pozycja_input)
                            if debug_przenies_gracza(gracze, wybrany_gracz, pozycja):
                                pozycja_input = ""  # Wyczyść po udanym przeniesieniu
                        else:
                            print("[DEBUG] Wprowadź prawidłową pozycję (0-35)")
                    elif wybrany_akcja == 4:  # Dodaj pieniądze
                        if kwota_input.isdigit() and int(kwota_input) > 0:
                            kwota = int(kwota_input)
                            debug_dodaj_pieniadze(gracze, wybrany_gracz, kwota)
                            kwota_input = ""  # Wyczyść po udanym dodaniu
                        else:
                            print("[DEBUG] Wprowadź prawidłową kwotę (większą od 0)")
                    elif wybrany_akcja == 5:  # Dodaj ECTS
                        if ects_input.isdigit() and int(ects_input) > 0:
                            ects = int(ects_input)
                            debug_dodaj_ects(gracze, wybrany_gracz, ects)
                            ects_input = ""  # Wyczyść po udanym dodaniu
                        else:
                            print("[DEBUG] Wprowadź prawidłową ilość ECTS (większą od 0)")
                    elif wybrany_akcja == 6:  # Ustaw turę
                        return debug_ustaw_ture(aktualny_gracz, wybrany_gracz), "close"
                
                # Obsługa wprowadzania tekstu tylko gdy odpowiednie pole jest aktywne
                elif wybrany_akcja == 3 and event.key == pygame.K_BACKSPACE:
                    pozycja_input = pozycja_input[:-1]
                elif wybrany_akcja == 3 and event.unicode.isdigit() and len(pozycja_input) < 2:
                    pozycja_input += event.unicode
                elif wybrany_akcja == 4 and event.key == pygame.K_BACKSPACE:
                    kwota_input = kwota_input[:-1]
                elif wybrany_akcja == 4 and event.unicode.isdigit() and len(kwota_input) < 6:
                    kwota_input += event.unicode
                elif wybrany_akcja == 5 and event.key == pygame.K_BACKSPACE:
                    ects_input = ects_input[:-1]
                elif wybrany_akcja == 5 and event.unicode.isdigit() and len(ects_input) < 2:
                    ects_input += event.unicode
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Usunięto obsługę myszy dla uproszczenia
                pass
        
        # Tło
        ekran.fill(CIEMNY_NIEBIESKI)
        
        # Półprzezroczyste nakładka
        overlay = pygame.Surface((1200, 1000), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        ekran.blit(overlay, (0, 0))
        
        # Okno menu
        menu_rect = pygame.Rect(200, 50, 800, 750)
        narysuj_zaokraglony_prostokat(ekran, BIALY, menu_rect, 15)
        pygame.draw.rect(ekran, CZARNY, menu_rect, 3, border_radius=15)
        
        # Tytuł
        czcionka_tytul = pygame.font.SysFont('Arial', 36, bold=True)
        tekst_tytul = czcionka_tytul.render("MENU DEBUGOWANIA", True, CZERWONY)
        tytul_rect = tekst_tytul.get_rect(center=(600, 100))
        ekran.blit(tekst_tytul, tytul_rect)
        
        # Wybór gracza
        czcionka_gracz = pygame.font.SysFont('Arial', 24, bold=True)
        tekst_gracz = czcionka_gracz.render("Wybrany gracz:", True, CZARNY)
        ekran.blit(tekst_gracz, (250, 140))
        
        # Karty graczy
        for i, gracz in enumerate(gracze):
            x = 250 + i * 150
            y = 170
            kolor = gracz[KEY_KOLOR] if i == wybrany_gracz else SZARY
            
            # Karta gracza
            karta_rect = pygame.Rect(x, y, 130, 80)
            narysuj_zaokraglony_prostokat(ekran, kolor, karta_rect, 10)
            pygame.draw.rect(ekran, CZARNY, karta_rect, 2, border_radius=10)
            
            # Nazwa gracza
            czcionka_nazwa = pygame.font.SysFont('Arial', 16, bold=True)
            tekst_nazwa = czcionka_nazwa.render(gracz[KEY_NAZWA], True, BIALY)
            nazwa_rect = tekst_nazwa.get_rect(center=(x + 65, y + 20))
            ekran.blit(tekst_nazwa, nazwa_rect)
            
            # Informacje
            czcionka_info = pygame.font.SysFont('Arial', 12)
            tekst_poz = czcionka_info.render(f"Poz: {gracz[KEY_POZYCJA]}", True, BIALY)
            tekst_ects = czcionka_info.render(f"ECTS: {gracz[KEY_ECTS]}", True, BIALY)
            ekran.blit(tekst_poz, (x + 5, y + 40))
            ekran.blit(tekst_ects, (x + 5, y + 55))
            
            # Znacznik aktualnej tury
            if i == aktualny_gracz:
                pygame.draw.circle(ekran, ZLOTY, (x + 120, y + 10), 8)
                czcionka_tura = pygame.font.SysFont('Arial', 10, bold=True)
                tekst_tura = czcionka_tura.render("TURA", True, CZARNY)
                ekran.blit(tekst_tura, (x + 115, y + 6))
        
        # Lista akcji
        czcionka_akcja = pygame.font.SysFont('Arial', 20)
        tekst_akcje = czcionka_akcja.render("Dostępne akcje:", True, CZARNY)
        ekran.blit(tekst_akcje, (250, 280))
        
        for i, akcja in enumerate(akcje):
            y = 310 + i * 30
            kolor = ZIELONY if i == wybrany_akcja else SZARY_JASNY
            
            # Tło akcji
            akcja_rect = pygame.Rect(250, y, 500, 25)
            narysuj_zaokraglony_prostokat(ekran, kolor, akcja_rect, 5)
            
            # Tekst akcji
            tekst_akcja = czcionka_akcja.render(f"{i+1}. {akcja}", True, CZARNY)
            ekran.blit(tekst_akcja, (260, y + 3))
        
        # Pola input dla wybranych akcji
        if wybrany_akcja == 3:  # Przenies gracza
            czcionka_input = pygame.font.SysFont('Arial', 18)
            tekst_label = czcionka_input.render("Pozycja (0-35):", True, CZARNY)
            ekran.blit(tekst_label, (250, 570))
            
            input_rect = pygame.Rect(400, 565, 200, 30)
            kolor_input = ZIELONY_TLO
            narysuj_zaokraglony_prostokat(ekran, kolor_input, input_rect, 5)
            pygame.draw.rect(ekran, CZARNY, input_rect, 2, border_radius=5)
            
            tekst_input = czcionka_input.render(pozycja_input, True, CZARNY)
            ekran.blit(tekst_input, (410, 570))
            
        elif wybrany_akcja == 4:  # Dodaj pieniądze
            czcionka_input = pygame.font.SysFont('Arial', 18)
            tekst_label = czcionka_input.render("Kwota:", True, CZARNY)
            ekran.blit(tekst_label, (250, 570))
            
            input_rect = pygame.Rect(400, 565, 200, 30)
            kolor_input = ZIELONY_TLO
            narysuj_zaokraglony_prostokat(ekran, kolor_input, input_rect, 5)
            pygame.draw.rect(ekran, CZARNY, input_rect, 2, border_radius=5)
            
            tekst_input = czcionka_input.render(kwota_input, True, CZARNY)
            ekran.blit(tekst_input, (410, 570))
            
        elif wybrany_akcja == 5:  # Dodaj ECTS
            czcionka_input = pygame.font.SysFont('Arial', 18)
            tekst_label = czcionka_input.render("Ilość ECTS:", True, CZARNY)
            ekran.blit(tekst_label, (250, 570))
            
            input_rect = pygame.Rect(400, 565, 200, 30)
            kolor_input = ZIELONY_TLO
            narysuj_zaokraglony_prostokat(ekran, kolor_input, input_rect, 5)
            pygame.draw.rect(ekran, CZARNY, input_rect, 2, border_radius=5)
            
            tekst_input = czcionka_input.render(ects_input, True, CZARNY)
            ekran.blit(tekst_input, (410, 570))
        
        # Instrukcje
        czcionka_instr = pygame.font.SysFont('Arial', 16)
        instrukcje = [
            "←→ = wybierz gracza    ↑↓ = wybierz akcję",
            "ENTER = wykonaj akcję    ESC = zamknij menu",
            "Dla opcji z polami: wpisz wartość i naciśnij ENTER"
        ]
        
        for i, instr in enumerate(instrukcje):
            tekst_instr = czcionka_instr.render(instr, True, SZARY_CIEMNY)
            ekran.blit(tekst_instr, (250, 620 + i * 20))
        
        pygame.display.flip()
        clock.tick(60)
    
    return aktualny_gracz, "close"
