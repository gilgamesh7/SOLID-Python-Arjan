
'''
Interface Segregation Principle : A client should never be forced to implement an interface that it doesn’t use, or clients shouldn’t be forced to depend on methods they do not use.
    Problem  :
        auth_ses method in debit card / paypal payments for MFA is not used in credit
    Solution :
        Use composition - new authorisation class SMSAuth
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

class SMSAuth:
    authorised = False

    def verify_code(self, code):
        logger.info(f"Verifying code {code}")
        self.authorised = True

    def is_authorised(self)-> bool :
        return self.authorised

    
class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code, authoriser: SMSAuth):
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

    def __init__(self, email_address, authoriser: SMSAuth):
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

paypal_processor = PaypalPaymentProcessor("quaerendo@invenietis.com", authoriser)
authoriser.verify_code(67890)
paypal_processor.pay(order)

credit_processor = CreditPaymentProcessor("78910")
credit_processor.pay(order)