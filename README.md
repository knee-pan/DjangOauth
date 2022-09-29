# DjangOauth
Django Oauth Sample

* python manage.py createsuperuser
* django-admin startapp account
* pipenv install django-oauth-toolkit

```
INSTALLED_APPS = [
    ...
    "account",
    "oauth2_provider",
]


urlpatterns = [
    ...
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
```
* Yeni bir projeye başlıyorsanız, varsayılan Users modeli sizin için yeterli olsa bile özel bir Users modeli kurmanız önemle tavsiye edilir.
* Bu model, varsayılan user modeliyle aynı şekilde davranır, ancak ihtiyaç duyulursa gelecekte bunu özelleştirebileceksiniz. 
```
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
```
* settings.py'da hangi user modelinin kullanılacağını belirtmek gerek : ``` AUTH_USER_MODEL='account.User'```

* ```shell python manage.py makemigrations, migrate ```

* This will make available endpoints to authorize, generate token and create OAuth applications.

* Last change, add LOGIN_URL to iam/settings.py:```shell LOGIN_URL='/admin/login/'```

* createsuper user and open localhost/admin, there you will see django oauth-toolkit

* http://127.0.0.1:7000/o/applications/register/

* clientId : DVfYFIoj8bYJUd2lKeEKVNuvbctKxEWt7xGVa3Tq
* clientSecret : pbkdf2_sha256$260000$pqjMtV3Uq6mDOxvvZGsZmE$WjliiFCsXHapmqgSA6v6gEnDoXxaBZHYb2LLBBirDks=
* save clientId & clientSecret

* {name: web-app, 'clientId': --- 'clientSecret': ----, clientType: confidential, AuthType: Authorization code, redirect uris: localhost/noexist/call}

* ``` export ID=clientID, export SECRET=clientSecret ```

* Now let’s generate an authentication code grant with PKCE (Proof Key for Code Exchange), useful to prevent authorization code injection. 

* To do so, you must first generate a code_verifier random string between 43 and 128 characters, which is then encoded to produce a code_challenge:

```
import random
import string
import base64
import hashlib

code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
code_verifier = base64.urlsafe_b64encode(code_verifier.encode('utf-8'))

code_challenge = hashlib.sha256(code_verifier).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')
```

* save the code_challenge : FvWWc5XFqUCJkf2KCGLLaynkhcpj2mVSQXzIP1-4oxk
* code_verifier output : b'ODRYTjlSMzZHWFg2MkhNM1ROSEYxSU5GRkpNNTJDUElTQllQVFNCQjhWUlhQSzdYTTVTSTAyVEpZQTZESFdFRFk3TkdCWVNNWlpVWDVLVEdCOVI5RjBMN1A2UFg5TVpISDRUMDdYUDE2RjUzUllRT1hRN1NDQUVEMEw='
* save as the code_verifier like this : ODRYTjlSMzZHWFg2MkhNM1ROSEYxSU5GRkpNNTJDUElTQllQVFNCQjhWUlhQSzdYTTVTSTAyVEpZQTZESFdFRFk3TkdCWVNNWlpVWDVLVEdCOVI5RjBMN1A2UFg5TVpISDRUMDdYUDE2RjUzUllRT1hRN1NDQUVEMEw=

* http://127.0.0.1:7000/o/authorize/?response_type=code&code_challenge=FvWWc5XFqUCJkf2KCGLLaynkhcpj2mVSQXzIP1-4oxk&client_id=DVfYFIoj8bYJUd2lKeEKVNuvbctKxEWt7xGVa3Tq&redirect_uri=http://django-oauth-toolkit.herokuapp.com/consumer/exchange/

* Bu, uygulamanızı tanımlar, kullanıcıdan kaynaklarına erişmesi için uygulamanızı yetkilendirmesi istenir.
Note the parameters we pass:

* response_type: code
* code_challenge: FvWWc5XFqUCJkf2KCGLLaynkhcpj2mVSQXzIP1-4oxk
* client_id: vW1RcAl7Mb0d5gyHNQIAcH110lWoOW2BmWJIero8
* redirect_uri: http://django-oauth-toolkit.herokuapp.com/consumer/exchange/


