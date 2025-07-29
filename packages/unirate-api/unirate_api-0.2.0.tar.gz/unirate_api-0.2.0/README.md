# Unirate Python API Client

A simple Python client for the [Unirate API](https://unirateapi.com) - providing free, real-time and historical currency exchange rates.

## Features

- 🔄 **Real-time exchange rates** - Get current currency conversion rates
- 📈 **Historical data** - Access historical exchange rates for any date
- ⏰ **Time series data** - Retrieve exchange rate data over date ranges
- 💰 **Currency conversion** - Convert amounts between currencies (current and historical)
- 🌍 **590+ currencies supported** - Including cryptocurrencies
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

# Convert currency
amount = client.convert(100, 'USD', 'EUR')
print(f'100 USD = {amount} EUR')

# Get supported currencies
currencies = client.get_supported_currencies()
print(f'Supported currencies: {len(currencies)}')
```

## API Methods

### Current Rates & Conversion

#### `get_rate(from_currency, to_currency)`
Get the current exchange rate between two currencies.

```python
rate = client.get_rate('USD', 'EUR')
```

#### `convert(amount, from_currency, to_currency)`
Convert an amount from one currency to another using current rates.

```python
converted = client.convert(100, 'USD', 'EUR')
```

#### `get_supported_currencies()`
Get a list of all supported currency codes.

```python
currencies = client.get_supported_currencies()
```

### Historical Data

#### `get_historical_rate(from_currency, to_currency, date)`
Get the exchange rate between two currencies for a specific historical date.

```python
# Get USD to EUR rate for January 1st, 2024
historical_rate = client.get_historical_rate('USD', 'EUR', '2024-01-01')
print(f'USD to EUR on 2024-01-01: {historical_rate}')
```

#### `get_historical_rates(base_currency, date)`
Get all exchange rates for a base currency on a specific historical date.

```python
# Get all USD rates for January 1st, 2024
rates = client.get_historical_rates('USD', '2024-01-01')
print(f'USD to EUR: {rates["EUR"]}')
print(f'USD to GBP: {rates["GBP"]}')
```

#### `convert_historical(amount, from_currency, to_currency, date)`
Convert an amount using historical exchange rates for a specific date.

```python
# Convert 100 USD to EUR using rates from January 1st, 2024
converted = client.convert_historical(100, 'USD', 'EUR', '2024-01-01')
print(f'100 USD = {converted} EUR (on 2024-01-01)')
```

#### `get_time_series(from_currency, to_currency, start_date, end_date)`
Get time series exchange rate data for a currency pair over a date range.

```python
# Get USD to EUR rates for the first week of January 2024
time_series = client.get_time_series('USD', 'EUR', '2024-01-01', '2024-01-07')
for date, rate in time_series.items():
    print(f'{date}: {rate}')
```

## Complete Example

```python
from unirate import UnirateClient

def main():
    # Initialize client
    client = UnirateClient('your-api-key-here')
    
    try:
        print('=== Current Rates ===')
        
        # Current exchange rate
        current_rate = client.get_rate('USD', 'EUR')
        print(f'Current USD to EUR: {current_rate}')
        
        # Currency conversion
        converted = client.convert(1000, 'USD', 'EUR')
        print(f'1000 USD = {converted} EUR')
        
        print('\n=== Historical Data ===')
        
        # Historical rate for specific date
        historical_rate = client.get_historical_rate('USD', 'EUR', '2024-01-01')
        print(f'USD to EUR on 2024-01-01: {historical_rate}')
        
        # Historical conversion
        historical_converted = client.convert_historical(1000, 'USD', 'EUR', '2024-01-01')
        print(f'1000 USD = {historical_converted} EUR (on 2024-01-01)')
        
        # Time series data
        time_series = client.get_time_series('USD', 'EUR', '2024-01-01', '2024-01-05')
        print('USD to EUR time series:')
        for date, rate in time_series.items():
            print(f'  {date}: {rate}')
            
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
```

## Error Handling

The client raises `UnirateError` for API-related errors:

```python
from unirate import UnirateClient, UnirateError

client = UnirateClient('your-api-key')

try:
    rate = client.get_rate('USD', 'INVALID')
except UnirateError as e:
    print(f'API Error: {e}')
```

## API Key

Get your free API key from [https://unirateapi.com](https://unirateapi.com). No credit card required!

## Supported Currencies

The API supports 590+ currencies including:
- **Traditional currencies**: USD, EUR, GBP, JPY, CAD, AUD, etc.
- **Cryptocurrencies**: BTC, ETH, LTC, and many more

Use `get_supported_currencies()` to get the complete list.

## Requirements

- Python 3.7+
- requests

## License

MIT License