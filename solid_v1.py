
'''
Single responsibility :
    Order class does too many things : 
        Payments should not be part of order
    
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

    def pay(self, payment_type, security_code):
        if (payment_type == 'debit'):
            logger.info(f"Processing debit payment type")
            logger.info(f"Verififying security code {security_code}")
            self.status = "paid"
        elif payment_type == 'credit':
            logger.info(f"Processing credit payment type")
            logger.info(f"Verififying security code {security_code}")
            self.status = "paid"  
        else:
            raise Exception(f"Unknown payment type : {payment_type}")         

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB Cable", 2, 5)

logger.info(order.total_price())
order.pay("debit", "123456")