"""Contains views for the workouts application. These are mostly class-based views.
"""
from rest_framework import generics, mixins
from rest_framework import permissions

from rest_framework.parsers import (
    JSONParser,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Q
from rest_framework import filters
from workouts.parsers import MultipartJsonParser
from workouts.permissions import (
    IsOwner,
    IsCoachAndVisibleToCoach,
    IsOwnerOfWorkout,
    IsCoachOfWorkoutAndVisibleToCoach,
    IsReadOnly,
    IsPublic,
    IsWorkoutPublic,
    mediaPermissionAccess
)
from workouts.mixins import CreateListModelMixin
from workouts.models import Workout, Exercise, ExerciseInstance, WorkoutFile
from workouts.serializers import WorkoutSerializer, ExerciseSerializer
from workouts.serializers import RememberMeSerializer
from workouts.serializers import ExerciseInstanceSerializer, WorkoutFileSerializer
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
import json
from collections import namedtuple
import base64, pickle
from django.core.signing import Signer
from django.views.static import serve 

class MediaDetail(
    generics.GenericAPIView,
):
    permission_classes = [permissions.IsAuthenticated & mediaPermissionAccess]

    def get(self, request, path, document_root, *args, **kwargs):
        return self.protected_serve(request, path, document_root)


    def protected_serve(self, request, path, document_root=None, show_indexes=False):
        return serve(request, path, document_root, show_indexes)










