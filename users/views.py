from django.shortcuts import render, redirect
from .models import User, Forget_password
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from . import helper, email_template
# Create your views here.

def signup(request):
    return render(request, 'users/user_signup.html')

def signup_submit(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['re-password']
        isDuplicateUsername = check_duplicate(request, 'username', username)
        isDuplicateEmail = check_duplicate(request, 'email', email)
        if isDuplicateUsername:
            if isDuplicateEmail:
                if password == re_password:
                    user_data = User(username=username, email=email, password=password)
                    user_data.save()
                    messages.info(request, 'Signup successfully', extra_tags='signup')
                    return redirect('/user/signin/')
                else :
                    messages.info(request, 'Passwords not match', extra_tags='signup')
                    return redirect('/user/signup/')
            else:
                messages.info(request, 'Email is exist. Please choose another email.', extra_tags='signup')
                return redirect('/user/signup/')
        else:
            messages.info(request, 'Username is exist. Please choose anoter username.', extra_tags='signup')
            return redirect('/user/signup/')

    return render(request, 'users/user_signup.html')

def check_duplicate(request, fieldName, fieldValue):
    filter_kwargs = {fieldName: fieldValue}
    field_filter = User.objects.filter(**filter_kwargs).count()
    if field_filter >=1 :
        return False
    else:
        return True

def signin(request):
    if request.COOKIES.get('email'):
        my_dict = {
            'email' : request.COOKIES.get('email'),
            'password' : request.COOKIES.get('password')
        }
        return render(request, 'users/user_signin.html',context = my_dict)
    return render(request, 'users/user_signin.html')

def signin_submit(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        remember_me = False
        if 'remember' in request.POST:
            remember_me = request.POST['remember']
            remember_me = int(remember_me)

        if request.COOKIES.get('email'):
            del request.COOKIES['email']
            del request.COOKIES['password']

        isUser = User.objects.filter(email = email, password=password).count()

        if isUser == 1 :
            userDetails = User.objects.filter(email = email, password=password)
            request.session['userid'] = userDetails[0].id
            if remember_me :
                response = redirect('/')
                response.set_cookie('email',email)
                response.set_cookie('password',password)
                return response
            else:
                return redirect('/')
        else:
            messages.info(request, 'Username and password is not match..', extra_tags='signin')
            return redirect('/user/signin/')
    return render(request, 'users/user_signin.html')

def forget_password(request):
    return render(request, 'users/forget_password.html')

def forget_password_submit(request):
    if request.method == 'POST':
        email = request.POST['email']
        isEmailExist = User.objects.filter(email = email).count()
        if isEmailExist >= 1:
            userid = User.objects.filter(email = email)[0].id
            s = 25
            ran = helper.random_string(13,12)
            recover = Forget_password(user_id=userid,token=ran,current_time=datetime.now())
            send_mail_temp = email_template.send_email(email, ran)

            if send_mail_temp:
                recover.save()
                messages.info(request, 'Check your mail to reset your password.', extra_tags='email')
                return redirect('/user/signin/')
            else:
                messages.info(request, 'Somethign went wrong', extra_tags='email')
                return redirect('/user/signin/')
        else:
            messages.info(request, 'Not a registered email.', extra_tags='email')
            return redirect('/user/forget_password/')
    else:
        return redirect('/')
def rocovery_template(request, token):
    if token:
        get_token = Forget_password.objects.get(token = token) #add condition for && updated_at==null

        c_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        # print('current_time' , c_time)
        # print(type(c_time))

        # print(get_token)
        date = get_token.current_time + timedelta(minutes = 15)
        afterTime = date.strftime("%Y-%m-%d %H:%M:%S.%f")
        # print('field time',get_token.current_time)
        # print('after 15 min' , afterTime)
        # print(type(afterTime))

        # LastDate = dateutil.parser.parse(date)
        # now = pytz.utc.localize(timezone.now())
        if c_time <= afterTime:
            # print('okk time is in session')
            if not get_token.updated_at:
                get_id = get_token.id
                return render(request ,'users/forget_password.html',context={'id':get_id})
            else:
                messages.info(request, "Session expire.",extra_tags='sessionExpire')
                return redirect('/')
        else :
            messages.info(request, "Session expire. Plesase reset within 15 minutes.",extra_tags='notmatch')
            return redirect('/')
    else:
        messages.info(request, "Session expire. Plesase try again",extra_tags='notmatch')
        return redirect('/')

def password_recover(request,userid):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_pass = request.POST['re-password']

        r_id = Forget_password.objects.get(id = userid)

        if password == confirm_pass:

            r_id.updated_at = "{time}".format(time = datetime.now())
            r_id.save()
            user_id =r_id.user_id
            getEmail = User.objects.filter(id = user_id).update(password = password)
            # getEmail.save()

            # print(password)
            # print(confirm_pass)
            messages.info(request, "Password Reset Successfully",extra_tags='password')
            return redirect('/')
        else:
            messages.info(request, "Passwords should be same.",extra_tags='password')
            return redirect('/user/rocovery_template/'+r_id.token+'/')

    else:

        return redirect('/')



def signout(request):
    if 'userid' in request.session.keys():
        del request.session['userid']
    return redirect('/user/signin/')

def settings(request):
    if 'userid' in request.session :

        userid = request.session['userid']
        user_data = User.objects.filter(id = userid)
        my_dict = {
            'user' : user_data[0]
        }
        return render(request, 'users/user_settings.html', context = my_dict)
    else:
        return redirect('/')

def settings_edit(request):
    if 'userid' in request.session :
        userid = request.session['userid']
        user_data = User.objects.filter(id = userid)
        my_dict = {
            'user' : user_data[0],
            'edit':True,
            'userid' : userid
        }
        return render(request, 'users/user_settings.html', context = my_dict)
    else:
        return redirect('/')

def check_duplicate_exclude(request , fieldName , fieldValue , id):
    #print('fieldValue',fieldValue)
    filter_kwargs = { fieldName: fieldValue}
    #print(filter_kwargs)
    field_filter = User.objects.filter(**filter_kwargs)
    count = 0
    for i in field_filter:
        if i.id == id:
            pass
        else:
            count+=1

    #print('field_filter',field_filter)

    if count >= 1:
        return False
    else :
        return True

def settings_submit(request,userid):
    if 'userid' in request.session :
        if request.method == 'POST':

            user_data=  User.objects.get(id = userid)

            isDuplicateUsername = check_duplicate_exclude(request, 'username', request.POST['username'], user_data.id)
            isDuplicateEmail = check_duplicate_exclude(request, 'email', request.POST['email'], user_data.id)
            if isDuplicateUsername:
                if isDuplicateEmail:
                        user_data.username = request.POST['username']
                        user_data.email  = request.POST['email']
                        user_data.password = request.POST['password']
                        user_data.save()
                        messages.info(request, 'Profile Updated successfully', extra_tags='update')
                        return redirect('/user/user_settings/')
                else:
                    messages.info(request, 'Email is exist. Please choose another email.', extra_tags='err')
                    return redirect('/user/settings-edit/')
            else:
                messages.info(request, 'Username is exist. Please choose anoter username.', extra_tags='err')
                return redirect('/user/settings-edit/')

    else:
        return redirect('/')
