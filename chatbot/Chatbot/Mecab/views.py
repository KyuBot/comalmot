from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from eunjeon import Mecab

# Create your views here.
@api_view(['POST'])
def word(request):
    text = request.data['text']
    mecab = Mecab(dicpath='C:\\Users\\multicampus\\Desktop\\pjt_last\\s03p31b206\\chatbot\\Mecab\\mecab-ko-dic')
    a = mecab.pos(text)
    print(a)
    a = mecab.morphs(text)
    print(a)
    return Response({'message': a})



