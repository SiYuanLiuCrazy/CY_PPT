from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadForm
from .models import UploadedFile
import os
from django.conf import settings

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