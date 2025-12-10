from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


# Token generator for password reset
token_generator = PasswordResetTokenGenerator()


@csrf_exempt
@api_view(['POST'])
def request_password_reset(request):
    """
    Request password reset - sends email with reset link
    """
    email = request.data.get('email')
    
    if not email:
        return Response(
            {'error': 'Email is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
        
        # Generate token
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Create reset link (frontend URL)
        reset_link = f"http://localhost:5173/reset-password/{uid}/{token}"
        
        # Send email
        subject = 'Password Reset Request - HT Portal'
        message = f"""
Hello {user.username},

You requested to reset your password for HT Portal.

Click the link below to reset your password:
{reset_link}

This link will expire in 1 hour.

If you didn't request this, please ignore this email.

Best regards,
HT Portal Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        print(f"\n{'='*70}")
        print(f"PASSWORD RESET EMAIL SENT TO: {email}")
        print(f"{'='*70}")
        print(f"Reset Link: {reset_link}")
        print(f"{'='*70}\n")
        
    except User.DoesNotExist:
        # Don't reveal if email exists or not (security)
        pass
    
    # Always return success to prevent email enumeration
    return Response(
        {'message': 'If an account exists with this email, a password reset link has been sent.'},
        status=status.HTTP_200_OK
    )


@csrf_exempt
@api_view(['POST'])
def verify_reset_token(request):
    """
    Verify if reset token is valid
    """
    uid = request.data.get('uid')
    token = request.data.get('token')
    
    if not uid or not token:
        return Response(
            {'error': 'UID and token are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
        
        if token_generator.check_token(user, token):
            return Response(
                {'message': 'Token is valid', 'email': user.email},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid or expired token'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except (User.DoesNotExist, ValueError, TypeError):
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_400_BAD_REQUEST
        )


@csrf_exempt
@api_view(['POST'])
def reset_password(request):
    """
    Reset password with valid token
    """
    uid = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('password')
    
    if not uid or not token or not new_password:
        return Response(
            {'error': 'UID, token, and new password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate password length
    if len(new_password) < 6:
        return Response(
            {'error': 'Password must be at least 6 characters long'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
        
        if token_generator.check_token(user, token):
            # Set new password (automatically hashes it)
            user.set_password(new_password)
            user.save()
            
            print(f"\n{'='*70}")
            print(f"PASSWORD RESET SUCCESSFUL FOR: {user.email}")
            print(f"{'='*70}\n")
            
            return Response(
                {'message': 'Password has been reset successfully'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid or expired token'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except (User.DoesNotExist, ValueError, TypeError):
        return Response(
            {'error': 'Invalid token'},
            status=status.HTTP_400_BAD_REQUEST
        )
