from rest_framework.throttling import SimpleRateThrottle


class RegisterThrottle(SimpleRateThrottle):
    """
    Kayıt isteği engelleme"""

    scope = "registerThrottle"

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated or request.method == 'GET':
            return None  # Only throttle unauthenticated requests.
        """
        Kısıtlanmak istenen sayfaya POST işleminin yapılması
        """
        return self.cache_format % {
            "scope": self.scope,
            "ident": self.get_ident(request),
        }
