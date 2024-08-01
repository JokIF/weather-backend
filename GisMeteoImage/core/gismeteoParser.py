from django.conf import settings
from django.utils.translation import get_language, gettext as _
from babel.dates import format_datetime

from GisMeteoImage.core.classes import BaseDataParser
from GisMeteoImage.utils.decorators import JsonData

from datetime import timedelta, datetime, timezone
from typing import Optional


_ = str
json_data = JsonData("data")

    
class GismeteoParser(BaseDataParser):
    def __init__(self, data: dict, lang: Optional[str] = "ru_ru") -> None:
        super().__init__(data, lang)
        self._pressure = None
        self._wind_speed = None 
        self._wind_direction = None
        self._precipitation_type = None
        self._local = None
        self._icon = None
        self._tz = None

    @json_data("wind", "direction", "scale_8")
    def __wind_direction(self, wind_direction):
        match int(wind_direction):
            case 0:
                return _("calm")
            case 1:
                return _("N ↑")
            case 2:
                return _("N-E ↗")
            case 3:
                return _("E →")
            case 4:
                return _("S-E ↘")
            case 5:
                return _("S ↓")
            case 6:
                return _("S-W ↙")
            case 7:
                return _("W ←")
            case 8:
                return _("N-W ↖")

    @json_data("wind", "speed", "m_s")    
    def __wind_speed(self, wind_speed):
        return int(wind_speed)
    
    @json_data("pressure", "mm_hg_atm")
    def __pressure_value(self, value):
        return int(value)

    @json_data("precipitation", "type")
    def __precipitation_type(self, type_):
        PRECIPITATION_TYPES = {
            0: _("No precipitation"),
            1: _("rain"),
            2: _("snow"),
            3: _("Mixed rainfall")
        }
        return PRECIPITATION_TYPES[int(type_)], int(type_)

    @json_data("precipitation", "intensity")
    def __precipitation_intensity(self, intensity):
        PRECIPITATION_INTENSITY_TYPES = {
            1: _("Small"),
            2: "",
            3: _("heavy")
        }
        return PRECIPITATION_INTENSITY_TYPES[int(intensity)]
    
    @json_data("icon")
    def __define_icon(self, icon_name) -> str:
        match icon_name.split("_"):
            case [*_, "st"]:
                return "st"
            case [*_, ("r1" | "r2" | "r3") as rain]:
                return rain
            case [*_, ("s1" | "s2" | "s3") as snow]:
                return snow
            case [*_, ("rs1" | "rs2" | "rs3") as rsnow]:
                return rsnow
            case [("d" | "n") as day_night, *addition]:
                match addition:
                    case [("c1" | "c2" | "c3") as cloud, *_]:
                        return f"{day_night}_{cloud}"
                    case _:
                        return day_night
            case ["c1" | "c2" | "c3" as cloud]:
                return cloud

    @json_data("date", "local")
    def __get_local(self, local_iso: str):
        dtime = datetime.fromisoformat(local_iso)
        dtime = dtime.replace(tzinfo=self.tz)
        return dtime

    @json_data("date", "time_zone_offset")
    def __get_tz(self, tz_time) -> timezone:
        return timezone(timedelta(minutes=float(tz_time)))
    

    @property
    @json_data("humidity", "percent")    
    def humidity(self, value):
        return int(value)
    

    @property
    @json_data("precipitation", "amount")
    def precipitation_amount(self, amount):
        return int(amount)
    
    @property
    @json_data("temperature", "comfort", "C")
    def temperature(self, temper):
        return f"{round(temper):+}"

    @property
    @json_data("temperature", "water", "C")
    def temperature_water(self, temper):
        return f"{round(temper):+}"
    
    @property
    @json_data("temperature", "air", "C")
    def temperature_air(self, temper):
        return f"{round(temper):+}"

    @property
    @json_data("description", "full")
    def description(self, description_text):
        return description_text
    
    @property
    def wind(self):
        self._wind_speed = self._wind_speed or self.__wind_speed()
        self._wind_direction = self._wind_direction or self.__wind_direction()
        return _("%(speed)s m/s \n%(direction)s") % {"speed": self._wind_speed, "direction": self._wind_direction}
    
    @property
    def pressure(self):
        if self._pressure is None:
            self._pressure = self.__pressure_value()
        return _("%s \nmm Hg") % (self._pressure,)
    
    @property
    def precipitation(self):
        if self._precipitation_type is not None:
            return self._precipitation_type 
        type_, type_id = self.__precipitation_type()
        if type_id == 3 or type_id == 0:
            self._precipitation_type = type_
        else:
            self._precipitation_type = f"{self.__precipitation_intensity()} {type_}"
        return self._precipitation_type
    
    @property
    def icon(self) -> str:
        if self._icon is None:
            self._icon = settings.ICON_DIR / (self.__define_icon() + '.png')
        return self._icon
    
    
    @property
    def tz(self) ->timezone:
        if self._tz is None:
            self._tz = self.__get_tz()
        return self._tz

    @property
    def local(self) -> datetime:
        if self._local is None:
            self._local = self.__get_local()
        return self._local
    
    @property
    def time(self) -> str:
        return self.local.strftime("%H:%M")
    
    @property
    def weekday(self) -> str:
        return format_datetime(datetime=self.local, format="EEEE", locale=self.lang)
    
    @property
    def month(self) -> str:
        return format_datetime(datetime=self.local, format="d MMMM", locale=self.lang)
