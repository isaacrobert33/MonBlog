
from rest_framework import serializers
from restapi.models import Subject, Course

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']

class CourseSerializer(serializers.ModelSerializer):
       class Meta:
           model = Course
           fields = ['id', 'subject', 'title', 'slug',
                     'overview', 'created', 'owner',
                     'modules']