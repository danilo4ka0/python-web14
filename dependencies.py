import jwt
from fastapi import HTTPException

SECRET_KEY = "your_secret_key"

def verify_email(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

# Функція для обмеження кількості запитів
def rate_limit(request):
    return request.client.host
