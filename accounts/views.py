from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegisterForm 
# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class UserLoginView(LoginView):           # 로그인
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form) 

def register(request):
    if request.method == 'POST':
        print(request.POST['password'] == request.POST['confirm_password'])
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            return redirect('/accounts/login/')
    else:
        user_form = RegisterForm()

    return render(request, 'registration/register.html', {'user_form':user_form})