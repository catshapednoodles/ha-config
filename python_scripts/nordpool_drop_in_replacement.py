ROUND_DECIMALS = data.get('decimals', 4)
current_price_entity = hass.states.get(data.get('entsoe_current_entity_id', 'sensor.entso_e_current_electricity_market_price'))
entsoe_data = hass.states.get(data.get('entsoe_average_entity_id', 'sensor.entso_e_average_electricity_price_today'))

prices_today_from_entsoe = entsoe_data.attributes['prices_today']
prices_today_list_values = list(round(entry.get('price'), ROUND_DECIMALS) for entry in prices_today_from_entsoe)

prices_tomorrow_from_entsoe = entsoe_data.attributes['prices_tomorrow']
prices_tomorrow_list_values = list(round(entry.get('price'), ROUND_DECIMALS) for entry in prices_tomorrow_from_entsoe)

current_price = float(current_price_entity.state)

average_today = sum(prices_today_list_values) / len(prices_today_list_values)
price_percent_to_average = current_price / average_today
low_price = price_percent_to_average < 0.9

raw_today = []
for item in prices_today_from_entsoe:
    entry = {
        "start": dt_util.as_local(datetime.datetime.fromisoformat(item['time'])),
        "end": dt_util.as_local(datetime.datetime.fromisoformat(item['time']) + datetime.timedelta(hours=1)),
        "value": round(item['price'], ROUND_DECIMALS)
    }
    raw_today.append(entry)

raw_tomorrow = []
for item in prices_tomorrow_from_entsoe:
    entry = {
        "start": dt_util.as_local(datetime.datetime.fromisoformat(item['time'])),
        "end": dt_util.as_local(datetime.datetime.fromisoformat(item['time']) + datetime.timedelta(hours=1)),
        "value": round(item['price'], ROUND_DECIMALS)
    }
    raw_tomorrow.append(entry)

hass.states.set('sensor.nordpool_drop_in_replacement', round(current_price, ROUND_DECIMALS), {
    'friendly_name': 'Nordpool drop-in replacement',
    'unit_of_measurement': '€/kWh',
    'icon': 'mdi:currency-eur',
    'device_class': 'monetary',
    'state_class': 'state_class',
    'price_in_cents': False,
    'unit': 'kWh',
    'currency': 'EUR',
    'country': 'Netherlands',
    'region': 'NL',
    'current_price': round(current_price, ROUND_DECIMALS),
    'min': round(min(prices_today_list_values), ROUND_DECIMALS),
    'max': round(max(prices_today_list_values), ROUND_DECIMALS),
    'average': round(average_today, ROUND_DECIMALS),
    'price_percent_to_average': price_percent_to_average,
    'low_price': low_price,
    'today': prices_today_list_values,
    'raw_today': raw_today,
    'tomorrow_valid': prices_tomorrow_list_values != [],
    'tomorrow': prices_tomorrow_list_values,
    'raw_tomorrow': raw_tomorrow
})

manual_override_today = True

if manual_override:
    prices_tomorrow_list_values = [0.276,0.2590,0.274]

hass.states.set('sensor.debug', round(current_price, ROUND_DECIMALS), {
    'friendly_name': 'Nordpool drop-in replacement',
    'unit_of_measurement': '€/kWh',
    'icon': 'mdi:currency-eur',
    'device_class': 'monetary',
    'state_class': 'state_class',
    'price_in_cents': False,
    'unit': 'kWh',
    'currency': 'EUR',
    'country': 'Netherlands',
    'region': 'NL',
    'current_price': round(current_price, ROUND_DECIMALS),
    'min': round(min(prices_today_list_values), ROUND_DECIMALS),
    'max': round(max(prices_today_list_values), ROUND_DECIMALS),
    'average': round(average_today, ROUND_DECIMALS),
    'price_percent_to_average': price_percent_to_average,
    'low_price': low_price,
    'today': prices_today_list_values,
    'raw_today': raw_today,
    'tomorrow_valid': prices_tomorrow_list_values != [],
    'tomorrow': prices_tomorrow_list_values,
    'raw_tomorrow': raw_tomorrow
})