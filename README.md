## Тестовое python django back-end developer
## Разработайте back-end приложение с использованием Django и базой данных SQLite, которое будет предоставлять API для работы с объектами "Книга" и "Автор".

# API должно содержать следующие эндпойнты:

GET /api/books/ - список всех книг в базе данных
GET /api/books/<int:pk>/ - детальная информация об одной книге
POST /api/books/ - создание новой книги
PUT /api/books/<int:pk>/ - обновление информации о книге
DELETE /api/books/<int:pk>/ - удаление книги из базы данных
Требования к базе данных:

# Создать модели "Книга" и "Автор"
Каждая книга должна иметь атрибуты "Название", "Автор", "Описание" и "Дата публикации"
Каждый автор должен иметь атрибуты "Имя", "Фамилия" и "Дата рождения"
Требования к аутентификации:

Для доступа к эндпойнтам нужно использовать токен-аутентификацию
При создании новой книги авторизованный пользователь должен быть автором книги.
Требования к тестированию:

Написать тесты для API, которые проверяют корректность работы каждого эндпойнта
Использовать библиотеку pytest-django для тестирования

http://localhost:8000/api/auth/users/   создание пользователей

http://127.0.0.1:8000/auth/token/login/  получение токена
