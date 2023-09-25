from sections.storage_backend import get_cloud_storage
from rest_framework import serializers
from .models import Section
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.utils.module_loading import import_module
from django.utils.text import slugify
from django.contrib.auth.models import User


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class SectionSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    collaborators = serializers.PrimaryKeyRelatedField(many=True, queryset=get_user_model().objects.all())
    nested_sections = RecursiveField(many=True, read_only=True)
    content = serializers.CharField(write_only=True, required=False)

    permission_classes = [IsAuthenticated]

    class Meta:
        model = Section
        fields = ['id', 'title', 'author', 'parent_section', 'root', 'collaborators', 'nested_sections', 'content']

    def create(self, validated_data):
        self._check_permissions('Authors')
        section, content = self._create_section(validated_data)        
        self._handle_content(section, content)
        return section

    def update(self, instance, validated_data):
        self._check_permissions('Authors', 'Collaborators')
        self._update_section(instance, validated_data)

        self._handle_content(instance, validated_data.get('content'))
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['content'] = self._read_content(instance)
        #TODO: I know this is not optimal as for every Secion in the Sections list queryset it will connect to Cloud Storage
        # This could be fixed in the future.
        return ret

    def _check_permissions(self, *groups):
        user = self.context['request'].user
        if any(user.groups.filter(name=group).exists() for group in groups):
            return
        else:
            raise PermissionDenied("You do not have the necessary permissions to perform this action.")

    def _create_section(self, validated_data):
        collaborators = validated_data.pop('collaborators')
        content = validated_data.pop('content', "")
        parent_section = validated_data.get('parent_section')
        root = validated_data.get('root')
        if not root and not parent_section:
            raise serializers.ValidationError("Non root sections must have a parent section.")
        if root and parent_section:
            raise serializers.ValidationError("Root sections cant have a parent section in the same time")
        section = Section.objects.create(**validated_data)            
        self._add_collaborators(collaborators, section)
        return section, content

    def _update_section(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        new_parent_section = validated_data.get('parent_section')
        if new_parent_section and new_parent_section != instance.parent_section:
            raise serializers.ValidationError("Parent section can't be updated.")
        if instance.parent_section and validated_data.get('root', False):
            raise serializers.ValidationError("A section with a parent section cannot be a root section.")
        instance.root = validated_data.get('root', instance.root)
        self._add_collaborators(validated_data.get('collaborators'), instance)

    def _add_collaborators(self, collaborators, section):
        if section.parent_section and section.parent_section.collaborators:
            section.collaborators.set(section.parent_section.collaborators.all())
            return
        if collaborators is not None:            
            collaborators_group = Group.objects.get(name='Collaborators')
            for collaborator in collaborators:
                if not collaborator.groups.filter(name='Collaborators').exists():
                    collaborator.groups.add(collaborators_group)
            section.collaborators.set(collaborators)

    def _handle_content(self, section, content):
        if content:
            cloud_storage = get_cloud_storage()
            if not cloud_storage.file_exist(section.content_url) or not section.content_url:
                section.content_url = cloud_storage.create_folder(folder_path=section.storage_key, content=content)
                section.save()
            else:
                cloud_storage.update_folder(folder_path=section.storage_key, content=content)

    def _read_content(self, instance):
        cloud_storage = get_cloud_storage()
        return cloud_storage.read_file(instance.content_url)
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user