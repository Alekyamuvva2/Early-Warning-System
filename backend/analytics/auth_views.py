from django.contrib.auth.models import User
from rest_framework import status, views, response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class RegisterView(views.APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        
        if not username or not password:
            return response.Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(username=username).exists():
            return response.Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
        user = User.objects.create_user(username=username, password=password, email=email)
        token, _ = Token.objects.get_or_create(user=user)
        
        return response.Response({
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'role': 'advisor' if user.is_staff else 'student'
        }, status=status.HTTP_201_CREATED)

class LoginView(views.APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return response.Response({
                'token': token.key,
                'username': user.username,
                'role': 'advisor' if user.is_staff else 'student'
            })
        return response.Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework.permissions import IsAuthenticated

class ProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return response.Response({
            'username': user.username,
            'email': user.email,
            'role': 'advisor' if user.is_staff else 'student'
        })
        
    def put(self, request):
        user = request.user
        new_username = request.data.get('username')
        new_email = request.data.get('email')
        
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                return response.Response({'error': 'Username already taken'}, status=400)
            user.username = new_username
            
        if new_email is not None:
            user.email = new_email
            
        user.save()
        return response.Response({
            'username': user.username,
            'email': user.email,
            'role': 'advisor' if user.is_staff else 'student',
            'success': 'Profile updated successfully'
        })
    def delete(self, request):
        user = request.user
        user.delete()
        return response.Response({'success': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
