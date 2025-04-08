class Urls:
    base_url = 'https://stellarburgers.nomoreparties.site'
    user_register = f'{base_url}/api/auth/register'
    user_auth = f'{base_url}/api/auth/login'
    user_update = f'{base_url}/api/auth/user'
    user_delete = f'{base_url}/api/auth/user'
    order_create = f'{base_url}/api/orders'
    get_user_orders = f'{base_url}/api/orders'

    headers = {'Content-Type': 'application/json'}