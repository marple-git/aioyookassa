from aioyookassa.core.client import YooKassa
from aioyookassa.types.enum import (ConfirmationType, PaymentMode,
                                    PaymentSubject, Currency)
from aioyookassa.types.payment import (Confirmation, Customer, PaymentAmount,
                                       PaymentItem, Receipt)


async def test_client_init():
    # APi key is in env variable YOOKASSA_API_KEY. located in .env file
    import os

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("YOOKASSA_KEY")
    shop_id = os.getenv("YOOKASSA_SHOP_ID")
    client = YooKassa(api_key=api_key, shop_id=shop_id)
    confirmation = Confirmation(type=ConfirmationType.REDIRECT, return_url='https://example.com')
    item = PaymentItem(description='test', quantity="1", amount=PaymentAmount(value=100, currency='RUB'), vat_code=1, payment_subject=PaymentSubject.PAYMENT, payment_mode=PaymentMode.FULL_PAYMENT)
    receipt = Receipt(customer=Customer(email='test@gmail.com'), items=[item])
    payment = await client.payments.create_payment(
        amount=PaymentAmount(value=100), confirmation=confirmation, receipt=receipt)
    print(payment)
    await client.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_client_init())