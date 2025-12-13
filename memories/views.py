import base64
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from .models import Memory
from .serializers import MemorySerializer
from api.permissions import IsAdminOrManagerOrReadOnly

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class MemoryViewSet(viewsets.ModelViewSet):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [IsAdminOrManagerOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        # Check if a file was uploaded
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            try:
                # Read file content
                file_content = uploaded_file.read()
                
                # Convert to base64
                encoded_string = base64.b64encode(file_content).decode('utf-8')
                
                # Determine mime type
                mime_type = uploaded_file.content_type if uploaded_file.content_type else 'application/octet-stream'
                
                # Create data URI
                final_string = f"data:{mime_type};base64,{encoded_string}"
                
                # Update data dictionary
                data['file'] = final_string
            except Exception as e:
                return Response({'error': f'File processing failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
        # If file is NOT in request.FILES, check if it's already in data (base64 string case)
        # If not, it will likely fail validation, but let's be explicit
        elif 'file' not in data or not data['file']:
             return Response({'error': 'No file provided. request.FILES is empty and data["file"] is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
