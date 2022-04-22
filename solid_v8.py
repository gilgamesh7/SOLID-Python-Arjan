
'''
Dependency Inversion Principle : Entities must depend on abstractions, not on concretions. It states that the high-level module must not depend on the low-level module, but they should depend on abstractions.
    Problem  :
        is_authorised is allowed only after concrete SMS_Auth, which does verification.
    Solution :
        Use an abstract class for authorisation , which means more authorisation types can be added
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

class Authoriser(ABC):
    @abstractmethod
    def is_authorised(self)-> bool :
        pass

class SMSAuth(Authoriser):
    authorised = False

    def verify_code(self, code):
        logger.info(f"Verifying code {code}")
        self.authorised = True

    def is_authorised(self)-> bool :
        return self.authorised

class NotARobot(Authoriser):
    authorised = False

    def not_a_robot(self):
        logger.info(f"Are you a robot ?")
        self.authorised = True

    def is_authorised(self)-> bool :
        return self.authorised

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code, authoriser: Authoriser):
        self.authoriser = authoriser
        self.security_code = security_code

    def pay(self, order):
        if not self.authoriser.is_authorised():
            raise Exception("Not authorised")
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

    def __init__(self, email_address, authoriser: Authoriser):
        self.authoriser = authoriser
        self.email_address = email_address


    def pay(self, order):
        if not self.authoriser.is_authorised():
            raise Exception("Not authorised")
        logger.info(f"Processing paypal payment type")
        logger.info(f"Verififying email address {self.email_address}")
        order.status = "paid"  

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB Cable", 2, 5)

logger.info(order.total_price())

authoriser = SMSAuth()
debit_processor = DebitPaymentProcessor("123456",authoriser)
authoriser.verify_code(12345)
debit_processor.pay(order)

authoriser = NotARobot()
paypal_processor = PaypalPaymentProcessor("quaerendo@invenietis.com", authoriser)
authoriser.not_a_robot()
paypal_processor.pay(order)

credit_processor = CreditPaymentProcessor("78910")
credit_processor.pay(order)