from typing import Optional, TypedDict


class Transaction(TypedDict):
    id: int
    description: str
    date: str
    paid: bool
    amount_cents: int
    total_installments: int
    installment: int
    recurring: bool
    account_id: int
    account_type: str
    category_id: int
    contact_id: Optional[int]
    notes: str
    attachments_count: int
    credit_card_id: int
    credit_card_invoice_id: int
    paid_credit_card_id: Optional[int]
    paid_credit_card_invoice_id: Optional[int]
    oposite_transaction_id: Optional[int]
    oposite_account_id: Optional[int]
    created_at: str
    updated_at: str
