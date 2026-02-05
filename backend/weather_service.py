"""
Weather Service Module
Fetches weather data from Open-Meteo API with caching
"""
import math
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional


class WeatherService:
    """Fetches and caches weather data from Open-Meteo API."""

    API_URL = "https://api.open-meteo.com/v1/forecast"
    CURRENT_CACHE_DURATION = timedelta(minutes=15)
    FORECAST_CACHE_DURATION = timedelta(hours=1)

    # WMO Weather interpretation codes
    WEATHER_CODES = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    # WMO code -> unicode emoji mapping
    WEATHER_EMOJIS = {
        0: "\u2600\ufe0f",     # ☀️
        1: "\U0001f324\ufe0f", # 🌤️
        2: "\u26c5",           # ⛅
        3: "\u2601\ufe0f",     # ☁️
        45: "\U0001f32b\ufe0f",# 🌫️
        48: "\U0001f32b\ufe0f",# 🌫️
        51: "\U0001f326\ufe0f",# 🌦️
        53: "\U0001f326\ufe0f",# 🌦️
        55: "\U0001f327\ufe0f",# 🌧️
        56: "\U0001f327\ufe0f",# 🌧️
        57: "\U0001f327\ufe0f",# 🌧️
        61: "\U0001f326\ufe0f",# 🌦️
        63: "\U0001f327\ufe0f",# 🌧️
        65: "\U0001f327\ufe0f",# 🌧️
        66: "\U0001f327\ufe0f",# 🌧️
        67: "\U0001f327\ufe0f",# 🌧️
        71: "\U0001f328\ufe0f",# 🌨️
        73: "\U0001f328\ufe0f",# 🌨️
        75: "\u2744\ufe0f",    # ❄️
        77: "\U0001f328\ufe0f",# 🌨️
        80: "\U0001f326\ufe0f",# 🌦️
        81: "\U0001f327\ufe0f",# 🌧️
        82: "\U0001f327\ufe0f",# 🌧️
        85: "\U0001f328\ufe0f",# 🌨️
        86: "\u2744\ufe0f",    # ❄️
        95: "\u26c8\ufe0f",    # ⛈️
        96: "\u26c8\ufe0f",    # ⛈️
        99: "\u26c8\ufe0f",    # ⛈️
    }

    # Moon phase emojis (8 phases)
    MOON_PHASES = [
        ("\U0001f311", "New Moon"),
        ("\U0001f312", "Waxing Crescent"),
        ("\U0001f313", "First Quarter"),
        ("\U0001f314", "Waxing Gibbous"),
        ("\U0001f315", "Full Moon"),
        ("\U0001f316", "Waning Gibbous"),
        ("\U0001f317", "Last Quarter"),
        ("\U0001f318", "Waning Crescent"),
    ]

    def __init__(self, latitude: float, longitude: float, temperature_unit: str = "fahrenheit"):
        self.latitude = latitude
        self.longitude = longitude
        self.temperature_unit = temperature_unit
        self._current_cache: Optional[Dict] = None
        self._current_cache_time: Optional[datetime] = None
        self._forecast_cache: Optional[Dict] = None
        self._forecast_cache_time: Optional[datetime] = None

    def _is_current_cache_valid(self) -> bool:
        if self._current_cache is None or self._current_cache_time is None:
            return False
        return datetime.now() - self._current_cache_time < self.CURRENT_CACHE_DURATION

    def _is_forecast_cache_valid(self) -> bool:
        if self._forecast_cache is None or self._forecast_cache_time is None:
            return False
        return datetime.now() - self._forecast_cache_time < self.FORECAST_CACHE_DURATION

    def _get_weather_description(self, code: int) -> str:
        return self.WEATHER_CODES.get(code, "Unknown")

    def _get_weather_emoji(self, code: int) -> str:
        return self.WEATHER_EMOJIS.get(code, "\u2601\ufe0f")

    @staticmethod
    def _get_moon_phase(dt: datetime = None):
        """Calculate moon phase using the synodic month algorithm."""
        if dt is None:
            dt = datetime.now()
        # Known new moon: Jan 6, 2000 18:14 UTC
        known_new_moon = datetime(2000, 1, 6, 18, 14)
        synodic_month = 29.53058867
        days_since = (dt - known_new_moon).total_seconds() / 86400
        phase = (days_since % synodic_month) / synodic_month  # 0.0 to 1.0
        index = int(phase * 8) % 8
        emoji, name = WeatherService.MOON_PHASES[index]
        return {"emoji": emoji, "name": name, "phase": round(phase, 2)}

    def _temp_unit_symbol(self) -> str:
        return "\u00b0F" if self.temperature_unit == "fahrenheit" else "\u00b0C"

    def get_weather(self) -> Dict:
        """Get full weather data: current conditions + 5-day forecast."""
        current = self._get_current()
        forecast = self._get_forecast()
        moon = self._get_moon_phase()

        return {
            "current": current,
            "forecast": forecast,
            "moon": moon,
            "temperature_unit": self.temperature_unit,
            "unit_symbol": self._temp_unit_symbol(),
        }

    def _get_current(self) -> Dict:
        """Get current weather conditions."""
        if self._is_current_cache_valid():
            return {**self._current_cache, "cached": True}

        try:
            params = {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,uv_index,weather_code",
                "temperature_unit": self.temperature_unit,
                "wind_speed_unit": "mph",
                "timezone": "auto",
            }
            response = requests.get(self.API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            c = data.get("current", {})
            code = c.get("weather_code", 0)

            result = {
                "temperature": c.get("temperature_2m"),
                "feels_like": c.get("apparent_temperature"),
                "humidity": c.get("relative_humidity_2m"),
                "wind_speed": c.get("wind_speed_10m"),
                "uv_index": c.get("uv_index"),
                "weather_code": code,
                "description": self._get_weather_description(code),
                "emoji": self._get_weather_emoji(code),
                "cached": False,
            }
            self._current_cache = result
            self._current_cache_time = datetime.now()
            return result

        except requests.RequestException as e:
            if self._current_cache is not None:
                return {**self._current_cache, "cached": True, "error": str(e)}
            return {
                "temperature": None, "feels_like": None, "humidity": None,
                "wind_speed": None, "uv_index": None, "weather_code": None,
                "description": "Weather unavailable", "emoji": "\u2601\ufe0f",
                "cached": False, "error": str(e),
            }

    def _get_forecast(self) -> Dict:
        """Get 5-day daily forecast with sunrise/sunset."""
        if self._is_forecast_cache_valid():
            return {**self._forecast_cache, "cached": True}

        try:
            params = {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "daily": "temperature_2m_max,temperature_2m_min,weather_code,sunrise,sunset,uv_index_max",
                "temperature_unit": self.temperature_unit,
                "timezone": "auto",
                "forecast_days": 5,
            }
            response = requests.get(self.API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            daily = data.get("daily", {})

            days = []
            dates = daily.get("time", [])
            for i in range(len(dates)):
                code = daily["weather_code"][i]
                dt = datetime.strptime(dates[i], "%Y-%m-%d")
                days.append({
                    "date": dates[i],
                    "day_name": dt.strftime("%a").lower(),
                    "high": daily["temperature_2m_max"][i],
                    "low": daily["temperature_2m_min"][i],
                    "weather_code": code,
                    "description": self._get_weather_description(code),
                    "emoji": self._get_weather_emoji(code),
                    "sunrise": daily["sunrise"][i],
                    "sunset": daily["sunset"][i],
                    "uv_index_max": daily["uv_index_max"][i],
                })

            result = {"days": days, "cached": False}
            self._forecast_cache = result
            self._forecast_cache_time = datetime.now()
            return result

        except requests.RequestException as e:
            if self._forecast_cache is not None:
                return {**self._forecast_cache, "cached": True, "error": str(e)}
            return {"days": [], "cached": False, "error": str(e)}
