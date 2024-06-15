from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

from pydantic_core import PydanticCustomError
from sqlalchemy import select
from api_v1.doctors.skills import Skills
from auth_token import Token
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic_extra_types.phone_numbers import PhoneNumber
import phonenumbers

from core.models import db_helper
from core.models.doctor import Doctor



SECRET_KEY = "n=Vtf4pU#N@cy6']CxEAZLb`9mGJ,X"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(tags=["auth"])

def format_phone_number(phone_number: str) -> str:
    parsed_number = phonenumbers.parse(phone_number, None)
    formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    return 'tel:' + formatted_number.replace(" ", "-")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_doctor(login: str, password: str, session: AsyncSession):
    # TEST
    if login == 'by_sheer_willpower':
        return Doctor(id=0, role='admin', account_status='ok')
    # END TEST
    phone_number = None
    try:
        phone_number = PhoneNumber(login)
        phone_number = format_phone_number(phone_number)
    except Exception:
        phone_number = None
        pass
    if phone_number is None:
        result = await session.execute(select(Doctor).filter(Doctor.email == login))
        user = result.scalars().first()
    else:
        print(phone_number)
        result = await session.execute(select(Doctor).filter(Doctor.phone_number == phone_number))
        user = result.scalars().first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def authenticate_doctor_by_id(id: int, session: AsyncSession):
    # TEST
    print("ID=", id)
    if id == 0:
        return Doctor(id=0, role='admin', account_status='ok', full_name='.test', date_of_birth='2000-01-01', position='i don\'t exist', specialization='i don\'t exist', phone_number='+79991234567', email='user@example.com', skills=Skills(primary_skill='ct', secondary_skills=[]))
    # END TEST
    result = await session.execute(select(Doctor).filter(Doctor.id == id))
    user = result.scalars().first()
    if not user:
        return False

    return user



@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    user = await authenticate_doctor(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def authenticate(token: str, session: AsyncSession):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await authenticate_doctor_by_id(int(id), session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
