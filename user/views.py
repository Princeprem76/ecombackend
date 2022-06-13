import six
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserEmail, UserDetails
from .serializers import UserhasDataSerial
from .utils import Util


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def activatepw(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        users = UserEmail.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserEmail.DoesNotExist):
        users = None
    if users is not None and account_activation_token.check_token(users, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        return Response({
            "message": "User Verified!",
            "user_id": uid,
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "message": "Invalid Activation Link!",
        },
            status=status.HTTP_400_BAD_REQUEST, )


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        users = UserEmail.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserEmail.DoesNotExist):
        users = None
    if users is not None and account_activation_token.check_token(users, token):
        users.is_verified = True
        users.save()
        uid = force_str(urlsafe_base64_decode(uidb64))
        return Response({
            "message": "Email Verified!",
            "user_id": uid,
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "message": "Invalid Activation Link!",
        },
            status=status.HTTP_400_BAD_REQUEST, )


# Create your views here.


class Create_User(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            userSign = UserEmail.objects.create_user(
                email=data['email'],
                password=data['password'],
            )
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('../templates/emailtemplate.html', {
                'user': userSign,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(userSign.pk)),
                'token': account_activation_token.make_token(userSign),
            })
            to_email = data['email']
            data = {'email_body': message,
                    'email': to_email, 'subject': mail_subject}
            Util.send_email(data)
            userSign.save()
            return Response({
                "message": "Verification link sent!",
            }, status=status.HTTP_200_OK)

        except:
            return Response({
                "message": "Error!",
            },
                status=status.HTTP_400_BAD_REQUEST, )


class Login_User(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        global email, password
        if request.method == 'POST':
            data = request.data
            email = data['email']
            password = data['password']
        try:
            user = authenticate(username=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                login(request, user)
                userdetails = UserEmail.objects.get(email=email)
                serializer = UserhasDataSerial(userdetails, many=False)
                if userdetails.is_verified == False:
                    reverify(request, userdetails, email)
                response = {
                    "user_id": userdetails.id,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user_data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "Email or password doesn't match!",
                }, status=status.HTTP_400_BAD_REQUEST)
        except UserEmail.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)


class emailpass(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            emails = data['email']
            signupdata = UserEmail.objects.get(email=emails)
            current_site = get_current_site(request)
            mail_subject = 'Change Your Password.'
            message = render_to_string('../templates/passwordtemplate.html', {
                'user': signupdata,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(signupdata.pk)),
                'token': account_activation_token.make_token(signupdata),
            })
            to_email = emails
            data = {'email_body': message,
                    'email': to_email, 'subject': mail_subject}
            Util.send_email(data)
            messages.success(request, "")
            return Response({"message": "Check your email for password reset link", }, status=status.HTTP_200_OK, )
        except:
            return HttpResponse('error')


def reverify(request, signupdata, emails):
    try:
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('../templates/emailtemplate.html', {
            'user': signupdata,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(signupdata.pk)),
            'token': account_activation_token.make_token(signupdata),
        })
        to_email = emails
        data = {'email_body': message,
                'email': to_email, 'subject': mail_subject}
        Util.send_email(data)
        return Response({"message": "Check your email for email verification link!", }, status=status.HTTP_200_OK, )
    except:
        return Response({
            "message": "Error!",
        },
            status=status.HTTP_400_BAD_REQUEST, )


class forgetpw(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            newpw = data['password']
            repw = data['repassword']
            if newpw == repw:
                userdata = UserEmail.objects.get(id=kwargs['id'])
                userdata.set_password(newpw)
                userdata.save()
                return Response({"message": "The password has been reset!", }, status=status.HTTP_200_OK, )
        except:
            return Response({
                "message": "Error!",
            },
                status=status.HTTP_400_BAD_REQUEST, )


class signup(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            user = data['UserName']
            age = data['UserAge']
            contact = data['UserContact']
            address = data['userAddress']
            gender = data['gender']
            UserDetails(Name=user, age=age, phone=contact, address=address, gender=gender,
                        email_id=id).save()
            dat = UserEmail.objects.get(id=kwargs['id'])
            dat.has_data = True
            dat.save()
            return Response({"message": "The Signup process is completed. Please Login!", },
                            status=status.HTTP_200_OK, )
        except:
            return Response({
                "message": "Error!",
            },
                status=status.HTTP_400_BAD_REQUEST, )


def logouts(request):
    logout(request)
    return Response({"message": "Successfully Logged Out", }, status=status.HTTP_200_OK, )


def details(request):
    if request.method == 'POST':
        data = request.data
        try:
            address = data['userAddress']
            age = data['UserAge']
            contact = data['UserContact']
            userData = UserDetails.objects.get(email__email=request.user)
            userData.age = age
            userData.phone = contact
            userData.address = address
            userData.save()
            return Response({"message": "The details has been updated!", }, status=status.HTTP_200_OK, )
        except:
            return Response({
                "message": "Error!",
            },
                status=status.HTTP_400_BAD_REQUEST, )


def changepass(request):
    if request.method == 'POST':
        data = request.data
        try:
            oldpass = data['oldpassword']
            newpw = data['password']
            repw = data['repassword']
            user = authenticate(username=request.user, password=oldpass)
            if user is not None:
                if newpw == repw:
                    userdata = UserEmail.objects.get(email=request.user)
                    userdata.set_password(newpw)
                    userdata.save()
                    return Response({"message": "The password has been updated!", }, status=status.HTTP_200_OK, )
                else:

                    return Response({
                        "message": "The password doesn't match",
                    },
                        status=status.HTTP_400_BAD_REQUEST, )
            else:
                return Response({
                    "message": "Wrong Password!",
                },
                    status=status.HTTP_400_BAD_REQUEST, )
        except:
            return Response({
                "message": "Error!",
            },
                status=status.HTTP_400_BAD_REQUEST, )
