from django.shortcuts import redirect
from logger import logger

EXEMPT_URLS = (
    '',
    'change-password'
)


class LoginRequiredMiddleWare:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, *args, **kwargs):
        try:
            assert hasattr(request, 'user')
            if not request.user.is_authenticated:
                path = request.path_info.lstrip('/')
                if path not in EXEMPT_URLS:
                    return redirect('home:login')
        except AssertionError as e:
            logger().exception(e)
