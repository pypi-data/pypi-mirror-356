"""
Bazowa klasa dla wszystkich dostawców.
"""

import os
import time
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from loguru import logger
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext

from webload.config import settings, get_output_path


class BaseProvider(ABC):
    """Bazowa klasa dla wszystkich dostawców."""
    
    def __init__(self, name: str, credentials: Dict[str, Any]):
        """
        Inicjalizacja dostawcy.
        
        Args:
            name: Nazwa dostawcy
            credentials: Dane uwierzytelniające
        """
        self.name = name
        self.credentials = credentials
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        # Sprawdź, czy dostawca ma skonfigurowane dane uwierzytelniające
        if not self._validate_credentials():
            logger.warning(f"Dostawca {self.name} nie ma skonfigurowanych wszystkich wymaganych danych uwierzytelniających")
    
    @property
    @abstractmethod
    def required_credentials(self) -> List[str]:
        """Lista wymaganych danych uwierzytelniających."""
        pass
    
    @property
    @abstractmethod
    def base_url(self) -> str:
        """Bazowy URL dostawcy."""
        pass
    
    def _validate_credentials(self) -> bool:
        """
        Sprawdza, czy wszystkie wymagane dane uwierzytelniające są dostępne.
        
        Returns:
            True, jeśli wszystkie wymagane dane są dostępne, False w przeciwnym razie
        """
        for cred in self.required_credentials:
            if cred not in self.credentials or not self.credentials[cred]:
                logger.error(f"Brak wymaganego poświadczenia '{cred}' dla dostawcy {self.name}")
                return False
        return True
    
    def setup_browser(self) -> None:
        """
        Konfiguruje przeglądarkę i kontekst.
        """
        try:
            playwright = sync_playwright().start()
            
            # Wybierz typ przeglądarki
            if settings.BROWSER_TYPE == "firefox":
                self.browser = playwright.firefox.launch(headless=settings.HEADLESS)
            elif settings.BROWSER_TYPE == "webkit":
                self.browser = playwright.webkit.launch(headless=settings.HEADLESS)
            else:
                self.browser = playwright.chromium.launch(headless=settings.HEADLESS)
            
            # Konfiguracja kontekstu przeglądarki
            context_options = {
                "user_agent": settings.USER_AGENT,
                "viewport": {"width": 1920, "height": 1080},
                "ignore_https_errors": True,
                "accept_downloads": True
            }
            
            # Dodaj konfigurację proxy, jeśli jest włączona
            if settings.USE_PROXY and settings.PROXY_HOST and settings.PROXY_PORT:
                proxy_config = {
                    "server": f"{settings.PROXY_HOST}:{settings.PROXY_PORT}"
                }
                
                if settings.PROXY_USERNAME and settings.PROXY_PASSWORD:
                    proxy_config["username"] = settings.PROXY_USERNAME
                    proxy_config["password"] = settings.PROXY_PASSWORD
                
                context_options["proxy"] = proxy_config
            
            self.context = self.browser.new_context(**context_options)
            self.page = self.context.new_page()
            
            # Ustawienie timeoutów
            self.page.set_default_timeout(30000)  # 30 sekund
            self.page.set_default_navigation_timeout(60000)  # 60 sekund
            
            logger.info(f"Przeglądarka skonfigurowana dla dostawcy {self.name}")
        except Exception as e:
            logger.error(f"Błąd podczas konfiguracji przeglądarki dla dostawcy {self.name}: {e}")
            self.cleanup()
            raise
    
    def cleanup(self) -> None:
        """
        Zamyka przeglądarkę i zwalnia zasoby.
        """
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            logger.info(f"Przeglądarka zamknięta dla dostawcy {self.name}")
        except Exception as e:
            logger.error(f"Błąd podczas zamykania przeglądarki dla dostawcy {self.name}: {e}")
    
    @abstractmethod
    def login(self) -> bool:
        """
        Logowanie do serwisu dostawcy.
        
        Returns:
            True, jeśli logowanie się powiodło, False w przeciwnym razie
        """
        pass
    
    @abstractmethod
    def download_documents(self, year: int, month: int) -> List[Path]:
        """
        Pobiera dokumenty dla określonego miesiąca i roku.
        
        Args:
            year: Rok
            month: Miesiąc
            
        Returns:
            Lista ścieżek do pobranych plików
        """
        pass
    
    def run(self, year: int, month: int) -> Tuple[int, int]:
        """
        Uruchamia proces pobierania dokumentów.
        
        Args:
            year: Rok
            month: Miesiąc
            
        Returns:
            Krotka (liczba_sukcesów, liczba_błędów)
        """
        if not self._validate_credentials():
            return 0, 0
        
        success_count = 0
        error_count = 0
        
        try:
            # Konfiguracja przeglądarki
            self.setup_browser()
            
            # Logowanie
            if not self.login():
                logger.error(f"Nie udało się zalogować do {self.name}")
                return 0, 1
            
            # Pobieranie dokumentów
            downloaded_files = self.download_documents(year, month)
            
            success_count = len(downloaded_files)
            if success_count > 0:
                logger.success(f"Pobrano {success_count} plików od dostawcy {self.name} za {month:02d}/{year}")
            else:
                logger.info(f"Nie znaleziono plików do pobrania od dostawcy {self.name} za {month:02d}/{year}")
        
        except Exception as e:
            logger.error(f"Błąd podczas pobierania dokumentów od dostawcy {self.name}: {e}")
            error_count = 1
        
        finally:
            # Zamknięcie przeglądarki
            self.cleanup()
        
        return success_count, error_count
    
    def wait_for_download(self, timeout: int = None) -> None:
        """
        Czeka określony czas, aby umożliwić zakończenie pobierania.
        
        Args:
            timeout: Czas oczekiwania w sekundach
        """
        if timeout is None:
            timeout = settings.DOWNLOAD_TIMEOUT
        
        logger.info(f"Oczekiwanie {timeout} sekund na zakończenie pobierania...")
        time.sleep(timeout)
    
    def get_output_directory(self, year: int, month: int) -> Path:
        """
        Zwraca ścieżkę do katalogu wyjściowego dla pobranych plików.
        
        Args:
            year: Rok
            month: Miesiąc
            
        Returns:
            Ścieżka do katalogu wyjściowego
        """
        return get_output_path(year, month, self.name.lower())
    
    def save_html_to_pdf(self, html_content: str, output_path: Path) -> bool:
        """
        Zapisuje zawartość HTML do pliku PDF.
        
        Args:
            html_content: Zawartość HTML
            output_path: Ścieżka do pliku wyjściowego
            
        Returns:
            True, jeśli operacja się powiodła, False w przeciwnym razie
        """
        try:
            # Utwórz nową stronę
            temp_page = self.context.new_page()
            
            # Ustaw zawartość HTML
            temp_page.set_content(html_content)
            
            # Zapisz jako PDF
            temp_page.pdf(path=str(output_path))
            
            # Zamknij stronę
            temp_page.close()
            
            logger.info(f"Zapisano HTML do PDF: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Błąd podczas zapisywania HTML do PDF: {e}")
            return False
