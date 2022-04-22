
'''
Interface Segregation Principle : A client should never be forced to implement an interface that it doesn’t use, or clients shouldn’t be forced to depend on methods they do not use.
    Problem  :
        auth_ses method in debit card / paypal payments for MFA is not used in credit
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
    def auth_ses(self,code):
        pass

    @abstractmethod
    def pay(self, order):
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code
        self.verify = False

    def auth_ses(self, code):
        logger.info(f"Verifying SMS Code {code}")
        self.verify = True

    def pay(self, order):
        if not self.verify:
            raise Exception("Not authorised")
        logger.info(f"Processing debit payment type")
        logger.info(f"Verififying security code {self.security_code}")
        order.status = "paid" 


class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self.security_code = security_code
        
    def auth_ses(self, code):
        raise Exception(f"Credit card payments do not support MFA")

    def pay(self, order):
            logger.info(f"Processing credit payment type")
            logger.info(f"Verififying security code {self.security_code}")
            order.status = "paid"  

class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email_address):
        self.email_address = email_address
        self.verify = False
        
    def auth_ses(self, code):
        logger.info(f"Verifying SMS Code {code}")
        self.verify = True
        
    def pay(self, order):
        if not self.verify:
            raise Exception("Not authorised")
        logger.info(f"Processing paypal payment type")
        logger.info(f"Verififying email address {self.email_address}")
        order.status = "paid"  

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB Cable", 2, 5)

logger.info(order.total_price())

debit_processor = DebitPaymentProcessor("123456")
debit_processor.auth_ses("X")
debit_processor.pay(order)

credit_processor = CreditPaymentProcessor("78910")
credit_processor.pay(order)

credit_processor = CreditPaymentProcessor("78910")
credit_processor.auth_ses("Z")
