import requests

import Utils
from models.InteractMessage import InteractMessage
from Utils import create_jwt, generate_xswift_signature_for_post, log

# Aufgabe 0: Host und Access Token einrichten (Consumer Key und Secret einsetzen)
host = "?"
access_token = 'Bearer ' + create_jwt("?", "?")


# Aufgabe 1: Interact-Nachricht posten
def post_interact_message():
    # Aufgabe 1.1: InteractMessage-Objekt erstellen und Eigenschaften setzen
    msg = InteractMessage()
    # ... weitere Eigenschaften setzen

    # Aufgabe 1.2: XML-Payload für die Interact-Nachricht vorbereiten (korrekte Werte in pacs_008.xml eintragen)
    msg.set_payload(Utils.get_pacs_008_xml())

    # Aufgabe 1.3: URL zum Posten der Interact-Nachricht auf den richtigen Endpoint erstellen
    url = f"{host}/?"

    x_swift_signature, data_as_json = generate_xswift_signature_for_post(url, msg.to_dict())
    message_post_response = requests.post(url, data=data_as_json,
                                          headers={'Authorization': access_token,
                                                   'X-SWIFT-Signature': x_swift_signature})

    log("Aufgabe 1: Interact-Nachricht posten (post_interact_message)", message_post_response,
        "response_post_interact_message.json")

    return message_post_response, msg


# Aufgabe 2: Liste der Distributions abrufen
def get_distributions():
    # Aufgabe 2.1: URL zum Abrufen der Distribution-Liste vom richtigen Endpoint erstellen
    url = f"{host}/?"

    get_distributions_response = requests.get(url, headers={'Authorization': access_token})

    log("Aufgabe 2: Liste der Distributions abrufen (get_distributions)", get_distributions_response,
        "distributions_list.json")

    return get_distributions_response


# Aufgabe 3: InterAct-Nachricht anhand der Distribution-ID abrufen
def get_interact_message():
    # Aufgabe 3.1: URL zum Abrufen einer InterAct-Nachricht anhand der Distribution-ID vom richtigen Endpunkt erstellen
    url = f"{host}/?"

    get_interact_message_response = requests.get(url, headers={'Authorization': access_token})

    log("Aufgabe 3: InterAct-Nachricht anhand der Distribution-ID abrufen (get_interact_message)",
        get_interact_message_response, "interAct_message.json")

    return get_interact_message_response, url


# Aufgabe 4: Acknowledgement für eine Distribution posten
def post_ack():
    # Aufgabe 4.1: URL zum Posten eines Acknowledgements für eine Distribution auf den richtigen Endpunkt erstellen
    url = f"{host}/?"

    data = {}
    x_swift_signature, data_as_json = generate_xswift_signature_for_post(url, data)

    post_ack_response = requests.post(url, data=data_as_json,
                                      headers={'Authorization': access_token,
                                               'X-SWIFT-Signature': x_swift_signature})

    log("Aufgabe 4: Acknowledgement für eine Distribution posten (post_ack)", post_ack_response,
        "response_post_ack.json")

    return post_ack_response, url


if __name__ == '__main__':
    post_interact_message()
    get_distributions()
    get_interact_message()
    post_ack()
