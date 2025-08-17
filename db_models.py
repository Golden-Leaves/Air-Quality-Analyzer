from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float,DateTime
from datetime import datetime
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
class Weather(db.Model):
    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Location
    city_name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(10), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    # Weather condition
    weather_id: Mapped[int] = mapped_column(Integer, nullable=False)  # condition id (e.g. 804)
    weather_main: Mapped[str] = mapped_column(String(50), nullable=False)  # "Clouds"
    weather_description: Mapped[str] = mapped_column(String(100), nullable=False)  # "overcast clouds"
    icon_code: Mapped[str] = mapped_column(String(10), nullable=False)  # 04d

    # Main meteorology
    temp_c: Mapped[float] = mapped_column(Float, nullable=False)  
    feels_like_c: Mapped[float] = mapped_column(Float, nullable=False)
    temp_min_c: Mapped[float] = mapped_column(Float, nullable=False)
    temp_max_c: Mapped[float] = mapped_column(Float, nullable=False)
    pressure_hpa: Mapped[int] = mapped_column(Integer, nullable=False)
    humidity: Mapped[int] = mapped_column(Integer, nullable=False)
    sea_level_hpa: Mapped[int] = mapped_column(Integer, nullable=True)
    ground_level_hpa: Mapped[int] = mapped_column(Integer, nullable=True)

    # Visibility
    visibility_m: Mapped[int] = mapped_column(Integer, nullable=True)

    # Wind
    wind_speed_mps: Mapped[float] = mapped_column(Float, nullable=False)
    wind_deg: Mapped[int] = mapped_column(Integer, nullable=False)
    wind_gust_mps: Mapped[float] = mapped_column(Float, nullable=True)

    # Clouds
    cloud_pct: Mapped[int] = mapped_column(Integer, nullable=False)

    # System info
    sunrise: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sunset: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Metadata
    ts: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # "dt"
    timezone_offset: Mapped[int] = mapped_column(Integer, nullable=False)
    source_id: Mapped[int] = mapped_column(Integer, nullable=False)  # OWM city ID
    
class AirData(db.Model):
    __tablename__ = "air_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    ts: Mapped[datetime] = mapped_column(DateTime, nullable=False)  #Timestamp at the time of reading
    aqi_us: Mapped[int] = mapped_column(Integer, nullable=False) #We are using the US's standards
    main_pollutant_us: Mapped[str] = mapped_column(String(10), nullable=False)
    
    def __repr__(self) -> str:
        return f"<AirData(city='{self.city}', aqi_us={self.aqi_us}, temp={self.temperature_c}°C)>"
