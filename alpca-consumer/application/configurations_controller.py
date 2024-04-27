from pydantic import BaseModel, EmailStr
from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import json
from domain.models.configuration import Configuration, SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ConfigurationData(BaseModel):
    subscriber_emails: List[EmailStr]
    run_check: bool


@router.post("/configurations/", response_model=ConfigurationData)
def create_or_update_configuration(
    config_data: ConfigurationData,
    db: Session = Depends(get_db)
):
    config = db.query(Configuration).filter(Configuration.id == 1).first()
    if config:
        config.subscribers = json.dumps(config_data.subscriber_emails)
        config.run_check = config_data.run_check
    else:
        config = Configuration(
            subscriber_list=json.dumps(config_data.subscriber_emails),
            run_check=config_data.run_check
        )
        db.add(config)

    db.commit()

    return {
        "subscriber_emails": json.loads(config.subscribers),
        "run_check": config.run_check
    }


@router.get("/configurations")
def read_configuration(db: Session = Depends(get_db)):
    config = db.query(Configuration).filter(Configuration.id == 1).first()
    if not config:
        return {}
    return {"run_check": config.run_check, "subscribers": config.subscriber_list}
