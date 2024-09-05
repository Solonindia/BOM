from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import UserActivity


class UserActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            button_clicked = request.POST.get('button_clicked') or request.GET.get('button_clicked')
            if button_clicked:
                UserActivity.objects.create(
                    user=request.user,
                    action='button_click',
                    button_clicked=button_clicked,
                    timestamp=timezone.now()
                )


    def process_response(self, request, response):
        if request.user.is_authenticated:
            # Log logout activity
            if 'logout' in request.path:
                UserActivity.objects.create(
                    user=request.user,
                    action='logout',
                    logout_time=timezone.now()
                )
        return response  # Ensure the response is returned

    def process_exception(self, request, exception):
        if request.user.is_authenticated:
            UserActivity.objects.create(
                user=request.user,
                action=request.path,
                timestamp=timezone.now(),
            )
        return None