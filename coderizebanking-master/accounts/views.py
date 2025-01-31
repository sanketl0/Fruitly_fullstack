from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.hashers import make_password
import json
import random
from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
# from .permission import IsUserWithAccessPermission
from rest_framework.views import APIView
from rest_framework.response import Response
User = get_user_model()

class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        mobile_number = data.get('mobile_number')
        password = data.get('password')
        role = data.get('role')

        # Check if the mobile_number already exists
        if User.objects.filter(mobile_number=mobile_number).exists():
            return JsonResponse({'error': 'mobile_number already in use'}, status=400)

        # Validate the role
        if role not in ['user1', 'user2', 'admin']:
            return JsonResponse({'error': 'Invalid role. Must be one of [user1, user2, admin]'}, status=400)

        if role == 'user1' or role == 'user2':
            # Both user1 and user2 require approval from admin
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                mobile_number=mobile_number,
                role=role,
                is_active=False,  # Not active until approved
                is_approved=False  # Not approved initially
            )
        else:
            # Admin gets full access immediately
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                mobile_number=mobile_number,
                role=role,
                is_active=True,  # Admin is active immediately
                is_approved=True  # Admin is approved immediately
            )

        # Hash the password and save the user
        user.set_password(password)
        user.save()

        if role == 'user1' or role == 'user2':
            return JsonResponse({'message': f'{role} registered successfully, awaiting admin approval'}, status=201)
        else:
            return JsonResponse({'message': 'Admin registered successfully'}, status=201)



class ApproveUserView(View):
    def post(self, request):
        data = json.loads(request.body)
        mobile_number = data.get('mobile_number')

        try:
            user = User.objects.get(mobile_number=mobile_number)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        # Check if the user is already approved
        if user.is_approved:
            return JsonResponse({'error': 'User already approved'}, status=400)

        # Only Admin can approve users
        if request.user.role != 'admin':
            return JsonResponse({'error': 'You do not have permission to approve users'}, status=403)

        user.is_approved = True
        user.is_active = True  # Set the user to active once approved
        user.save()

        return JsonResponse({'message': 'User approved successfully'}, status=200)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            mobile_number = data.get('mobile_number')
            password = data.get('password')
            role = data.get('role')

            if not mobile_number or not password or not role:
                return JsonResponse({'error': 'mobile_number, password, and role are required'}, status=400)

            # Fetch the user based on the mobile_number
            try:
                user = User.objects.get(mobile_number=mobile_number)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Invalid mobile_number or password'}, status=400)

            # ✅ Check if the user is approved BEFORE authentication
            if not user.is_approved:
                return JsonResponse({'error': 'Your account is pending approval by the admin'}, status=403)

            # ✅ Check if the user is active
            if not user.is_active:
                return JsonResponse({'error': 'Your account is inactive'}, status=403)

            # Authenticate the user
            user = authenticate(request, username=mobile_number, password=password)
            if user is None:
                return JsonResponse({'error': 'Invalid mobile_number or password'}, status=400)

            # Ensure the role provided during login matches the user's registered role
            if role != user.role:
                return JsonResponse({'error': f'You must log in as a {user.role} user'}, status=400)

            # Generate or retrieve an authentication token for the user
            token, created = Token.objects.get_or_create(user=user)

            return JsonResponse({
                'message': 'Login successful',
                'user': user.mobile_number,
                'token': token.key,
                'role': user.role
            }, status=200)

        except Exception as e:
            print(f"Unexpected error: {str(e)}")  # Log the error for debugging
            return JsonResponse({'error': 'An unexpected error occurred. Please try again later.'}, status=500)

# class LoginView(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         email = data.get('email')
#         password = data.get('password')
#         role = data.get('role')  # Ensure the client sends the role during login

#         try:
#             # Fetch the user based on the email
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return JsonResponse({'error': 'Invalid email or password'}, status=400)

#         # Authenticate the user with the provided password
#         user = authenticate(request, username=email, password=password)

#         if user is None:
#             return JsonResponse({'error': 'Invalid email or password'}, status=400)

#         # Check if the user is approved and active
#         if not user.is_approved:
#             return JsonResponse({'error': 'Your account is pending approval'}, status=400)

#         if not user.is_active:
#             return JsonResponse({'error': 'Your account is inactive'}, status=400)

#         # Role-based restrictions:
#         # Ensure the role provided during login matches the role the user is registered with
#         if role != user.role:
#             return JsonResponse({'error': f'You must log in as a {user.role} user'}, status=400)

#         # Generate or retrieve an authentication token for the user
#         token, created = Token.objects.get_or_create(user=user)

#         return JsonResponse({
#             'message': 'Login successful',
#             'user': user.email,
#             'token': token.key,
#             'role':role
#         }, status=200)

