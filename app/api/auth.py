


from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from jose import JWTError, jwt 


ALGORITHM = 'HS256'
SECRET_KEY = 'sdjfa;lsdkjf;aklsjdf;asdkljf;klasdj'


bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl = 'auth/token')

    
class Token(BaseModel):
    access_token: str 
    token_type: str 

def hash_password(password:str):
    return bcrypt_context.hash(password)

def check_password(password:str , hashed_password:str):
    return bcrypt_context.verify(password , hashed_password)

def create_access_token(email:str , id:int , expires_delta: timedelta):
    encode = {'sub':str(id) , 'email':email}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY , algorithm = ALGORITHM)

def get_current_user(token:str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        email: str = payload.get('email')
        id: int = payload.get('sub')
        if email is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        else:
            return id
    except JWTError:
              raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")