# Webload

Biblioteka do automatycznego pobierania faktur i wyciągów z różnych serwisów internetowych.

## Opis

Webload to narzędzie, które automatycznie pobiera faktury, wyciągi i inne dokumenty finansowe z różnych serwisów internetowych (PayPal, Wise, Aftermarket, itp.) i organizuje je w strukturze katalogów według dat i dostawców.

## Funkcje

- Automatyczne logowanie do serwisów za pomocą podanych danych uwierzytelniających
- Pobieranie faktur i wyciągów w formatach PDF, CSV, HTML
- Konwersja dokumentów HTML do PDF (jeśli potrzebne)
- Organizacja plików w strukturze katalogów YYYY.MM/{provider}/files
- Obsługa wielu dostawców (PayPal, Wise, Aftermarket, OVH, itp.)
- Uruchamianie w kontenerze Docker dla izolacji i bezpieczeństwa
- Planowanie automatycznych pobrań
- Integracja z modułem pdf_to_json.py do automatycznej konwersji PDF na JSON
- Testy jednostkowe dla kluczowych komponentów

## Wymagania

- Python 3.8+
- Docker
- Poetry (zarządzanie zależnościami)

## Instalacja

```bash
# Klonowanie repozytorium
git clone https://github.com/fin-officer/webload.git
cd webload

# Instalacja zależności za pomocą Poetry
poetry install

# Konfiguracja zmiennych środowiskowych
cp .env.example .env
# Edytuj plik .env i dodaj swoje dane uwierzytelniające
```

## Konfiguracja

Skopiuj plik `.env.example` do `.env` i uzupełnij dane uwierzytelniające dla serwisów, z których chcesz pobierać dokumenty:

```
# Przykład konfiguracji
WISE_EMAIL=twoj_email@example.com
WISE_PASSWORD=twoje_haslo

PAYPAL_EMAIL=twoj_email@example.com
PAYPAL_PASSWORD=twoje_haslo

# Dodaj więcej danych uwierzytelniających dla innych serwisów
```

## Użycie

### Uruchomienie z Poetry

```bash
# Pobieranie dokumentów dla wszystkich dostawców
poetry run webload download-all

# Pobieranie dokumentów dla konkretnego dostawcy
poetry run webload download --provider paypal

# Pobieranie dokumentów dla konkretnego miesiąca
poetry run webload download --month 9 --year 2024

# Pobieranie dokumentów dla konkretnego dostawcy i miesiąca
poetry run webload download --provider wise --month 9 --year 2024

# Pobieranie i przetwarzanie dokumentów na JSON
poetry run webload download-and-process --month 9 --year 2024

# Pobieranie i przetwarzanie dokumentów dla konkretnego dostawcy
poetry run webload download-and-process --provider wise --month 9 --year 2024 --languages pol eng
```

### Uruchomienie w Dockerze

```bash
# Budowanie obrazu Docker
docker build -t webload .

# Uruchomienie kontenera
docker run --rm -v $(pwd)/downloads:/app/downloads -v $(pwd)/.env:/app/.env webload download-all

# Uruchomienie kontenera z pobieraniem i przetwarzaniem na JSON
docker run --rm -v $(pwd)/downloads:/app/downloads -v $(pwd)/.env:/app/.env webload download-and-process --month 9 --year 2024
```

## Obsługiwani dostawcy

- Wise (statements)
- PayPal (accountStatements)
- SAV (transaction_list)
- OpenAI (billing history)
- Aftermarket (faktury)
- DDRegistrar (faktury)
- Premium.pl (faktury)
- Namecheap (zamówienia)
- Fiverr (billing)
- OVH (historia płatności)
- IONOS (billing)
- STRATO (faktury)
- Spaceship (orders-transactions)
- Meetup.com (historia płatności)
- Adobe
- GoDaddy
- Afternic
- Scribd (historia płatności)
- Envato (statements)
- Proton
- LinkedIn

## Struktura katalogów

Pobrane dokumenty są organizowane w następującej strukturze:

```
downloads/
  └── YYYY.MM/
      └── {provider}/
          └── files/
              ├── invoice_1.pdf
              ├── invoice_2.pdf
              └── statement.pdf
      └── json/
          └── invoice_1.json
          └── invoice_2.json
```

## Integracja z pdf_to_json

Biblioteka webload integruje się z istniejącym modułem `pdf_to_json.py` do konwersji plików PDF na format JSON:

- Automatyczne pobieranie dokumentów i ich konwersja w jednym kroku
- Wsparcie dla wielu języków rozpoznawania tekstu
- Możliwość wyboru między standardową konwersją a użyciem invoice2data
- Konfiguracja przez parametry wiersza poleceń

## Testy

```bash
# Uruchomienie testów jednostkowych
poetry run pytest

# Uruchomienie testów z raportowaniem pokrycia kodu
poetry run pytest --cov=webload
```

## Rozwój

Aby dodać obsługę nowego dostawcy:

1. Utwórz nowy plik w katalogu `webload/providers/`
2. Zaimplementuj klasę dostawcy dziedziczącą po `BaseProvider`
3. Zarejestruj dostawcę w `webload/providers/__init__.py`

## Licencja

Ten projekt jest objęty licencją [MIT](LICENSE).
