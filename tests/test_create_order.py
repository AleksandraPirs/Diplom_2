from conftest import *


class TestCreateOrder:
    @allure.title('Проверка ответа о создании заказа на запрос с указанными ингредиентами аутентифицированным юзером')
    @allure.description('С помощью параметризации выполняем два теста: по очереди отправляем запросы '
                        'с разными наборами ингредиентов в бургере. Аккаунт для проверки создается фикстурой '
                        'перед тестом и удаляется после.')
    @pytest.mark.parametrize('burger_ingredients', [IngredientData.burger_1, IngredientData.burger_2])
    def test_create_order_authenticated_user_success(self, create_new_user_and_delete, burger_ingredients):
        headers = {'Authorization': create_new_user_and_delete[1]['accessToken']}
        payload = {'ingredients': [burger_ingredients]}
        response = requests.post(Urls.order_create, data=payload, headers=headers)
        deserials = response.json()
        assert response.status_code == 200
        assert deserials['success'] is True
        assert 'name' in deserials.keys()
        assert 'number' in deserials['order'].keys()

    @allure.title('Проверка ответа о создании заказа на запрос с указанными ингредиентами неаутентифицированным юзером')
    @allure.description('С помощью параметризации выполняем два теста: по очереди отправляем запросы '
                        'с разными наборами ингредиентов в бургере. Токен аккаунта не передается.')
    @pytest.mark.parametrize('burger_ingredients', [IngredientData.burger_1, IngredientData.burger_2])
    def test_create_order_unauthenticated_user_success(self, burger_ingredients):
        payload = {'ingredients': burger_ingredients}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(Urls.order_create, json=payload, headers=headers)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True
        assert 'name' in response_data
        assert 'order' in response_data
        assert 'number' in response_data['order']

    @allure.title('Проверка ответа при создании заказа запросом с неуказанными ингредиентами аутентифицированным юзером')
    @allure.description('Хэш ингредиента в запросе не передается. Аккаунт для проверки создается фикстурой '
                        'перед тестом и удаляется после.')
    def test_create_order_empty_ingredients_authenticated_user_expected_error(self, create_new_user_and_delete):
        headers = {'Authorization': create_new_user_and_delete[1]['accessToken']}
        payload = {'ingredients': []}
        response = requests.post(Urls.order_create, data=payload, headers=headers)
        assert response.status_code == 400 and response.json() == {'success': False,
                                                                   'message': 'Ingredient ids must be provided'}

    @allure.title('Проверка ответа при создании заказа запросом с неуказанными ингредиентами '
                  'неаутентифицированным юзером')
    @allure.description('Хэш ингредиента в запросе не передается. Токен аккаунта не передается.')
    def test_create_order_empty_ingredients_unauthenticated_user_expected_error(self):
        payload = {'ingredients': []}
        response = requests.post(Urls.order_create, data=payload, headers=Urls.headers)
        assert response.status_code == 400 and response.json() == {'success': False,
                                                                   'message': 'Ingredient ids must be provided'}

    @allure.title('Проверка ответа при создании заказа запросом с невалидным хэшем ингредиента '
                  'аутентифицированным юзером')
    @allure.description('В запрос передается хэш несуществующего ингредиента. Аккаунт для проверки создается фикстурой '
                        'перед тестом и удаляется после.')
    def test_create_order_invalid_ingredients_authenticated_user_expected_error(self, create_new_user_and_delete):
        user_data = create_new_user_and_delete[1]
        headers = {'Authorization': user_data['accessToken']}
        payload = {'ingredients': [IngredientData.invalid_hash_ingredient]}
        response = requests.post(Urls.order_create, json=payload, headers=headers)

        assert response.status_code == 500
        assert response.json() == {
            'success': False,
            'message': 'One or more ids provided are incorrect'
        }