from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginRequiredMixin(LoginRequiredMixin):

    permission_denied_message = _("Вы не авторизованы! Пожалуйста, выполните вход.")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING,
                             self.permission_denied_message)
            return self.handle_no_permission()
        
        return super(CustomLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )
