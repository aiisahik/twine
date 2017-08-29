import json
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from rest_framework.permissions import IsAuthenticated
from . import models, serializers
from account.models import Profile

class PlayerAPIViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PlayerSerializer
    def get_queryset(self):
        print "self.request.user.profile", self.request.user.profile

        return models.Player.objects.filter(judge=self.request.user.profile).all()


class BattleAPIViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.BattleSerializer
    """
    A simple ViewSet for listing or retrieving users.
    """
    def get_queryset(self):
        return models.Battle.objects.filter(judge=self.request.user.profile).all()

    def list(self, request):
        num_battles = 100
        if request.GET.get('num', None):
            num_battles = int(request.GET.get('num'))
        if request.user.profile:
            queryset = models.Battle.objects.filter(judge=judge, pick_date__isnull=True)[0:num_battles]
            serializer = serializers.BattleSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"success": False})

    def retrieve(self, request, pk=None):
        if request.user.profile:
            queryset = models.Battle.objects.filter(judge=request.user.profile)
            battle = get_object_or_404(queryset, pk=pk)
            serializer = serializers.BattleSerializer(battle)
            return Response(serializer.data)
        else:
            raise HttpResponseForbidden("User lacks profile")

    def partial_update(self, request, pk=None):
        import pdb;pdb.set_trace()
        request_data = json.loads(request.body)
        winner = request_data.get('winner', None)
        if pk and winner:
            battle = models.Battle.objects.get(id=pk)
            battle.pick(winner)
            serializer = serializers.BattleSerializer(battle)
            return Response(serializer.data)
        else:
            return Response({"success": False})

    # def update(self, request, pk=None):
    #     return self.partial_update(request, *args, **kwargs)
