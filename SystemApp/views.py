from django.shortcuts import render, HttpResponse

from .models import Vendor, Transaction, Individual

import dateutil.parser as dtp


def index(request):
    individuals = Individual.objects.all()
    total = len(individuals)
    return render(request, 'SystemApp/users.html',
                  context={
                      'users': individuals,
                      'total': total
                  })


def vendor_lst(request, user_id):
    vendors = Vendor.objects.all().order_by('store_name')
    result = []
    for i in vendors:
        ts = Transaction.objects.filter(vendor=i, user__auth_id=int(user_id))
        amount = spent_money(user_id, transactions=ts)
        result.append((i, amount, len(ts)))
    return render(request, 'SystemApp/vendor_lst.html',
                  context={'info': result, 'user_id': user_id})


def vendor_transactions(request, user_id, vendor_id):
    vendor = Vendor.objects.filter(id=vendor_id)[0]
    transactions = Transaction.objects.filter(vendor=vendor,
                                              user__auth_id=int(user_id))
    return render(request, 'SystemApp/base.html',
                  context={
                      'transactions': transactions[:100],
                      'total': 'For ' + str(vendor)
                  })


def income_vs_expense(request, user_id):
    incomes = Transaction.objects.filter(
        amount__gt=0, user__auth_id=int(user_id))  # positive transactions
    # dates = [t.date for t in incomes]
    result = []
    for t in incomes:
        d = t.date
        ts = Transaction.objects.filter(
            date__month=d.month, date__year=d.year, user__auth_id=int(user_id))
        amount = spent_money(user_id, transactions=ts)
        result.append((d.strftime('%B %Y'), t.amount, amount))

    context = {
        'the_info': result,
        'title': "Monthly Income and Expenditure",
        'X': "Months",
        'Y': "Income & Expenses",
        'v1_type': "Income ($)",
        'v2_type': "Expense ($)"

    }

    return render(request, 'SystemApp/pages/income_info.html',
                  context=context)


def provide_vendors(user_id, per_expense=True, transactions=None):
    v = Vendor.objects.all().order_by('store_name')

    v_expenses = []

    for ven in v:
        if ven.store_name != 'Paycheck':
            v_expenses.append((ven, spent_money(
                user_id, vendor=ven, per_expense=per_expense,
                transactions=transactions)))

    if per_expense:
        data = sorted(v_expenses, key=lambda x: -x[1])
    else:
        data = sorted(v_expenses, key=lambda x: -x[1])

    return data


def vendors_vs_expense(request, user_id):
    v = provide_vendors(user_id)[:20]
    context = {
        'the_info': v,
        'pie_title': "Top 20: Vendors vs Expense",
        'hg_title': "Top 20: Vendors vs Expense",
        'bar_X': "Vendor",
        'bar_Y': "Expense",
        'series_name': "Expense Total ($)"

    }
    return render(request, 'SystemApp/pages/vendors_info.html', context)


def vendors_vs_transactions(request, user_id):
    v = provide_vendors(user_id, per_expense=False)[:20]
    context = {
        'the_info': v,
        'pie_title': "Top 20: Vendors vs Num Transaction",
        'hg_title': "Top 20: Vendors vs Num Transaction",
        'bar_X': "Vendor",
        'bar_Y': "Num of Transactions",
        'series_name': "Transaction Total"

    }
    return render(request, 'SystemApp/pages/vendors_info.html', context)


def transportation(request, user_id):
    transport_types = ['Public Transportation', 'Taxi', 'Uber', 'Lyft']

    vens = [Vendor.objects.filter(store_name=v)[0] for v in transport_types]
    ts = []
    for v in vens:
        if v:
            t = Transaction.objects.filter(vendor=v, user__auth_id=int(user_id))
            ts.append((v, spent_money(user_id, transactions=t)))

    context = {
        'the_info': ts,
        'hg_title': "Transportation vs Expense",
        'bar_X': "Transportation Means",
        'bar_Y': "Spent Money",
        'series_name': "Total Spent ($)"


    }
    return render(request, 'SystemApp/pages/transport_info.html', context)


def get_income(user_id):
    ts = Transaction.objects.filter(amount__gte=0, user__auth_id=int(user_id))
    total = 0
    for t in ts:
        total += t.amount
    return total, ts


def spent_money(user_id, vendor=None, per_expense=True, transactions=None):
    if not transactions:
        if vendor:
            transactions = Transaction.objects.filter(
                vendor=vendor, user__auth_id=int(user_id))
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


def restaurant_info(user_id):
    transactions = Transaction.objects.filter(vendor__store_name='Restaurant',
                                              user__auth_id=int(user_id))
    lst = []
    for t in transactions:
        if t.name not in lst:
            lst.append(t.name)
    return lst


def per_date(request, user_id):
    start = dtp.parse('1/1/2013')
    end = dtp.parse('3/10/2013')

    if request.method == 'POST':
        given = request.POST['subject']
        given = given.split('-')
        start = dtp.parse(given[0])
        end = dtp.parse(given[1])
        # print(start, end)

    t = Transaction.objects.filter(date__gte=start, date__lt=end,
                                   user__auth_id=int(user_id))

    context = {'title': "Top 10: Vendors vs Expense",
               "start": str(start.date()), "end": str(end.date()),
               "the_info": per_days(t, user_id),
               "user_id": user_id
               }
    return render(request, 'SystemApp/pages/date_info.html', context)


def per_days(transactions, user_id):
    days = {}
    days_expense_transactions = []
    for t in transactions:
        if t.date not in days:
            days[t.date] = None
            ts = transactions.filter(date=t.date, user__auth_id=int(user_id))
            days_expense_transactions.append(
                (t.date, len(ts), spent_money(user_id, transactions=ts)))
    return days_expense_transactions



