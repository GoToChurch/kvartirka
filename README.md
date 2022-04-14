=====
Test Blog
=====

Тестовое задание: создание блога с возможностью подписки
Не реализована упаковка в докер, т.к я не знаком с этой технологией

Запуск
-----------

1. Добавить "test_blog" в список INSTALLED_APPS, который находиться в settings.py в директории проекта:

    INSTALLED_APPS = [
        ...
        'test_blog',
    ]

2. Добавить test_blog URLconf в urls.py в директории проекта:

    path('test_blog/', include('test_blog.urls')),

3. Выполнить команду ``python manage.py migrate`` в терминале, чтобы создать модели test_blog.

4. Выполнить команду ``python manage.py runserver`` и перейти по адресу visit http://127.0.0.1:8000/, чтобы начать взаимодействие с блогами
