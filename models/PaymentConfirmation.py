from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Union


@dataclass
class Money:
    currency: Optional[str] = None
    amount: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "currency": self.currency,
            "amount": self.amount,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Money":
        return Money(
            currency=data.get("currency"),
            amount=data.get("amount"),
        )


@dataclass
class Agent:
    bicfi: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bicfi": self.bicfi,
        }


@dataclass
class ChargesInformationItem:
    amount: Optional[Money] = None
    agent: Optional[Agent] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "amount": None if self.amount is None else self.amount.to_dict(),
            "agent": None if self.agent is None else self.agent.to_dict(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ChargesInformationItem":
        amount = data.get("amount") or None
        agent = data.get("agent") or None
        return ChargesInformationItem(
            amount=None if amount is None else Money(**amount),
            agent=None if agent is None else Agent(**agent),
        )


class PaymentConfirmation:
    def __init__(
        self,
        from_: Optional[str] = None,
        transaction_status: Optional[str] = None,
        tracker_informing_party: Optional[str] = None,
        instruction_identification: Optional[str] = None,
        service_level: Optional[str] = None,
        payment_scenario: Optional[str] = None,
        charges_information: Optional[List[ChargesInformationItem]] = None,
        confirmed_date: Optional[str] = None,
        confirmed_amount: Optional[Money] = None,
        remaining_to_be_confirmed_amount: Optional[Money] = None,
    ):
        # Hinweis: "from" ist in Python ein Keyword, daher intern from_ verwendet.
        self.from_ = from_
        self.transaction_status = transaction_status
        self.tracker_informing_party = tracker_informing_party
        self.instruction_identification = instruction_identification
        self.service_level = service_level
        self.payment_scenario = payment_scenario
        self.charges_information = charges_information or []
        self.confirmed_date = confirmed_date
        self.confirmed_amount = confirmed_amount
        self.remaining_to_be_confirmed_amount = remaining_to_be_confirmed_amount

    # Setter
    def set_from(self, from_: str) -> None:
        self.from_ = from_

    def set_transaction_status(self, transaction_status: str) -> None:
        self.transaction_status = transaction_status

    def set_tracker_informing_party(self, tracker_informing_party: str) -> None:
        self.tracker_informing_party = tracker_informing_party

    def set_instruction_identification(self, instruction_identification: str) -> None:
        self.instruction_identification = instruction_identification

    def set_service_level(self, service_level: str) -> None:
        self.service_level = service_level

    def set_payment_scenario(self, payment_scenario: str) -> None:
        self.payment_scenario = payment_scenario

    def set_charges_information(
        self,
        charges_information: Sequence[Union[ChargesInformationItem, Dict[str, Any]]],
    ) -> None:
        """Setzt charges_information.

        Akzeptiert entweder:
        - eine Liste von ChargesInformationItem-Objekten oder
        - eine Liste von Dicts (wie im JSON-Beispiel).
        """
        normalized: List[ChargesInformationItem] = []
        for item in charges_information or []:
            if isinstance(item, ChargesInformationItem):
                normalized.append(item)
            elif isinstance(item, dict):
                normalized.append(ChargesInformationItem.from_dict(item))
            else:
                raise TypeError(
                    "charges_information muss eine Liste aus ChargesInformationItem oder Dict sein; "
                    f"bekommen: {type(item)!r}"
                )
        self.charges_information = normalized

    def add_charges_information_item(self, item: ChargesInformationItem) -> None:
        self.charges_information.append(item)

    def set_confirmed_date(self, confirmed_date: str) -> None:
        self.confirmed_date = confirmed_date

    def set_confirmed_amount(self, confirmed_amount: Union[Money, Dict[str, Any]]) -> None:
        if isinstance(confirmed_amount, Money):
            self.confirmed_amount = confirmed_amount
        elif isinstance(confirmed_amount, dict):
            self.confirmed_amount = Money.from_dict(confirmed_amount)
        else:
            raise TypeError(
                "confirmed_amount muss Money oder Dict sein; "
                f"bekommen: {type(confirmed_amount)!r}"
            )

    def set_remaining_to_be_confirmed_amount(
        self,
        remaining_to_be_confirmed_amount: Union[Money, Dict[str, Any]],
    ) -> None:
        if isinstance(remaining_to_be_confirmed_amount, Money):
            self.remaining_to_be_confirmed_amount = remaining_to_be_confirmed_amount
        elif isinstance(remaining_to_be_confirmed_amount, dict):
            self.remaining_to_be_confirmed_amount = Money.from_dict(remaining_to_be_confirmed_amount)
        else:
            raise TypeError(
                "remaining_to_be_confirmed_amount muss Money oder Dict sein; "
                f"bekommen: {type(remaining_to_be_confirmed_amount)!r}"
            )

    # Getter
    def get_from(self) -> Optional[str]:
        return self.from_

    def get_transaction_status(self) -> Optional[str]:
        return self.transaction_status

    def get_tracker_informing_party(self) -> Optional[str]:
        return self.tracker_informing_party

    def get_instruction_identification(self) -> Optional[str]:
        return self.instruction_identification

    def get_service_level(self) -> Optional[str]:
        return self.service_level

    def get_payment_scenario(self) -> Optional[str]:
        return self.payment_scenario

    def get_charges_information(self) -> List[ChargesInformationItem]:
        return self.charges_information

    def get_confirmed_date(self) -> Optional[str]:
        return self.confirmed_date

    def get_confirmed_amount(self) -> Optional[Money]:
        return self.confirmed_amount

    def get_remaining_to_be_confirmed_amount(self) -> Optional[Money]:
        return self.remaining_to_be_confirmed_amount

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from": self.from_,
            "transaction_status": self.transaction_status,
            "tracker_informing_party": self.tracker_informing_party,
            "instruction_identification": self.instruction_identification,
            "service_level": self.service_level,
            "payment_scenario": self.payment_scenario,
            "charges_information": [item.to_dict() for item in (self.charges_information or [])],
            "confirmed_date": self.confirmed_date,
            "confirmed_amount": None if self.confirmed_amount is None else self.confirmed_amount.to_dict(),
            "remaining_to_be_confirmed_amount": None
            if self.remaining_to_be_confirmed_amount is None
            else self.remaining_to_be_confirmed_amount.to_dict(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PaymentConfirmation":
        charges_information = [
            ChargesInformationItem.from_dict(item)
            for item in (data.get("charges_information", []) or [])
        ]

        confirmed_amount_data = data.get("confirmed_amount")
        remaining_data = data.get("remaining_to_be_confirmed_amount")

        return PaymentConfirmation(
            from_=data.get("from"),
            transaction_status=data.get("transaction_status"),
            tracker_informing_party=data.get("tracker_informing_party"),
            instruction_identification=data.get("instruction_identification"),
            service_level=data.get("service_level"),
            payment_scenario=data.get("payment_scenario"),
            charges_information=charges_information,
            confirmed_date=data.get("confirmed_date"),
            confirmed_amount=None if confirmed_amount_data is None else Money.from_dict(confirmed_amount_data),
            remaining_to_be_confirmed_amount=None if remaining_data is None else Money.from_dict(remaining_data),
        )

    def __str__(self) -> str:
        return (
            f"from: {self.from_}\n"
            f"transaction_status: {self.transaction_status}\n"
            f"tracker_informing_party: {self.tracker_informing_party}\n"
            f"instruction_identification: {self.instruction_identification}\n"
            f"service_level: {self.service_level}\n"
            f"payment_scenario: {self.payment_scenario}\n"
            f"charges_information: {[ci.to_dict() for ci in (self.charges_information or [])]}\n"
            f"confirmed_date: {self.confirmed_date}\n"
            f"confirmed_amount: {None if self.confirmed_amount is None else self.confirmed_amount.to_dict()}\n"
            f"remaining_to_be_confirmed_amount: {None if self.remaining_to_be_confirmed_amount is None else self.remaining_to_be_confirmed_amount.to_dict()}\n"
        )

    @staticmethod
    def example() -> "PaymentConfirmation":
        """Erzeugt ein Beispiel-Objekt mit den Werten aus dem vorgegebenen JSON-Beispiel."""
        return PaymentConfirmation(
            from_="BICCXXXXXXX",
            transaction_status="ACCC",
            tracker_informing_party="BICCXXXXXXX",
            instruction_identification="789",
            service_level="G001",
            payment_scenario="CCTR",
            charges_information=[
                ChargesInformationItem(
                    amount=Money(currency="IDR", amount="10"),
                    agent=Agent(bicfi="BICCXXXXXXX"),
                )
            ],
            confirmed_date="2021-11-25T14:33:00.000Z",
            confirmed_amount=Money(currency="IDR", amount="500"),
            remaining_to_be_confirmed_amount=Money(currency="IDR", amount="490"),
        )
