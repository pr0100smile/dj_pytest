import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_first_course(client, course_factory, student_factory):
    """
    1. Проверка получения первого курса
    """
    course = course_factory(_quantity=1)
    course_id = str(course[0].id)
    print(course_id)
    url = reverse('courses-detail', args=(course_id,))
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data['name'] == course[0].name


@pytest.mark.django_db
def test_create_courses(client, course_factory, student_factory):
    """
    2. Проверка получения списка курсов
    """
    students = student_factory(_quantity=7)
    courses = course_factory(_quantity=14)
    url = reverse('courses-list')
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_filter_courses_id(client, course_factory, student_factory):
    """
    3. Проверка фильтрации списка курсов по id
    """
    courses = course_factory(_quantity=7)
    course_id = courses[5].id
    url = reverse('courses-detail', args=(course_id,))
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data['name'] == courses[5].name


@pytest.mark.django_db
def test_filter_courses_name(client, course_factory, student_factory):
    """
    4. Проверка фильтрации списка курсов по name
    """
    students = student_factory(_quantity=15)
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url, {'name': courses[5].name})
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == courses[5].name


@pytest.mark.django_db
def test_success_create_courses(client, course_factory, student_factory):
    """
    5. Тест успешного создания курса
    """
    count = Course.objects.count()
    url = reverse('courses-list')
    response = client.post(url, data={'name': 'Django'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_success_update_courses(client, course_factory, student_factory):
    """
    6. Тест успешного обновления курса
    """
    students = student_factory(_quantity=22)
    courses = course_factory(_quantity=33)
    course_id = str(courses[9].id)
    url = reverse('courses-detail', args=(course_id,))
    response = client.patch(url, data={'name': 'Django Advanced'})
    data = response.json()

    assert response.status_code == 200
    assert data['name'] == 'Django Advanced'


@pytest.mark.django_db
def test_success_delete_courses(client, course_factory, student_factory):
    """
    7. Тест успешного удаления курса
    """
    students = student_factory(_quantity=38)
    courses = course_factory(_quantity=14)
    course_id = str(courses[12].id)
    count = Course.objects.count()
    url = reverse('courses-detail', args=(course_id,))
    response = client.delete(url)

    assert response.status_code == 204
    assert Course.objects.count() == count - 1