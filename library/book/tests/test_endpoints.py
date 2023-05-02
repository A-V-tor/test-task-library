import pytest
from rest_framework.test import APIClient
from book.models import Book, Author
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


@pytest.fixture()
def api_client():
    return APIClient


class TestListBooksNoToken:
    endpoint = '/api/books/'

    @pytest.mark.django_db
    def test_list_books(self, api_client):
        response = api_client().get(self.endpoint)
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_create_book(self, api_client):
        response = api_client().post(self.endpoint)
        assert response.status_code == 401


class TestListBooksByToken:
    endpoint_by_token = '/auth/token/login/'
    endpoint = '/api/books/'

    @pytest.fixture()
    def new_user(self):
        return User.objects.create(
            username='admin', password=make_password('admin')
        )

    @pytest.fixture()
    def new_author(self, new_user):
        new_author = Author.objects.filter(user=new_user).first()
        new_author.first_name = 'test'
        new_author.last_name = 'test2'
        new_author.birthday = '1999-09-01'
        new_author.save()
        return None

    @pytest.fixture()
    def test_token(self, api_client, new_author):
        data_user = {'username': 'admin', 'password': 'admin'}
        response = api_client().post(
            self.endpoint_by_token,
            data=data_user,
            format='json',
        )
        response_data = response.json()
        auth_token = response_data.get('auth_token')
        assert response.status_code == 200
        assert 'auth_token' in response_data
        return auth_token

    @pytest.fixture()
    def new_book(self):
        return {
            'title': 'Мартин Иден',
            'description': 'Рассказ про молодого писателя',
            'publication_date': '1909-09-01',
            'author': {
                'user': 1,
                'first_name': 'Джек',
                'last_name': 'Лондон',
                'birthday': '2023-04-30',
            },
        }

    @pytest.mark.django_db
    def test_url_get(self, api_client, test_token):
        response = api_client().get(
            self.endpoint,
            HTTP_AUTHORIZATION='Token ' + test_token,
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_url_post(self, api_client, test_token, new_book):
        response = api_client().post(
            self.endpoint,
            data=new_book,
            format='json',
            HTTP_AUTHORIZATION='Token ' + test_token,
        )
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_url_put(self, api_client, test_token, new_author, new_book):
        response = api_client().post(
            self.endpoint,
            data=new_book,
            format='json',
            HTTP_AUTHORIZATION='Token ' + test_token,
        )
        assert response.status_code == 201

        book = Book.objects.filter(title='Мартин Иден').first()

        update_book = {
            'title': 'test-title',
            'description': 'Рассказ про молодого писателя',
            'publication_date': '1909-09-01',
        }

        response = api_client().put(
            f'/api/books/{book.id}/',
            data=update_book,
            format='json',
            HTTP_AUTHORIZATION='Token ' + test_token,
        )
        assert 'test-title' in response.content.decode('utf-8')

    @pytest.mark.django_db
    def test_url_delete(self, api_client, test_token, new_author, new_book):
        api_client().post(
            self.endpoint,
            data=new_book,
            format='json',
            HTTP_AUTHORIZATION='Token ' + test_token,
        )
        book = Book.objects.filter(title='Мартин Иден').first()
        response = api_client().delete(
            f'/api/books/{book.id}/',
            HTTP_AUTHORIZATION='Token ' + test_token,
        )

        assert response.status_code == 200