* http://django-oauth-toolkit.herokuapp.com/consumer/exchange/'i redirect_uri olarak kullandığımızı unutmayın, bir Sayfa bulunamadı (404) alacaksınız, ancak aşağıdaki gibi bir url alırsanız işe yaradı:

* "GET /noexist/callback?code=QCo4MxPjwAiO8dn8L7w2WZjO426Z3n HTTP/1.1" 404 2389

* Bu, size bir kod vermeye çalışan OAuth2 sağlayıcısıdır. bu durumda export CODE=QCo4MxPjwAiO8dn8L7w2WZjO426Z3n

# ya da

* http://django-oauth-toolkit.herokuapp.com/consumer/exchange/?code=WwBJqUuCovGQlQMJK49M76nIOl6W3K olarak dönerken code : WwBJqUuCovGQlQMJK49M76nIOl6W3K

* Now that you have the user authorization is time to get an access token:

```curl -X POST \
    -H "Cache-Control: no-cache" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    "http://127.0.0.1:7000/o/token/" \
    -d "client_id=${ID}" \
    -d "client_secret=${SECRET}" \
    -d "code=${CODE}" \
    -d "code_verifier=${CODE_VERIFIER}" \
    -d "redirect_uri=http://django-oauth-toolkit.herokuapp.com/consumer/exchange/" \
    -d "grant_type=authorization_code" 
    ```

* dönen değer:
```
{
  "access_token": "jooqrnOrNa0BrNWlg68u9sl6SkdFZg",
  "expires_in": 36000,
  "token_type": "Bearer",
  "scope": "read write",
  "refresh_token": "HNvDQjjsnvDySaK0miwG4lttJEl9yD"
}
```
* To access the user resources we just use the access_token:
```
curl \
    -H "Authorization: Bearer jooqrnOrNa0BrNWlg68u9sl6SkdFZg" \
    -X GET http://localhost:8000/resource
```
* {"error": "invalid_client"}% Error Handling :  



# Credential içinde aynı

* http://127.0.0.1:7000/o/applications/register/
* credential seç ve redirect uris yazma
```
import base64
client_id = "IYEyUyqwx142atdCvkOLfMJLJxYxaoqCEih6a5kA"
secret = "pbkdf2_sha256$260000$OEa9fgO8QBMmscqtWv4aAq$PzE4lGe8V1SixoEdyX5v4Pvrk4V+sjo7rK0kr6bpI2I="
credential = "{0}:{1}".format(client_id, secret)
base64.b64encode(credential.encode("utf-8"))

export CREDENTIAL=SVlFeVV5cXd4MTQyYXRkQ3ZrT0xmTUpMSnhZeGFvcUNFaWg2YTVrQTpwYmtkZjJfc2hhMjU2JDI2MDAwMCRPRWE5ZmdPOFFCTW1zY3F0V3Y0YUFxJFB6RTRsR2U4VjFTaXhvRWR5WDV2NFB2cms0Vitzam83ckswa3I2YnBJMkk9

curl -X POST \
    -H "Authorization: Basic ${CREDENTIAL}" \
    -H "Cache-Control: no-cache" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    "http://127.0.0.1:7000/o/token/" \
    -d "grant_type=client_credentials"


* {"error": "invalid_client"}%
 ```

# CORS

* Django'da geliştirilen uygulamaların, farklı etki alanlarında (hatta yalnızca farklı bağlantı noktalarında) barındırılan diğer uygulamalarla etkileşime girmesi gerekebilir. Bu isteklerin başarılı olması için sunucunuzda kaynaklar arası kaynak paylaşımını (CORS) kullanmanız gerekir. CORS, farklı etki alanlarında barındırılan kaynaklarla etkileşime izin veren bir mekanizmadır. 

* CORS'un nasıl çalıştığını göstermek için, domain.com'da yaşayan bir web uygulamanız olduğunu varsayalım. Ancak uygulama, kullanıcı bilgilerini kaydetmek için başka bir URL'de barındırılan bir API'yi çağırır; örneğin, api.domain.com. ( örn google ile giriş) Bu nedenle, api.domain.com'a veri kaydetme isteği gönderildiğinde, sunucu istekleri başlıklarına ve isteğin kaynağına göre değerlendirir. Sunucuda domain.com URL'sine izin verirseniz, uygun yanıtı sağlayacaktır. Etki alanına izin verilmiyorsa, sunucu bir hata verir. Bu bilgi alışverişi, HTTP başlıkları kullanılarak gerçekleşir.

