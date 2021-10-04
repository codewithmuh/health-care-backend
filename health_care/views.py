from django.http import HttpResponse
from django.template.loader import render_to_string


def complete_view(request):
    html = render_to_string("email/user_email_confirmed.html")
    return HttpResponse(html)
