import requests


def test_recommendation(user_id):
    url = "http://0.0.0.0:8000/recommend"
    params = {"userId": user_id}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"Recomendações para o usuário {user_id}:")
        for i, rec in enumerate(data["recommendations"], 1):
            print(f"{i}. {rec}")
    else:
        print(f"Erro: {response.status_code}")
        print(response.json())


if __name__ == "__main__":
    # Substitua pelo userId que deseja testar
    test_user_id = "f98d1132f60d46883ce49583257104d15ce723b3bbda2147c1e31ac76f0bf069"
    test_recommendation(test_user_id)
