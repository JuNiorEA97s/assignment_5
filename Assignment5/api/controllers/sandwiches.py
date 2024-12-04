from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter()


@router.post("/sandwiches/", response_model=schemas.Sandwich)
def create_sandwich(sandwich: schemas.SandwichCreate, db: Session = Depends(get_db)):
    db_sandwich = models.Sandwich(**sandwich.dict())
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich


@router.get("/sandwiches/", response_model=list[schemas.Sandwich])
def read_all_sandwiches(db: Session = Depends(get_db)):
    return db.query(models.Sandwich).all()


@router.get("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich)
def read_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if db_sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return db_sandwich


@router.put("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich)
def update_sandwich(sandwich_id: int, sandwich: schemas.SandwichUpdate, db: Session = Depends(get_db)):
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    if db_sandwich.first() is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")

    update_data = sandwich.dict(exclude_unset=True)
    db_sandwich.update(update_data, synchronize_session=False)
    db.commit()
    return db_sandwich.first()


@router.delete("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich)
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    if db_sandwich.first() is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    db_sandwich.delete(synchronize_session=False)
    db.commit()
    return db_sandwich.first()
