#!/usr/bin/env python3
"""
Interfejs wiersza poleceń dla biblioteki webload.
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import click
from loguru import logger
from tqdm import tqdm

from webload.config import settings, get_provider_credentials, get_available_providers
from webload.providers import get_provider_class, get_all_providers, BaseProvider
from webload.integration.pdf_processor import download_and_process


def setup_logging(log_level: str) -> None:
    """
    Konfiguruje system logowania.
    
    Args:
        log_level: Poziom logowania
    """
    # Usuń domyślny handler
    logger.remove()
    
    # Dodaj handler dla konsoli
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True,
    )
    
    # Dodaj handler dla pliku
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"webload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
    )
    
    logger.info(f"Logi będą zapisywane do pliku: {log_file}")


def run_provider(provider_name: str, year: int, month: int) -> Tuple[int, int]:
    """
    Uruchamia dostawcę dla określonego miesiąca i roku.
    
    Args:
        provider_name: Nazwa dostawcy
        year: Rok
        month: Miesiąc
        
    Returns:
        Krotka (liczba_sukcesów, liczba_błędów)
    """
    try:
        # Pobierz dane uwierzytelniające
        credentials = get_provider_credentials(provider_name)
        
        if not credentials:
            logger.error(f"Brak danych uwierzytelniających dla dostawcy {provider_name}")
            return 0, 1
        
        # Pobierz klasę dostawcy
        provider_class = get_provider_class(provider_name)
        
        # Utwórz instancję dostawcy
        provider = provider_class(credentials)
        
        # Uruchom dostawcę
        return provider.run(year, month)
    
    except Exception as e:
        logger.error(f"Błąd podczas uruchamiania dostawcy {provider_name}: {e}")
        return 0, 1


@click.group()
@click.version_option()
def cli():
    """Narzędzie do automatycznego pobierania faktur i wyciągów z różnych serwisów."""
    pass


@cli.command("list-providers")
def list_providers():
    """Wyświetla listę dostępnych dostawców."""
    # Pobierz wszystkich zarejestrowanych dostawców
    all_providers = get_all_providers()
    
    # Pobierz dostawców z danymi uwierzytelniającymi
    available_providers = get_available_providers()
    
    click.echo("Dostępni dostawcy:")
    for provider in sorted(all_providers):
        status = "✅" if provider in available_providers else "❌"
        click.echo(f"{status} {provider}")
    
    if not available_providers:
        click.echo("\nBrak skonfigurowanych dostawców. Dodaj dane uwierzytelniające do pliku .env")


@cli.command("download")
@click.option("--provider", "-p", help="Nazwa dostawcy (np. wise, paypal)")
@click.option("--month", "-m", type=int, help="Miesiąc (1-12)")
@click.option("--year", "-y", type=int, help="Rok (np. 2024)")
@click.option("--log-level", default="INFO", 
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
              help="Poziom logowania")
def download(provider: Optional[str], month: Optional[int], year: Optional[int], log_level: str):
    """Pobiera dokumenty dla określonego dostawcy i okresu."""
    # Konfiguracja logowania
    setup_logging(log_level)
    
    # Ustaw domyślne wartości dla miesiąca i roku
    if not month or not year:
        current_date = datetime.now()
        month = month or current_date.month
        year = year or current_date.year
    
    # Sprawdź poprawność miesiąca
    if month < 1 or month > 12:
        logger.error(f"Nieprawidłowy miesiąc: {month}. Podaj wartość od 1 do 12.")
        sys.exit(1)
    
    # Sprawdź poprawność roku
    if year < 2000 or year > datetime.now().year + 1:
        logger.error(f"Nieprawidłowy rok: {year}. Podaj wartość od 2000 do {datetime.now().year + 1}.")
        sys.exit(1)
    
    # Jeśli podano konkretnego dostawcę
    if provider:
        logger.info(f"Pobieranie dokumentów od dostawcy {provider} za {month:02d}/{year}")
        success, error = run_provider(provider, year, month)
        
        if success > 0:
            logger.success(f"Pobrano {success} plików od dostawcy {provider}")
        
        if error > 0:
            logger.warning(f"Wystąpiło {error} błędów podczas pobierania od dostawcy {provider}")
    
    else:
        # Pobierz wszystkich dostępnych dostawców
        available_providers = get_available_providers()
        
        if not available_providers:
            logger.error("Brak skonfigurowanych dostawców. Dodaj dane uwierzytelniające do pliku .env")
            sys.exit(1)
        
        logger.info(f"Pobieranie dokumentów od wszystkich dostawców za {month:02d}/{year}")
        
        total_success = 0
        total_error = 0
        
        # Uruchom każdego dostawcę
        for provider_name in tqdm(available_providers, desc="Dostawcy"):
            logger.info(f"Uruchamianie dostawcy: {provider_name}")
            success, error = run_provider(provider_name, year, month)
            
            total_success += success
            total_error += error
        
        logger.info(f"Pobieranie zakończone. Pobrano {total_success} plików, wystąpiło {total_error} błędów.")


@cli.command("download-all")
@click.option("--months", "-m", type=int, default=1, help="Liczba miesięcy wstecz do pobrania")
@click.option("--log-level", default="INFO", 
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
              help="Poziom logowania")
def download_all(months: int, log_level: str):
    """Pobiera dokumenty dla wszystkich dostawców za określoną liczbę miesięcy wstecz."""
    # Konfiguracja logowania
    setup_logging(log_level)
    
    # Sprawdź poprawność liczby miesięcy
    if months < 1 or months > 36:
        logger.error(f"Nieprawidłowa liczba miesięcy: {months}. Podaj wartość od 1 do 36.")
        sys.exit(1)
    
    # Pobierz wszystkich dostępnych dostawców
    available_providers = get_available_providers()
    
    if not available_providers:
        logger.error("Brak skonfigurowanych dostawców. Dodaj dane uwierzytelniające do pliku .env")
        sys.exit(1)
    
    logger.info(f"Pobieranie dokumentów za ostatnie {months} miesięcy")
    
    # Generuj listę miesięcy do pobrania
    current_date = datetime.now()
    periods = []
    
    for i in range(months):
        year = current_date.year
        month = current_date.month - i
        
        # Obsłuż przejście do poprzedniego roku
        while month <= 0:
            year -= 1
            month += 12
        
        periods.append((year, month))
    
    total_success = 0
    total_error = 0
    
    # Dla każdego okresu
    for year, month in tqdm(periods, desc="Okresy"):
        logger.info(f"Pobieranie dokumentów za {month:02d}/{year}")
        
        # Dla każdego dostawcy
        for provider_name in tqdm(available_providers, desc="Dostawcy", leave=False):
            logger.info(f"Uruchamianie dostawcy {provider_name} za {month:02d}/{year}")
            success, error = run_provider(provider_name, year, month)
            
            total_success += success
            total_error += error
    
    logger.info(f"Pobieranie zakończone. Pobrano {total_success} plików, wystąpiło {total_error} błędów.")


@cli.command("download-and-process")
@click.option("--provider", "-p", help="Nazwa dostawcy (np. wise, paypal)")
@click.option("--month", "-m", type=int, help="Miesiąc (1-12)")
@click.option("--year", "-y", type=int, help="Rok (np. 2024)")
@click.option("--languages", "-l", multiple=True, help="Języki do rozpoznawania tekstu (np. pol, eng)")
@click.option("--use-invoice2data/--no-invoice2data", default=True, 
              help="Czy używać biblioteki invoice2data do ekstrakcji danych")
@click.option("--overwrite/--no-overwrite", default=False, 
              help="Czy nadpisywać istniejące pliki JSON")
@click.option("--cfo-root", help="Ścieżka do katalogu głównego projektu CFO")
@click.option("--log-level", default="INFO", 
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
              help="Poziom logowania")
def download_and_process(
    provider: Optional[str],
    month: Optional[int],
    year: Optional[int],
    languages: List[str],
    use_invoice2data: bool,
    overwrite: bool,
    cfo_root: Optional[str],
    log_level: str
):
    """Pobiera dokumenty i przetwarza je na format JSON."""
    # Konfiguracja logowania
    setup_logging(log_level)
    
    # Lista dostawców
    providers = [provider] if provider else None
    
    # Wywołaj funkcję pobierania i przetwarzania
    downloaded, download_errors, processed, process_errors = download_and_process(
        providers=providers,
        year=year,
        month=month,
        process_pdfs=True,
        languages=languages if languages else None,
        use_invoice2data=use_invoice2data,
        overwrite=overwrite,
        cfo_root_dir=cfo_root
    )
    
    # Wyświetl podsumowanie
    click.echo("\nPodsumowanie:")
    click.echo(f"- Pobrano dokumentów: {downloaded}")
    click.echo(f"- Błędy pobierania: {download_errors}")
    click.echo(f"- Przetworzono plików PDF na JSON: {processed}")
    click.echo(f"- Błędy przetwarzania: {process_errors}")
    
    # Ustal kod wyjścia
    if download_errors > 0 or process_errors > 0:
        sys.exit(1)
    else:
        sys.exit(0)


def main():
    """Funkcja główna."""
    try:
        cli()
    except KeyboardInterrupt:
        logger.warning("Przerwano przez użytkownika")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Wystąpił nieoczekiwany błąd: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
