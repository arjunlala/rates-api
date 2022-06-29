from fastapi import FastAPI, Depends, Path
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Pensford).all()


@app.get("/sofr/{mat_date}/{floor}/{ceiling}/{spread}")
def read_api(mat_date: str, floor: float, ceiling: float, spread: float, db: Session = Depends(get_db)):
    list_of_pensfords = db.query(models.Pensford).all()
    sofr_list = []
    for row in list_of_pensfords:
        row = row.__dict__
        ref_date = row.get("maturity_date")
        if (ref_date == mat_date):
            break
        else:
            new_sofr = row.get("sofr")/100 + spread
            if (new_sofr > ceiling):
                row["sofr"] = ceiling
            elif (new_sofr < floor):
                row["sofr"] = floor
            else:
                row["sofr"] = new_sofr
            del row["libor"]
            sofr_list.append(row)
    return sofr_list


@app.get("/libor/{mat_date}/{floor}/{ceiling}/{spread}")
def read_api(mat_date: str, floor: float, ceiling: float, spread: float, db: Session = Depends(get_db)):
    list_of_pensfords = db.query(models.Pensford).all()
    libor_list = []
    for row in list_of_pensfords:
        row = row.__dict__
        ref_date = row.get("maturity_date")
        if (ref_date == mat_date):
            break
        else:
            new_libor = row.get("libor")/100 + spread
            if (new_libor > ceiling):
                row["libor"] = ceiling
            elif (new_libor < floor):
                row["libor"] = floor
            else:
                row["libor"] = new_libor
            del row["sofr"]
            libor_list.append(row)
    return libor_list
