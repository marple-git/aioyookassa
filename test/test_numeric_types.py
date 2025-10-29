"""
Test that all numeric fields support int, float, str, and Decimal types
"""
from decimal import Decimal

from aioyookassa.types import (
    InvoiceCartItem,
    InvoiceReceiptItem,
    PaymentAmount,
    PaymentItem,
)
from aioyookassa.types.enum import PaymentMode, PaymentSubject
from aioyookassa.types.receipt_registration import ReceiptRegistrationItem


def test_payment_amount_types():
    """Test PaymentAmount with different value types"""
    
    # Integer
    amount1 = PaymentAmount(value=100, currency="RUB")
    assert amount1.value == 100
    
    # Float
    amount2 = PaymentAmount(value=100.50, currency="RUB")
    assert amount2.value == 100.50
    
    # String
    amount3 = PaymentAmount(value="100.00", currency="RUB")
    assert amount3.value == "100.00"
    
    # Decimal
    amount4 = PaymentAmount(value=Decimal("100.00"), currency="RUB")
    assert amount4.value == Decimal("100.00")
    
    print("✅ PaymentAmount: все типы работают")


def test_payment_item_quantity():
    """Test PaymentItem quantity with different types"""
    
    amount = PaymentAmount(value="100.00", currency="RUB")
    
    # Integer
    item1 = PaymentItem(
        description="Test",
        amount=amount,
        vat_code=2,
        quantity=5,
        payment_subject=PaymentSubject.COMMODITY,
        payment_mode=PaymentMode.FULL_PAYMENT,
    )
    assert item1.quantity == 5
    
    # Float
    item2 = PaymentItem(
        description="Test",
        amount=amount,
        vat_code=2,
        quantity=2.5,
        payment_subject=PaymentSubject.COMMODITY,
        payment_mode=PaymentMode.FULL_PAYMENT,
    )
    assert item2.quantity == 2.5
    
    # String
    item3 = PaymentItem(
        description="Test",
        amount=amount,
        vat_code=2,
        quantity="3",
        payment_subject=PaymentSubject.COMMODITY,
        payment_mode=PaymentMode.FULL_PAYMENT,
    )
    assert item3.quantity == "3"
    
    # Decimal
    item4 = PaymentItem(
        description="Test",
        amount=amount,
        vat_code=2,
        quantity=Decimal("1.5"),
        payment_subject=PaymentSubject.COMMODITY,
        payment_mode=PaymentMode.FULL_PAYMENT,
    )
    assert item4.quantity == Decimal("1.5")
    
    print("✅ PaymentItem.quantity: все типы работают")


def test_receipt_registration_item_quantity():
    """Test ReceiptRegistrationItem quantity with different types"""
    
    amount = PaymentAmount(value="50.00", currency="RUB")
    
    # Integer
    item1 = ReceiptRegistrationItem(
        description="Test",
        quantity=2,
        amount=amount,
        vat_code=2,
    )
    assert item1.quantity == 2
    
    # Float
    item2 = ReceiptRegistrationItem(
        description="Test",
        quantity=1.5,
        amount=amount,
        vat_code=2,
    )
    assert item2.quantity == 1.5
    
    # String
    item3 = ReceiptRegistrationItem(
        description="Test",
        quantity="3",
        amount=amount,
        vat_code=2,
    )
    assert item3.quantity == "3"
    
    # Decimal
    item4 = ReceiptRegistrationItem(
        description="Test",
        quantity=Decimal("2.75"),
        amount=amount,
        vat_code=2,
    )
    assert item4.quantity == Decimal("2.75")
    
    print("✅ ReceiptRegistrationItem.quantity: все типы работают")


def test_invoice_cart_item_quantity():
    """Test InvoiceCartItem quantity with different types"""
    
    price = PaymentAmount(value="100.00", currency="RUB")
    
    # Integer
    item1 = InvoiceCartItem(description="Test", price=price, quantity=1)
    assert item1.quantity == 1
    
    # Float
    item2 = InvoiceCartItem(description="Test", price=price, quantity=2.5)
    assert item2.quantity == 2.5
    
    # String
    item3 = InvoiceCartItem(description="Test", price=price, quantity="3")
    assert item3.quantity == "3"
    
    # Decimal
    item4 = InvoiceCartItem(description="Test", price=price, quantity=Decimal("1.5"))
    assert item4.quantity == Decimal("1.5")
    
    print("✅ InvoiceCartItem.quantity: все типы работают")


def test_invoice_receipt_item_quantity():
    """Test InvoiceReceiptItem quantity with different types"""
    
    amount = PaymentAmount(value="50.00", currency="RUB")
    
    # Integer
    item1 = InvoiceReceiptItem(
        description="Test",
        amount=amount,
        vat_code=2,
        quantity=2,
    )
    assert item1.quantity == 2
    
    # Float
    item2 = InvoiceReceiptItem(
        description="Test",
        amount=amount,
        vat_code=2,
        quantity=1.5,
    )
    assert item2.quantity == 1.5
    
    # String
    item3 = InvoiceReceiptItem(
        description="Test",
        amount=amount,
        vat_code=2,
        quantity="3",
    )
    assert item3.quantity == "3"
    
    # Decimal
    item4 = InvoiceReceiptItem(
        description="Test",
        amount=amount,
        vat_code=2,
        quantity=Decimal("2.5"),
    )
    assert item4.quantity == Decimal("2.5")
    
    print("✅ InvoiceReceiptItem.quantity: все типы работают")


if __name__ == "__main__":
    test_payment_amount_types()
    test_payment_item_quantity()
    test_receipt_registration_item_quantity()
    test_invoice_cart_item_quantity()
    test_invoice_receipt_item_quantity()
    
    print("\n" + "="*60)
    print("🎉 Все тесты пройдены!")
    print("="*60)
    print("\n✨ Все числовые поля поддерживают:")
    print("   - int (целые числа)")
    print("   - float (дробные числа)")
    print("   - str (строки)")
    print("   - Decimal (точные десятичные)")


