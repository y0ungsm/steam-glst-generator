import requests

API_KEY = "PUT_UR_API_KEY_HERE"

def generate_gslt(name):
    url = "https://api.steampowered.com/IGameServersService/CreateAccount/v1/"
    payload = {
        "key": API_KEY,
        "appid": 730,
        "memo": name,
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()["response"]["steamid"]
    else:
        return None

def delete_gslt(token):
    url = "https://api.steampowered.com/IGameServersService/DeleteAccount/v1/"
    payload = {
        "key": API_KEY,
        "steamid": token
    }
    response = requests.post(url, data=payload)
    return response.status_code == 200

action = input("Wybierz akcję (generate/delete): ")

if action.lower() == "generate":
    num_tokens = int(input("Podaj liczbę tokenów do wygenerowania: "))
    name = input("Podaj nazwę dla tokenów: ")
    for i in range(num_tokens):
        token = generate_gslt(name)
        if token:
            print(f"Token GSLT {i+1}/{num_tokens} został wygenerowany: {token}")
        else:
            print(f"Nie udało się wygenerować tokenu GSLT {i+1}/{num_tokens}.")
elif action.lower() == "delete":
    name = input("Podaj nazwę tokenów do usunięcia: ")
    response = requests.get(f"https://api.steampowered.com/IGameServersService/GetAccountList/v1/?key={API_KEY}")
    if response.status_code == 200:
        token_list = response.json()["response"]["servers"]
        tokens_to_delete = []
        for token in token_list:
            if token["memo"] == name:
                tokens_to_delete.append(token["steamid"])
        if len(tokens_to_delete) == 0:
            print(f"Nie znaleziono tokenów o nazwie '{name}'.")
        else:
            num_tokens = len(tokens_to_delete)
            for i in range(num_tokens):
                token = tokens_to_delete[i]
                if delete_gslt(token):
                    print(f"Token GSLT {i+1}/{num_tokens} został usunięty.")
                else:
                    print(f"Nie udało się usunąć tokenu GSLT {i+1}/{num_tokens}.")
    else:
        print("Nie mogę pobrać listy tokenów.")
else:
    print("Wybierz 'generate' lub 'delete'")
