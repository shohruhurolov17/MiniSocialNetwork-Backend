from django.core import signing


def generate_verification_url(user_id) -> str:

    data = {'user_id': str(user_id) }

    signed_data = signing.dumps(data)

    return f'http://localhost:8000/api/v1/auth/verify/{signed_data}'