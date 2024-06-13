from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from core.models import User
from core.validators import validate_username
from reviews.models import Category, Comment, Genre, Review, Title


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



class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        # fields = '__all__'
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):

    genres = serializers.SlugRelatedField(slug_field='slug',
                                          queryset=Genre.objects.all(),
                                          many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего года."
            )
        return value

    def get_rating(self, obj):
        ratings_sum = sum(obj.reviews.all(), key=lambda review: review.score)
        return ratings_sum // obj.reviews.count()


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        exclude = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('user', 'title')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        exclude = ('review',)
