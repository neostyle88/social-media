from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "bio",
            "avatar",
        )
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserListSerializer(UserSerializer):
    followers_count = serializers.IntegerField(
        source="followers.count", read_only=True
    )
    followings_count = serializers.IntegerField(
        source="followings.count", read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "full_name",
            "is_online",
            "avatar",
            "followers_count",
            "followings_count",
        )


class UserDetailSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "is_online",
            "full_name",
            "followers",
            "followings",
            "bio",
        )
