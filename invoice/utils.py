from datetime import date
from decimal import Decimal

from .models import Bill, CapitalCall, Investor


def calculate_membership_fee(investor):
    total_investment = sum(inv.amount for inv in investor.investments.all())
    return Decimal("0") if total_investment > 50000 else Decimal("3000")


def calculate_upfront_fees(investment):
    return investment.amount * investment.fee_percentage / 100 * 5


def calculate_yearly_fees(investment, year):
    fee_percentage = investment.fee_percentage
    if investment.date.year >= 2019:
        if year == 1:
            days_in_year = 366 if investment.date.year % 4 == 0 else 365
            return (
                (investment.date.timetuple().tm_yday / days_in_year)
                * fee_percentage
                / 100
                * investment.amount
            )
        elif year == 2:
            return fee_percentage / 100 * investment.amount
        elif year == 3:
            return (fee_percentage - Decimal("0.20")) / 100 * investment.amount
        elif year == 4:
            return (fee_percentage - Decimal("0.50")) / 100 * investment.amount
        else:
            return (fee_percentage - Decimal("1.00")) / 100 * investment.amount
    else:
        if year == 1:
            days_in_year = 366 if investment.date.year % 4 == 0 else 365
            return (
                (investment.date.timetuple().tm_yday / days_in_year)
                * fee_percentage
                / 100
                * investment.amount
            )
        else:
            return fee_percentage / 100 * investment.amount


def generate_bills(investor_id):
    investor = Investor.objects.get(id=investor_id)
    bills = []

    # Membership fee
    membership_fee = calculate_membership_fee(investor)
    if membership_fee > 0:
        bills.append(
            Bill.objects.create(
                investor=investor,
                bill_type="MEMBERSHIP",
                amount=membership_fee,
                date=date.today(),
            )
        )

    # Investment fees
    for investment in investor.investments.all():
        # Upfront fees
        upfront_fees = calculate_upfront_fees(investment)
        bills.append(
            Bill.objects.create(
                investor=investor,
                investment=investment,
                bill_type="UPFRONT",
                amount=upfront_fees,
                date=date.today(),
            )
        )

        # Yearly fees
        current_year = date.today().year
        for year in range(1, 6):  # Assuming 5 years of yearly fees
            if investment.date.year + year <= current_year:
                yearly_fee = calculate_yearly_fees(investment, year)
                bills.append(
                    Bill.objects.create(
                        investor=investor,
                        investment=investment,
                        bill_type="YEARLY",
                        amount=yearly_fee,
                        date=date(
                            investment.date.year + year,
                            investment.date.month,
                            investment.date.day,
                        ),
                    )
                )

    return bills


def generate_capital_call(investor_id):
    investor = Investor.objects.get(id=investor_id)
    bills = generate_bills(investor_id)
    total_amount = sum(bill.amount for bill in bills)

    capital_call = CapitalCall.objects.create(
        investor=investor,
        total_amount=total_amount,
        date=date.today(),
        due_date=date.today().replace(month=date.today().month + 1),  # Due in 1 month
        iban="FR7630006000011234567890189",  # Example IBAN
    )
    capital_call.bills.set(bills)

    return capital_call
