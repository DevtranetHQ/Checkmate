import requests as req
import os
import sys
import json

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

headers = {"X-API-KEY": config["X-API-KEY"]}


def email_in_endpoint(url, email) -> bool:
    r = req.post(url, json={"email": email}, headers=headers)
    if r.status_code == 200:
        return r.json()["data"]["userRoles"]
    else:
        return False


def add_user(url, email, discordId, discordUsername) -> bool:
    r = req.post(
        url, json={"email": email, "discordId": discordId, "discordUsername": discordUsername}, headers=headers
    )
    if r.status_code == 201:
        return True
    else:
        return False
