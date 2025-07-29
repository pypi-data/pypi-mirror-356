"""
Dostawca Aftermarket - pobieranie faktur i historii transakcji.
"""

import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from loguru import logger
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from webload.providers.base import BaseProvider


class AftermarketProvider(BaseProvider):
    """Dostawca Aftermarket - pobieranie faktur i historii transakcji."""
    
    def __init__(self, credentials: Dict[str, Any]):
        """
        Inicjalizacja dostawcy Aftermarket.
        
        Args:
            credentials: Dane uwierzytelniające
        """
        super().__init__("Aftermarket", credentials)
    
    @property
    def required_credentials(self) -> List[str]:
        """Lista wymaganych danych uwierzytelniających."""
        return ["username", "password"]
    
    @property
    def base_url(self) -> str:
        """Bazowy URL dostawcy."""
        return "https://www.aftermarket.pl"
    
    def login(self) -> bool:
        """
        Logowanie do serwisu Aftermarket.
        
        Returns:
            True, jeśli logowanie się powiodło, False w przeciwnym razie
        """
        try:
            logger.info("Logowanie do Aftermarket...")
            
            # Przejdź do strony logowania
            self.page.goto(f"{self.base_url}/login")
            
            # Poczekaj na załadowanie formularza logowania
            self.page.wait_for_selector('#username')
            
            # Wprowadź nazwę użytkownika
            self.page.fill('#username', self.credentials["username"])
            
            # Wprowadź hasło
            self.page.fill('#password', self.credentials["password"])
            
            # Kliknij przycisk "Zaloguj"
            self.page.click('button[type="submit"]')
            
            # Sprawdź, czy logowanie się powiodło (czekaj na dashboard)
            try:
                self.page.wait_for_selector('.user-menu, .account-menu', timeout=30000)
                logger.success("Zalogowano do Aftermarket")
                return True
            except PlaywrightTimeoutError:
                # Sprawdź, czy jest komunikat o błędzie
                error_message = self.page.query_selector('.alert-danger, .error-message')
                if error_message:
                    logger.error(f"Błąd logowania: {error_message.inner_text()}")
                else:
                    logger.error("Nie udało się zalogować do Aftermarket. Sprawdź dane uwierzytelniające.")
                return False
                
        except Exception as e:
            logger.error(f"Błąd podczas logowania do Aftermarket: {e}")
            return False
    
    def download_documents(self, year: int, month: int) -> List[Path]:
        """
        Pobiera faktury z Aftermarket dla określonego miesiąca i roku.
        
        Args:
            year: Rok
            month: Miesiąc
            
        Returns:
            Lista ścieżek do pobranych plików
        """
        downloaded_files = []
        
        try:
            # Przejdź do strony faktur
            logger.info(f"Pobieranie faktur Aftermarket za {month:02d}/{year}...")
            self.page.goto(f"{self.base_url}/account/invoices")
            
            # Poczekaj na załadowanie strony
            self.page.wait_for_selector('.invoices-list, table.invoices')
            
            # Filtruj faktury według daty (jeśli dostępne)
            self._filter_invoices_by_date(year, month)
            
            # Znajdź faktury z wybranego miesiąca i roku
            invoice_rows = self._find_invoices_for_period(year, month)
            
            if not invoice_rows:
                logger.info(f"Nie znaleziono faktur Aftermarket za {month:02d}/{year}")
                return []
            
            logger.info(f"Znaleziono {len(invoice_rows)} faktur Aftermarket za {month:02d}/{year}")
            
            # Przygotuj katalog wyjściowy
            output_dir = self.get_output_directory(year, month)
            
            # Pobierz każdą fakturę
            for i, row in enumerate(invoice_rows):
                try:
                    # Znajdź przycisk pobierania PDF
                    download_button = row.query_selector('a[href*="pdf"], a[href*="download"], a:has-text("Pobierz")')
                    
                    if not download_button:
                        logger.warning(f"Nie znaleziono przycisku pobierania dla faktury {i+1}")
                        continue
                    
                    # Pobierz identyfikator faktury (jeśli dostępny)
                    invoice_id = self._extract_invoice_id(row)
                    
                    # Kliknij przycisk pobierania
                    with self.page.expect_download() as download_info:
                        download_button.click()
                    
                    # Pobierz plik
                    download = download_info.value
                    
                    # Generuj nazwę pliku
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    filename = f"aftermarket_invoice_{invoice_id}_{timestamp}.pdf" if invoice_id else f"aftermarket_invoice_{i+1}_{timestamp}.pdf"
                    
                    # Zapisz plik
                    output_path = output_dir / filename
                    download.save_as(output_path)
                    
                    logger.success(f"Pobrano fakturę: {output_path}")
                    downloaded_files.append(output_path)
                    
                    # Krótka pauza między pobieraniami
                    time.sleep(1)
                
                except Exception as e:
                    logger.error(f"Błąd podczas pobierania faktury {i+1}: {e}")
            
            # Pobierz historię transakcji (jeśli dostępna)
            transaction_files = self._download_transaction_history(year, month)
            downloaded_files.extend(transaction_files)
            
        except Exception as e:
            logger.error(f"Błąd podczas pobierania dokumentów z Aftermarket: {e}")
        
        return downloaded_files
    
    def _filter_invoices_by_date(self, year: int, month: int) -> None:
        """
        Filtruje faktury według daty (jeśli dostępne).
        
        Args:
            year: Rok
            month: Miesiąc
        """
        try:
            # Sprawdź, czy istnieje filtr dat
            date_filter = self.page.query_selector('.date-filter, #date-filter')
            
            if date_filter:
                # Kliknij filtr dat
                date_filter.click()
                time.sleep(1)
                
                # Ustaw datę początkową (pierwszy dzień miesiąca)
                start_date_input = self.page.query_selector('input[name="start_date"], #start-date')
                if start_date_input:
                    start_date_input.fill(f"{year}-{month:02d}-01")
                
                # Ustaw datę końcową (ostatni dzień miesiąca)
                # Oblicz ostatni dzień miesiąca
                if month == 12:
                    next_month = 1
                    next_year = year + 1
                else:
                    next_month = month + 1
                    next_year = year
                
                end_date = f"{year}-{month:02d}-28"  # Bezpieczna wartość dla wszystkich miesięcy
                
                end_date_input = self.page.query_selector('input[name="end_date"], #end-date')
                if end_date_input:
                    end_date_input.fill(end_date)
                
                # Zatwierdź filtr
                apply_button = self.page.query_selector('button[type="submit"], .apply-filter')
                if apply_button:
                    apply_button.click()
                    time.sleep(2)  # Poczekaj na odświeżenie listy
        
        except Exception as e:
            logger.error(f"Błąd podczas filtrowania faktur: {e}")
    
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
            rows = self.page.query_selector_all('table tr:not(:first-child), .invoice-item')
            
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
                "%Y-%m-%d",   # "2024-01-15"
                "%d.%m.%Y",   # "15.01.2024"
                "%d-%m-%Y",   # "15-01-2024"
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
            # spróbuj wyciągnąć datę za pomocą wyrażenia regularnego
            date_pattern = r'(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})'
            match = re.search(date_pattern, date_text)
            
            if match:
                day, extracted_month, extracted_year = map(int, match.groups())
                return extracted_year == year and extracted_month == month
            
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
            id_cell = row.query_selector('td:nth-child(2), .invoice-number')
            
            if id_cell:
                return id_cell.inner_text().strip()
            
            # Alternatywnie, spróbuj pobrać identyfikator z atrybutu data-*
            data_id = row.get_attribute('data-invoice-id') or row.get_attribute('data-id')
            
            if data_id:
                return data_id
            
            return None
        
        except Exception:
            return None
    
    def _download_transaction_history(self, year: int, month: int) -> List[Path]:
        """
        Pobiera historię transakcji w formacie CSV/PDF.
        
        Args:
            year: Rok
            month: Miesiąc
            
        Returns:
            Lista ścieżek do pobranych plików
        """
        downloaded_files = []
        
        try:
            # Przejdź do strony historii transakcji
            logger.info(f"Pobieranie historii transakcji Aftermarket za {month:02d}/{year}...")
            self.page.goto(f"{self.base_url}/account/transactions")
            
            # Poczekaj na załadowanie strony
            self.page.wait_for_selector('.transactions-list, table.transactions')
            
            # Filtruj transakcje według daty
            self._filter_transactions_by_date(year, month)
            
            # Sprawdź, czy istnieje przycisk eksportu
            export_button = self.page.query_selector('a[href*="export"], button.export, button:has-text("Eksport")')
            
            if not export_button:
                logger.info("Nie znaleziono przycisku eksportu historii transakcji")
                return []
            
            # Przygotuj katalog wyjściowy
            output_dir = self.get_output_directory(year, month)
            
            # Kliknij przycisk eksportu
            export_button.click()
            time.sleep(1)
            
            # Sprawdź, czy pojawiło się menu z opcjami eksportu
            csv_option = self.page.query_selector('a[href*="csv"], button:has-text("CSV")')
            pdf_option = self.page.query_selector('a[href*="pdf"], button:has-text("PDF")')
            
            # Pobierz w formacie CSV (jeśli dostępne)
            if csv_option:
                with self.page.expect_download() as download_info:
                    csv_option.click()
                
                # Pobierz plik
                download = download_info.value
                
                # Generuj nazwę pliku
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"aftermarket_transactions_{year}_{month:02d}_{timestamp}.csv"
                
                # Zapisz plik
                output_path = output_dir / filename
                download.save_as(output_path)
                
                logger.success(f"Pobrano historię transakcji CSV: {output_path}")
                downloaded_files.append(output_path)
            
            # Pobierz w formacie PDF (jeśli dostępne)
            if pdf_option:
                with self.page.expect_download() as download_info:
                    pdf_option.click()
                
                # Pobierz plik
                download = download_info.value
                
                # Generuj nazwę pliku
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"aftermarket_transactions_{year}_{month:02d}_{timestamp}.pdf"
                
                # Zapisz plik
                output_path = output_dir / filename
                download.save_as(output_path)
                
                logger.success(f"Pobrano historię transakcji PDF: {output_path}")
                downloaded_files.append(output_path)
        
        except Exception as e:
            logger.error(f"Błąd podczas pobierania historii transakcji: {e}")
        
        return downloaded_files
    
    def _filter_transactions_by_date(self, year: int, month: int) -> None:
        """
        Filtruje transakcje według daty.
        
        Args:
            year: Rok
            month: Miesiąc
        """
        try:
            # Sprawdź, czy istnieje filtr dat
            date_filter = self.page.query_selector('.date-filter, #date-filter')
            
            if date_filter:
                # Kliknij filtr dat
                date_filter.click()
                time.sleep(1)
                
                # Ustaw datę początkową (pierwszy dzień miesiąca)
                start_date_input = self.page.query_selector('input[name="start_date"], #start-date')
                if start_date_input:
                    start_date_input.fill(f"{year}-{month:02d}-01")
                
                # Ustaw datę końcową (ostatni dzień miesiąca)
                # Oblicz ostatni dzień miesiąca
                if month == 12:
                    next_month = 1
                    next_year = year + 1
                else:
                    next_month = month + 1
                    next_year = year
                
                end_date = f"{year}-{month:02d}-28"  # Bezpieczna wartość dla wszystkich miesięcy
                
                end_date_input = self.page.query_selector('input[name="end_date"], #end-date')
                if end_date_input:
                    end_date_input.fill(end_date)
                
                # Zatwierdź filtr
                apply_button = self.page.query_selector('button[type="submit"], .apply-filter')
                if apply_button:
                    apply_button.click()
                    time.sleep(2)  # Poczekaj na odświeżenie listy
        
        except Exception as e:
            logger.error(f"Błąd podczas filtrowania transakcji: {e}")
