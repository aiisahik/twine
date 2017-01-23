from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from . import serializers, models

class AccountView(TemplateView):
    template_name = 'base/_base.html'
    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        response = self.render_to_response(context)
        return response

    def get_context_data(self, **kwargs):
    	context = {}
    	return context

class ProfileAPIViewSet(ModelViewSet):
    queryset = models.Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return self.queryset.select_related('user')


# Create your views here.
