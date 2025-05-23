from fastapi import APIRouter, Depends, status, Response
from enum import Enum
from typing import List

from sqlalchemy.orm import Session

from auth.outh2 import get_current_user
from db import db_user
from db.database import get_db
from db.models import DbUser
from schemas import UserBase, UserDisplay

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


@router.get('/', response_model=List[UserDisplay])
def get_users(db: Session = Depends(get_db), current_user: UserBase =Depends(get_current_user)):
    return db_user.get_all_users(db)


@router.get('/{id}', response_model=UserDisplay)
def get_user(id:int, db: Session = Depends(get_db), current_user: UserBase =Depends(get_current_user)):
    return db_user.get_user(db, id)


@router.put('/{id}', response_model=UserDisplay)
def update_user(id: int, request: UserBase, db: Session = Depends(get_db), current_user: UserBase =Depends(get_current_user)):
    return db_user.update_user(db, id, request)


@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db)):
    return db_user.delete_user(db, id)

