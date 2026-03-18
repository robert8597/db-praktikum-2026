import base64
import os
import json
import unittest
import Beginner
import xml.etree.ElementTree as ET


class TestBeginner(unittest.TestCase):

    def test_post_interact_message(self):
        with open(os.path.join(os.path.dirname(__file__), 'responses/response_post_interact_message.json'), 'r') as f:
            response_interact_message_post_json = json.load(f)

        message_post_response, msg = Beginner.post_interact_message()

        self.assertEqual(
            message_post_response.json(),
            response_interact_message_post_json
        )

        self.assertEqual(
            message_post_response.status_code,
            201
        )

        self.assertEqual(msg.get_sender_reference(), "BankOnTech", "Absenderreferenz ist falsch")
        self.assertEqual(msg.get_service_code(), "swift.finplus!pc", "Service-Code ist falsch")
        self.assertEqual(msg.get_message_type(), "pacs.008.001.13", "Nachrichtentyp ist falsch")
        self.assertEqual(msg.get_requestor(), "ou=xxx,o=deutdeff,o=swift", "Requestor ist falsch")
        self.assertEqual(msg.get_responder(), "ou=xxx,o=bktrus33,o=swift", "Responder ist falsch")
        self.assertEqual(msg.get_format(), "MX", "Format ist falsch")

        xml_content = base64.b64decode(msg.get_payload()).decode("utf-8")
        root = ET.fromstring(xml_content)

        ns = {'ns': 'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.13'}

        amt = root.find('.//ns:IntrBkSttlmAmt', ns)
        self.assertIsNotNone(amt, "IntrBkSttlmAmt fehlt im XML")
        self.assertEqual(amt.text, '100.00', f"IntrBkSttlmAmt-Wert ist falsch: {amt.text}")
        self.assertEqual(amt.attrib.get('Ccy'), 'EUR', f"IntrBkSttlmAmt-Währung ist falsch: {amt.attrib.get('Ccy')}")

        agrd_rate = root.find('.//ns:AgrdRate', ns)
        self.assertIsNotNone(agrd_rate, "AgrdRate fehlt im XML")
        self.assertEqual(agrd_rate.find('ns:UnitCcy', ns).text, 'EUR', "UnitCcy ist falsch oder fehlt")
        self.assertEqual(agrd_rate.find('ns:QtdCcy', ns).text, 'USD', "QtdCcy ist falsch oder fehlt")
        self.assertEqual(agrd_rate.find('ns:PreAgrdXchgRate', ns).text, '1.17246',
                         "PreAgrdXchgRate ist falsch oder fehlt")

        dbtr = root.find('.//ns:Dbtr', ns)
        self.assertIsNotNone(dbtr, "Dbtr fehlt im XML")
        self.assertEqual(dbtr.find('ns:Nm', ns).text, 'Max Mustermann', "Dbtr-Name ist falsch oder fehlt")

        dbtr_agt = root.find('.//ns:DbtrAgt/ns:FinInstnId', ns)
        self.assertIsNotNone(dbtr_agt, "DbtrAgt/FinInstnId fehlt im XML")
        self.assertEqual(dbtr_agt.find('ns:BICFI', ns).text, 'DEUTDEFFXXX', "DbtrAgt BICFI ist falsch oder fehlt")
        self.assertEqual(dbtr_agt.find('ns:Nm', ns).text, 'DEUTSCHE BANK AG', "DbtrAgt-Name ist falsch oder fehlt")

        cdtr_agt = root.find('.//ns:CdtrAgt/ns:FinInstnId', ns)
        self.assertIsNotNone(cdtr_agt, "CdtrAgt/FinInstnId fehlt im XML")
        self.assertEqual(cdtr_agt.find('ns:BICFI', ns).text, 'BKTRUS33XXX',
                         "CdtrAgt BICFI ist falsch oder fehlt")
        self.assertEqual(cdtr_agt.find('ns:Nm', ns).text, 'DEUTSCHE BANK TRUST COMPANY AMERICAS',
                         "CdtrAgt-Name ist falsch oder fehlt")

        cdtr = root.find('.//ns:Cdtr', ns)
        self.assertIsNotNone(cdtr, "Cdtr fehlt im XML")
        self.assertEqual(cdtr.find('ns:Nm', ns).text, 'Jane Doe', "Cdtr-Name ist falsch oder fehlt")

    def test_get_distributions(self):
        with open(os.path.join(os.path.dirname(__file__), 'responses/response_distributions_list.json'), 'r') as f:
            response_list_of_distributions_json = json.load(f)

        get_distributions_response = Beginner.get_distributions()

        self.assertEqual(
            get_distributions_response.json(),
            response_list_of_distributions_json
        )

        self.assertEqual(
            get_distributions_response.status_code,
            200
        )

    def test_get_interact_message(self):
        with open(os.path.join(os.path.dirname(__file__), 'responses/response_get_interact_message.json'), 'r') as f:
            response_get_interact_message_json = json.load(f)

        get_interact_message_response, url = Beginner.get_interact_message()

        self.assertIn("44984189499", url)

        self.assertEqual(
            get_interact_message_response.json(),
            response_get_interact_message_json
        )

        self.assertEqual(
            get_interact_message_response.status_code,
            200
        )

    def test_post_ack(self):
        post_ack_response, url = Beginner.post_ack()

        self.assertIn("44984189499", url)

        self.assertEqual(
            post_ack_response.status_code,
            204,
            "Posting des Acknowledgements ist fehlgeschlagen"
        )


if __name__ == "__main_":
    unittest.main()
