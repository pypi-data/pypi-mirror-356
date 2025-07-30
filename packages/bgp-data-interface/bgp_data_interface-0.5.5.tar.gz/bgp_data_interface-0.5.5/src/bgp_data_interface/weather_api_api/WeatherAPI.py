from datetime import datetime
import pandas as pd
import pytz
import requests
from typing import Any

FORECAST_URL = "https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={lat_long}&days={days}&aqi=yes&alerts=no"
HISTORICAL_URL = "https://api.weatherapi.com/v1/history.json?key={api_key}&q={lat_long}&dt={date}"

BKK_TZ = pytz.timezone('Asia/Bangkok')


# Note
# The weather API (free version) can only return 
# 3 forecast days and 
# 7 historical days.
#
class WeatherAPI:

    def __init__(self, api_key: str)  -> None:
        self.api_key = api_key


    def forecast(self, params: dict[str, Any]) -> pd.DataFrame:
        lat_long = self._get_lat_long(params)

        days = 1
        if 'start_date' in params and 'end_date' in params:
            start_date = pd.to_datetime(params['start_date'])
            end_date = pd.to_datetime(params['end_date'])
            days = (end_date - start_date).days + 1

        return self._hourly_forecast(lat_long, days)


    def _get_lat_long(self, params: dict[str, Any]) -> str:
        latitude = params.get('latitude', '13.4916354486428')
        longitude = params.get('longitude', '100.85609829815238')
        
        return f"{latitude},{longitude}"


    def _hourly_forecast(self, lat_long: str, days: int) -> pd.DataFrame:
        url = FORECAST_URL.format(
            api_key=self.api_key,
            lat_long=lat_long,
            days=days
        )

        response = requests.request("GET", url)
        json = response.json()
        forecast_day = json.get('forecast', {}) \
            .get('forecastday', [{}])
        
        result: list[dict] = []
        for day in forecast_day:
            for hour in day.get('hour', []):
                self._append_hour(result, hour)

        df = pd.DataFrame(data=result)
        df['date_time'] = pd.to_datetime(df['date_time'])

        return df


    def _append_hour(self, result: list, hour: dict) -> None:
        result.append({
            "date_time": hour.get('time', ""),
            "temperature_c": hour.get('temp_c', ""),
            "is_day": hour.get('is_day', ""),
            "condition": hour.get('condition', {}).get('text', ""),
            "condition_code": hour.get('condition', {}).get('code', ""),
            "wind_kph": hour.get('wind_kph', ""),
            "wind_degree": hour.get('wind_degree', ""),
            "wind_direction": hour.get('wind_dir', ""),
            "pressure_millibar": hour.get('pressure_mb', ""),
            "precipitation_mm": hour.get('precip_mm', ""),
            "snow_cm": hour.get('snow_cm', ""),
            "humidity": hour.get('humidity', ""),
            "cloud": hour.get('cloud', ""),
            "feelslike_c": hour.get('feelslike_c', ""),
            "windchill_c": hour.get('windchill_c', ""),
            "heatindex_c": hour.get('heatindex_c', ""),
            "dewpoint_c": hour.get('dewpoint_c', ""),
            "chance_of_rain": hour.get('chance_of_rain', ""),
            "chance_of_snow": hour.get('chance_of_snow', ""),
            "vis_km": hour.get('vis_km', ""),
            "gust_kph": hour.get('gust_kph', ""),
            "uv": hour.get('uv', ""),
        })


    def historical(self, params: dict[str, Any]) -> pd.DataFrame:
        lat_long = self._get_lat_long(params)

        start_date = datetime.today()
        end_date = datetime.today()
        if 'start_date' in params and 'end_date' in params:
            start_date = pd.to_datetime(params['start_date'])
            end_date = pd.to_datetime(params['end_date'])
            # start_date = pd.to_datetime(params['start_date']).tz_localize(BKK_TZ)
            # end_date = pd.to_datetime(params['end_date']).tz_localize(BKK_TZ)

        all_df = []
        for single_date in pd.date_range(start=start_date, end=end_date):
            all_df.append(self._hourly_historical(lat_long, single_date))

        if all_df:
            return pd.concat(all_df, ignore_index=True) 
        
        return pd.DataFrame()


    def _hourly_historical(self, lat_long: str, date: datetime) -> pd.DataFrame:
        url = HISTORICAL_URL.format(
            api_key=self.api_key,
            lat_long=lat_long,
            date=date.strftime("%Y-%m-%d")
        )

        print(url)

        response = requests.request("GET", url)
        json = response.json()
        forecast_day = json.get('forecast', {}) \
            .get('forecastday', [{}])

        result: list[dict] = []
        for hour in forecast_day[0].get('hour', []):
            self._append_hour(result, hour)

        df = pd.DataFrame(data=result)
        df['date_time'] = pd.to_datetime(df['date_time'])

        return df
