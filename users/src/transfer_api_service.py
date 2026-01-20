from abc import ABC, abstractmethod

import stripe
from django.db import models

from config.settings import BASE_URL


class TransferAPIService(ABC):
    """Base API service for work with transfer services"""

    @abstractmethod
    def create_product(self, **kwargs) -> dict:
        pass

    @abstractmethod
    def create_price(self, **kwargs) -> dict:
        pass

    @abstractmethod
    def create_session(self, **kwargs) -> dict:
        pass


class StripeAPIService(TransferAPIService):
    """API service for work with stripe service"""

    api_key: str

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def create_transfer_and_return_data(self, product: models, amount: float) -> dict:
        """
        Create transfer and return data

        :param product: Lesson or Course object
        :param amount: amount from Payment object
        :return: dict with params of transfer
        """

        stripe.api_key = self.api_key

        if product.stripe_product_id:
            product_id = product.stripe_product_id
        else:
            product_id = self.create_product(product.name).get("id")
            product.stripe_product_id = product_id
            product.save()

        price_id = stripe.Price.create(currency="rub", unit_amount=int(amount * 100), product=product_id).get("id")
        session_dict = stripe.checkout.Session.create(
            success_url=BASE_URL,
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
        )
        session_id = session_dict.get("id")
        link = session_dict.get("url")

        return {"product_id": product_id, "price_id": price_id, "session_id": session_id, "link": link}

    def retrieve_session(self, session_id: str) -> dict:
        stripe.api_key = self.api_key
        return stripe.checkout.Session.retrieve(session_id)

    def create_product(self, product_name: str) -> dict:
        client = stripe.StripeClient(self.api_key)
        return client.v1.products.create({"name": product_name})

    def create_price(self, product: str, amount: int) -> dict:
        stripe.api_key = self.api_key
        return stripe.Price.create(
            currency="rub",
            unit_amount=amount,
            product=product,
        )

    def create_session(self, price: str) -> dict:
        stripe.api_key = self.api_key
        return stripe.checkout.Session.create(
            success_url=BASE_URL,
            line_items=[{"price": price, "quantity": 1}],
            mode="payment",
        )
