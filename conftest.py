import random
import string
import pytest


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


@pytest.fixture(scope='function')
def full_courier_data():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    return {"login": login, "password": password, "first_name": first_name}


@pytest.fixture(scope='function')
def required_courier_data():
    login = generate_random_string(10)
    password = generate_random_string(10)
    return {"login": login, "password": password}
