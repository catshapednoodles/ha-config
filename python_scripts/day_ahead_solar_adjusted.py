ROUND_DECIMALS = data.get('decimals', 4)
current_price_entity = hass.states.get(data.get('entsoe_current_entity_id', 'sensor.day_ahead_current_electricity_market_price'))
entsoe_data = hass.states.get(data.get('entsoe_average_entity_id', 'sensor.day_ahead_average_electricity_price_today'))
nordpool_data = hass.states.get(data.get('nordpool_entity_id', 'sensor.nordpool_kwh_nl_eur_4_09_0'))
zonneplan_data = hass.states.get(data.get('zonneplan_entity_id', 'sensor.zonneplan_current_electricity_tariff'))
pv_forecast_data = hass.states.get(data.get('pv_forecast_entity_id', 'sensor.p_pv_forecast'))
pv_forecast_entity = hass.states.get('sensor.day_ahead_pv_forecast')

today = datetime.datetime.now().date()
tomorrow = today + datetime.timedelta(days=1)
# Costs should be 0.02118, but apparently Tibber gives this back for now.
costs = 0

pv_forecasts = []
raw_today = []
prices_today = []
solar_adjusted_today = []
raw_tomorrow = []
prices_tomorrow = []
solar_adjusted_tomorrow = []
ev_charging_today = []
ev_charging_tomorrow = []

# old_pv_data = pv_forecast_entity.attributes['pv_forecast'] if pv_forecast_entity is not None else []
# new_pv_data = pv_forecast_data.attributes['forecasts'] if pv_forecast_data is not None else []
# full_list = list({v['date']: v for v in old_pv_data + new_pv_data}.values())

# for item in full_list:
#     date = datetime.datetime.fromisoformat(item['date']).date()
#     if date >= today and float(item['p_pv_forecast']) > 0:
#         pv_forecasts.append(item)

manual_override_today = False

