from django.shortcuts import render, get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework import generics
from restapi.models import Subject
from restapi.api.serializers import SubjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from io import BytesIO

# Create your views here.

class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SingleSubject(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        subject = SubjectSerializer
        return Response(subject)