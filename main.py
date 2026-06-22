from fastapi import FastAPI,HTTPException,Depends,Header
from jose import jwt
from datetime import datetime, timedelta,timezone

app = FastAPI()

SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

def create_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#token generate

@app.post("/login")
def login(username: str, password: str):
    # For demonstration purposes, we are using hardcoded username and password
    if username == "user" and password == "password":
        token = create_token({"sub": username})
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    #token verify

def verify_token(token: str = Header(None)):
       
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return username
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        #protected route
@app.get("/protected")
def protected_route(username: str = Depends(verify_token)):
    return {"message": f"Hello, {username}. You have access to this protected route."}
