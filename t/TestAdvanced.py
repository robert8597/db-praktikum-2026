import os
import json
import unittest
import Advanced
from Utils import log


class TestAdvanced(unittest.TestCase):

    def test_get_payment_transaction_details(self):
        with open(os.path.join(os.path.dirname(__file__), 'responses/response_get_payment_transaction_details.json'), 'r') as f:
            response_get_payment_transaction_details_json = json.load(f)

        get_payment_transaction_details_response = Advanced.get_payment_transaction_details()

        log("Aufgabe 1: Transaktionsdetails einer Zahlung abrufen (get_payment_transaction_details)", get_payment_transaction_details_response,
           "payment_transaction_details.json")

        self.assertEqual(
            get_payment_transaction_details_response.status_code,
            200,
            f"HTTP-Statuscode ist nicht 200, sondern {get_payment_transaction_details_response.status_code}"
        )

        self.assertEqual(
            get_payment_transaction_details_response.json(),
            response_get_payment_transaction_details_json,
            "Response-JSON für Payment Transaction Details entspricht nicht der erwarteten Fixture"
        )

    def test_update_status_of_gcct_payment_transaction(self):

        update_status_response, paymentConfirmation = Advanced.update_status_of_gcct_payment_transaction()

        self.assertEqual(
            update_status_response.status_code,
            200,
            f"HTTP-Statuscode ist nicht 200, sondern {update_status_response.status_code}"
        )

        self.assertEqual(paymentConfirmation.get_from(), "DEUTDEFFXXX", "Feld 'from' ist falsch")
        self.assertEqual(paymentConfirmation.get_transaction_status(), "ACCC", "Feld 'transaction_status' ist falsch")
        self.assertEqual(paymentConfirmation.get_tracker_informing_party(), "DEUTDEFFXXX", "Feld 'tracker_informing_party' ist falsch")
        self.assertEqual(paymentConfirmation.get_instruction_identification(), "789", "Feld 'instruction_identification' ist falsch")
        self.assertEqual(paymentConfirmation.get_service_level(), "G001", "Feld 'service_level' ist falsch")
        self.assertEqual(paymentConfirmation.get_payment_scenario(), "CCTR", "Feld 'payment_scenario' ist falsch")
        self.assertEqual(paymentConfirmation.get_confirmed_date(), "2026-03-19T12:00:00Z", "Feld 'confirmed_date' ist falsch")

        charges = paymentConfirmation.get_charges_information()
        self.assertIsNotNone(charges, "charges_information ist None")
        self.assertEqual(len(charges), 1, f"charges_information hat nicht 1 Element, sondern {len(charges)}")

        charges_item = charges[0]
        self.assertIsNotNone(charges_item.amount, "charges_information[0].amount fehlt")
        self.assertEqual(charges_item.amount.currency, "EUR", "charges_information[0].amount.currency ist falsch")
        self.assertEqual(charges_item.amount.amount, "10", "charges_information[0].amount.amount ist falsch")

        self.assertIsNotNone(charges_item.agent, "charges_information[0].agent fehlt")
        self.assertEqual(charges_item.agent.bicfi, "BICCXXXXXXX", "charges_information[0].agent.bicfi ist falsch")

        confirmed_amount = paymentConfirmation.get_confirmed_amount()
        self.assertIsNotNone(confirmed_amount, "confirmed_amount fehlt")
        self.assertEqual(confirmed_amount.currency, "EUR", "confirmed_amount.currency ist falsch")
        self.assertEqual(confirmed_amount.amount, "500", "confirmed_amount.amount ist falsch")

        remaining_amount = paymentConfirmation.get_remaining_to_be_confirmed_amount()
        self.assertIsNotNone(remaining_amount, "remaining_to_be_confirmed_amount fehlt")
        self.assertEqual(remaining_amount.currency, "EUR", "remaining_to_be_confirmed_amount.currency ist falsch")
        self.assertEqual(remaining_amount.amount, "490", "remaining_to_be_confirmed_amount.amount ist falsch")


if __name__ == "__main__":
    unittest.main()
