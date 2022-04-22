
'''
Liskov Substitution Principle : every subclass or derived class should be substitutable for their base or parent class.
    Problem  :
        Paypal payments work with emails & not security codes
    Solution :
        Remove security code from abstract class & add to initialisation of class
'''
import logging
from abc import ABC, abstractmethod


try:
    logging.basicConfig(level=logging.INFO, format="{asctime} | {name} | {levelno} - {funcName} | {lineno} | {message}", style='{')
    logger = logging.getLogger("SOLID")
    logger.info("Initiated Logger")
except Exception as err:
    print(f"{err}")
    quit()

class Order:
    items = []
    quantities = []
    prices = []
    status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]

        return total

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
            logger.info(f"Processing debit payment type")
            logger.info(f"Verififying security code {self.security_code}")
            order.status = "paid" 

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code
        
    def pay(self, order):
            logger.info(f"Processing credit payment type")
            logger.info(f"Verififying security code {self.security_code}")
            order.status = "paid"  

class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email_address):
        self.email_address = email_address
        
    def pay(self, order):
            logger.info(f"Processing paypal payment type")
            logger.info(f"Verififying email address {self.email_address}")
            order.status = "paid"  

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB Cable", 2, 5)

logger.info(order.total_price())

debit_processor = DebitPaymentProcessor("123456")
debit_processor.pay(order)

paypal_processor = PaypalPaymentProcessor("quaerendo@invenietis.com")
paypal_processor.pay(order)
