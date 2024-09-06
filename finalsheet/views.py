from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.template import RequestContext
from .models import TotalCost
from .forms import TotalCostForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm,LoginForm
from django.contrib import messages
from datetime import datetime 
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import LoginForm
from .models import UserActivity
from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponse
from io import BytesIO


def button_page(request):
    if request.method == 'POST':
        if 'admin' in request.POST:
            return redirect('login')
        elif 'user' in request.POST:
            return redirect('loginu')
    return render(request, 'button_page.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('user')  # Replace 'add_bom' with your desired page name
            else:
                # Return an 'invalid login' error message.
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

VALID_USERNAME = 'admin'
VALID_PASSWORD = 'res@123'

def login1_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                # Redirect to the main page or a protected page
                return redirect('admin')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def admin_page(request):
    return render(request,'admin.html')

def user_page(request):
    return render(request,'user.html')

def user_activity_view(request):
    activities = UserActivity.objects.all()  # Adjust according to your model
    return render(request, 'user_activity.html', {'activities': activities})

def logout_view(request):
    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user,
            action='logout',
            logout_time=timezone.now()
        )
    logout(request)
    return redirect('loginu')

def add_bom(request):
    form1 = TotalCostForm()
    try:
        previous_data = TotalCost.objects.latest('id')
    except TotalCost.DoesNotExist:
        previous_data = None  # Handle the case where no previous data exists

    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)

    if request.method == 'POST':
        form = TotalCostForm(request.POST)
        if previous_data is None:
            previous_data = TotalCostForm()
        f2 = float(request.POST['f2'])
        f3 = float(request.POST['f3'])
        f4 = float(request.POST['f4'])
        f5 = float(request.POST['f5'])
        f6 = float(request.POST['f6'])
        f7 = float(request.POST['f7'])
        f8 = float(request.POST['f8'])
        s1 = int(request.POST['s1'])
        s2 = float(request.POST['s2'])
        s3 = float(request.POST['s3'])
        s14 = float(request.POST['s14'])

          
        if form.is_valid():
            # Save form data
            form_data = form.save()

        v10 = f6*f8
        v11 = v10*0.2 + v10
        v12 = float(round(f2/1.87))
        v13 = float(round(f3/1.5))
        

        num_rows = 13  # Define the number of rows

        # Initialize lists to store values
        t_values, c_values, d_values = [], [], []

        # Loop through the POST data to extract values dynamically
        for i in range(1, num_rows + 1):
            t_values.append(float(request.POST.get(f't{i}', 0)))  # Default to 0 if not found
            c_values.append(float(request.POST.get(f'c{i}', 0)))  # Default to 0 if not found
            d_values.append(float(request.POST.get(f'd{i}', 0)))  # Default to 0 if not found 

        # Calculate results dynamically using list comprehensions
        r_values = [t - c for t, c in zip(t_values, c_values)]
        q_values = [r * d for r, d in zip(r_values, d_values)]

        # Create a list of dictionaries to pass to the template
        rows = []
        total_q = 0  # Initialize total quantity
        for i in range(1, num_rows + 1):
            rows.append({
                'i': i,
                'c': c_values[i - 1],
                't': t_values[i - 1],
                'd': d_values[i - 1],
                'r': r_values[i - 1],
                'q': round(q_values[i - 1],2)
            })
            total_q += q_values[i - 1]  # Add each q value to the total
        total_q = round(total_q,4)
        ct = float(total_q*1.2)

        #v14 = round((ct/280),2)
        v14 = round((ct/s14),2)
        
        #tick1 = round(value,2)
        #qty1 = round(value1,2)
        qty1 = s2
        th1 = round((s3*qty1),2)
        w3 = round((th1*2),2)

        w1 = f4- (s3*2)
        net_dia = round(w1-w3-0.2-0.6-0.4-0.3-0.4,2)
        s4 = qty1 - 2


        my_list = [19, 20, 22, 23, 23.5, 24, 26, 28, 30, 32, 34, 35, 37, 37.5, 38, 43, 40, 45, 48, 50,55,60,65,70,75,80,85,90,95,100]
        sorted_list = sorted(my_list, reverse=True)
        result_value = net_dia
        nearest_less_value = None
        for value in sorted_list:
            if value <= result_value:
                nearest_less_value = value
                break

        # Assuming nearest_less_value, v14, v12, f5, w1, TotalCost, and updated_data are defined earlier

        cd = nearest_less_value
        ad = nearest_less_value - 2
        ssa = round(((ad + 2) * (ad + 2)), 2)
        ssc = round(((cd + 2) * (cd + 2)), 2)

        ld = round(3.14 * cd * 1.1, 2)

        aA = round(((3.14 * ad * ad) / 400), 2)
        cA = round(((3.14 * cd * cd) / 400), 2)

        wt = round(0.20 * v14, 2)
        wt2 = round(0.61 * v14, 2)
        wt3 = round((0.09 * cA), 2)
        wt4 = round((0.26 * cA), 2)
        wt5 = round((0.25 * cA), 2)
        wt6 = round((0.23 * cA), 2)
        wt7 = round((7.33 * cA * (0.05 / 10)), 2)
        wt1 = round((wt7 + wt), 2)

        T1 = round(((wt / (aA * 1.07)) * 10), 2)
        T2 = round(((wt1 / (aA * 1.91)) * 10), 2)
        T3 = round(((wt2 / (cA * 2.81)) * 10), 2)
        T4 = round(((wt3 / (cA * 1.88)) * 10), 2)
        T5 = round(((wt4 / (cA * 3.86)) * 10), 2)
        T6 = round(((wt5 / (cA * 4.00)) * 10), 2)
        T7 = round(((wt6 / (cA * 3.89)) * 10), 2)

        weight = round(wt / aA, 2)
        weight2 = round(wt2 / cA, 2)
        weight3 = round(wt3 / cA, 2)
        weight4 = round(wt4 / cA, 2)
        weight5 = round(wt5 / cA, 2)
        weight6 = round(wt6 / cA, 2)

        tw1 = round(v12 * wt, 2)
        tw2 = round(v12 * wt1, 2)
        tw3 = round(v12 * wt2, 2)
        tw4 = round(v12 * wt3, 2)
        tw5 = round(v12 * wt4 * s1, 2)
        tw6 = round(6 * wt5, 2)
        tw7 = round(5 * wt6, 2)
        tw8 = round(v12 * wt7, 2)
        tw9 = round(v12 * wt7, 2)

        a22 = round((f5 + 2) * ((6 + 2)) / 100, 2)
        a25 = round((f5 + 2) * (6 + 2) / 100, 2)
        a26 = round((f5 + 2) * (6 + 2) / 100, 2)
        a31 = round((50 + 2) * (6 + 2) / 100, 2)
        a34 = round((cd + 2) * (cd + 2), 6)
        a37 = round((cd + 2) * (cd + 2) / 100, 6)
        a43 = round((cd + 2) * (cd + 2), 6)
        a57 = round(((cd + 2) * (cd + 2) / 100) + ((100 * 8) / 100), 2)
        a58 = round(((cd + 2) * (cd + 2) / 100) + ((100 * 8) / 100), 2)
        a63 = round((cd + 2) * (cd + 2), 6)
        a71 = round((f5 + 2) * (6 + 2) / 100, 2)
        a72 = round((f5 + 2) * (6 + 2) / 100, 2)
        a81 = round((f5 * ld * 2), 2)
        a84 = round(((f5 * ld) / 100), 2)
        a92 = round((f5 * ld * s4), 2)
        a93 = round((w1 + 2) * (w1 + 2) / 100, 6)
        a94 = round((cd + 2) * (cd + 2), 6)

        v22 = round((a22 * 0.15) / 10, 2)
        v25 = round((a25 * 0.15) / 10, 4)
        v26 = round((a26 * 0.15) / 10, 4)
        v31 = round((a31 * 0.15) / 10, 4)
        v37 = round((a37 * 1) / 10, 4)
        v42 = round((cA * T6) / 10, 2)
        v51 = round((cA * 0.05) / 10, 4)
        v52 = round((cA * 0.05) / 10, 4)
        v53 = round((aA * T1) / 10, 4)
        v54 = round((cA * T3) / 10, 2)
        v55 = round((cA * T4) / 10, 2)
        v56 = round((cA * T5) / 10, 2)
        v57 = round((a57 * 0.15) / 10, 2)
        v58 = round((a58 * 0.15) / 10, 2)
        v62 = round((cA * T7) / 10, 2)
        v63 = round((a63 * 1.6) / 10, 2)
        v71 = round((a71 * 0.15) / 10, 2)
        v72 = round((a72 * 0.15) / 10, 2)
        v84 = round((a84 * 0.1) / 10, 2)
        v93 = round((a93 * 1.0) / 10, 2)
        v94 = round((a94 * 1.6) / 10, 2)

        w22 = round(((9 * v22 * 3) / 1000), 6)
        w25 = round(((9 * v25 * 3) / 1000), 6)
        w26 = round(((9 * v26 * 2) / 1000), 6)
        w31 = round(((9 * v31 * 2) / 1000), 6)
        w34 = round((a34 * 1.07) / 100000, 6)
        w37 = round(v37 * 2.15 * 13 / 1000, 6)
        w42 = tw6
        w43 = round((a43 * 1.07) / 100000, 6)
        w51 = round((v12 * 8 * v51) / 1000, 6)
        w52 = tw9
        w53 = tw1
        w54 = tw3
        w55 = tw4
        w56 = tw5
        w57 = round((9 * v57 * 2) / 1000, 6)
        w58 = round((9 * v58 * 2) / 1000, 6)
        w62 = tw7
        w63 = round((a63 * 1.07) / 100000, 6)
        w71 = round((1.5 * v71 * 4) / 1000, 6)
        w72 = round((1.5 * v72 * 6) / 1000, 6)
        w81 = round((a81 * 1.07) / 100000, 6)
        w84 = round((1.5 * v84 * 2) / 1000, 6)
        w92 = round((a92 * 1.07) / 100000, 6)
        w93 = round(((2.15 * v93 * 9) / 1000), 6)
        w94 = round((a94 * 1.07) / 100000, 6)

        updated_data = TotalCost.objects.latest('id')

