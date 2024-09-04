from app.models import CustomUser
import json
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from utils.jwt_utils import TokenGenration
from datetime import datetime,timezone
from utils.redis_utils import RedisClient

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            raise exceptions.AuthenticationFailed("Invalid Token Provided",400)
        
        if not token.startswith("Bearer"):
            raise exceptions.AuthenticationFailed("Invalid Token Provided",code=400)
        token = token.split(" ")[-1]
        
        payload = TokenGenration().decode(token)
        
        username = payload.get("sub") 
        user=None
        try:
            user = CustomUser.objects.get(id=username)
        except Exception as e:
            print('e: ', e)
            raise exceptions.AuthenticationFailed("Invalid Token Provided",code=400)
        expire = payload.get("exp")
        expiration_datetime = datetime.fromtimestamp(expire, tz=timezone.utc)
        if datetime.now(timezone.utc) > expiration_datetime:
            raise exceptions.AuthenticationFailed("Token has expired",code=401)
        
        get_user_token = RedisClient().get(f"token:{user.email}")
        
        if not get_user_token:
            raise exceptions.APIException("Token is invalid",200)
        
        saved_token = json.loads(get_user_token)
        if not get_user_token:
            raise exceptions.AuthenticationFailed("Invalid Token Provided",code=400)
        
        if saved_token["access_token"] != token:
            raise exceptions.AuthenticationFailed("Invalid Token provided",code=400)
        return user,None

