from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Origin
from ..schemas import OriginResponse

router = APIRouter(prefix="/api/v1/origins", tags=["origins"])


@router.get("", response_model=list[OriginResponse])
def list_origins(db: Session = Depends(get_db)):
    return db.query(Origin).all()


@router.get("/{slug}", response_model=OriginResponse)
def get_origin(slug: str, db: Session = Depends(get_db)):
    origin = db.query(Origin).filter(Origin.slug == slug).first()
    if not origin:
        raise HTTPException(status_code=404, detail="Origin not found")
    return origin
