from django.contrib import messages
from django.shortcuts import redirect, render



def is_auth(template_name, request, context):
    if request.user.is_authenticated:
        return render(request, template_name, context=context)
    else:
        messages.add_message(
            request,
            messages.ERROR,
            "Вы не авторизованы! Пожалуйста, выполните вход.",
            fail_silently=True,
        )
        return redirect("login")
