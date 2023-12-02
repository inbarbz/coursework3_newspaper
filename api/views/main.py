from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def main_spa(request: HttpRequest) -> HttpResponse:
    #return render(request, 'api/spa/index.html', {})
    if request.user.is_authenticated:
        # return render(request, 'api/spa/index.html', {})
        return redirect('http://localhost:5173/')
    username = request.user.username
    return HttpResponse('username: ' + username)
