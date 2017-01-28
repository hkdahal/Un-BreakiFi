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


def parse():
    path = '/Users/hdahal/Desktop/Projects/Intuit/PlayGround/' \
           'transaction-data/user-7.csv'
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

