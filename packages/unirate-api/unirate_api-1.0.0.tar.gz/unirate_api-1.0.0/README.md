# Unirate Python API Client

A comprehensive Python client for the [Unirate API](https://unirateapi.com) - providing free, real-time and historical currency exchange rates, plus VAT rates.

## Features

- 🔄 **Real-time exchange rates** - Get current currency conversion rates
- 📈 **Historical data** - Access historical exchange rates for any date (1999-2025)
- ⏰ **Time series data** - Retrieve exchange rate data over date ranges (max 5 years)
- 💰 **Currency conversion** - Convert amounts between currencies (current and historical)
- 🏛️ **VAT rates** - Get VAT rates for countries worldwide
- 📊 **Multiple output formats** - JSON, XML, CSV, TSV support
- 🌍 **170+ currencies supported** - Including cryptocurrencies
- 🆓 **Completely free** - No credit card required
- 🚀 **Easy to use** - Simple, intuitive API

## Installation

```bash
pip install unirate-api
```

## Quick Start

```python
from unirate import UnirateClient

# Initialize the client
client = UnirateClient('your-api-key-here')

# Get current exchange rate
rate = client.get_rate('USD', 'EUR')
print(f'USD to EUR rate: {rate}')

# Convert currency (note: to_currency is first parameter)
amount = client.convert('EUR', 100, 'USD')
print(f'100 USD = {amount} EUR')

# Get supported currencies
currencies = client.get_supported_currencies()
print(f'Supported currencies: {len(currencies)}')
```

## API Methods

### Current Rates & Conversion

#### `get_rate(from_currency='USD', to_currency=None, format='json', callback=None)`
Get current exchange rates. If `to_currency` is omitted, returns rates for all currencies.

```python
# Single currency rate
rate = client.get_rate('USD', 'EUR')

# All rates for base currency
all_rates = client.get_rate('USD')

# Get rates in CSV format
csv_data = client.get_rate('USD', 'EUR', format='csv')
```

#### `convert(to_currency, amount=1, from_currency='USD', format='json', callback=None)`
Convert an amount from one currency to another using current rates.

```python
# Convert with default amount (1)
converted = client.convert('EUR', from_currency='USD')

# Convert specific amount
converted = client.convert('EUR', 100, 'USD')

# Get conversion result in XML format
xml_result = client.convert('EUR', 100, 'USD', format='xml')
```

#### `get_supported_currencies(format='json', callback=None)`
Get a list of all supported currency codes.

```python
currencies = client.get_supported_currencies()

# Get currencies in CSV format
csv_currencies = client.get_supported_currencies(format='csv')
```

### Historical Data

#### `get_historical_rate(date, amount=1, from_currency='USD', to_currency=None, format='json', callback=None)`
Get historical exchange rates for a specific date. If `to_currency` is omitted, returns rates for all currencies.

```python
# Single currency historical rate
rate = client.get_historical_rate('2024-01-01', from_currency='USD', to_currency='EUR')

# All historical rates for base currency
all_rates = client.get_historical_rate('2024-01-01', from_currency='USD')

# Historical conversion with amount
converted = client.get_historical_rate('2024-01-01', amount=100, from_currency='USD', to_currency='EUR')
```

#### `get_historical_rates(date, amount=1, base_currency='USD', format='json', callback=None)`
Alias for `get_historical_rate` to get all exchange rates for a base currency on a specific date.

```python
rates = client.get_historical_rates('2024-01-01', base_currency='USD')
```

#### `convert_historical(amount, from_currency, to_currency, date, format='json', callback=None)`
Convert an amount using historical exchange rates for a specific date.

```python
converted = client.convert_historical(100, 'USD', 'EUR', '2024-01-01')
```

#### `get_time_series(start_date, end_date, amount=1, base_currency='USD', currencies=None, format='json', callback=None)`
Get time series exchange rate data over a date range (max 5 years).

```python
# Time series for specific currencies
time_series = client.get_time_series(
    '2024-01-01', 
    '2024-01-07',
    base_currency='USD',
    currencies=['EUR', 'GBP']
)

# Time series for all currencies
all_series = client.get_time_series('2024-01-01', '2024-01-07', base_currency='USD')

# Time series with amount conversion
converted_series = client.get_time_series(
    '2024-01-01', 
    '2024-01-07',
    amount=100,
    base_currency='USD',
    currencies=['EUR']
)
```

### New Features

#### `get_historical_limits(format='json', callback=None)`
Get information about available historical data limits per currency.

```python
limits = client.get_historical_limits()
print(f"Total currencies with historical data: {limits['total_currencies']}")

for currency, info in limits['currencies'].items():
    print(f"{currency}: {info['earliest_date']} to {info['latest_date']}")
```

#### `get_vat_rates(country=None, format='json', callback=None)`
Get VAT rates for all countries or a specific country.

```python
# Get all VAT rates
all_vat = client.get_vat_rates()
print(f"Total countries: {all_vat['total_countries']}")

# Get VAT rate for specific country
germany_vat = client.get_vat_rates('DE')
vat_info = germany_vat['vat_data']
print(f"Germany VAT rate: {vat_info['vat_rate']}%")

# Get VAT rates in CSV format
csv_vat = client.get_vat_rates(format='csv')
```

## Output Formats

All methods support multiple output formats:

- `json` (default) - Returns Python dict/list
- `xml` - Returns XML string
- `csv` - Returns CSV string
- `tsv` - Returns TSV string

```python
# JSON (default)
json_data = client.get_rate('USD', 'EUR')

# XML format
xml_data = client.get_rate('USD', 'EUR', format='xml')

# CSV format
csv_data = client.get_rate('USD', 'EUR', format='csv')

# TSV format
tsv_data = client.get_rate('USD', 'EUR', format='tsv')
```

## JSONP Support

For JSON responses, you can specify a JSONP callback function:

```python
jsonp_data = client.get_rate('USD', 'EUR', callback='myCallback')
```

## Complete Example

```python
from unirate import UnirateClient

def main():
    client = UnirateClient('your-api-key-here')
    
    try:
        print('=== Current Rates ===')
        
        # Current exchange rate
        rate = client.get_rate('USD', 'EUR')
        print(f'Current USD to EUR: {rate}')
        
        # All rates for USD
        all_rates = client.get_rate('USD')
        print(f'EUR: {all_rates["EUR"]}, GBP: {all_rates["GBP"]}')
        
        # Currency conversion
        converted = client.convert('EUR', 1000, 'USD')
        print(f'1000 USD = {converted} EUR')
        
        print('\n=== Historical Data ===')
        
        # Historical rate
        historical_rate = client.get_historical_rate('2024-01-01', from_currency='USD', to_currency='EUR')
        print(f'USD to EUR on 2024-01-01: {historical_rate}')
        
        # Historical conversion
        historical_converted = client.convert_historical(1000, 'USD', 'EUR', '2024-01-01')
        print(f'1000 USD = {historical_converted} EUR (on 2024-01-01)')
        
        # Time series data
        time_series = client.get_time_series(
            '2024-01-01', '2024-01-05',
            base_currency='USD',
            currencies=['EUR', 'GBP']
        )
        print('USD time series:')
        for date, rates in time_series.items():
            print(f'  {date}: EUR={rates["EUR"]}, GBP={rates["GBP"]}')
        
        print('\n=== New Features ===')
        
        # Historical limits
        limits = client.get_historical_limits()
        print(f'Total currencies: {limits["total_currencies"]}')
        
        # VAT rates
        vat_rates = client.get_vat_rates()
        print(f'Total countries with VAT: {vat_rates["total_countries"]}')
        
        # Germany VAT
        germany_vat = client.get_vat_rates('DE')
        print(f'Germany VAT: {germany_vat["vat_data"]["vat_rate"]}%')
        
        print('\n=== Format Examples ===')
        
        # CSV format
        csv_data = client.get_rate('USD', 'EUR', format='csv')
        print('CSV format:', csv_data[:50] + '...')
        
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
```

## Error Handling

The client provides specific exception types for different error scenarios:

```python
from unirate import UnirateClient
from unirate.exceptions import (
    UnirateError, 
    AuthenticationError, 
    RateLimitError, 
    InvalidCurrencyError, 
    InvalidDateError, 
    APIError
)

client = UnirateClient('your-api-key')

try:
    rate = client.get_rate('USD', 'INVALID')
except AuthenticationError:
    print('Invalid API key')
except InvalidCurrencyError:
    print('Invalid currency code')
except RateLimitError:
    print('Rate limit exceeded')
except InvalidDateError:
    print('Invalid date format')
except APIError as e:
    print(f'API Error: {e} (Status: {e.status_code})')
except UnirateError as e:
    print(f'General API Error: {e}')
```

## Rate Limits

- **Currency endpoints**: Standard rate limits apply
- **Historical endpoints**: 50 requests per hour
- **VAT endpoints**: 1800 requests per hour

## API Key

Get your free API key from [https://unirateapi.com](https://unirateapi.com). No credit card required!

## Supported Currencies

The API supports 170+ currencies including:
- **Traditional currencies**: USD, EUR, GBP, JPY, CAD, AUD, etc.
- **Cryptocurrencies**: BTC, ETH, LTC, and many more

Use `get_supported_currencies()` to get the complete list.

## Historical Data Coverage

Historical data is available from 1999 to 2025, with coverage varying by currency:
- **Major currencies**: Full coverage from 1999-01-01
- **Some currencies**: Limited historical data (use `get_historical_limits()` to check)

## Requirements

- Python 3.7+
- requests

## Changelog

### Version 1.0.0
- **NEW**: VAT rates endpoint (`get_vat_rates()`)
- **NEW**: Historical limits endpoint (`get_historical_limits()`)
- **NEW**: Multiple output formats (JSON, XML, CSV, TSV)
- **NEW**: JSONP callback support
- **BREAKING**: Updated method signatures with optional parameters and defaults
- **BREAKING**: `convert()` method parameter order changed (`to_currency` first)
- **BREAKING**: Historical methods now require `date` as first parameter
- **IMPROVED**: Better error handling with specific exception types
- **IMPROVED**: Enhanced response parsing for new API structure

## License

MIT License