# Ensure values are not None and provide a default value if they are
        def safe_float(value, default=0.0):
            return float(value) if value is not None else default

        c21 = round(1 * safe_float(updated_data.ru21))
        c22 = round((w22 * safe_float(updated_data.ru22)), 2)
        c23 = round(1 * safe_float(updated_data.ru23))
        c24 = round(2 * safe_float(updated_data.ru24))
        c25 = round((w25 * safe_float(updated_data.ru25)), 2)
        c26 = round((w26 * safe_float(updated_data.ru26)), 2)
        c31 = round((w31 * safe_float(updated_data.ru31)), 2)
        c32 = round(1 * safe_float(updated_data.ru32), 4)
        c33 = round((w34 * safe_float(updated_data.ru33)), 4)
        c34 = round(1 * safe_float(updated_data.ru34))
        c35 = round(1 * safe_float(updated_data.ru35))
        c37 = round(w37 * safe_float(updated_data.ru37))
        c41 = round(1 * safe_float(updated_data.ru41))
        c43 = round((w43 * safe_float(updated_data.ru43)), 4)
        c44 = round(1 * safe_float(updated_data.ru44))
        c51 = round(w51 * safe_float(updated_data.ru51))
        c52 = round(w51 * safe_float(updated_data.ru52))
        c57 = round(w57 * safe_float(updated_data.ru57))
        c58 = round(w58 * safe_float(updated_data.ru58))
        c61 = round(2 * safe_float(updated_data.ru61))
        c63 = round((w63 * safe_float(updated_data.ru63)), 4)

        # Continue to use safe_float for the remaining calculations
        c64 = round(1 * safe_float(updated_data.ru64))
        c65 = round(1 * safe_float(updated_data.ru65))
        c71 = round(w71 * safe_float(updated_data.ru71), 4)
        c72 = round(w72 * safe_float(updated_data.ru72))
        c73 = round(3 * safe_float(updated_data.ru73))
        c74 = round(4 * safe_float(updated_data.ru74))
        c81 = round((w81 * safe_float(updated_data.ru81)), 4)
        c82 = round(1 * safe_float(updated_data.ru82))
        c83 = round(1 * safe_float(updated_data.ru83))
        c84 = round((w84 * safe_float(updated_data.ru84)), 4)
        c91 = round(1 * safe_float(updated_data.ru91))
        c92 = round((w92 * safe_float(updated_data.ru92)), 4)
        c93 = round((w93 * safe_float(updated_data.ru93)), 4)
        c94 = round((w94 * safe_float(updated_data.ru94)), 4)
        c95 = round(1 * safe_float(updated_data.ru95))
        c96 = round(0.2 * safe_float(updated_data.ru96))
        c97 = round(0.1 * safe_float(updated_data.ru97))

        tap = wt * v12
        lisi = round((tap * 0.85 * 0.001 * 1.1), 6)
        ebtap = round((tap * 0.15), 6)
        licl1 = round((ebtap * 0.8), 6)
        mgo1 = round((ebtap * 0.2 * 0.001 * 1.1), 6)
        licl11 = round((licl1 * 0.45 * 0.001 * 1.1), 6)
        kcl11 = round((licl1 * 0.55 * 0.001 * 1.1), 6)

        cat = wt2 * v12
        fes2 = round((cat * 0.735 * 0.001 * 1.1), 6)
        li2s = round((cat * 0.015 * 0.001 * 1.1), 6)
        ebcat = round((cat * 0.25), 6)
        lical2 = ebcat * 0.8
        mgo2 = round((ebcat * 0.2 * 0.001 * 1.1), 6)
        licl21 = round((lical2 * 0.45 * 0.001 * 1.1), 6)
        kcl21 = round((lical2 * 0.55 * 0.001 * 1.1), 6)

        electrolyte = wt3 * v12
        licl3 = electrolyte * 0.6 
        licl31 = round((licl3 * 0.45 * 0.001 * 1.1), 6)
        kcl31 = round((licl3 * 0.55 * 0.001 * 1.1), 6)
        mgo3 = round((electrolyte * 0.4 * 0.001 * 1.1), 6)

        hp = (wt4 * v12 * s1) + (wt5 * 6) + (wt6 * 5)
        hpfe = round((hp * 0.87 * 0.001 * 1.1), 4)
        hpkclo4 = round((hp * 0.13 * 0.001 * 1.1), 6)

        rc1a = round((lisi * safe_float(updated_data.ru1a)), 6)
        rc1c = round((licl11 * safe_float(updated_data.ru1c)), 6)
        rc1d = round((kcl11 * safe_float(updated_data.ru1d)), 6)
        rc1e = round((mgo1 * safe_float(updated_data.ru1e)), 6)
        rc2a = round((fes2 * safe_float(updated_data.ru2a)), 6)
        rc2b = round((li2s * safe_float(updated_data.ru2b)), 6)
        rc2d = round((licl21 * safe_float(updated_data.ru2d)), 6)
        rc2e = round((kcl21 * safe_float(updated_data.ru2e)), 6)
        rc2f = round((mgo2 * safe_float(updated_data.ru2f)), 6)
        rc3b = round((licl31 * safe_float(updated_data.ru3b)), 6)
        rc3c = round((kcl31 * safe_float(updated_data.ru3c)), 6)
        rc3d = round((mgo3 * safe_float(updated_data.ru3d)), 6)
        rc4a = round((hpfe * safe_float(updated_data.ru4a)), 6)
        rc4b = round((hpkclo4 * safe_float(updated_data.ru4b)), 6)
        total_cost_sheet = sum([c21,c22,c23,c24,c25,c26,c31,c32,c33,c34,c35,c37,c41,c43,c44,c51,c52,c57,c58,c61,
        c63,c64,c65,c71,c72,c73,c74,c81,c82,c83,c84,c91,c92,c93,c94,c95,c96,c97,
        rc1a,rc1c,rc1d,rc1e,rc2a,rc2b,rc2d,rc2e,rc2f,rc3b,rc3c,rc3d,rc4a,rc4b])
        #total_cost = rc1a+rc1c+rc1d+rc1e+rc2a+rc2b+rc2d+rc2e+rc2f+rc3b+rc3c+rc3d+rc4a+rc4b+c21+c22+c23+c24+c25+c26+c31+c32+c33+c34+c35+c37+c41+c43+c44+c51+c52+c57+c58+c61+c63+c64+c65+c71+c72+c73+c74+c81+c82+c83+c84+c91+c92+c93+c94+c95+c96+c97

        p1 = round(total_cost_sheet * 0.15 * 15,6)
        p2 = round(total_cost_sheet * 0.15 * 12,6)
        p3 = round(total_cost_sheet * 0.12 * 10,6)
        p5 = round(total_cost_sheet * 0.12 * 10,6)
        p8 = round(total_cost_sheet * 0.12 * 15,6)

        total_p = round(p1+p2+p3+p5+p8,6)

        data = {'ru1a':updated_data.ru1a,'ru1c':updated_data.ru1c,'ru1d':updated_data.ru1d,'ru1e':updated_data.ru1e,
        'ru2a':updated_data.ru2a,'ru2b':updated_data.ru2b,'ru2d':updated_data.ru2d,'ru2e':updated_data.ru2e,
        'ru2f':updated_data.ru2f,'ru3b':updated_data.ru3b,'ru3c':updated_data.ru3c,'ru3d':updated_data.ru3d,
        'ru4a':updated_data.ru4a,'ru4b':updated_data.ru4b,

        'rc1a':rc1a,'rc1c':rc1c,'rc1d':rc1d,'rc1e':rc1e,'rc2a':rc2a,'rc2b':rc2b,'rc2d':rc2d,'rc2e':rc2e,
        'rc2f':rc2f,'rc3b':rc3b,'rc3c':rc3c,'rc3d':rc3d,'rc4a':rc4a,'rc4b':rc4b,'total_cost':total_cost_sheet,

        'f2':f2,'f3':f3,'f4':f4,'f5':f5,'f6':f6,'f7':f7, 'f8':f8,
        'v10':v10,'v11':v11,'v12':v12,'v13':v13,
        'v14':v14,'cd':cd,'ad':ad,'aA':aA,'cA':cA,'wt':wt,'wt2':wt2,'wt3':wt3,'wt4':wt4,'wt5':wt5,'wt6':wt6,'wt7':wt7,'wt1':wt1,
        'weight':weight,'weight2':weight2,'weight3':weight3,'weight4':weight4,'weight5':weight5,'weight6':weight6,
        'T1':T1,'T2':T2,'T3':T3,'T4':T4,'T5':T5,'T6':T6,'T7':T7,
        'rows': rows, 'total_q': total_q,'ct':ct,
        #'tick1':tick1,
        'qty1':qty1,'th1':th1,'s3':s3,'s4':s4,
        'w1':w1,'w3':w3,'net_dia':net_dia, 'ld':ld,

        'lisi':lisi,'ebtap':ebtap,'mgo1':mgo1,'licl11':licl11,'kcl11':kcl11,'fes2':fes2,'li2s':li2s,'ebcat':ebcat,
        'mgo2':mgo2,'licl21':licl21,'kcl21':kcl21,
        'licl31':licl31,'kcl31':kcl31,'mgo3':mgo3,'hpfe':hpfe,'hpkclo4':hpkclo4,

        'tw1':tw1,'tw2':tw2,'tw3':tw3,'tw4':tw4,'tw5':tw5,'tw6':tw6,'tw7':tw7,'tw8':tw8,'tw9':tw9,

        'a22':a22,'a25':a25,'a26':a26,
        'a31':a31,'a34':a34,
        'a43':a43,'a57':a57,'a58':a58,
        'a63':a63,
        'a71':a71,'a72':a72,
        'a81':a81,'a84':a84,
        'a92':a92,'a93':a93,'a94':a94,

        'v22':v22,'v25':v25,'v26':v26,
        'v31':v31,#'v34':v34,
        'v42':v42,
        #'v43':v43,
        'v51':v51,'v52':v52,'v53':v53,'v54':v54,'v55':v55,'v56':v56,'v57':v57,'v58':v58,
        'v62':v62,'v63':v63,
        'v71':v71,'v72':v72,
        #'v81':v81,
        'v84':v84,
        #'v92':v92,
        'v93':v93,'v94':v94, 'a37':a37,'v37':v37,'w37':w37,'c37':c37,
        
        'r21':updated_data.ru21,'r22':updated_data.ru22,'r23':updated_data.ru23,'r24':updated_data.ru24,'r25':updated_data.ru25,'r26':updated_data.ru26,
        'r31':updated_data.ru31,'r32':updated_data.ru32,'r34':updated_data.ru34,'r35':updated_data.ru35,'r33':updated_data.ru33,       
        'r41':updated_data.ru41,'r43':updated_data.ru43,'r44':updated_data.ru44,'r37':updated_data.ru37,
        'r51':updated_data.ru51,'r52':updated_data.ru52,'r57':updated_data.ru57,'r58':updated_data.ru58,
        'r61':updated_data.ru61,'r63':updated_data.ru63,'r64':updated_data.ru24,'r65':updated_data.ru65,
        'r71':updated_data.ru71,'r72':updated_data.ru72,'r73':updated_data.ru73,'r74':updated_data.ru24,
        'r81':updated_data.ru81,'r82':updated_data.ru82,'r83':updated_data.ru83,'r84':updated_data.ru84,
        'r91':updated_data.ru91,'r92':updated_data.ru92,'r93':updated_data.ru93,'r94':updated_data.ru94,'r95':updated_data.ru95,
        'r96':updated_data.ru96,'r97':updated_data.ru97,

        'w22':w22,'w25':w25,'w26':w26,
        'w31':w31,
        #'w33':w33,
        'w34':w34,
        'w42':w42,
        'w43':w43,
        'w51':w51,'w52':w52,'w53':w53,'w54':w54,'w55':w55,'w56':w56,'w57':w57,'w58':w58,
        'w62':w62,
        'w63':w63,
        'w71':w71,
        'w72':w72,
        'w81':w81,'w84':w84,
        'w92':w92,
        'w93':w93,
        'w94':w94,

        'c21':c21,'c22':c22,'c23':c23,'c24':c24,'c25':c25,'c26':c26,
        'c31':c31,'c32':c32,'c34':c34,'c35':c35,'c33':c33,
        'c41':c41,'c43':c43,'c44':c44,
        'c51':c51,'c52':c52,'c57':c57,'c58':c58,
        'c61':c61,'c63':c63,'c64':c64,'c65':c65,
        'c71':c71,'c72':c72,'c73':c73,'c74':c74,
        'c81':c81,'c82':c82,'c83':c83,'c84':c84,
        'c91':c91,'c92':c92,'c93':c93,'c94':c94,'c95':c95,'c96':c96,'c97':c97,
        'previous_data':previous_data,

        'p1':p1,'p2':p2,'p3':p3,'p5':p5,'p8':p8,'total_p':total_p,'s14':s14
        }
        timestamp_str = timezone.now().strftime('%Y%m%d%H%M%S')
        pdf_file_name = f"result_bom_{timestamp_str}.pdf"
        pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', pdf_file_name)

        # Ensure the 'downloads' directory exists
        os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)

        # Render HTML to string
        html = render_to_string('resulting.html', data, request=request)

        # Create a response object with PDF mime type
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="{pdf_file_name}"'

        # Use BytesIO to generate the PDF
        result = BytesIO()

        # Generate PDF with landscape orientation (A4 size)
        pisa_status = pisa.CreatePDF(
            html,
            dest=result,
            encoding='utf-8',
            default_css="""
            @page {
                size: A4 landscape; /* A4 size in landscape orientation */
                margin: 1cm; /* Set page margins */
            }
            """
        )

        # If there is an error in PDF generation, return an error response
        if pisa_status.err:
            return HttpResponse(f"PDF Creation Error: {pisa_status.err}", status=500)

        # Save the PDF to file system
        with open(pdf_file_path, 'wb') as pdf_file:
            pdf_file.write(result.getvalue())

        # Save user activity for file download
        UserActivity.objects.create(
            user=request.user,
            action='File Downloaded',
            file_downloaded=f'downloads/{pdf_file_name}',
            file_details='Details of the downloaded PDF',
            timestamp=timezone.now()  # Use timezone-aware datetime
        )

        # Return the PDF response to display in the browser
        result.seek(0)
        response.write(result.read())
        return response
    else:
        upload_range = range(1, 21)
        return render(request, 'input2.html',{'form1':form1,'previous_data':previous_data,'upload_range': upload_range})



