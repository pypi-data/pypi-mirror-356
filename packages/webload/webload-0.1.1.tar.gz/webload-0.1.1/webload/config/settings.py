"""
Moduł konfiguracyjny dla biblioteki webload.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, List

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

# Załadowanie zmiennych środowiskowych z pliku .env
load_dotenv()

class Settings(BaseSettings):
    """Główne ustawienia aplikacji."""
    
    # Konfiguracja ogólna
    OUTPUT_DIR: str = Field(default="./downloads", description="Katalog wyjściowy na pobrane pliki")
    HEADLESS: bool = Field(default=True, description="Czy uruchamiać przeglądarkę w trybie headless")
    DOWNLOAD_TIMEOUT: int = Field(default=60, description="Timeout pobierania plików w sekundach")
    LOG_LEVEL: str = Field(default="INFO", description="Poziom logowania")
    
    # Konfiguracja przeglądarki
    BROWSER_TYPE: str = Field(default="chromium", description="Typ przeglądarki: chromium, firefox, webkit")
    USER_AGENT: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        description="User-Agent przeglądarki"
    )
    
    # Konfiguracja proxy
    USE_PROXY: bool = Field(default=False, description="Czy używać proxy")
    PROXY_HOST: Optional[str] = Field(default=None, description="Host proxy")
    PROXY_PORT: Optional[int] = Field(default=None, description="Port proxy")
    PROXY_USERNAME: Optional[str] = Field(default=None, description="Nazwa użytkownika proxy")
    PROXY_PASSWORD: Optional[str] = Field(default=None, description="Hasło proxy")
    
    # Dane uwierzytelniające dla poszczególnych dostawców
    # Wise
    WISE_EMAIL: Optional[str] = None
    WISE_PASSWORD: Optional[str] = None
    WISE_API_KEY: Optional[str] = None
    WISE_API_SECRET: Optional[str] = None
    
    # PayPal
    PAYPAL_EMAIL: Optional[str] = None
    PAYPAL_PASSWORD: Optional[str] = None
    PAYPAL_CLIENT_ID: Optional[str] = None
    PAYPAL_CLIENT_SECRET: Optional[str] = None
    
    # SAV
    SAV_USERNAME: Optional[str] = None
    SAV_PASSWORD: Optional[str] = None
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_ORG_ID: Optional[str] = None
    
    # Aftermarket
    AFTERMARKET_EMAIL: Optional[str] = None
    AFTERMARKET_PASSWORD: Optional[str] = None
    
    # DDRegistrar
    DDREGISTRAR_EMAIL: Optional[str] = None
    DDREGISTRAR_PASSWORD: Optional[str] = None
    
    # Premium.pl
    PREMIUM_EMAIL: Optional[str] = None
    PREMIUM_PASSWORD: Optional[str] = None
    
    # Namecheap
    NAMECHEAP_USERNAME: Optional[str] = None
    NAMECHEAP_PASSWORD: Optional[str] = None
    NAMECHEAP_API_KEY: Optional[str] = None
    NAMECHEAP_API_USER: Optional[str] = None
    
    # Fiverr
    FIVERR_EMAIL: Optional[str] = None
    FIVERR_PASSWORD: Optional[str] = None
    
    # OVH
    OVH_EMAIL: Optional[str] = None
    OVH_PASSWORD: Optional[str] = None
    OVH_APPLICATION_KEY: Optional[str] = None
    OVH_APPLICATION_SECRET: Optional[str] = None
    OVH_CONSUMER_KEY: Optional[str] = None
    
    # IONOS
    IONOS_EMAIL: Optional[str] = None
    IONOS_PASSWORD: Optional[str] = None
    
    # STRATO
    STRATO_USERNAME: Optional[str] = None
    STRATO_PASSWORD: Optional[str] = None
    
    # Spaceship
    SPACESHIP_EMAIL: Optional[str] = None
    SPACESHIP_PASSWORD: Optional[str] = None
    
    # Meetup.com
    MEETUP_EMAIL: Optional[str] = None
    MEETUP_PASSWORD: Optional[str] = None
    
    # Adobe
    ADOBE_EMAIL: Optional[str] = None
    ADOBE_PASSWORD: Optional[str] = None
    
    # GoDaddy
    GODADDY_USERNAME: Optional[str] = None
    GODADDY_PASSWORD: Optional[str] = None
    GODADDY_API_KEY: Optional[str] = None
    GODADDY_API_SECRET: Optional[str] = None
    
    # Afternic
    AFTERNIC_USERNAME: Optional[str] = None
    AFTERNIC_PASSWORD: Optional[str] = None
    
    # Scribd
    SCRIBD_EMAIL: Optional[str] = None
    SCRIBD_PASSWORD: Optional[str] = None
    
    # Envato
    ENVATO_USERNAME: Optional[str] = None
    ENVATO_PASSWORD: Optional[str] = None
    ENVATO_API_KEY: Optional[str] = None
    
    # Proton
    PROTON_EMAIL: Optional[str] = None
    PROTON_PASSWORD: Optional[str] = None
    
    # LinkedIn
    LINKEDIN_EMAIL: Optional[str] = None
    LINKEDIN_PASSWORD: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Instancja ustawień
settings = Settings()

def get_provider_credentials(provider_name: str) -> Dict[str, Any]:
    """
    Pobiera dane uwierzytelniające dla określonego dostawcy.
    
    Args:
        provider_name: Nazwa dostawcy (lowercase)
        
    Returns:
        Słownik z danymi uwierzytelniającymi
    """
    provider_name = provider_name.upper()
    credentials = {}
    
    # Pobierz wszystkie zmienne środowiskowe dla danego dostawcy
    for key, value in settings.dict().items():
        if key.startswith(provider_name + "_") and value is not None:
            # Usuń prefix dostawcy i dodaj do słownika
            credential_key = key[len(provider_name) + 1:].lower()
            credentials[credential_key] = value
    
    return credentials

def get_available_providers() -> List[str]:
    """
    Zwraca listę dostępnych dostawców na podstawie skonfigurowanych danych uwierzytelniających.
    
    Returns:
        Lista nazw dostawców
    """
    providers = set()
    
    for key in settings.dict().keys():
        if "_" in key:
            provider_name = key.split("_")[0].lower()
            if provider_name not in ["output", "download", "log", "browser", "user", "proxy"]:
                providers.add(provider_name)
    
    return sorted(list(providers))

def get_output_path(year: int, month: int, provider: str) -> Path:
    """
    Generuje ścieżkę wyjściową dla pobranych plików.
    
    Args:
        year: Rok
        month: Miesiąc
        provider: Nazwa dostawcy
        
    Returns:
        Ścieżka do katalogu wyjściowego
    """
    base_path = Path(settings.OUTPUT_DIR)
    output_path = base_path / f"{year}.{month:02d}" / provider / "files"
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path
