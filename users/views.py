from django.shortcuts import render
from .models import CustomUser
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import MyAuthForm
import datetime


def phone_validation(phone):
    if phone.startswith('+998'):
        if len(phone) == 13:
            return True
        elif len(phone) == 17 and '-' in phone:
            return True
        else:
            return False
    else:
        return False


def date_validator(date):
    """Validates a date string in DD-MM-YYYY format"""
    try:
        datetime.datetime.strptime(date, '%d-%m-%Y')
        return True
    except ValueError:
        return False


def register(request):
    """Register a new user"""
    if request.method != 'POST':
        form = MyAuthForm
    else:
        form = MyAuthForm(data=request.POST)
        if form.is_valid():
            form = form.cleaned_data
            phone = form['username']
            birthdate = str(form['password'])
            first_name = form['first_name']
            last_name = form['last_name']
            if not phone_validation(phone):
                phone_error = 'Provide a real phone number'
                return render(request, 'registration/register.html', {'form': form, 'phone_error': phone_error})
            elif not date_validator(birthdate):
                phone_error = 'Provide a real date'
                return render(request, 'registration/register.html', {'form': form, 'phone_error': phone_error})
            else:
                try:
                    new_user = CustomUser.objects.create_user(username=phone, password=birthdate, first_name=first_name, last_name=last_name)
                except:
                    phone_error = 'This user already exists'
                    return render(request, 'registration/register.html', {'form': form, 'phone_error': phone_error})
                else:
                    login(request, new_user)
                    return redirect('restaurant:index')
    context = {'form': form}
    return render(request, 'registration/register.html', context)