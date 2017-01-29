from django.shortcuts import render, HttpResponse

import csv

from .models import Vendor, Transaction

import dateutil.parser as dtp


def index(request):
    transactions = Transaction.objects.all()
    total = [len(transactions), len(Vendor.objects.all())]

    return render(request, 'SystemApp/base.html',
                  context={
                      'transactions': transactions[:50],
                      'total': total
                  })


def provide_vendors(per_expense=True, transactions=None):
    v = Vendor.objects.all().order_by('store_name')

    v_expenses = []

    for ven in v:
        if ven.store_name != 'Paycheck':
            v_expenses.append((ven, spent_money(vendor=ven, per_expense=per_expense, transactions=transactions)))

    if per_expense:
        data = sorted(v_expenses, key=lambda x: -x[1])[:10]
    else:
        data = sorted(v_expenses, key=lambda x: -x[1])[:10]

    return data


def vendors_vs_expense(request):
    v = provide_vendors()
    context = {'vendors': v, 'title': "Top 10: Vendors vs Expense"}
    return render(request, 'SystemApp/vendors.html', context)


def vendors_vs_transactions(request):
    v = provide_vendors(per_expense=False)
    context = {'vendors': v, 'title': "Top 10: Vendors vs Transactions"}
    return render(request, 'SystemApp/vendors.html', context)


def spent_money(vendor=None, per_expense=True, transactions=None):
    if not transactions:
        if vendor:
            transactions = Transaction.objects.filter(vendor=vendor)
        else:
            return 0
    total = 0
    for t in transactions:
        if t.is_expense():
            total += abs(t.amount)
    if per_expense:
        return total
    else:
        return len(transactions)


def per_date(request):
    start = dtp.parse('1/1/2013')
    end = dtp.parse('1/10/2013')

    if request.method == 'POST':
        given = request.POST['subject']
        given = given.split('-')
        start = dtp.parse(given[0])
        end = dtp.parse(given[1])
        # print(start, end)

    t = Transaction.objects.filter(date__gte=start, date__lt=end)
    if t:
        data = provide_vendors(transactions=t)
    else:
        data = []
    context = {'vendors': data, 'title': "Top 10: Vendors vs Expense",
               "start": str(start.date()), "end": str(end.date()),
               "daily_info": per_days(t)
               }
    return render(request, 'SystemApp/dates.html', context)


def per_days(transactions):
    days = {}
    days_expense_transactions = []
    for t in transactions:
        if t.date not in days:
            days[t.date] = None
            ts = transactions.filter(date=t.date)
            days_expense_transactions.append(
                (t.date, len(ts), spent_money(transactions=ts)))
    return days_expense_transactions


def parse():
    path = '/Users/hdahal/Desktop/Projects/Intuit/PlayGround/' \
           'transaction-data/user-0.csv'
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            auth_id = row['auth_id']

            try:
                d = dtp.parse(row[' Date'])
            except:
                # print(e)
                print("FOR: ", row[' Date'])

            location = row[' Location ']

            vendor_name, transaction_name = parse_vendor(row[' Vendor'])

            the_vendor = Vendor.objects.filter(store_name=vendor_name)
            if not the_vendor:
                the_vendor = Vendor.objects.create(store_name=vendor_name)
            else:
                the_vendor = the_vendor[0]
            amount = row[' Amount']
            try:
                Transaction.objects.create(
                    auth_id=auth_id, date=d, amount=float(amount),
                    location=location, name=transaction_name, vendor=the_vendor)
            except ValueError as e:
                print(e)


def parse_vendor(name):
    name = name.strip()
    split_name = name.split('-')

    if len(split_name) == 1:
        return split_name[0], split_name[0]
    return (i.strip() for i in split_name)

