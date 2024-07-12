from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadForm
from .models import UploadedFile
import os
from django.conf import settings
from django.contrib import messages
from .forms import UploadForm, SignUpForm
from django.contrib.auth import authenticate, login, logout


def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            tag = form.cleaned_data['tag']
            file_name = uploaded_file.name

            # 上传文件到服务器路径
            upload_path = os.path.join(settings.UPLOAD_PATH, file_name)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            with open(upload_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # 保存文件到本地路径
            save_path = os.path.join(settings.SAVE_PATH, file_name)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            # 保存文件信息到数据库
            UploadedFile.objects.create(
                file_path=save_path,
                file_name=file_name,
                tag=tag
            )
            return HttpResponse(f'File uploaded successfully and saved to {save_path}')
    else:
        form = UploadForm()
    return render(request, 'upload/upload.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('upload_file')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')