```

MIDDLEWARE = [
    ...
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsPostCsrfMiddleware",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False


CORS_ORIGIN_WHITELIST = (
    "google.com",
    "localhost:8000",
    "127.0.0.1:9000",
    "http://localhost:7000",
)

CSRF_TRUSTED_ORIGINS = [
    "http://change.allowed.com",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
```
* Yukarıdaki yapılandırmadan fazlasını gerektiren bir kullanım durumunuz varsa, belirli bir isteğe izin verilip verilmeyeceğini kontrol etmek için kod ekleyebilirsiniz.
```
from corsheaders.signals import check_request_enabled

from .models import ModelName


def cors_allow_mymodel(sender, request, **kwargs):
    return ModelName.objects.filter(host=request.host).exists()


check_request_enabled.connect(cors_allow_mymodel)

```
* apps.py : 
```
class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"

    def ready(self):
        import account.handlers

```



* go to http://localhost:8000/admin and log in
* After that point your browser to http://localhost:8000/o/applications/ and add an Application instance.
* Client id and Client Secret are automatically generated; you have to provide the rest of the informations.

```
CSRF_TRUSTED_ORIGINS = [
    "http://change.allowed.com",
    "http://django-oauth-toolkit.herokuapp.com/consumer/exchange/",
]
```

* http://127.0.0.1:7000/o/applications/register/

* clientId : DVfYFIoj8bYJUd2lKeEKVNuvbctKxEWt7xGVa3Tq
* clientSecret : pbkdf2_sha256$260000$pqjMtV3Uq6mDOxvvZGsZmE$WjliiFCsXHapmqgSA6v6gEnDoXxaBZHYb2LLBBirDks=

* http://127.0.0.1:7000/o/authorize/?response_type=code&code_challenge=FvWWc5XFqUCJkf2KCGLLaynkhcpj2mVSQXzIP1-4oxk&client_id=DVfYFIoj8bYJUd2lKeEKVNuvbctKxEWt7xGVa3Tq&redirect_uri=http://django-oauth-toolkit.herokuapp.com/consumer/exchange/

Dönen kod :-> http://django-oauth-toolkit.herokuapp.com/consumer/exchange/?code=WwBJqUuCovGQlQMJK49M76nIOl6W3K

curl -X POST -H "Cache-Control: no-cache" -H "Content-Type: application/x-www-form-urlencoded" "http://127.0.0.1:7000/o/token/" -d "client_id=${ID}" -d "client_secret=${SECRET}" -d "code=${CODE}" -d "redirect_uri=http://django-oauth-toolkit.herokuapp.com/consumer/exchange/" -d "grant_type=authorization_code"


**** test your oauth2 provider (sample consumer) : http://django-oauth-toolkit.herokuapp.com/consumer/
**** http://django-oauth-toolkit.herokuapp.com/consumer/exchange/?state=random_state_string&response_type=code&client_id=DVfYFIoj8bYJUd2lKeEKVNuvbctKxEWt7xGVa3Tq

# REDIS - Django Üzerinde Redis Cache

* ``` brew install redis / brew uninstall redis ```
* ``` brew list ```

* Başlangıçta redis açılsın istiyorsak: ``` ln -sfv /usr/local/opt/redis/*.plist ~/Library/LaunchAgents ```

* Brew aracılığı ile Redis sunucumuzu başlatalım: ``` brew services start redis ```
* Konfigürasyon dosyası kullanarak Redis’i başlatmak:  ``` redis-server /usr/local/etc/redis.conf ```
* ``` brew services stop redis ```
* ``` redis config konumu : /usr/local/etc/redis.conf ```
* ``` redis paket detayı : brew info redis ```
* ``` redis çalışma test : redis-cli ping ```
* ``` pipenv install django-redis-cache  ```
```

CACHES = {
"default": {
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": "redis://127.0.0.1:6379",
    "OPTIONS": {
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
    }
  }
}

```

``` 
redis-cli
```

``` 
redis-cli client list
```

### Note : If you haven't installed 'drf_yasg', swagger will not work. 

``` 
https://www.jasonmars.org/2020/04/22/add-swagger-to-django-rest-api-quickly-4-mins-without-hiccups/
```
