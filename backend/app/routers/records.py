from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..models import CoffeeRecord, Origin
from ..schemas import CoffeeRecordInput, CoffeeRecordResponse

router = APIRouter(prefix="/api/v1/records", tags=["records"])


def get_owned_record(record_id: int, uid: str, db: Session) -> CoffeeRecord:
    record = db.query(CoffeeRecord).filter(
        CoffeeRecord.id == record_id,
        CoffeeRecord.firebase_uid == uid,
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


def validate_origin(origin_id: int | None, db: Session):
    if origin_id is not None and not db.query(Origin.id).filter(Origin.id == origin_id).first():
        raise HTTPException(status_code=400, detail="Origin not found")


@router.get("", response_model=list[CoffeeRecordResponse])
def list_records(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(CoffeeRecord).filter(
        CoffeeRecord.firebase_uid == user["uid"]
    ).order_by(CoffeeRecord.drank_at.desc(), CoffeeRecord.id.desc()).all()


@router.post("", response_model=CoffeeRecordResponse, status_code=status.HTTP_201_CREATED)
def create_record(payload: CoffeeRecordInput, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    validate_origin(payload.origin_id, db)
    record = CoffeeRecord(firebase_uid=user["uid"], **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.put("/{record_id}", response_model=CoffeeRecordResponse)
def update_record(record_id: int, payload: CoffeeRecordInput, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    record = get_owned_record(record_id, user["uid"], db)
    validate_origin(payload.origin_id, db)
    for field, value in payload.model_dump().items():
        setattr(record, field, value)
    record.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(record)
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    record = get_owned_record(record_id, user["uid"], db)
    db.delete(record)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
