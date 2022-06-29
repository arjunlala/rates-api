from sqlalchemy import Column, Float, String
from database import Base


class Pensford(Base):
    __tablename__ = "monthly_rates"
    maturity_date = Column(String, primary_key=True, index = True)
    sofr = Column(Float)
    libor = Column(Float)
