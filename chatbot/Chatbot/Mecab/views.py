from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from khaiii import KhaiiiApi

# Create your views here.


@api_view(['POST'])
def word(request):
    text = request.data['text']
    api = KhaiiiApi()  # 내 설치 경로

    morphs = []

    for word in api.analyze(text):
        for morph in word.morphs:
            morphs.append((morph.lex, morph.tag))

    return Response({'message': morphs})
