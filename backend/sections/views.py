from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group

from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Section
from .serializers import SectionSerializer, UserSerializer
from sections.storage_backend import get_cloud_storage


class SectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sections to be viewed or edited.
    """
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the sections
        for the currently authenticated user.
        """
        user = self.request.user
        return Section.objects.filter(author=user) | Section.objects.filter(collaborators=user)

    @action(detail=False)
    def root_list(self, request):
        """
        This view should return a list of all the root sections
        for the currently authenticated user.
        """        
        root_sections = self.get_queryset().filter(root=True)
        serializer = self.get_serializer(root_sections, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Set the author as the current logged in user
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        # Check if the user is the author or a collaborator
        section = serializer.instance
        if self.request.user != section.author and self.request.user not in section.collaborators.all():
            raise PermissionDenied("Only the author or collaborators can update sections.")

        # Update the section in the database
        serializer.save()

    def perform_destroy(self, instance):
        # Check if the user is in the 'Author' group
        if not self.request.user.groups.filter(name='Authors').exists():
            raise PermissionDenied("Only authors can delete sections.")

        # Delete the corresponding folder in the cloud storage
        cloud_storage = get_cloud_storage()
        cloud_storage.delete_folder(instance.storage_key)

        # Delete the section from the database
        instance.delete()


class UserRegistrationView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)            
            user.groups.add(Group.objects.get(name='Authors'))
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserLoginView(APIView):
    permission_classes = []
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

