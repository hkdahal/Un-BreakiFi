from django.shortcuts import render

from .models import Vendor, Transaction, Individual

import dateutil.parser as dtp

from io import TextIOWrapper

import interact as parse


def index(request):
    individuals = Individual.objects.all()
    total = len(individuals)
    return render(request, 'SystemApp/users.html',
                  context={
                      'page_title': 'Home',
                      'users': individuals,
                      'total': total,
                      'current': 'Overview',
                      'display': True
                  })


def vendor_lst(request, user_id):
    vendors = Vendor.objects.all().order_by('store_name')
    result = []
    for i in vendors:
        ts = Transaction.objects.filter(vendor=i, user__auth_id=int(user_id))
        amount = spent_money(user_id, transactions=ts)
        result.append((i, amount, len(ts)))
    return render(request, 'SystemApp/vendor_lst.html',
                  context={
                      'info': result,
                      'user_id': int(user_id),
                      'page_title': 'Vendors',
                      'current': 'Vendors',
                      'current_url': 'vendors',
                  })


def vendor_transactions(request, user_id, vendor_id):
    vendor = Vendor.objects.filter(id=vendor_id)[0]
    transactions = Transaction.objects.filter(vendor=vendor,
                                              user__auth_id=int(user_id))
    return render(request, 'SystemApp/base.html',
                  context={
                      'page_title': 'Transactions',
                      'transactions': transactions[:100],
                      'total': 'For ' + str(vendor),
                      'current': 'Vendors',
                      'user_id': int(user_id),
                      'current_url': 'vendor/'+str(vendor_id)
                  })


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
    v = provide_vendors(user_id)[:30]
    context = {
        'page_title': 'Expenses',
        'the_info': v,
        'pie_title': "Top 20: Vendors vs Expense",
        'hg_title': "Top 20: Vendors vs Expense",
        'bar_X': "Vendor",
        'bar_Y': "Expense",
        'series_name': "Expense Total ($)",
        'height_size': 130,
        'current': 'VE',
        'user_id': int(user_id),
        'current_url': 'vendors/expense'

    }
    return render(request, 'SystemApp/pages/vendors_info.html', context)


