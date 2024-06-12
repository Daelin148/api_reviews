from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User
from reviews.validators import validate_username


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username, ]
    )
    email = serializers.EmailField(required=True, max_length=254)

    def validate(self, data):
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():
            return data
        if (User.objects.filter(username=data['username']).exists()
                or User.objects.filter(email=data['email']).exists()):
            raise serializers.ValidationError(
                'Пользователь с такими данными уже существует!'
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class UserMeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
