<!DOCTYPE html>
{% load static %}

<html lang="ru">

<head>
    <meta charset="UTF-8">

    <title>Список читателей</title>

    <link rel="stylesheet"
          href="{% static 'css/client_list.css' %}">
</head>

<body>

<div class="logo">
    <a href="{% url 'main_page' %}">
        SmartLib
    </a>
</div>

<h1 class="page-title">
    Список читателей
</h1>

<div class="table-container">

<table>

    <thead>

    <tr>

        <th>
            <a href="?sort={% if current_sort == 'last_name' %}-last_name{% else %}last_name{% endif %}">
                Фамилия
            </a>
        </th>

        <th>
            <a href="?sort={% if current_sort == 'first_name' %}-first_name{% else %}first_name{% endif %}">
                Имя
            </a>
        </th>

        <th>
            <a href="?sort={% if current_sort == 'birth_date' %}-birth_date{% else %}birth_date{% endif %}">
                Дата рождения
            </a>
        </th>

        <th>
            <a href="?sort={% if current_sort == 'address' %}-address{% else %}address{% endif %}">
                Адрес
            </a>
        </th>

        <th>
            <a href="?sort={% if current_sort == 'email' %}-email{% else %}email{% endif %}">
                Email
            </a>
        </th>

    </tr>

    </thead>

    <tbody>

    {% for client in page_obj %}

        <tr>

            <td>{{ client.last_name }}</td>

            <td>{{ client.first_name }}</td>

            <td>{{ client.birth_date }}</td>

            <td>{{ client.address }}</td>

            <td>{{ client.email }}</td>

        </tr>

    {% empty %}

        <tr>
            <td colspan="5" class="empty-table">
                Читатели отсутствуют
            </td>
        </tr>

    {% endfor %}

    </tbody>

</table>

</div>

<div class="pagination">

    {% if page_obj.has_previous %}

        <a href="?page=1&sort={{ current_sort }}">
            «
        </a>

        <a href="?page={{ page_obj.previous_page_number }}&sort={{ current_sort }}">
            Назад
        </a>

    {% endif %}

    <span>
        Страница {{ page_obj.number }}
        из {{ page_obj.paginator.num_pages }}
    </span>

    {% if page_obj.has_next %}

        <a href="?page={{ page_obj.next_page_number }}&sort={{ current_sort }}">
            Вперед
        </a>

        <a href="?page={{ page_obj.paginator.num_pages }}&sort={{ current_sort }}">
            »
        </a>

    {% endif %}

</div>

<script src="{% static 'js/client_list.js' %}"></script>

</body>
</html>