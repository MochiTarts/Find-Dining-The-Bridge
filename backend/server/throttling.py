from rest_framework.throttling import BaseThrottle, AnonRateThrottle

class LoginHourThrottle(BaseThrottle):
    '''
    def allow_request(self, request, view):
        return random.randint(1, 10) != 1
    '''

    # this is only for display purpose, actual wait time is dependent on the throttling settings
    def wait(self):
        """
        Optionally, return a recommended number of seconds to wait before
        the next request.
        """
        # an hour
        waited_second = 3600
        return waited_second

class LoginThrottle(LoginHourThrottle, AnonRateThrottle):
    scope = 'login_hour'
