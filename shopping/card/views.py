from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CardSerializer
from django.contrib import messages


class AddCard(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        serializer = CardSerializer
        return Response({'serializer': serializer}, status=200, template_name='card/addcard.html')

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = CardSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'serializer': serializer}, template_name='card/addcard.html')
        serializer.save()
        messages.add_message(request, messages.SUCCESS, 'Card details Saved Successfully Now please select the card '
                                                        'to pay.')
        return redirect('/checkout/')
