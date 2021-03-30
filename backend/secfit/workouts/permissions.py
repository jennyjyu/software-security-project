"""Contains custom DRF permissions classes for the workouts app
"""
from rest_framework import permissions
from workouts.models import Workout
from workouts.models import Workout, Exercise, ExerciseInstance, WorkoutFile
from django.db.models import Q
from users.models import Offer, AthleteFile




class IsOwner(permissions.BasePermission):
    """Checks whether the requesting user is also the owner of the existing object"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOfWorkout(permissions.BasePermission):
    """Checks whether the requesting user is also the owner of the new or existing object"""

    def has_permission(self, request, view):
        if request.method == "POST":
            if request.data.get("workout"):
                workout_id = request.data["workout"].split("/")[-2]
                workout = Workout.objects.get(pk=workout_id)
                if workout:
                    return workout.owner == request.user
            return False

        return True

    def has_object_permission(self, request, view, obj):
        return obj.workout.owner == request.user


class IsCoachAndVisibleToCoach(permissions.BasePermission):
    """Checks whether the requesting user is the existing object's owner's coach
    and whether the object (workout) has a visibility of Public or Coach.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner.coach == request.user and (
            obj.visibility == "PU" or obj.visibility == "CO"
        )


class IsCoachOfWorkoutAndVisibleToCoach(permissions.BasePermission):
    """Checks whether the requesting user is the existing workout's owner's coach
    and whether the object has a visibility of Public or Coach.
    """

    def has_object_permission(self, request, view, obj):
        return obj.workout.owner.coach == request.user and (
            obj.workout.visibility == "PU" or obj.workout.visibility == "CO"
        )


class IsPublic(permissions.BasePermission):
    """Checks whether the object (workout) has visibility of Public."""

    def has_object_permission(self, request, view, obj):
        return obj.visibility == "PU"


class IsWorkoutPublic(permissions.BasePermission):
    """Checks whether the object's workout has visibility of Public."""

    def has_object_permission(self, request, view, obj):
        return obj.workout.visibility == "PU"


class IsReadOnly(permissions.BasePermission):
    """Checks whether the HTTP request verb is only for retrieving data (GET, HEAD, OPTIONS)"""

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS

class mediaPermissionAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        """A workoutfile should be visible to the requesting user if any of the following hold:
            - The file is on a public visibility workout
            - The file was written by the user
            - The file is on a coach visibility workout and the user is the workout owner's coach
            - The file is on a workout owned by the user
            """
        path = view.kwargs["path"].split("/")
        qs = False
        # Check if the file is a workout file
        if path[0] in "workouts":
            qs = WorkoutFile.objects.filter(
                Q(workout=int(path[1]))
                & (
                    Q(owner=request.user)
                    | Q(workout__owner=request.user)
                    | (
                        Q(workout__visibility="CO")
                        & Q(workout__owner__coach=request.user)
                    )
                    | Q(workout__visibility="PU")
                )  
            ).distinct()
        # Check if the file is a athelete or coach file
        elif path[0] in "users":
            qs = AthleteFile.objects.filter(
                Q(athelete=int(path[1]))
                & (
                    Q(owner=request.user) 
                    | Q(athlete=request.user)
                )
            ).distinct()
        return qs

class IsCoachOfReferencedWorkoutAndVisibleToCoach(permissions.BasePermission):
    """Checks whether the requesting user is the referenced workout's owner's coach
    and whether the referenced workout has a visibility of Public or Coach.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            if request.data.get("workout"):
                workout_id = request.data["workout"].split("/")[-2]
                workout = Workout.objects.get(pk=workout_id)
                if workout:
                    return workout.owner.coach == request.user and (
                           workout.visibility == "PU" or workout.visibility == "CO")
            return False
        return True
