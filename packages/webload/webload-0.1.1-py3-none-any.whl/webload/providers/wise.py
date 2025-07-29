"""
Dostawca Wise - pobieranie wyciągów i faktur.
"""

import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from loguru import logger
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from webload.providers.base import BaseProvider


class WiseProvider(BaseProvider):
    """Dostawca Wise - pobieranie wyciągów i faktur."""
    
    def __init__(self, credentials: Dict[str, Any]):
        """
        Inicjalizacja dostawcy Wise.
        
        Args:
            credentials: Dane uwierzytelniające
        """
        super().__init__("Wise", credentials)
    
    @property
    def required_credentials(self) -> List[str]:
        """Lista wymaganych danych uwierzytelniających."""
        return ["email", "password"]
    
    @property
    def base_url(self) -> str:
        """Bazowy URL dostawcy."""
        return "https://wise.com"
    
    def login(self) -> bool:
        """
        Logowanie do serwisu Wise.
        
        Returns:
            True, jeśli logowanie się powiodło, False w przeciwnym razie
        """
        try:
            logger.info("Logowanie do Wise...")
            
            # Przejdź do strony logowania
            self.page.goto(f"{self.base_url}/login")
            
            # Poczekaj na załadowanie formularza logowania
            self.page.wait_for_selector('input[name="email"]')
            
            # Wprowadź email
            self.page.fill('input[name="email"]', self.credentials["email"])
            self.page.click('button[type="submit"]')
            
            # Poczekaj na pole hasła
            self.page.wait_for_selector('input[name="password"]')
            
            # Wprowadź hasło
            self.page.fill('input[name="password"]', self.credentials["password"])
            self.page.click('button[type="submit"]')
            
            # Sprawdź, czy logowanie się powiodło (czekaj na dashboard)
            try:
                self.page.wait_for_selector('.dashboard', timeout=30000)
                logger.success("Zalogowano do Wise")
                return True
            except PlaywrightTimeoutError:
                # Sprawdź, czy jest wymagane dodatkowe uwierzytelnianie
                if self.page.query_selector('.two-factor-auth'):
                    logger.error("Wymagane dodatkowe uwierzytelnianie. Zaloguj się ręcznie i spróbuj ponownie.")
                else:
                    logger.error("Nie udało się zalogować do Wise. Sprawdź dane uwierzytelniające.")
                return False
                
        except Exception as e:
            logger.error(f"Błąd podczas logowania do Wise: {e}")
            return False
    
    def download_documents(self, year: int, month: int) -> List[Path]:
        """
        Pobiera wyciągi i faktury z Wise dla określonego miesiąca i roku.
        
        Args:
            year: Rok
            month: Miesiąc
            
        Returns:
            Lista ścieżek do pobranych plików
        """
        downloaded_files = []
        
        try:
            # Przejdź do strony wyciągów
            logger.info(f"Pobieranie wyciągów Wise za {month:02d}/{year}...")
            self.page.goto(f"{self.base_url}/balances/statements/standard")
            
            # Poczekaj na załadowanie strony
            self.page.wait_for_selector('.statements-page')
            
            # Wybierz rok i miesiąc
            self._select_date_range(year, month)
            
            # Pobierz wyciągi
            statement_files = self._download_statements()
            downloaded_files.extend(statement_files)
            
            # Przejdź do strony faktur (jeśli dostępne)
            logger.info(f"Pobieranie faktur Wise za {month:02d}/{year}...")
            try:
                self.page.goto(f"{self.base_url}/invoices")
                
                # Poczekaj na załadowanie strony
                self.page.wait_for_selector('.invoices-page', timeout=10000)
                
                # Wybierz rok i miesiąc
                self._select_date_range(year, month)
                
                # Pobierz faktury
                invoice_files = self._download_invoices()
                downloaded_files.extend(invoice_files)
            except Exception as e:
                logger.warning(f"Nie udało się pobrać faktur z Wise: {e}")
            
        except Exception as e:
            logger.error(f"Błąd podczas pobierania dokumentów z Wise: {e}")
        
        return downloaded_files
    
    def _select_date_range(self, year: int, month: int) -> None:
        """
        Wybiera zakres dat na stronie.
        
        Args:
            year: Rok
            month: Miesiąc
        """
        try:
            # Kliknij w selektor dat
            date_selector = self.page.query_selector('.date-range-selector')
            if date_selector:
                date_selector.click()
                
                # Poczekaj na otwarcie kalendarza
                self.page.wait_for_selector('.date-picker')
                
                # Wybierz miesiąc i rok
                # Implementacja zależy od dokładnej struktury kalendarza w Wise
                # To jest uproszczona wersja
                
                # Przejdź do odpowiedniego miesiąca/roku
                current_date = datetime.now()
                months_to_go_back = (current_date.year - year) * 12 + (current_date.month - month)
                
                for _ in range(months_to_go_back):
                    prev_button = self.page.query_selector('.previous-month')
                    if prev_button:
                        prev_button.click()
                        time.sleep(0.5)
                
                # Wybierz pierwszy dzień miesiąca
                first_day = self.page.query_selector(f'[data-date="{year}-{month:02d}-01"]')
                if first_day:
                    first_day.click()
                
                # Wybierz ostatni dzień miesiąca (zakładając, że to 28-31)
                last_day_of_month = 31
                while last_day_of_month > 27:
                    last_day_selector = f'[data-date="{year}-{month:02d}-{last_day_of_month}"]'
                    last_day = self.page.query_selector(last_day_selector)
                    if last_day:
                        last_day.click()
                        break
                    last_day_of_month -= 1
                
                # Zatwierdź wybór
                apply_button = self.page.query_selector('button.apply')
                if apply_button:
                    apply_button.click()
                    time.sleep(2)  # Poczekaj na odświeżenie listy
        
        except Exception as e:
            logger.error(f"Błąd podczas wybierania zakresu dat: {e}")
    
    def _download_statements(self) -> List[Path]:
        """
        Pobiera wyciągi z aktualnie wyświetlonej strony.
        
        Returns:
            Lista ścieżek do pobranych plików
        """
        downloaded_files = []
        
        try:
            # Znajdź wszystkie przyciski pobierania
            download_buttons = self.page.query_selector_all('button[data-testid="statement-download-button"]')
            
            if not download_buttons:
                logger.info("Nie znaleziono wyciągów do pobrania")
                return []
            
            logger.info(f"Znaleziono {len(download_buttons)} wyciągów do pobrania")
            
            # Przygotuj katalog wyjściowy
            output_dir = self.get_output_directory(year=int(self.page.url.split("/")[-1].split("-")[0]),
                                                 month=int(self.page.url.split("/")[-1].split("-")[1]))
            
            # Pobierz każdy wyciąg
            for i, button in enumerate(download_buttons):
                try:
                    # Kliknij przycisk pobierania
                    with self.page.expect_download() as download_info:
                        button.click()
                    
                    # Pobierz plik
                    download = download_info.value
                    
                    # Generuj nazwę pliku
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    filename = f"wise_statement_{i+1}_{timestamp}.pdf"
                    
                    # Zapisz plik
                    output_path = output_dir / filename
                    download.save_as(output_path)
                    
                    logger.success(f"Pobrano wyciąg: {output_path}")
                    downloaded_files.append(output_path)
                    
                    # Krótka pauza między pobieraniami
                    time.sleep(1)
                
                except Exception as e:
                    logger.error(f"Błąd podczas pobierania wyciągu {i+1}: {e}")
        
        except Exception as e:
            logger.error(f"Błąd podczas pobierania wyciągów: {e}")
        
        return downloaded_files
    
    def _download_invoices(self) -> List[Path]:
        """
        Pobiera faktury z aktualnie wyświetlonej strony.
        
        Returns:
            Lista ścieżek do pobranych plików
        """
        downloaded_files = []
        
        try:
            # Znajdź wszystkie przyciski pobierania faktur
            download_buttons = self.page.query_selector_all('button[data-testid="invoice-download-button"]')
            
            if not download_buttons:
                logger.info("Nie znaleziono faktur do pobrania")
                return []
            
            logger.info(f"Znaleziono {len(download_buttons)} faktur do pobrania")
            
            # Przygotuj katalog wyjściowy
            output_dir = self.get_output_directory(year=int(self.page.url.split("/")[-1].split("-")[0]),
                                                 month=int(self.page.url.split("/")[-1].split("-")[1]))
            
            # Pobierz każdą fakturę
            for i, button in enumerate(download_buttons):
                try:
                    # Kliknij przycisk pobierania
                    with self.page.expect_download() as download_info:
                        button.click()
                    
                    # Pobierz plik
                    download = download_info.value
                    
                    # Generuj nazwę pliku
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    filename = f"wise_invoice_{i+1}_{timestamp}.pdf"
                    
                    # Zapisz plik
                    output_path = output_dir / filename
                    download.save_as(output_path)
                    
                    logger.success(f"Pobrano fakturę: {output_path}")
                    downloaded_files.append(output_path)
                    
                    # Krótka pauza między pobieraniami
                    time.sleep(1)
                
                except Exception as e:
                    logger.error(f"Błąd podczas pobierania faktury {i+1}: {e}")
        
        except Exception as e:
            logger.error(f"Błąd podczas pobierania faktur: {e}")
        
        return downloaded_files
