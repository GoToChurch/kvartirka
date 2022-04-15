=====
Test Blog
=====

Запуск
-----------

1. Добавить "test_blog" и "api_blog" в список INSTALLED_APPS, который находиться в settings.py в директории проекта:

    INSTALLED_APPS = [
        ...
        'test_blog',
        'api_blog',
    ]

2. Добавить test_blog и api_blog URLconf в urls.py в директории проекта:

    path('test_blog/', include('test_blog.urls')),
    path('api_blog/', include('api_blog.urls')),

3. Выполнить команду ``python manage.py migrate`` в терминале, чтобы создать модели test_blog.

4. Выполнить команду ``python manage.py runserver`` и перейти по адресу visit http://127.0.0.1:8000/, чтобы начать взаимодействие с блогами
