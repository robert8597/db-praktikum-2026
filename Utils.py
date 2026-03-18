import base64
import datetime
import hashlib
import json
import random
from base64 import b64encode
import os

import jwt
import requests

import logging

# logging.basicConfig(level=logging.DEBUG)

host = "https://sandbox.swift.com"

proxies = {
    'http': 'userproxy.intranet.db.com:8080',
    'https': 'userproxy.intranet.db.com:8080',
}


def generate_xswift_signature_for_post(url, data):
    if isinstance(data, dict):
        data_as_json = json.dumps(data).replace(" ", "")
    else:
        data_as_json = data.replace(" ", "")

    private_key = get_private_key()

    aud_dynamic = url.replace("https://", "")
    digest = sha256_base64(data_as_json)
    expiration_time = calculate_expiration_time()

    nr_payload = {
        "aud": aud_dynamic,
        "sub": "CN=desktop, O=sandbox, O=swift",
        "jti": generateJti(),
        "exp": expiration_time,
        "iat": expiration_time - 1900,
        "digest": digest,
        "nbf": expiration_time - 905
    }

    header = {
        "typ": 'JWT',
        "alg": 'RS256',
        "x5c": get_certificate(),
    }

    x_swift_signature = jwt.encode(nr_payload, private_key, headers=header, algorithm='RS256')

    # print(x_swift_signature)

    return x_swift_signature, data_as_json


def create_jwt(consumer_key, consumer_secret):
    private_key = get_private_key()

    expiration_time = calculate_expiration_time()

    payload = {
        "iat": expiration_time - 1900,
        "nbf": expiration_time - 905,
        "exp": expiration_time,
        "jti": generateJti(),
        "iss": consumer_key,
        "aud": 'sandbox.swift.com/oauth2/v1/token',
        "sub": 'CN=demo-swift-sandbox-consumer, O=Demo, L=London, S=London, C=GB',
    }

    header = {
        "typ": 'JWT',
        "alg": 'RS256',
        "x5c": get_certificate(),
    }

    assertion = jwt.encode(payload, private_key, headers=header, algorithm='RS256')

    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": assertion,
        "scope": "swift.alliancecloud.api"
    }

    # print(data)

    authstr = 'Basic ' + b64encode((consumer_key + ':' + consumer_secret).encode('utf-8')).decode(
        'utf-8')

    headers = {
        'Authorization': authstr,
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    token_response = requests.post(host + "/oauth2/v1/token", headers=headers, data=data)
    response_data = token_response.json()

    if token_response.status_code != 200:
        raise Exception(
            f"Access-Token konnte nicht abgerufen werden: {response_data}\n"
            f"\n##### Bitte Consumer Key und Secret prüfen #####"
        )

    return response_data['access_token']


def generateJti():
    newJti = ""
    charset = "abcdefghijklmnopqrstuvwxyz0123456789"
    for i in range(0, 12):
        newJti += random.choice(charset)
    return newJti


def sha256_base64(data):
    ascii_string = data.encode('utf-8')
    b64urlString = base64.urlsafe_b64encode(ascii_string).decode()
    digest_preb64 = hashlib.sha256(b64urlString.encode()).digest()
    return base64.b64encode(digest_preb64).decode()


def calculate_expiration_time():
    return int(datetime.datetime.now().timestamp() + datetime.timedelta(minutes=15).total_seconds())


def get_private_key():
    private_key_from_swift = requests.get(host + "/sandbox-selfsigned-dummy-secret/privatekey2")
    return f"-----BEGIN PRIVATE KEY-----\n{private_key_from_swift.text}\n-----END PRIVATE KEY-----"


def get_certificate():
    certificate = requests.get(host + "/sandbox-selfsigned-dummy-secret/certificate2")
    return [certificate.text]


# def get_pacs_008_xml():
#     with open("pacs_008.xml", "r") as file:
#         return file.read()

def get_pacs_008_xml():
    import os
    file_name = "pacs_008.xml"

    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return file.read()

    parent_path = os.path.join("..", file_name)
    if os.path.exists(parent_path):
        with open(parent_path, "r") as file:
            return file.read()

    raise FileNotFoundError(f"{file_name} nicht gefunden (weder im aktuellen noch im übergeordneten Verzeichnis)")


def log(task, response, file_name):
    if response is None:
        print(f"Fehler bei {task}: Keine Antwort (response ist None)")
        return

    is_success = 200 <= response.status_code < 300

    # Kopfblock: Wir drucken ohne extra Leerzeile am Ende, damit 'Body:' direkt danach kommt.
    print(f"{task}\nAntwort\nCode: {response.status_code}")

    # Body/Content-Type nur informativ ausgeben (direkt nach 'Code: ...')
    if response.text:
        print(f"Body: {response.text}")

    # Leerzeile als visueller Trenner
    print()

    if not is_success:
        # Bei Fehlern nichts dumpen, aber hilfreiche Info ausgeben
        print(f"Fehler bei {task}: {response.text}")
        return

    os.makedirs("antworten", exist_ok=True)
    out_path = os.path.join("antworten", file_name)

    # Nicht jede 2xx-Response enthält JSON (z.B. 204 No Content oder leerer Body).
    content_type = (response.headers.get("Content-Type") or "").lower()
    body = response.text or ""

    # Wenn es offensichtlich JSON ist (Content-Type) oder der Body wie JSON aussieht, versuchen wir zu parsen.
    looks_like_json = body.lstrip().startswith("{") or body.lstrip().startswith("[")
    should_try_json = "json" in content_type or looks_like_json

    if should_try_json and body.strip():
        try:
            with open(out_path, "w") as file:
                json.dump(response.json(), file, indent=4)
            return
        except (json.JSONDecodeError, ValueError):
            # Fallback: Body als Text speichern
            pass

    # Fallback: Nicht-JSON-Body speichern (oder leer, falls keine Daten)
    with open(out_path, "w", encoding="utf-8") as file:
        file.write(body)
