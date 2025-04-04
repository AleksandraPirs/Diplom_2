from conftest import *

@pytest.fixture
def updated_user_data():
    return {
        'email': create_random_email(),
        'password': create_random_password(),
        'name': create_random_username()
    }

class TestUserUpdate:
    @allure.title('Проверка ответа на запрос изменения данных аутентифицированного пользователя')
    def test_update_user_authenticated_success(self, create_new_user_and_delete, updated_user_data):
        response = requests.patch(Urls.user_update,
                                headers={'Authorization': create_new_user_and_delete[1]['accessToken']},
                                json=updated_user_data)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data['success'] is True
        assert response_data['user']['email'] == updated_user_data['email']
        assert response_data['user']['name'] == updated_user_data['name']

    @allure.title('Проверка ответа на запрос изменения данных неаутентифицированного пользователя')
    def test_update_user_unauthenticated_expected_error(self, updated_user_data):
        headers = {'Content-Type': 'application/json'}
        response = requests.patch(Urls.user_update,
                                headers=headers,
                                json=updated_user_data)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert 'authorised' in response_data.get('message', '').lower()