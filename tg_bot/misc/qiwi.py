import uuid
from dataclasses import dataclass
from yoomoney import Quickpay, Client
from tg_bot.config import load_config


@dataclass
class Payment:
    price: int
    pay_id: str
    id: int

    def create(self):
        client = Client(token=load_config().tg_bot.money_token)
        quickpay = Quickpay(
            receiver=load_config().tg_bot.wallet,
            targets=f"id купленного товара : {self.id}",
            quickpay_form="shop",
            paymentType="SB",
            sum=self.price,
            label=self.pay_id,
        )
        return quickpay.redirected_url

    def check_payment(self):
        client = Client(token=load_config().tg_bot.money_token)
        history = client.operation_history(label=self.pay_id)
        for operation in history.operations:
            # print(operation.status)
            if operation.status == "success":
                return "success"
        raise ValueError()

    # https://sun9-12.userapi.com/impg/V3HVKENj1efgBylDD0zC-QA7TpyGWVV-hw0Pmw/sPv7XaKFtKY.jpg?size=359x499&quality=96&sign=bb068fb23e24902f050b2bc024af04e2&type=album
    # lubanovich
    # https://static.insales-cdn.com/images/products/1/2182/81324166/49602088.jpg
