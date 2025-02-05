from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status,permissions
from rest_framework.response import Response

from allowed_emails.models import AllowedEmail


class CustomUserViewSet(DjoserUserViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # First, check if the email is allowed before attempting to create the user
        email = request.data.get('email')
        try:
            isAllowed = AllowedEmail.objects.get(email=email)
            # Store the allowed email object to delete it after the user is created
            self.isAllowed = isAllowed
            return super().create(request, *args, **kwargs)
        except AllowedEmail.DoesNotExist:
            return Response({'error': 'Email not allowed'}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        # Call the original perform_create method to create the user
        super().perform_create(serializer)
    
        # After the user is created, delete the allowed email object
        if hasattr(self, 'isAllowed'):
            self.isAllowed.delete()
