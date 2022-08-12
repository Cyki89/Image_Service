from django.contrib.auth.models import AnonymousUser


class AccountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if isinstance(request.user, AnonymousUser):
            request.account_perm = None 
        else:
            request.account_perm = request.user.account.tier

        response = self.get_response(request)

        return response