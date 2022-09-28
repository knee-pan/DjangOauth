from corsheaders.signals import check_request_enabled

from .models import User


def cors_allow_myuser(sender, request, **kwargs):
    return User.objects.filter(host=request.host).exists()


check_request_enabled.connect(cors_allow_myuser)


# def cors_allow_api_to_everyone(sender, request, **kwargs):
#     return request.path.startswith("/api/")


# check_request_enabled.connect(cors_allow_api_to_everyone)
