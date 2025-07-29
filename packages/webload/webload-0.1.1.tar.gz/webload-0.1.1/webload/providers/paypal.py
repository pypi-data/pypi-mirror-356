"""
Dostawca PayPal - pobieranie wyciągów i faktur.
"""

import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from loguru import logger
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from webload.providers.base import BaseProvider


class PayPalProvider(BaseProvider):
    """Dostawca PayPal - pobieranie wyciągów i faktur."""
    
    def __init__(self, credentials: Dict[str, Any]):
        """
        Inicjalizacja dostawcy PayPal.
        
        Args:
            credentials: Dane uwierzytelniające
        """
        super().__init__("PayPal", credentials)
    
    @property
    def required_credentials(self) -> List[str]:
        """Lista wymaganych danych uwierzytelniających."""
        return ["email", "password"]
    
    @property
    def base_url(self) -> str:
        """Bazowy URL dostawcy."""
        return "https://www.paypal.com"
    
    def login(self) -> bool:
        """
        Logowanie do serwisu PayPal.
        
        Returns:
            True, jeśli logowanie się powiodło, False w przeciwnym razie
        """
        try:
            logger.info("Logowanie do PayPal...")
            
            # Przejdź do strony logowania
            self.page.goto(f"{self.base_url}/signin")
            
            # Poczekaj na załadowanie formularza logowania
            self.page.wait_for_selector('#email')
            
            # Wprowadź email
            self.page.fill('#email', self.credentials["email"])
            
            # Kliknij przycisk "Next"
            next_button = self.page.query_selector('button#btnNext')
            if next_button:
                next_button.click()
                
                # Poczekaj na pole hasła
                self.page.wait_for_selector('#password')
            
            # Wprowadź hasło
            self.page.fill('#password', self.credentials["password"])
            
            # Kliknij przycisk "Login"
            self.page.click('#btnLogin')
            
            # Sprawdź, czy logowanie się powiodło (czekaj na dashboard)
            try:
                self.page.wait_for_selector('.dashboard, .paypal-dashboard', timeout=30000)
                logger.success("Zalogowano do PayPal")
                return True
            except PlaywrightTimeoutError:
                # Sprawdź, czy jest wymagane dodatkowe uwierzytelnianie
                if self.page.query_selector('.captcha, .twoFactorAuth'):
                    logger.error("Wymagane dodatkowe uwierzytelnianie. Zaloguj się ręcznie i spróbuj ponownie.")
                else:
                    logger.error("Nie udało się zalogować do PayPal. Sprawdź dane uwierzytelniające.")
                return False
                
        except Exception as e:
            logger.error(f"Błąd podczas logowania do PayPal: {e}")
            return False
    
    def download_documents(self, year: int, month: int) -> List[Path]:
        """
        Pobiera wyciągi i faktury z PayPal dla określonego miesiąca i roku.
        
        Args:
            year: Rok
            month: Miesiąc
            
        Returns:
            Lista ścieżek do pobranych plików
        """
        downloaded_files = []
        
        try:
            # Przejdź do strony wyciągów
            logger.info(f"Pobieranie wyciągów PayPal za {month:02d}/{year}...")
            self.page.goto(f"{self.base_url}/reports/accountStatements")
            
            # Poczekaj na załadowanie strony
            self.page.wait_for_selector('.statements-page, #statementTypeContainer')
            
            # Wybierz typ wyciągu (miesięczny)
            self._select_monthly_statement()
            
            # Wybierz rok i miesiąc
            self._select_statement_period(year, month)
            
            # Pobierz wyciągi
            statement_files = self._download_statements()
            downloaded_files.extend(statement_files)
            
            # Przejdź do strony aktywności (transakcji)
            logger.info(f"Pobieranie historii transakcji PayPal za {month:02d}/{year}...")
            self.page.goto(f"{self.base_url}/activities")
            
            # Poczekaj na załadowanie strony
            self.page.wait_for_selector('.activity-tab, #transactionList')
            
            # Wybierz zakres dat
            self._select_activity_date_range(year, month)
            
            # Pobierz raport CSV
            csv_files = self._download_activity_report(year, month)
            downloaded_files.extend(csv_files)
            
        except Exception as e:
            logger.error(f"Błąd podczas pobierania dokumentów z PayPal: {e}")
        
        return downloaded_files
    
    def _select_monthly_statement(self) -> None:
        """
        Wybiera typ wyciągu miesięcznego.
        """
        try:
            # Kliknij selektor typu wyciągu
            statement_type_selector = self.page.query_selector('#statementTypeSelector, select[name="statementType"]')
            if statement_type_selector:
                statement_type_selector.click()
                time.sleep(1)
                
                # Wybierz opcję "Monthly"
                monthly_option = self.page.query_selector('option[value="MONTHLY"]')
                if monthly_option:
                    monthly_option.click()
                    time.sleep(2)  # Poczekaj na odświeżenie
        except Exception as e:
            logger.error(f"Błąd podczas wybierania typu wyciągu: {e}")
    
    def _select_statement_period(self, year: int, month: int) -> None:
        """
        Wybiera okres wyciągu.
        
        Args:
            year: Rok
            month: Miesiąc
        """
        try:
            # Kliknij selektor okresu
            period_selector = self.page.query_selector('#statementPeriodSelector, select[name="statementPeriod"]')
            if period_selector:
                period_selector.click()
                time.sleep(1)
                
                # Znajdź i wybierz odpowiedni okres (format: "MMM YYYY")
                month_name = datetime(year, month, 1).strftime("%b")
                period_value = f"{month_name} {year}"
                
                period_option = self.page.query_selector(f'option[value*="{period_value}"], option:text("{period_value}")')
                if period_option:
                    period_option.click()
                    time.sleep(2)  # Poczekaj na odświeżenie
                else:
                    logger.warning(f"Nie znaleziono okresu {period_value}")
        except Exception as e:
            logger.error(f"Błąd podczas wybierania okresu wyciągu: {e}")
    
    def _download_statements(self) -> List[Path]:
        """
        Pobiera wyciągi z aktualnie wyświetlonej strony.
        
        Returns:
            Lista ścieżek do pobranych plików
        """
        downloaded_files = []
        
        try:
            # Znajdź przycisk pobierania PDF
            download_button = self.page.query_selector('button[data-test-id="download-pdf-button"], .downloadPDF')
            
            if not download_button:
                logger.info("Nie znaleziono przycisku pobierania wyciągu")
                return []
            
            # Przygotuj katalog wyjściowy
            output_dir = self.get_output_directory(year=int(self.page.url.split("=")[-1].split("-")[0]),
                                                 month=int(self.page.url.split("=")[-1].split("-")[1]))
            
            # Kliknij przycisk pobierania
            with self.page.expect_download() as download_info:
                download_button.click()
            
            # Pobierz plik
            download = download_info.value
            
            # Generuj nazwę pliku
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"paypal_statement_{timestamp}.pdf"
            
            # Zapisz plik
            output_path = output_dir / filename
            download.save_as(output_path)
            
            logger.success(f"Pobrano wyciąg: {output_path}")
            downloaded_files.append(output_path)
            
        except Exception as e:
            logger.error(f"Błąd podczas pobierania wyciągu: {e}")
        
        return downloaded_files
    
    def _select_activity_date_range(self, year: int, month: int) -> None:
        """
        Wybiera zakres dat dla historii aktywności.
        
        Args:
            year: Rok
            month: Miesiąc
        """
        try:
            # Kliknij selektor zakresu dat
            date_range_selector = self.page.query_selector('.dateFilterSelector, button[data-test-id="date-filter"]')
            if date_range_selector:
                date_range_selector.click()
                time.sleep(1)
                
                # Wybierz opcję "Custom"
                custom_option = self.page.query_selector('li[data-test-id="custom-date-filter"], .customDateOption')
                if custom_option:
                    custom_option.click()
                    time.sleep(1)
                
                # Ustaw datę początkową (pierwszy dzień miesiąca)
                start_date_input = self.page.query_selector('input[name="startDate"], #startDate')
                if start_date_input:
                    start_date_input.fill(f"{month:02d}/01/{year}")
                
                # Ustaw datę końcową (ostatni dzień miesiąca)
                end_date = datetime(year, month % 12 + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
                end_date = end_date.replace(day=1) - datetime.timedelta(days=1)
                
                end_date_input = self.page.query_selector('input[name="endDate"], #endDate')
                if end_date_input:
                    end_date_input.fill(f"{end_date.month:02d}/{end_date.day:02d}/{end_date.year}")
                
                # Zatwierdź wybór
                apply_button = self.page.query_selector('button[data-test-id="apply-date-filter"], .applyDateFilter')
                if apply_button:
                    apply_button.click()
                    time.sleep(3)  # Poczekaj na odświeżenie listy
        
        except Exception as e:
            logger.error(f"Błąd podczas wybierania zakresu dat: {e}")
    
    def _download_activity_report(self, year: int, month: int) -> List[Path]:
        """
        Pobiera raport aktywności w formacie CSV.
        
        Args:
            year: Rok
            month: Miesiąc
            
        Returns:
            Lista ścieżek do pobranych plików
        """
        downloaded_files = []
        
        try:
            # Kliknij przycisk "Download"
            download_dropdown = self.page.query_selector('button[data-test-id="download-dropdown"], .downloadButton')
            if download_dropdown:
                download_dropdown.click()
                time.sleep(1)
                
                # Wybierz opcję "CSV"
                csv_option = self.page.query_selector('li[data-test-id="csv-download"], .csvOption')
                if csv_option:
                    # Przygotuj katalog wyjściowy
                    output_dir = self.get_output_directory(year, month)
                    
                    # Kliknij opcję CSV i oczekuj na pobranie
                    with self.page.expect_download() as download_info:
                        csv_option.click()
                    
                    # Pobierz plik
                    download = download_info.value
                    
                    # Generuj nazwę pliku
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    filename = f"paypal_activity_{year}_{month:02d}_{timestamp}.csv"
                    
                    # Zapisz plik
                    output_path = output_dir / filename
                    download.save_as(output_path)
                    
                    logger.success(f"Pobrano raport aktywności: {output_path}")
                    downloaded_files.append(output_path)
                else:
                    logger.warning("Nie znaleziono opcji pobierania CSV")
            else:
                logger.warning("Nie znaleziono przycisku pobierania")
        
        except Exception as e:
            logger.error(f"Błąd podczas pobierania raportu aktywności: {e}")
        
        return downloaded_files
