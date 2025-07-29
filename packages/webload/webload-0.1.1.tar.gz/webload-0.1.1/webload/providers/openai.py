"""
Dostawca OpenAI - pobieranie faktur i historii płatności.
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from loguru import logger
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from webload.providers.base import BaseProvider


class OpenAIProvider(BaseProvider):
    """Dostawca OpenAI - pobieranie faktur i historii płatności."""
    
    def __init__(self, credentials: Dict[str, Any]):
        """
        Inicjalizacja dostawcy OpenAI.
        
        Args:
            credentials: Dane uwierzytelniające
        """
        super().__init__("OpenAI", credentials)
    
    @property
    def required_credentials(self) -> List[str]:
        """Lista wymaganych danych uwierzytelniających."""
        return ["email", "password"]
    
    @property
    def base_url(self) -> str:
        """Bazowy URL dostawcy."""
        return "https://platform.openai.com"
    
    def login(self) -> bool:
        """
        Logowanie do serwisu OpenAI.
        
        Returns:
            True, jeśli logowanie się powiodło, False w przeciwnym razie
        """
        try:
            logger.info("Logowanie do OpenAI...")
            
            # Przejdź do strony logowania
            self.page.goto(f"{self.base_url}/login")
            
            # Poczekaj na załadowanie formularza logowania
            self.page.wait_for_selector('input[name="username"]')
            
            # Wprowadź email
            self.page.fill('input[name="username"]', self.credentials["email"])
            
            # Kliknij przycisk "Continue"
            self.page.click('button[type="submit"]')
            
            # Poczekaj na pole hasła
            self.page.wait_for_selector('input[name="password"]')
            
            # Wprowadź hasło
            self.page.fill('input[name="password"]', self.credentials["password"])
            
            # Kliknij przycisk "Continue"
            self.page.click('button[type="submit"]')
            
            # Sprawdź, czy logowanie się powiodło (czekaj na dashboard)
            try:
                self.page.wait_for_selector('.dashboard, .org-dashboard', timeout=30000)
                logger.success("Zalogowano do OpenAI")
                return True
            except PlaywrightTimeoutError:
                # Sprawdź, czy jest wymagane dodatkowe uwierzytelnianie
                if self.page.query_selector('.mfa-prompt'):
                    logger.error("Wymagane uwierzytelnianie dwuetapowe. Zaloguj się ręcznie i spróbuj ponownie.")
                else:
                    logger.error("Nie udało się zalogować do OpenAI. Sprawdź dane uwierzytelniające.")
                return False
                
        except Exception as e:
            logger.error(f"Błąd podczas logowania do OpenAI: {e}")
            return False
    
    def download_documents(self, year: int, month: int) -> List[Path]:
        """
        Pobiera faktury z OpenAI dla określonego miesiąca i roku.
        
        Args:
            year: Rok
            month: Miesiąc
            
        Returns:
            Lista ścieżek do pobranych plików
        """
        downloaded_files = []
        
        try:
            # Przejdź do strony historii płatności
            logger.info(f"Pobieranie faktur OpenAI za {month:02d}/{year}...")
            self.page.goto(f"{self.base_url}/billing/usage")
            
            # Poczekaj na załadowanie strony
            self.page.wait_for_selector('.usage-page, .billing-page')
            
            # Przejdź do zakładki historii płatności
            payment_history_tab = self.page.query_selector('a[href*="payment-history"], a:text("Payment history")')
            if payment_history_tab:
                payment_history_tab.click()
                time.sleep(2)
            else:
                # Spróbuj bezpośrednio przejść do strony historii płatności
                self.page.goto(f"{self.base_url}/billing/payment-history")
                self.page.wait_for_selector('.payment-history-page, .billing-history')
            
            # Poczekaj na załadowanie tabeli faktur
            self.page.wait_for_selector('table.billing-history-table, .invoice-list')
            
            # Znajdź faktury z wybranego miesiąca i roku
            invoice_rows = self._find_invoices_for_period(year, month)
            
            if not invoice_rows:
                logger.info(f"Nie znaleziono faktur OpenAI za {month:02d}/{year}")
                return []
            
            logger.info(f"Znaleziono {len(invoice_rows)} faktur OpenAI za {month:02d}/{year}")
            
            # Przygotuj katalog wyjściowy
            output_dir = self.get_output_directory(year, month)
            
            # Pobierz każdą fakturę
            for i, row in enumerate(invoice_rows):
                try:
                    # Znajdź przycisk pobierania PDF
                    download_button = row.query_selector('a[href*="pdf"], button:has-text("Download"), a:has-text("PDF")')
                    
                    if not download_button:
                        logger.warning(f"Nie znaleziono przycisku pobierania dla faktury {i+1}")
                        continue
                    
                    # Kliknij przycisk pobierania
                    with self.page.expect_download() as download_info:
                        download_button.click()
                    
                    # Pobierz plik
                    download = download_info.value
                    
                    # Pobierz identyfikator faktury (jeśli dostępny)
                    invoice_id = self._extract_invoice_id(row)
                    
                    # Generuj nazwę pliku
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    filename = f"openai_invoice_{invoice_id}_{timestamp}.pdf" if invoice_id else f"openai_invoice_{i+1}_{timestamp}.pdf"
                    
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
            logger.error(f"Błąd podczas pobierania faktur z OpenAI: {e}")
        
        return downloaded_files
    
    def _find_invoices_for_period(self, year: int, month: int) -> List[Any]:
        """
        Znajduje wiersze tabeli z fakturami dla określonego miesiąca i roku.
        
        Args:
            year: Rok
            month: Miesiąc
            
        Returns:
            Lista elementów DOM reprezentujących wiersze z fakturami
        """
        matching_rows = []
        
        try:
            # Znajdź wszystkie wiersze tabeli
            rows = self.page.query_selector_all('table tr, .invoice-item')
            
            # Dla każdego wiersza sprawdź datę
            for row in rows:
                # Pobierz tekst daty (format może się różnić)
                date_cell = row.query_selector('td:nth-child(1), .invoice-date')
                
                if not date_cell:
                    continue
                
                date_text = date_cell.inner_text()
                
                # Sprawdź, czy data zawiera szukany miesiąc i rok
                if self._is_date_matching(date_text, year, month):
                    matching_rows.append(row)
        
        except Exception as e:
            logger.error(f"Błąd podczas wyszukiwania faktur: {e}")
        
        return matching_rows
    
    def _is_date_matching(self, date_text: str, year: int, month: int) -> bool:
        """
        Sprawdza, czy tekst daty zawiera określony miesiąc i rok.
        
        Args:
            date_text: Tekst daty
            year: Rok
            month: Miesiąc
            
        Returns:
            True, jeśli data pasuje do określonego miesiąca i roku
        """
        try:
            # Różne formaty dat
            date_formats = [
                "%b %d, %Y",  # "Jan 15, 2024"
                "%B %d, %Y",  # "January 15, 2024"
                "%d %b %Y",   # "15 Jan 2024"
                "%d %B %Y",   # "15 January 2024"
                "%Y-%m-%d",   # "2024-01-15"
                "%m/%d/%Y",   # "01/15/2024"
                "%d/%m/%Y",   # "15/01/2024"
            ]
            
            # Próbuj parsować datę w różnych formatach
            for date_format in date_formats:
                try:
                    date = datetime.strptime(date_text.strip(), date_format)
                    return date.year == year and date.month == month
                except ValueError:
                    continue
            
            # Jeśli nie udało się sparsować w standardowych formatach,
            # sprawdź, czy tekst zawiera nazwę miesiąca i rok
            month_names = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
            
            month_abbrs = [
                "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
            ]
            
            # Sprawdź, czy tekst zawiera rok
            if str(year) in date_text:
                # Sprawdź, czy tekst zawiera nazwę miesiąca
                if month_names[month-1] in date_text or month_abbrs[month-1] in date_text:
                    return True
            
            return False
        
        except Exception:
            return False
    
    def _extract_invoice_id(self, row: Any) -> Optional[str]:
        """
        Wyciąga identyfikator faktury z wiersza tabeli.
        
        Args:
            row: Element DOM reprezentujący wiersz tabeli
            
        Returns:
            Identyfikator faktury lub None, jeśli nie znaleziono
        """
        try:
            # Spróbuj znaleźć komórkę z identyfikatorem
            id_cell = row.query_selector('td:nth-child(2), .invoice-id')
            
            if id_cell:
                return id_cell.inner_text().strip()
            
            # Alternatywnie, spróbuj pobrać identyfikator z atrybutu data-*
            data_id = row.get_attribute('data-invoice-id') or row.get_attribute('data-id')
            
            if data_id:
                return data_id
            
            return None
        
        except Exception:
            return None
