from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from .models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор модели Author."""

    class Meta:
        model = Author
        fields = '__all__'


class AllBooksSerializer(serializers.ModelSerializer):
    """Сериализатор списка кних для /api/books/ ."""

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = Author.objects.filter(
            user_id=request.user.id
        ).first()
        return super().create(validated_data)


class BooksSerializer(serializers.ModelSerializer):
    """Сериализатор конкретной книги для /api/books/id/ ."""

    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор модели User."""

    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    birthday = serializers.DateField()

    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = (
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'birthday',
        )

    def create(self, validated_data):
        """Создание пользователя и автора.

        Args:
            validated_data: dictionary валидные данные

        Функция создает экземпляр модели Author и связывает

        с экземпляром модели User

        Returns:
            user:   user object  экземпляр модели User
        """
        User = get_user_model()
        username = validated_data['username']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        birthday = validated_data['birthday']

        user = User.objects.create(
            username=username,
            email=email,
        )

        user.set_password(validated_data['password'])
        user.save()
        author = Author.objects.filter(user=user).first()
        author.first_name = first_name
        author.last_name = last_name
        author.birthday = birthday
        author.save()
        return user
