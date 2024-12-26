from decouple import config
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import jwt
from .models import User

JWT_SECRET_KEY = config('JWT_SECRET_KEY')


class AuthorizeError(Exception):
    pass


def create_jwt(email):

    return jwt.encode({'email': email}, JWT_SECRET_KEY, algorithm="HS256")


def valid_email(email):
    if email is None or email == '':
        return True, 'email cannot be empty'
    try:
        validate_email(email)
        return False, None
    except ValidationError:
        return True, 'email is incorrect'


def authorization(bearer_token):
    if bearer_token is None:
        raise AuthorizeError

    try:
        load_data = jwt.decode(
            bearer_token[7:], JWT_SECRET_KEY, algorithms=["HS256"]
            )
    except jwt.InvalidTokenError as e:
        raise AuthorizeError from e

    error, _ = valid_email(load_data.get('email'))
    if error:
        raise AuthorizeError
    objects = User.objects.filter(email=load_data.get('email'))
    if not objects.exists():
        raise AuthorizeError
    return objects[0]
