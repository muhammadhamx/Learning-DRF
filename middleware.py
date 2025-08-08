from django.http import JsonResponse

class CustomServerErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        try:
            response = self.get_response(request)
            if response.status_code >= 500:
                return JsonResponse({
                    "error": "Internal Server Error",
                    "message": "Something went wrong. Please contact support."
                }, status=500)
            else:
                return response

        except Exception as e:
            return JsonResponse({
                "error": "Internal Server Error",
                "message": "Something went wrong. Please contact support."
            }, status=500)
