from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User
from api_yamdb.settings import ADM_MAIL
from .permissions import IsAdminOnly
from .serializers import (
    SignUpSerializer,
    TokenSerializer,
    UserMeSerializer,
    UserSerializer
)


class SignUpView(generics.CreateAPIView):
    """Вью Регистрации нового пользователя по username и email.
    Отправка письма с кодом подтверждения пользователю.
    """
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Код подтверждения: {confirmation_code}',
            from_email=ADM_MAIL,
            recipient_list=(user.email,),
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(generics.CreateAPIView):
    """Вью получения токена"""
    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        print(request.data)
        serializer = TokenSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        print(serializer.data)
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            print(token)

            return Response({'token': f'{token}'}, status.HTTP_200_OK)
        print(user)
        print(confirmation_code)
        return Response(
            {'message': 'Неверный код подтверждения.'},
            status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """Вью управления пользователем."""
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def edit_profile(self, request):
        """Редактирование собственной страницы."""
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                self.request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserMeSerializer(self.request.user)
        return Response(serializer.data)
