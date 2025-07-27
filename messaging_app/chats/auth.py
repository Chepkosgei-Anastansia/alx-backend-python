from rest_framework_simplejwt.tokens import RefreshToken
from chats.models import User


def get_tokens_for_user(user: User):
    """
    Generates refresh and access tokens for a given user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
