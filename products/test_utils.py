from django.contrib.auth import get_user_model

def get_test_form_data():
    data = {
            "name": "test product",
            "brand": "test brand",
            "colour": "test colour",
            "size": 1,
            "paint_type": "OL",
            "cost_price": "4.99",
            "retail_price": "9.99",
            "inventory_count": "10"
        }
    
    return data

def create_test_user(username, password, email):

    test_username = username
    test_password = password
    test_email = email

    user = get_user_model().objects.create_user(
        username=test_username,
        password=test_password,
        email=test_email
    )

    return user