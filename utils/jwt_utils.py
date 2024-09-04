from datetime import datetime, timedelta, timezone
import jwt
from config.config import JwtSettings
from rest_framework.exceptions import AuthenticationFailed

class TokenGenration:
    
    def __init__(self):
        jwt_setting = JwtSettings()
        self.ACCESS_TOKEN_EXPIRE_MINUTES = jwt_setting.ACCESS_TOKEN_EXPIRE_MINUTES
        self.REFRESH_TOKEN_EXPIRE_MINUTES =jwt_setting. REFRESH_TOKEN_EXPIRE_MINUTES
        self.SECRET_KEY = jwt_setting.SECRET_KEY
        self.ALGORITHM = jwt_setting.ALGORITHM
    
    def decode(self,token):
        try:
            return jwt.decode(token,self.SECRET_KEY,algorithms=[self.ALGORITHM])
        except Exception as e:
            raise AuthenticationFailed(detail="Token is invalid",code=400)
    
    def encode_jwt(self,data):
        return jwt.encode(data,self.SECRET_KEY,algorithm=self.ALGORITHM)
    
    def create_access_token(self,data:dict):
        data.update({'exp':datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)})
        return self.encode_jwt(data)
    
    def create_refresh_token(self,data:dict):
        data.update({"exp":datetime.now(timezone.utc) + timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES)})
        return self.encode_jwt(data)