def vendors_vs_transactions(request, user_id):
    v = provide_vendors(user_id, per_expense=False)[:30]
    context = {
        'page_title': 'Transactions',
        'the_info': v,
        'pie_title': "Top 20: Vendors vs Num Transaction",
        'hg_title': "Top 20: Vendors vs Num Transaction",
        'bar_X': "Vendor",
        'bar_Y': "Num of Transactions",
        'series_name': "Transaction Total",
        'height_size': 130,
        'current': 'VT',
        'user_id': int(user_id),
        'current_url': 'vendors/transactions'

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
        'page_title': 'Transportation',
        'the_info': ts,
        'hg_title': "Transportation vs Expense",
        'bar_X': "Transportation Means",
        'bar_Y': "Spent Money",
        'series_name': "Total Spent ($)",
        'height_size': 98,
        'current': 'TE',
        'user_id': int(user_id),
        'current_url': 'transport'

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


def restaurant_info(request, user_id):
    transactions = Transaction.objects.filter(vendor__store_name='Restaurant',
                                              user__auth_id=int(user_id))
    dct = {}
    for t in transactions:
        if t.name not in dct:
            dct[t.name] = abs(t.amount)
        else:
            dct[t.name] += abs(t.amount)
    data = []
    for item in dct:
        data.append((item, dct[item]))
    context = {
        'page_title': 'Restaurants',
        'the_info': data,
        'hg_title': "Transportation vs Expense",
        'bar_X': "Transportation Means",
        'bar_Y': "Spent Money",
        'series_name': "Total Spent ($)",
        'height_size': 98,
        'current': 'RE',
        'current_url': 'foods',
        'user_id': int(user_id)

    }
    return render(request, 'SystemApp/pages/transport_info.html', context)


def per_date(request, user_id):
    start = dtp.parse('1/1/2013')
    end = dtp.parse('2/10/2013')

    monthly_expense_income(request, user_id)

    if request.method == 'POST':
        given = request.POST['subject']
        given = given.split('-')
        start = dtp.parse(given[0])
        end = dtp.parse(given[1])
        # print(start, end)

    t = Transaction.objects.filter(date__gte=start, date__lt=end,
                                   user__auth_id=int(user_id))

    data = per_days(t, user_id)
    context = {
        'page_title': 'Over Time',
        'area_title': "Activities over {0} and {1}".format(start.date(),
                                                           end.date()),
        "start": str(start.date()), "end": str(end.date()),
        "the_info": data,
        "user_id": user_id,
        "area_X": 'Selected Dates',
        "area_Y": 'Total Expense',
        "area_series_name": 'Total Expense',
        'current': 'ToT',
        'current_url': 'dates',
        'user_id': int(user_id)
    }
    return render(request, 'SystemApp/pages/good_date_info.html', context)


def per_days(transactions, user_id):
    days = {}
    days_expense_transactions = []
    for t in transactions:
        if t.date not in days:
            days[t.date] = None
            ts = transactions.filter(date=t.date, user__auth_id=int(user_id))
            days_expense_transactions.append(
                (t.date, spent_money(user_id, transactions=ts)))
    return days_expense_transactions


def day_specific_transactions(request, user_id, d):

    if 'monthly' in d:
        d = d[len('monthly'):]
        d = dtp.parse(d)
        the_date = d.strftime("%B %Y")
        ts = Transaction.objects.filter(
            user__auth_id=user_id, date__month=d.month, date__year=d.year)
    else:
        the_date = dtp.parse(d)
        ts = Transaction.objects.filter(user__auth_id=user_id, date=the_date)

    return render(request, 'SystemApp/base.html',
                  context={
                      'page_title': 'Transactions',
                      'transactions': ts[:100],
                      'total': 'For {0} on {1}'.format(user_id,
                                                       the_date
                                                       ),
                      'current': 'ToT',
                      'user_id': int(user_id),

                  })


def monthly_expense_income(request, user_id):
    monthly_income_expense = []

    years = ['2013', '2014']
    for year in years:
        for month in range(1, 13):
            total_income = 0
            total_expense = 0
            the_ts = Transaction.objects.filter(
                user__auth_id=user_id, date__month=month, date__year=year)
            for t in the_ts:
                if t.is_expense():
                    total_expense += abs(t.amount)
                else:
                    total_income += t.amount
            if the_ts:
                d = the_ts[0].date
                monthly_income_expense.append((d.strftime('%B %Y'),
                                               total_income, total_expense, d))

    context = {
        'page_title': 'Monthly Income and Expense',
        'the_info': monthly_income_expense,
        'title': "Monthly Income and Expenditure",
        'X': "Months",
        'Y': "Income & Expenses",
        'v1_type': "Income ($)",
        'v2_type': "Expense ($)",
        'user_id': int(user_id),
        'current': 'MIE',
        'current_url': 'ie',

    }

    return render(request, 'SystemApp/pages/income_info.html',
                  context=context)


def housing_expense(request, user_id):
    housing_transactions = Transaction.objects.filter(
        user__auth_id=user_id, name__contains='Housing Rent')
    payments = []

    for t in housing_transactions:
        payments.append((t.date, abs(t.amount)))

    context = {
        'page_title': 'Housing Rent',
        'the_info': payments,
        'title': "Monthly Housing Payments",
        'X': "Date of Payment",
        'Y': "Amount",
        'v1_type': "Paid($)",
        'v2_type': "Expense ($)",
        'user_id': int(user_id),
        'current': 'HE',
        'current_url': 'housing'

    }

    return render(request, 'SystemApp/pages/income_info.html',
                  context=context)


def add_user(request):
    users_added = []
    if request.method == 'POST':
        files = request.FILES.getlist('my_files')
        clean_files = []
        for file in files:
            if str(file).endswith('.csv'):
                f = TextIOWrapper(file.file,
                                  encoding=request.encoding)
                clean_files.append(f)
        if clean_files:
            users_added = parse.save_to_db(clean_files, uploaded=True)
    page_title = 'Add User'
    if users_added:
        page_title = 'Added users'
    context = {
        'page_title': page_title,
        'users_added': users_added,
        'current': 'ANU',
    }
    return render(request, 'SystemApp/pages/upload_user.html', context=context)


def api_guide(request):
    return render(request, 'SystemApp/pages/api_guide.html', context={})
