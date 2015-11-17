from user.forms import RegistrationForm
from user.models import Student
from user.models import Activation
from django.core.mail import send_mail
from user import mailsettings
import random
import string

from util.render_tools import adaptive_render


@adaptive_render
def register(request, render):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            userdata = form.cleaned_data
            createduser = Student.create(email=userdata['s_number'] + '@mail.zih.tu-dresden.de',
                                         password=userdata['password'],
                                         first_name=userdata['first_name'],
                                         last_name=userdata['family_name'],
                                         s_number=userdata['s_number'],
                                         faculty=userdata['faculty'])
            if createduser is None:
                return render(
                    request,
                    'registration/register.html',
                    {'title': 'Registration',
                     'error': 'The s-Number you entered is already in use!',
                     'form': form})
            else:
                activationMail(createduser.user, request)
                return render(
                    request,
                    'registration/success.html',
                    {'title': 'Registration successfull',
                     'acc': userdata['s_number']})
        else:
            return render(
                request,
                'registration/register.html',
                {'title': 'Registration',
                 'error': 'Please check your input.',
                 'form': form})
    else:
        form = RegistrationForm()
        return render(
            request,
            'registration/register.html',
            {'title': 'Registration',
             'form': form})


def generateToken(size=50, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def activationMail(user, request):
    user_token = generateToken()
    newActivation = Activation(user=user, token=user_token)
    newActivation.save()
    message = ''
    activateurl = request.build_absolute_uri() + '?token=' + user_token
    print(activateurl)
    with open('res/registrationmail.txt') as f:
        message = f.read()
        message = message.format(user=user.first_name,
                       url=activateurl)
    print(message)
    send_mail('Your registration at the iFSR course enrollment system',
              message,
              mailsettings.sender,
              [user.email],
              mailsettings.auth_user,
              mailsettings.auth_pass)
    print(user_token)
