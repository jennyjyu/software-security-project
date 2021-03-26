import django
from rest_framework import mixins, generics
from workouts.mixins import CreateListModelMixin
from rest_framework import permissions, status
from users.serializers import (
    UserSerializer,
    OfferSerializer,
    AthleteFileSerializer,
    UserPutSerializer,
    UserGetSerializer,
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from users.models import Offer, AthleteFile
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from users.permissions import IsCurrentUser, IsAthlete, IsCoach, IsRecipient
from workouts.permissions import IsOwner, IsReadOnly
from users.forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse, JsonResponse

# Create your views here.
class UserList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        self.serializer_class = UserGetSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('email_template.html', {
                    'username': request.data['username'], #Endret på for å passe til koden vår, printet for å finne formatet å endre til
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
            to_email = request.data['email'] #Endret på for å passe til koden vår, printet for å finne formatet å endre til 
            send_mail(mail_subject, message, None, [to_email], fail_silently=False)
            
            return JsonResponse({'Please confirm your email address to complete the registration':''})
        else:
            return HttpResponse('Something went wrong..', status=status.HTTP_400_BAD_REQUEST) #Googlet måte å legge inn bad request 

    def get_queryset(self):
        qs = get_user_model().objects.all()

        if self.request.user:
            # Return the currently logged in user
            status = self.request.query_params.get("user", None)
            if status and status == "current":
                qs = get_user_model().objects.filter(pk=self.request.user.pk)

        return qs

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

class UserDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    lookup_field_options = ["pk", "username"]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAuthenticated & (IsCurrentUser | IsReadOnly)]

    def get_object(self):
        for field in self.lookup_field_options:
            if field in self.kwargs:
                self.lookup_field = field
                break

        return super().get_object()

    def get(self, request, *args, **kwargs):
        self.serializer_class = UserGetSerializer
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.serializer_class = UserPutSerializer
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class OfferList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    permission_classes = [IsOwner | IsRecipient]
    serializer_class = OfferSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = Offer.objects.none()

        if self.request.user:
            qs = Offer.objects.filter(
                Q(owner=self.request.user) | Q(recipient=self.request.user)
            ).distinct()

            # filtering by status (if provided)
            status = self.request.query_params.get("status", None)
            if status is not None:
                qs = qs.filter(status=status)

            # filtering by category (sent or received)
            category = self.request.query_params.get("category", None)
            if category is not None:
                if category == "sent":
                    qs = qs.filter(owner=self.request.user)
                elif category == "received":
                    qs = qs.filter(recipient=self.request.user)

        return qs


class OfferDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [IsOwner | IsRecipient]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AthleteFileList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    CreateListModelMixin,
    generics.GenericAPIView,
):
    queryset = AthleteFile.objects.all()
    serializer_class = AthleteFileSerializer
    permission_classes = [permissions.IsAuthenticated & (IsAthlete | IsCoach)]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = AthleteFile.objects.none()

        if self.request.user:
            qs = AthleteFile.objects.filter(
                Q(athlete=self.request.user) | Q(owner=self.request.user)
            ).distinct()

        return qs


class AthleteFileDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = AthleteFile.objects.all()
    serializer_class = AthleteFileSerializer
    permission_classes = [permissions.IsAuthenticated & (IsAthlete | IsOwner)]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
