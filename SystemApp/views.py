from django.shortcuts import render, HttpResponse

import csv

from .models import Vendor, Transaction
import datetime


def index(request):
    return render(request, 'SystemApp/base.html')


def parse():
    path = '# path here'
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            auth_id = row['auth_id']
            d = [int(i) for i in row[' Date'].split('/')]
            date = datetime.date(year=d[2], month=d[0], day=d[1])
            location = row[' Location ']

            vendor_name, transaction_name = parse_vendor(row[' Vendor'])

            the_vendor = Vendor.objects.filter(store_name=vendor_name)
            if not the_vendor:
                the_vendor = Vendor.objects.create(store_name=vendor_name)
            else:
                the_vendor = the_vendor[0]
            amount = row[' Amount']
            Transaction.objects.create(
                auth_id=auth_id, date=date, amount=float(amount),
                location=location, name=transaction_name, vendor=the_vendor)


def parse_vendor(name):
    name = name.strip()
    split_name = name.split('-')

    if len(split_name) == 1:
        return split_name[0], split_name[0]
    return (i.strip() for i in split_name)

