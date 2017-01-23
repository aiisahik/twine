from django.shortcuts import render
from django.views.generic import View
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.http import Http404, HttpResponseRedirect, HttpResponse
from . import models, serializers


class BattleAPIViewSet(ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        num_battles = 100
        if request.GET.get('num', None):
            num_battles = int(request.GET.get('num'))
        queryset = models.Battle.objects.get_battles(num=num_battles, judge=request.user.profile)
        serializer = serializers.BattleSerializer(queryset, many=True)
        return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)
