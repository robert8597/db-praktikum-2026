import requests


# Aufgabe 0: Access Token einrichten


# Aufgabe 1: Transaktionsdetails einer Zahlung abrufen
# https://docs.developer.swift.com/docs/api-guides/gpi-apis/gpi-transaction-details-api-reference#tag/Get-Payment-Transaction-Details/operation/getPaymentTransactionDetails
def get_payment_transaction_details():
    # Aufgabe 1.1: URL zum Abrufen der Transaktionsdetails vom richtigen Endpunkt erstellen

    # Aufgabe 1.2: API-Aufruf erstellen
    response = None

    # Aufgabe 1.3: Korrekte Rückgabe
    return response


# Aufgabe 2: Status einer gCCT-Zahlungstransaktion aktualisieren
# https://docs.developer.swift.com/docs/api-guides/gpi-apis/gpi-customer-credit-transfer-api-reference#tag/Status-Confirmations
def update_status_of_gcct_payment_transaction():
    # Aufgabe 2.1: URL zum Aktualisieren des Status auf den richtigen Endpunkt erstellen

    # Aufgabe 2.2: PaymentConfirmation-Objekt erstellen und Eigenschaften setzen
    paymentConfirmation = None

    # Aufgabe 2.3: Signatur und JSON-Payload vorbereiten

    # Aufgabe 2.4 API-Aufruf erstellen
    response = None

    # Aufgabe 2.5: Korrekte Rückgabe
    return response, paymentConfirmation


if __name__ == '__main__':
    get_payment_transaction_details()
    update_status_of_gcct_payment_transaction()
