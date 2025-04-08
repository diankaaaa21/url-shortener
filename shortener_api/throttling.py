from rest_framework.throttling import UserRateThrottle


class CreateShortURLThrottle(UserRateThrottle):
    scope = "shorter"
