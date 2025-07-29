"""
Moduł integracyjny do pobierania i przetwarzania dokumentów PDF.

Ten moduł łączy funkcjonalność biblioteki webload do pobierania dokumentów
z istniejącym skryptem pdf_to_json.py do konwersji PDF na JSON.
"""

import os
import sys
import importlib.util
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

from loguru import logger

from webload.config import settings
from webload.providers import get_provider_class, get_all_providers


def import_pdf_to_json_module(cfo_root_dir: Optional[str] = None) -> Any:
    """
    Importuje moduł pdf_to_json.py z katalogu month.
    
    Args:
        cfo_root_dir: Opcjonalna ścieżka do katalogu głównego projektu CFO.
                     Jeśli nie podano, próbuje znaleźć automatycznie.
                     
    Returns:
        Zaimportowany moduł pdf_to_json
        
    Raises:
        ImportError: Jeśli nie udało się zaimportować modułu
    """
    try:
        # Jeśli nie podano katalogu głównego, spróbuj go znaleźć
        if cfo_root_dir is None:
            # Sprawdź, czy jesteśmy w katalogu webload
            current_dir = Path.cwd()
            if current_dir.name == "webload":
                cfo_root_dir = str(current_dir.parent)
            else:
                # Zakładamy, że jesteśmy w katalogu głównym projektu CFO
                cfo_root_dir = str(current_dir)
        
        # Ścieżka do modułu pdf_to_json.py
        module_path = Path(cfo_root_dir) / "month" / "pdf_to_json.py"
        
        if not module_path.exists():
            raise ImportError(f"Nie znaleziono pliku {module_path}")
        
        # Importuj moduł
        spec = importlib.util.spec_from_file_location("pdf_to_json", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return module
    
    except Exception as e:
        logger.error(f"Błąd podczas importowania modułu pdf_to_json: {e}")
        raise ImportError(f"Nie udało się zaimportować modułu pdf_to_json: {e}")


def download_and_process(
    providers: Optional[List[str]] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    process_pdfs: bool = True,
    languages: Optional[List[str]] = None,
    use_invoice2data: bool = True,
    overwrite: bool = False,
    cfo_root_dir: Optional[str] = None
) -> Tuple[int, int, int, int]:
    """
    Pobiera dokumenty z określonych dostawców i przetwarza je na format JSON.
    
    Args:
        providers: Lista nazw dostawców. Jeśli None, używa wszystkich dostępnych.
        year: Rok. Jeśli None, używa bieżącego roku.
        month: Miesiąc. Jeśli None, używa bieżącego miesiąca.
        process_pdfs: Czy przetwarzać pobrane pliki PDF na JSON.
        languages: Lista języków do rozpoznawania tekstu (dla pdf_to_json).
        use_invoice2data: Czy używać biblioteki invoice2data (dla pdf_to_json).
        overwrite: Czy nadpisywać istniejące pliki JSON.
        cfo_root_dir: Ścieżka do katalogu głównego projektu CFO.
        
    Returns:
        Krotka (liczba_pobranych, liczba_błędów_pobierania, liczba_przetworzonych, liczba_błędów_przetwarzania)
    """
    # Ustaw domyślne wartości dla roku i miesiąca
    if year is None or month is None:
        current_date = datetime.now()
        year = year or current_date.year
        month = month or current_date.month
    
    # Sprawdź poprawność miesiąca
    if month < 1 or month > 12:
        logger.error(f"Nieprawidłowy miesiąc: {month}. Podaj wartość od 1 do 12.")
        return 0, 1, 0, 0
    
    # Sprawdź poprawność roku
    if year < 2000 or year > datetime.now().year + 1:
        logger.error(f"Nieprawidłowy rok: {year}. Podaj wartość od 2000 do {datetime.now().year + 1}.")
        return 0, 1, 0, 0
    
    # Pobierz dostępnych dostawców
    available_providers = []
    if providers:
        # Filtruj tylko dostępnych dostawców z listy
        for provider_name in providers:
            try:
                # Sprawdź, czy dostawca istnieje
                provider_class = get_provider_class(provider_name)
                available_providers.append(provider_name)
            except ValueError:
                logger.warning(f"Dostawca '{provider_name}' nie istnieje")
    else:
        # Użyj wszystkich dostępnych dostawców
        from webload.config import get_available_providers
        available_providers = get_available_providers()
    
    if not available_providers:
        logger.error("Brak dostępnych dostawców")
        return 0, 1, 0, 0
    
    # Pobierz dokumenty od każdego dostawcy
    total_downloaded = 0
    total_download_errors = 0
    
    logger.info(f"Pobieranie dokumentów za {month:02d}/{year} od {len(available_providers)} dostawców")
    
    for provider_name in available_providers:
        try:
            logger.info(f"Pobieranie dokumentów od dostawcy {provider_name}")
            
            # Pobierz dane uwierzytelniające
            from webload.config import get_provider_credentials
            credentials = get_provider_credentials(provider_name)
            
            if not credentials:
                logger.error(f"Brak danych uwierzytelniających dla dostawcy {provider_name}")
                total_download_errors += 1
                continue
            
            # Utwórz instancję dostawcy
            provider_class = get_provider_class(provider_name)
            provider = provider_class(credentials)
            
            # Pobierz dokumenty
            success, error = provider.run(year, month)
            
            total_downloaded += success
            total_download_errors += error
            
            if success > 0:
                logger.success(f"Pobrano {success} plików od dostawcy {provider_name}")
            
            if error > 0:
                logger.warning(f"Wystąpiło {error} błędów podczas pobierania od dostawcy {provider_name}")
        
        except Exception as e:
            logger.error(f"Błąd podczas pobierania dokumentów od dostawcy {provider_name}: {e}")
            total_download_errors += 1
    
    # Jeśli nie trzeba przetwarzać plików PDF, zakończ
    if not process_pdfs:
        return total_downloaded, total_download_errors, 0, 0
    
    # Przetwórz pobrane pliki PDF na JSON
    total_processed = 0
    total_process_errors = 0
    
    try:
        # Importuj moduł pdf_to_json
        pdf_to_json = import_pdf_to_json_module(cfo_root_dir)
        
        # Katalog z pobranymi plikami
        output_dir = settings.output_dir
        pdf_dir = Path(output_dir) / f"{year}.{month:02d}"
        
        if not pdf_dir.exists():
            logger.warning(f"Katalog {pdf_dir} nie istnieje. Nie ma plików do przetworzenia.")
            return total_downloaded, total_download_errors, 0, 0
        
        # Katalog wyjściowy dla plików JSON
        json_output_dir = pdf_dir / "json"
        
        # Wywołaj funkcję convert_pdf_to_json
        logger.info(f"Przetwarzanie plików PDF z katalogu {pdf_dir}")
        success, failed = pdf_to_json.convert_pdf_to_json(
            pdf_dir=str(pdf_dir),
            output_dir=str(json_output_dir),
            languages=languages,
            overwrite=overwrite,
            month=month,
            year=year,
            use_invoice2data=use_invoice2data
        )
        
        total_processed = success
        total_process_errors = failed
        
        if success > 0:
            logger.success(f"Przetworzono {success} plików PDF na JSON")
        
        if failed > 0:
            logger.warning(f"Nie udało się przetworzyć {failed} plików PDF")
    
    except ImportError as e:
        logger.error(f"Nie udało się zaimportować modułu pdf_to_json: {e}")
        total_process_errors += 1
    except Exception as e:
        logger.error(f"Błąd podczas przetwarzania plików PDF: {e}")
        total_process_errors += 1
    
    return total_downloaded, total_download_errors, total_processed, total_process_errors