def view_downloaded_pdf(request, activity_id):
    activity = get_object_or_404(UserActivity, id=activity_id)
    
    if activity.file_downloaded:
        file_path = activity.file_downloaded.path  # Correctly get the file path
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    else:
        return HttpResponse('File not found', status=404)




from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from xhtml2pdf import pisa
import os
from django.conf import settings


def add_bom1(request):
    #form1 = TotalCostForm()
    if request.method == 'POST':
        #form = TotalCostForm(request.POST)
        f2 = float(request.POST['f2'])
        f3 = float(request.POST['f3'])
        f4 = float(request.POST['f4'])
        f5 = float(request.POST['f5'])
        f6 = float(request.POST['f6'])
        f7 = float(request.POST['f7'])
        f8 = float(request.POST['f8'])
        s1 = int(request.POST['s1'])
        s2 = float(request.POST['s2'])
        s3 = float(request.POST['s3'])
        s14 = float(request.POST['s14'])
        #print(s1)
        # if form.is_valid():
        #     form_data = form.save()

        v10 = f6*f8
        v11 = v10*0.2 + v10
        v12 = float(round(f2/1.87)) * s1
        v13 = float(round(f3/1.5))
        v15 = float(round(f2/1.87))
        #v14 = round((v11/280),2)
        

        num_rows = 13  # Define the number of rows

        # Initialize lists to store values
        t_values, c_values, d_values = [], [], []

        # Loop through the POST data to extract values dynamically
        for i in range(1, num_rows + 1):
            t_values.append(float(request.POST.get(f't{i}', 0)))  # Default to 0 if not found
            c_values.append(float(request.POST.get(f'c{i}', 0)))  # Default to 0 if not found
            d_values.append(float(request.POST.get(f'd{i}', 0)))  # Default to 0 if not found 

        # Calculate results dynamically using list comprehensions
        r_values = [t - c for t, c in zip(t_values, c_values)]
        q_values = [r * d for r, d in zip(r_values, d_values)]

        # Create a list of dictionaries to pass to the template
        rows = []
        total_q = 0  # Initialize total quantity
        for i in range(1, num_rows + 1):
            rows.append({
                'i': i,
                'c': c_values[i -    1],
                't': t_values[i - 1],
                'd': d_values[i - 1],
                'r': r_values[i - 1],
                'q': round(q_values[i - 1],2)
            })
            total_q += q_values[i - 1]  # Add each q value to the total
        total_q = round(total_q,4)
        ct = float(total_q*1.2)
        v14 = round((ct/s14),2)
        #print(v14)

        #tick1 = round(value,2)
        #qty1 = round(value1,2)
        qty1 = s2
        th1 = round((s3*qty1),2)
        w3 = round((th1*2),2)

        w1 = f4- (s3*2)
        net_dia = round(w1-w3-0.2-0.6-0.4-0.3-0.4,2)
        s4 = qty1 -2


        my_list = [19, 20, 22, 23, 23.5, 24, 26, 28, 30, 32, 34, 35, 37, 37.5, 38, 43, 40, 45, 48, 50]
        sorted_list = sorted(my_list, reverse=True)
        result_value = net_dia
        nearest_less_value = None
        for value in sorted_list:
            if value <= result_value:
                nearest_less_value = value
                break

        cd = nearest_less_value
        ad = nearest_less_value - 2
        ssa = round(((ad+2)*(ad+2)),2)
        ssc = round(((cd+2)*(cd+2)),2)

        ld = round(3.14 * cd * 1.1,2)

        aA = round(((3.14 * ad * ad) / 400),2)
        cA = round(((3.14 * cd * cd) / 400),2)

        wt = round(0.20 * v14,2)
        wt2 = round(0.61 * v14,2)
        wt3 = round((0.09 * cA),2)
        wt4 = round((0.26 * cA),2)
        wt5 = round((0.25 * cA),2)
        wt6 = round((0.23 * cA),2)
        wt7 = round((7.33*cA*(0.05/10)),2)
        wt1 = round((wt7 + wt),2)

        T1 = round(((wt/(aA*1.07))*10),2)
        T2 = round(((wt1/(aA*1.91))*10),2)
        T3 = round(((wt2/(cA*2.81))*10),2)
        T4 = round(((wt3/(cA*1.88))*10),2)
        T5 = round(((wt4/(cA*3.86))*10),2)
        T6 = round(((wt5/(cA*4.00))*10),2)
        T7 = round(((wt6/(cA*3.89))*10),2)
        # T8 = round((/(cA*7.33)),2)

        weight = round(wt/aA,2)
        #weight1 = round()
        weight2 = round(wt2/cA,2)
        weight3 = round(wt3/cA,2)
        weight4 = round(wt4/cA,2) 
        weight5 = round(wt5/cA,2)
        weight6 = round(wt6/cA,2)


        tw1 = round(v12 * wt,2)
        tw2 = round(v12*wt1,2)
        tw3 = round(v12*wt2,2)
        tw4 = round(v12*wt3,2)
        tw5 = round(v12*wt4*s1,2)
        tw6 = round(6*wt5,2)
        tw7 = round(5*wt6,2)
        tw8 = round(v12*wt7,2)
        tw9 = round(v12*wt7,2)

        a22 = round((f5+2)*((6+2))/100,2)        
        a25 = round((f5+2)*(6+2)/100,2)
        a26 = round((f5+2)*(6+2)/100,2)
        a31 = round((50+2)*(6+2)/100,2)
        a34 = round((cd+2)*(cd+2),6)
        a37 = round((cd+2)*(cd+2)/100,6)
        a43 = round((cd+2)*(cd+2),6)
        a57 = round(((cd+2)*(cd+2)/100)+((100*8)/100),2)
        a58 = round(((cd+2)*(cd+2)/100)+((100*8)/100),2)
        a63 = round((cd+2)*(cd+2),6)
        a71 = round((f5+2)*(6+2)/100,2)
        a72 = round((f5+2)*(6+2)/100,2)
        a81 = round((f5*ld*2),2)
        a84 = round(((f5*ld)/100),2)
        a92 = round((f5*ld*2),2)
        a93 = round((w1+2)*(w1+2)/100,6)
        a94 = round((cd+2)*(cd+2),6)
        

        v22 = round((a22*0.3)/10,2)
        v25 = round((a25*0.15)/10,4)
        v26 = round((a26*0.15)/10,4)
        v31 = round((a31*0.15)/10,4)
        #v34 = round((a34*t34)/10,2)
        v37 = round((a37*1)/10,4)
        v42 = round((cA*T6)/10,2)
        #v43 = round((a43*t43)/10,2)
        v51 = round((cA*0.05)/10,4)
        v52 = round((cA*0.05)/10,4)
        v53 = round((aA*T1)/10,4)
        v54 = round((cA*T3)/10,2)
        v55 = round((cA*T4)/10,2)
        v56 = round((cA*T5)/10,2)
        v57 = round((a57*0.15)/10,2)
        v58 = round((a58*0.15)/10,2)
        v62 = round((cA*T7)/10,2)
        v63 = round((a63*1.6)/10,2)
        v71 = round((a71*0.15)/10,2)
        v72 = round((a72*0.15)/10,2)
        #v81 = round((a81*t81)/10,2)
        v84 = round((a84*0.1)/10,2)
        #v92 = round((a92*t92)/10,2)
        v93 = round((a93*1.0)/10,2)
        v94 = round((a94*1.6)/10,2)

        w22 = round(((9*v22*3)/1000),6)#density*volume*quantity
        w25 = round(((9*v25*3)/1000),6)
        w26 = round(((9*v26*2)/1000),6)
        w31 = round(((9*v31*2)/1000),6)
        w34 = round((a34*1.07)/100000,6)
        w37 = round(v37*2.15*13/1000,6)
        w42 = tw6
        w43 = round((a43*1.07)/100000,6)
        w51 = round((v12*8*v51)/1000,6)#tw8
        w52 = tw9
        #print(w52)
        w53 = tw1
        w54 = tw3
        w55 = tw4
        w56 = tw5
        w57 = round((9*v57*2)/1000,6)
        w58 = round((9*v58*2)/1000,6)
        w62 = tw7
        w63 = round((a63*1.07)/100000,6)
        w71 = round((1.5*v71*3)/1000,6)
        w72 = round((1.5*v72*6)/1000,6)
        w81 = round((a81*1.07)/100000,6)
        w84 = round((1.5*v84*2)/1000,6)
        w92 = round((a92*1.07)/100000,6)
        w93 = round(((2.15*v93*9)/1000),6)
        w94 = round((a94*1.07)/100000,6)        


        tap = wt * v12
        lisi = round((tap * 0.85 * 0.001 * 1.1),6)
        ebtap = round((tap * 0.15),6)
        licl1 = round((ebtap * 0.8),6)
        mgo1 = round((ebtap * 0.2 * 0.001 * 1.1),6)
        licl11 = round((licl1 * 0.45 * 0.001 * 1.1),6)
        kcl11 = round((licl1 * 0.55 * 0.001 * 1.1),6)

        cat = wt2 * v12
        fes2 = round((cat * 0.735 * 0.001 * 1.1),6)
        li2s = round((cat * 0.015 * 0.001 * 1.1),6)
        ebcat = round((cat * 0.25),6)
        lical2 = ebcat * 0.8
        mgo2 = round((ebcat * 0.2 * 0.001 * 1.1),6)
        licl21 = round((lical2 * 0.45 * 0.001 * 1.1),6)
        kcl21 = round((lical2 * 0.55 * 0.001* 1.1),6)

        electrolyte = wt3 * v12
        licl3 = electrolyte * 0.6 
        licl31 = round((licl3 * 0.45 * 0.001 * 1.1),6)
        kcl31 = round((licl3 * 0.55 * 0.001 * 1.1),6)
        mgo3 = round((electrolyte * 0.4 * 0.001 * 1.1),6)

        hp = (wt4*v12*s1)+(wt5*6)+(wt6*5)
        hpfe = round((hp * 0.87 * 0.001 * 1.1),4)
        hpkclo4 = round((hp * 0.13 * 0.001 * 1.1),6)


        #total_cost = rc1a+rc1c+rc1d+rc1e+rc2a+rc2b+rc2d+rc2e+rc2f+rc3b+rc3c+rc3d+rc4a+rc4b+c21+c22+c23+c24+c25+c26+c31+c32+c33+c34+c35+c37+c41+c43+c44+c51+c52+c57+c58+c61+c63+c64+c65+c71+c72+c73+c74+c81+c82+c83+c84+c91+c92+c93+c94+c95+c96+c97
      

        data = {

        #'rc1a':rc1a,'rc1c':rc1c,'rc1d':rc1d,'rc1e':rc1e,'rc2a':rc2a,'rc2b':rc2b,'rc2d':rc2d,'rc2e':rc2e,
        #'rc2f':rc2f,'rc3b':rc3b,'rc3c':rc3c,'rc3d':rc3d,'rc4a':rc4a,'rc4b':rc4b,

        'f2':f2,'f3':f3,'f4':f4,'f5':f5,'f6':f6,'f7':f7, 'f8':f8,
        'v10':v10,'v11':v11,'v12':v12,'v13':v13,'v15':v15,
        'v14':v14,'cd':cd,'ad':ad,'aA':aA,'cA':cA,'wt':wt,'wt2':wt2,'wt3':wt3,'wt4':wt4,'wt5':wt5,'wt6':wt6,'wt7':wt7,'wt1':wt1,
        'weight':weight,'weight2':weight2,'weight3':weight3,'weight4':weight4,'weight5':weight5,'weight6':weight6,
        'T1':T1,'T2':T2,'T3':T3,'T4':T4,'T5':T5,'T6':T6,'T7':T7,
        'rows': rows, 'total_q': total_q,'ct':ct,
        #'tick1':tick1,
        's3':s3,'qty1':qty1,'th1':th1,'s4':s4,
        'w1':w1,'w3':w3,'net_dia':net_dia, 'ld':ld,

        'lisi':lisi,'ebtap':ebtap,'mgo1':mgo1,'licl11':licl11,'kcl11':kcl11,'fes2':fes2,'li2s':li2s,'ebcat':ebcat,
        'mgo2':mgo2,'licl21':licl21,'kcl21':kcl21,
        'licl31':licl31,'kcl31':kcl31,'mgo3':mgo3,'hpfe':hpfe,'hpkclo4':hpkclo4,

        'tw1':tw1,'tw2':tw2,'tw3':tw3,'tw4':tw4,'tw5':tw5,'tw6':tw6,'tw7':tw7,'tw8':tw8,'tw9':tw9,

        'a22':a22,'a25':a25,'a26':a26,
        'a31':a31,'a34':a34,
        'a43':a43,'a57':a57,'a58':a58,
        'a63':a63,
        'a71':a71,'a72':a72,
        'a81':a81,'a84':a84,
        'a92':a92,'a93':a93,'a94':a94,

        'v22':v22,'v25':v25,'v26':v26,
        'v31':v31,#'v34':v34,
        'v42':v42,
        #'v43':v43,
        'v51':v51,'v52':v52,'v53':v53,'v54':v54,'v55':v55,'v56':v56,'v57':v57,'v58':v58,
        'v62':v62,'v63':v63,
        'v71':v71,'v72':v72,
        #'v81':v81,
        'v84':v84,
        #'v92':v92,
        'v93':v93,'v94':v94, 'a37':a37,'v37':v37,'w37':w37,#'c37':c37,
        

        'w22':w22,'w25':w25,'w26':w26,
        'w31':w31,
        #'w33':w33,
        'w34':w34,
        'w42':w42,
        'w43':w43,
        'w51':w51,'w52':w52,'w53':w53,'w54':w54,'w55':w55,'w56':w56,'w57':w57,'w58':w58,
        'w62':w62,
        'w63':w63,
        'w71':w71,
        'w72':w72,
        'w81':w81,'w84':w84,
        'w92':w92,
        'w93':w93,
        'w94':w94,

        }
        # Create a fixed PDF filename
        pdf_file_name = "result_bom.pdf"
        pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', pdf_file_name)

        # Ensure the 'downloads' directory exists
        os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)

        # Render HTML to string
        html = render_to_string('result1.html', data, request=request)

        # Create a response object with PDF mime type
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_file_name}"'

        # Generate PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('PDF Creation Error: %s' % pisa_status.err, status=500)

        # Save PDF to file system
        with open(pdf_file_path, 'wb') as pdf_file:
            pisa.CreatePDF(html, dest=pdf_file)

        # Return the PDF response to display it in the browser
        return response
    else:
        upload_range = range(1, 21)
        return render(request, 'input1.html',{'upload_range': upload_range})