
'''
Single responsibility :
    Order class does too many things : 
        Payments should not be part of order
    Solution : 
        Split out payments
Open/Closed : Objects or entities should be open for extension but closed for modification.
    Problem  :
        New payment methods cannot be introduced without changing PaymentProcessor class
    
'''
import logging

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

class PaymentProcessor:
    def pay_credit(self, security_code):
            logger.info(f"Processing credit payment type")
            logger.info(f"Verififying security code {security_code}")
            order.status = "paid"  

    def pay_debit(self, order, security_code):
            logger.info(f"Processing debit payment type")
            logger.info(f"Verififying security code {security_code}")
            order.status = "paid" 

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB Cable", 2, 5)

logger.info(order.total_price())

procesor = PaymentProcessor()
procesor.pay_debit(order, "123456")