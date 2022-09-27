# DjangOauth
Django Oauth Sample

* python manage.py createsuperuser
* django-admin startapp account
* pipenv install django-oauth-toolkit

INSTALLED_APPS = [
    ...
    "account",
    "oauth2_provider",
]


urlpatterns = [
    ...
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

* Yeni bir projeye başlıyorsanız, varsayılan Users modeli sizin için yeterli olsa bile özel bir Users modeli kurmanız önemle tavsiye edilir.
* Bu model, varsayılan user modeliyle aynı şekilde davranır, ancak ihtiyaç duyulursa gelecekte bunu özelleştirebileceksiniz. 

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

* settings.py'da hangi user modelinin kullanılacağını belirtmek gerek : AUTH_USER_MODEL='account.User'

* python manage.py makemigrations, migrate

* This will make available endpoints to authorize, generate token and create OAuth applications.

* Last change, add LOGIN_URL to iam/settings.py: LOGIN_URL='/admin/login/'

* createsuper user and open localhost/admin, there you will see django oauth-toolkit

* http://127.0.0.1:7000/o/applications/register/

* save clientId & clientSecret

* {name: web-app, 'clientId': --- 'clientSecret': ----, clientType: confidential, AuthType: Authorization code, redirect uris: localhost/noexist/call}

* export ID=clientID, export SECRET=clientSecret

* Now let’s generate an authentication code grant with PKCE (Proof Key for Code Exchange), useful to prevent authorization code injection. 

* To do so, you must first generate a code_verifier random string between 43 and 128 characters, which is then encoded to produce a code_challenge:


import random
import string
import base64
import hashlib

code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
code_verifier = base64.urlsafe_b64encode(code_verifier.encode('utf-8'))

code_challenge = hashlib.sha256(code_verifier).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')

* save the code_challenge : TeR-uyQljNEquUFq1FPELneY2hAG1xR1sge5-8-H8J4

* http://127.0.0.1:8000/o/authorize/?response_type=code&code_challenge=TeR-uyQljNEquUFq1FPELneY2hAG1xR1sge5-8-H8J4&client_id=x6OuNUjboMa9Jq78lObiFyYNjK7C3DpCcSimfRI9&redirect_uri=http://127.0.0.1:7000/noexist/callback

* Bu, uygulamanızı tanımlar, kullanıcıdan kaynaklarına erişmesi için uygulamanızı yetkilendirmesi istenir.
Note the parameters we pass:

* response_type: code
* code_challenge: XRi41b-5yHtTojvCpXFpsLUnmGFz6xR15c3vpPANAvM
* client_id: vW1RcAl7Mb0d5gyHNQIAcH110lWoOW2BmWJIero8
* redirect_uri: http://127.0.0.1:7000/noexist/callback


* http://127.0.0.1:7000/noexist/callback'i redirect_uri olarak kullandığımızı unutmayın, bir Sayfa bulunamadı (404) alacaksınız, ancak aşağıdaki gibi bir url alırsanız işe yaradı:

* /noexist/callback?code=LdbkKk2B4bJBQagg78Ws4er9Teu27j

* Bu, size bir kod vermeye çalışan OAuth2 sağlayıcısıdır. bu durumda export CODE=LdbkKk2B4bJBQagg78Ws4er9Teu27j

* Now that you have the user authorization is time to get an access token:

* curl -X POST \
    -H "Cache-Control: no-cache" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    "http://127.0.0.1:7000/o/token/" \
    -d "client_id=${ID}" \
    -d "client_secret=${SECRET}" \
    -d "code=${CODE}" \
    -d "code_verifier=${CODE_VERIFIER}" \
    -d "redirect_uri=http://127.0.0.1:7000/noexist/callback" \
    -d "grant_type=authorization_code"


