from rest_framework.test import APIClient
from django.urls import reverse

def login(user_factory):
    """Realiza o login de um usuário e retorna os tokens de acesso

    Args:
        user_factory (User): usuário que se deseja logar

    Raises:
        ValueError: Login mal sucedido
        ValueError: Tokens de acesso não retornados corretamente

    Returns:
        Object: access e refresh tokens
    """

    client = APIClient()
    url = reverse('token_obtain_pair')
    
    login_data = {
        "username": user_factory.username,
        "password": '123'
    }

    response = client.post(url, login_data)
    
    if response.status_code != 200:
        raise ValueError(f"Falha no login: {response.status_code} - {response.data}")
    
    if 'access' not in response.data or 'refresh' not in response.data:
        raise ValueError("Resposta de login inválida: tokens não encontrados")
    
    return response.data
