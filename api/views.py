from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer

@csrf_exempt
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def login_view(request):
    email = request.data.get('username')  # Frontend sends email as 'username'
    password = request.data.get('password')
    
    print(f"DEBUG: Login attempt - email: {email}, password: {'*' * len(password) if password else 'None'}")
    
    # Try to find user by email
    try:
        user_obj = User.objects.get(email=email)
        print(f"DEBUG: Found user - username: {user_obj.username}, email: {user_obj.email}")
        
        # Authenticate using the actual username
        user = authenticate(request, username=user_obj.username, password=password)
        print(f"DEBUG: Authentication result: {user is not None}")
        
        if user:
            # Create Django session
            login(request, user)
            
            # Get user's groups
            groups = list(user.groups.values_list('name', flat=True))
            
            print(f"DEBUG: Login successful for {user.username}")
            return Response({
                'message': 'Login successful',
                'username': user.username,
                'email': user.email,
                'groups': groups
            }, status=status.HTTP_200_OK)
        else:
            print(f"DEBUG: Authentication failed - password incorrect")
    except User.DoesNotExist:
        print(f"DEBUG: User not found with email: {email}")
        pass
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