if manual_override_today:
    today_date = "2024-06-26"
    timezone = "+02:00"
    manual_list_today = [
        {
        "start": datetime.datetime.fromisoformat(today_date + "T00:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T00:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.276
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T01:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T01:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.259
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T02:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T02:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.274
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T03:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T03:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.268
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T04:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T04:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.290
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T05:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T05:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.268
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T06:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T06:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.259
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T07:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T07:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.277
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T08:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T08:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.292
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T09:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T09:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.246
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T10:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T10:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.144
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T11:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T11:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.092
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T12:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T12:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.056
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T13:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T13:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.041
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T14:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T14:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.041
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T15:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T15:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.092
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T16:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T16:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.153
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T17:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T17:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.247
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T18:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T18:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.268
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T19:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T19:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.293
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T20:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T20:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.288
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T21:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T21:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.294
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T22:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T22:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.286
        },
        {
        "start": datetime.datetime.fromisoformat(today_date + "T23:00:00" + timezone),
        "end": datetime.datetime.fromisoformat(today_date + "T23:00:00" + timezone) + datetime.timedelta(hours=1),
        "value": 0.264
        }
    ]
    manual_current_price = float(manual_list_today[datetime.datetime.now().hour]["value"])
    prices_from_nordpool = manual_list_today + nordpool_data.attributes['raw_tomorrow']
else:
    prices_from_nordpool_raw = nordpool_data.attributes['raw_today'] + nordpool_data.attributes['raw_tomorrow']
    prices_from_nordpool = [x for i, x in enumerate(prices_from_nordpool_raw) if i == prices_from_nordpool_raw.index(x)]

# check if nordpool or entsoe data must be used
if prices_from_nordpool != []:
    nordpool_used = True
    for item in prices_from_nordpool:
        item_time = item['start']
        if item_time.date() >= today and item['value'] is not None :
            start = dt_util.as_local(item_time)
            price = round(item['value'], ROUND_DECIMALS)
            # pv_forecast = None
            # for p in pv_forecasts:
            #     if p['date'] == item['time']:
            #         pv_forecast = float(p['p_pv_forecast'])
            #         break
            # solar_adjust = min(1, 1 - max(0, (pv_forecast - 600) / (3000 - 600))) if pv_forecast != None else 1
            # solar_adjusted_price = round(price - (costs - solar_adjust * costs), ROUND_DECIMALS)
            solar_adjusted_price = price
            raw_entry = {
                "start": start,
                "end": item['end'],
                "value": price,
                "value_solar_adjusted": solar_adjusted_price
            }
            ev_charging_entry = {
                "time": start,
                "price": price
            }
            if item_time.date() == today:
                raw_today.append(raw_entry)
                prices_today.append(price)
                solar_adjusted_today.append(solar_adjusted_price)
                ev_charging_today.append(ev_charging_entry)
            else:
                raw_tomorrow.append(raw_entry)
                prices_tomorrow.append(price)
                solar_adjusted_tomorrow.append(solar_adjusted_price)
                ev_charging_tomorrow.append(ev_charging_entry)
    current_price = float(nordpool_data.state) if not manual_override_today else manual_current_price
else:
    prices_from_entsoe = entsoe_data.attributes['prices']
    for item in prices_from_entsoe:
        item_time = datetime.datetime.fromisoformat(item['time'])
        if item_time.date() >= today and item['price'] is not None:
            start = dt_util.as_local(item_time)
            price = round(item['price'], ROUND_DECIMALS)
            # pv_forecast = None
            # for p in pv_forecasts:
            #     if p['date'] == item['time']:
            #         pv_forecast = float(p['p_pv_forecast'])
            #         break
            # solar_adjust = min(1, 1 - max(0, (pv_forecast - 600) / (3000 - 600))) if pv_forecast != None else 1
            # solar_adjusted_price = round(price - (costs - solar_adjust * costs), ROUND_DECIMALS)
            solar_adjusted_price = price
            raw_entry = {
                "start": start,
                "end": start + datetime.timedelta(hours=1),
                "value": price,
                "value_solar_adjusted": solar_adjusted_price
            }
            ev_charging_entry = {
                "time": start,
                "price": price
            }
            if item_time.date() == today:
                raw_today.append(raw_entry)
                prices_today.append(price)
                solar_adjusted_today.append(solar_adjusted_price)
                ev_charging_today.append(ev_charging_entry)
            else:
                raw_tomorrow.append(raw_entry)
                prices_tomorrow.append(price)
                solar_adjusted_tomorrow.append(solar_adjusted_price)
                ev_charging_tomorrow.append(ev_charging_entry)
    current_price = float(current_price_entity.state)

# Add data from tomorrow from Entso-e if nordpool still doesn't have them
if nordpool_used and prices_tomorrow == [] and entsoe_data.state != 'unavailable' and entsoe_data.attributes['prices_tomorrow'] != []:
    for item in prices_from_entsoe:
        item_time = datetime.datetime.fromisoformat(item['time'])
        if item_time.date() >= tomorrow and item['price'] is not None:
            start = dt_util.as_local(item_time)
            price = round(item['price'], ROUND_DECIMALS)
            # pv_forecast = None
            # for p in pv_forecasts:
            #     if p['date'] == item['time']:
            #         pv_forecast = float(p['p_pv_forecast'])
            #         break
            # solar_adjust = min(1, 1 - max(0, (pv_forecast - 600) / (3000 - 600))) if pv_forecast != None else 1
            # solar_adjusted_price = round(price - (costs - solar_adjust * costs), ROUND_DECIMALS)
            solar_adjusted_price = price
            raw_entry = {
                "start": start,
                "end": start + datetime.timedelta(hours=1),
                "value": price,
                "value_solar_adjusted": solar_adjusted_price
            }
            if item_time.date() == today:
                raw_today.append(raw_entry)
                prices_today.append(price)
                solar_adjusted_today.append(solar_adjusted_price)
            else:
                raw_tomorrow.append(raw_entry)
                prices_tomorrow.append(price)
                solar_adjusted_tomorrow.append(solar_adjusted_price)

average_today = sum(prices_today) / len(prices_today)
price_percent_to_average = current_price / average_today
low_price = price_percent_to_average < 0.9

hass.states.set('sensor.day_ahead_price', round(current_price, ROUND_DECIMALS), {
    'friendly_name': 'Day-ahead price',
    'unit_of_measurement': '€/kWh',
    'icon': 'mdi:currency-eur',
    'device_class': 'monetary',
    'state_class': 'measurement',
    'price_in_cents': False,
    'unit': 'kWh',
    'currency': 'EUR',
    'country': 'Netherlands',
    'region': 'NL',
    'current_price': round(current_price, ROUND_DECIMALS),
    'min': round(min(prices_today), ROUND_DECIMALS),
    'max': round(max(prices_today), ROUND_DECIMALS),
    'average': round(average_today, ROUND_DECIMALS),
    'price_percent_to_average': price_percent_to_average,
    'low_price': low_price,
    'today': solar_adjusted_today,
    'tomorrow': solar_adjusted_tomorrow,
    'tomorrow_valid': prices_tomorrow != [],
    'raw_today': raw_today,
    'raw_tomorrow': raw_tomorrow,
    'prices_today': ev_charging_today,
    'prices_tomorrow': ev_charging_tomorrow,
})

hass.states.set('sensor.day_ahead_pv_forecast', dt_util.as_local(datetime.datetime.now()), {
    'friendly_name': 'Day-ahead PV forecast',
    'icon': 'mdi:currency-eur',
    'state_class': 'timestamp',
    'pv_forecast': pv_forecasts,
})
