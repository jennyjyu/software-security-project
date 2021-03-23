from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from users.models import Offer, AthleteFile
from django import forms


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #Endret til password 1 og password 2 i hele denne og serializers.html fordi det er dette forms i django forventet 
    password1 = serializers.CharField(style={"input_type": "password"}, write_only=True)  
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "url",
            "id",
            "email",
            "username",
            "password1",
            "password2",
            "athletes",
            "coach",
            "workouts",
            "coach_files",
            "athlete_files",
        ]

    def validate_password1(self, value):
        data = self.get_initial()

        password = data.get("password1")
        password1 = data.get("password2")

        try:
            password_validation.validate_password(password)
        except forms.ValidationError as error:
            raise serializers.ValidationError(error.messages)

        if password != password1:
            raise serializers.ValidationError("Passwords must match!")

        return value

    def validate_email(self, value):
        data = self.get_initial()

        email = data.get("email")

        if not email:
            raise serializers.ValidationError("Enter a valid email address.")

        return value 

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        user_obj = get_user_model()(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        
        return user_obj


class UserGetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "url",
            "id",
            "email",
            "username",
            "athletes",
            "coach",
            "workouts",
            "coach_files",
            "athlete_files",
        ]


class UserPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["athletes"]

    def update(self, instance, validated_data):
        athletes_data = validated_data["athletes"]
        instance.athletes.set(athletes_data)

        return instance


class AthleteFileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = AthleteFile
        fields = ["url", "id", "owner", "file", "athlete"]

    def create(self, validated_data):
        return AthleteFile.objects.create(**validated_data)


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Offer
        fields = [
            "url",
            "id",
            "owner",
            "recipient",
            "status",
            "timestamp",
        ]
