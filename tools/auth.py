import datetime

import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt import exceptions
from django.conf import settings
salt=settings.SECRET_KEY

class JwtQuerParamsAuthrntication(BaseAuthentication):

    def authenticate(self, request):


        token = request.META.get("HTTP_AUTHORIZATION")

        payload=None
        msg=None
        try:
            payload=jwt.decode(token,salt,True)
        except exceptions.ExpiredSignatureError:

            raise AuthenticationFailed({'code':1001,'msg':'token已经失效'})
        except jwt.DecodeError:

            raise AuthenticationFailed({'code': 1002, 'msg':'token认证失败'})
        except jwt.InvalidTokenError:


            raise AuthenticationFailed({'code': 1003, 'msg': '非法token'})

        return (payload,token)




def create_token(payload):
    headers={
        'typ':'jwt',
        'alg':'HS256'
    }

    # payload['exp']=datetime.datetime.utcnow()+datetime.timedelta(minutes=timeout)
    token=jwt.encode(payload=payload,key=salt,algorithm='HS256',
                     headers=headers).decode('utf-8')

    return token