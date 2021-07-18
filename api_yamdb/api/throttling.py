from rest_framework.throttling import ScopedRateThrottle, SimpleRateThrottle

STAFF = ('moderator', 'admin')


class NonEmployeeRateThrottle(SimpleRateThrottle):
    scope = 'non-employee'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated and request.user.role in STAFF:
            return None
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


class NonEmployeeScopedRateThrottle(ScopedRateThrottle):

    def get_cache_key(self, request, view):
        if request.user.is_authenticated and request.user.role in STAFF:
            return None
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }
