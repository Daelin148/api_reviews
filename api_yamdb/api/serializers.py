from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.utils import timezone

from reviews.models import Title, Genre, Category, Comment, Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(slug_field='slug',
                                          queryset=Genre.objects.all(),
                                          many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего года."
            )
        return value


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
