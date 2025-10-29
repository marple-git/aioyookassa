"""
Example of using YooKassa Receipts API
"""
import asyncio
from datetime import datetime, timedelta, timezone

from aioyookassa import YooKassa
from aioyookassa.types import (Customer, PaymentAmount, ReceiptStatus, ReceiptType)
from aioyookassa.types.receipt_registration import (ReceiptRegistrationItem,
                                                    ReceiptSettlement)


async def main():
    # Initialize client
    client = YooKassa(
        api_key="your_api_key_here",
        shop_id=123456,
    )

    # Example 1: Create a receipt for payment
    print("=== Creating receipt for payment ===")

    items = [
        ReceiptRegistrationItem(
            description="Товар 1",
            quantity=1,
            amount=PaymentAmount(value=100.00, currency="RUB"),
            vat_code=2,
            payment_subject="commodity",
            payment_mode="full_prepayment",
        ),
        ReceiptRegistrationItem(
            description="Товар 2",
            quantity=2,
            amount=PaymentAmount(value="50.00", currency="RUB"),
            vat_code=2,
            payment_subject="commodity",
            payment_mode="full_prepayment",
        ),
    ]

    settlements = [
        ReceiptSettlement(
            type="cashless",
            amount=PaymentAmount(value="200.00", currency="RUB"),
        )
    ]

    customer = Customer(
        email="customer@example.com",
        phone="79000000000",
    )

    try:
        receipt = await client.receipts.create_receipt(
            type=ReceiptType.PAYMENT,  # Используем enum вместо строки
            customer=customer,
            items=items,
            settlements=settlements,
            payment_id="payment_id_here",
            send=True,
            internet=True,
            tax_system_code=1,
            timezone=180,
        )
        print(f"Receipt created: {receipt.id}")
        print(f"Type: {receipt.type}")
        print(f"Status: {receipt.status}")
    except Exception as e:
        print(f"Error creating receipt: {e}")

    # Example 2: Get receipts for payment
    print("\n=== Getting receipts for payment ===")

    try:
        receipts = await client.receipts.get_receipts(
            payment_id="payment_id_here",
            limit=10,
        )
        print(f"Found {len(receipts.items)} receipts")
        for receipt in receipts.items:
            print(f"  - Receipt {receipt.id}: {receipt.status}")
    except Exception as e:
        print(f"Error getting receipts: {e}")

    # Example 3: Get receipts by status
    print("\n=== Getting succeeded receipts ===")

    try:
        receipts = await client.receipts.get_receipts(
            status=ReceiptStatus.SUCCEEDED,  # Используем enum вместо строки
            limit=20,
        )
        print(f"Found {len(receipts.items)} succeeded receipts")
        for receipt in receipts.items:
            print(f"  - Receipt {receipt.id}: {receipt.fiscal_document_number}")
    except Exception as e:
        print(f"Error getting receipts: {e}")

    # Example 4: Get receipts for time period
    print("\n=== Getting receipts for last 7 days ===")

    try:
        receipts = await client.receipts.get_receipts(
            created_at_gte=datetime.now(timezone.utc) - timedelta(days=7),
            created_at_lte=datetime.now(timezone.utc),
            limit=50,
        )
        print(f"Found {len(receipts.items)} receipts in last 7 days")
    except Exception as e:
        print(f"Error getting receipts: {e}")

    # Example 5: Get specific receipt
    print("\n=== Getting specific receipt ===")

    try:
        receipt = await client.receipts.get_receipt("receipt_id_here")
        print(f"Receipt {receipt.id}")
        print(f"  Type: {receipt.type}")
        print(f"  Status: {receipt.status}")
        print(f"  Fiscal document: {receipt.fiscal_document_number}")
        print(f"  Items: {len(receipt.items)}")
    except Exception as e:
        print(f"Error getting receipt: {e}")

    # Example 6: Create receipt for refund
    print("\n=== Creating receipt for refund ===")

    try:
        refund_receipt = await client.receipts.create_receipt(
            type=ReceiptType.REFUND,  # Используем enum для возврата
            customer=customer,
            items=items,
            settlements=settlements,
            refund_id="refund_id_here",
            send=True,
            internet=True,
        )
        print(f"Refund receipt created: {refund_receipt.id}")
        print(f"Status: {refund_receipt.status}")
    except Exception as e:
        print(f"Error creating refund receipt: {e}")

    # Example 7: Pagination
    print("\n=== Pagination example ===")

    try:
        all_receipts = []
        cursor = None

        while True:
            receipts = await client.receipts.get_receipts(
                limit=10,
                cursor=cursor,
            )
            all_receipts.extend(receipts.items)
            print(f"Loaded {len(receipts.items)} receipts (total: {len(all_receipts)})")

            if not receipts.next_cursor:
                break
            cursor = receipts.next_cursor

        print(f"Total receipts loaded: {len(all_receipts)}")
    except Exception as e:
        print(f"Error during pagination: {e}")


if __name__ == "__main__":
    asyncio.run(main())

