from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from reviews.models import Review, Comment, Title

from .serializers import (CommentSerializer, ReviewSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        serializer.save(title=self.get_title())

    def get_queryset(self):
        return self.get_title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        serializer.save(review=self.get_review())

    def get_queryset(self):
        return self.get_review().comments.all()
