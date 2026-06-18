from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from users.models import User

class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')        
        password = request.POST.get('password')

        if not username or not password:
            return render(request, self.template_name, {'error': 'немає логіна або пароля'})
        
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, self.template_name, {'error': 'не ті дані авторизації'})
            
        login(request, user)
        return redirect('home_page')


class RegisterView(View):
    template_name = 'auth/register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')        
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not password or not confirm_password:
            return render(request, self.template_name, {'error': 'немає логіна або пароля'})
        
        if password != confirm_password:
            return render(request, self.template_name, {'error': 'паролі не однакові'})
        
        if User.objects.filter(username=username).exists():
            return render(request, self.template_name, {'error': 'користувач вже є'})
        
        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)
        return redirect('home_page')