from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
import urllib.request,re,pafy
from isodate import parse_duration

# Create your views here.
def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            if(User.objects.filter(username=username).exists()):
                messages.error(request,'Username already exists')
                return redirect('register')
            elif(User.objects.filter(email=email).exists()):
                messages.error(request,'User with this email already exists')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,password=password,email=email)
                user.save()
                messages.success(request,'Account created successfully!!')
                return redirect('register')
        else:
            messages.error(request,'Password not matching....')
            return redirect('register')
    else:
        return render(request,'register.html')
def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request,'Invalid username/password')
            return redirect('login')
    else:
        return render(request,'login.html')
def logout(request):
    auth.logout(request)
    return redirect('/')
def func(l):
    videos=[]
    for i in l:
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+i)
        video_ids=re.findall(r"watch\?v=(\S{11})", html.read().decode())
        video_ids=video_ids[:6]
        # print(video_ids)
        urls=list(map(lambda x:"https://www.youtube.com/watch?v="+x,video_ids))
        viewscount=list(map(lambda x:pafy.new(x).viewcount,urls))
        pos=viewscount.index(max(viewscount))
        video_data={
            'title':str(pafy.new(urls[pos]).title),
            'vidurl':urls[pos],
            'time':str(pafy.new(urls[pos]).duration),
            'thumbnail':pafy.new(urls[pos]).bigthumb
        }
        videos.append(video_data)
    #     # for id in video_ids:
    #     #     url="https://www.youtube.com/watch?v="+id
    #     #     video = pafy.new(url)
    #     #     if(video.viewcount>m):
    #     #         m=video.viewcount
    #     #         video_id=id
    #     lst.append("https://www.youtube.com/watch?v="+video_id)
    #     # # print(i)
    return videos

def courses(request):
    videos=[]
    l=[]
    if(request.method=='POST'):
        coursename=request.POST['search']
        if(coursename.lower()=='web development'):
            l=['html','css','bootstrap','javascript','php','mysql','git+and+github']
        elif(coursename.lower()=='learn programming' or coursename.lower()=='programming'):
            l=['c','c%2B%2B','java','python','c%23']
        elif(coursename.lower()=='ethical hacking'):
            l=['introduction+to+ethical+hacking','virus+and+worms','linux+hacking','physical+security','session+hijacking','footprinting','password+hacking']
        elif(coursename.lower()=='ui ux design'):
            l=['ui+vs+ux','user+persona','information+architechture','benchmarking','lofi+wireframes','user+journey','hifi+wireframes','learn+figma']
    videos=func(l)
    context={
        'videos':videos
    }
    return render(request,'courses.html',context)