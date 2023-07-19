
class MobileCSRFMiddleware:

    def process_request(self, request):
        if request.META.get('HTTP_USER_AGENT') and 'Mobile' in request.META.get('HTTP_USER_AGENT'):
            csrf_token = request.COOKIES.get('csrftoken')
            if csrf_token:
                request.META['HTTP_X_CSRFTOKEN'] = csrf_token