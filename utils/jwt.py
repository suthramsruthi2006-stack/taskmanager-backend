from jose import jwt
from datetime import datetime, timedelta
SECRET_KEY = "secret123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encodee = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encodee.update({
        "exp": expire
    })
    encode_jwt = jwt.encode(
        to_encodee,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encode_jwt