from rest_framework import serializers
from todolist.models import Todolist


class TodolistSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Todolist
        fields = '__all__'


class TodolistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todolist
        fields = ('title',)

