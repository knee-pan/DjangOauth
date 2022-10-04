from rest_framework.throttling import SimpleRateThrottle


class RegisterThrottle(SimpleRateThrottle):
    """
    Kayit isteği engelleme"""

    scope = "registerThrottle"

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated or request.method == 'GET':
            return None  # Only throttle unauthenticated requests.
        """
        Kisitlanmak istenen sayfaya POST işleminin yapilmasi
        """
        return self.cache_format % {
            "scope": self.scope,
            "ident": self.get_ident(request),
        }
