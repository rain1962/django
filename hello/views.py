from django.shortcuts import render
from django.shortcuts import HttpResponse,HttpResponseRedirect,redirect
from django.http import FileResponse,Http404,JsonResponse
from .form import LoginField
from hello.models import user,doc
from functools import wraps
from django.core.paginator import Paginator
import json
import time
import os
import json
from django.core import serializers

def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('is_login')=='1':
            return f(request,*arg,**kwargs)
        else:
            return redirect('/login/')
    return inner
@check_login
def useradd(request):
    err_msg=''
    login_form=LoginField(request.POST)
    if login_form.is_valid():
        if request.method == "POST":
            un=request.POST.get("username",None)
            up=request.POST.get("password",None)
            cor = request.POST.get("cor", None)
            dep = request.POST.get("dep", None)
            if len(un)<2:
                err_msg="too short username"
            else:
                p=user(username=un,password=up,cor=cor,dep=dep)
                p.save()
                return HttpResponse("register success")
    else:
        user_list=user.objects.all()
        return render(request,"useradd.html",{"user":user_list,"err_msg":err_msg})
def login(request):
    if request.method == "GET":
        return render(request,"login.html",)
    else:
        username=request.POST.get("username",None)
        password=request.POST.get("password",None)
        u=user.objects.filter(username=username,password=password)
        if u:
            request.session['is_login']='1'
            request.session['user_id']=u[0].id
            if username=="admin" :
                request.session['is_admin']='1'
                return redirect('/useradd/')

            return redirect('/index/')
    return render(request,'login.html')
@check_login
def index(request):
    user_id1 = request.session.get('user_id')
    userobj = user.objects.filter(id=user_id1)
    db = doc.objects.all()
    data=serializers.serialize('json',db)
    paginator=Paginator(db,3)
    page=request.GET.get('page')
    dbdata=paginator.get_page(page)
    print(json.loads(data))
    filename=''
    msg=''
    filepath = 'file/{}'.format(userobj[0].username)
    if request.method=='POST':
        file=request.FILES.get('file')
        docn = request.POST.get("docname", None)
        doccontent = request.POST.get("content", None)
        if docn:
            if file:
                isexsits=os.path.exists(filepath)
                if not isexsits:
                    os.makedirs(filepath)
                filename=file.name
                with open(os.path.join(filepath,file.name), 'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                    f.close()
            d=doc(docname=docn,content=doccontent,createdtime=time.strftime('%Y-%m-%d %H:%M:%S'),file=filename,author_id=user_id1)
            d.save()
            msg='success'
        else:
            msg='error'
    link=filepath+'/'+filename
    if userobj:
        return render(request,'index.html', {'user': userobj[0],'msg':msg,'dara':data,'link':link,'db':dbdata})
    else:
        return render(request,'index.html', {'user': 'unkown','msg':msg,'data':data,'link':link})

def download_file(request,filename):
    try:
        user_id1 = request.session.get('user_id')
        userobj = user.objects.filter(id=user_id1)
        filepath = 'file/{}'.format(userobj[0].username)
        def file_iterator(filename,chunk_size=512):
            print(filename,'****************')
            with open(os.path.join(filepath,filename),'rb') as f:
                if f:
                    yield f.read(chunk_size)
                    print('download success')
                else:
                    print('download fail')
        response=FileResponse(open(os.path.join(filepath,filename),'rb'))
        response['content_type']="application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(os.path.join(filepath,filename))
        return response
    except Exception:
        raise Http404
