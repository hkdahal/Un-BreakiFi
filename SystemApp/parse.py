import csv

import dateutil.parser as dtp

import glob

import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UnBreakiFi.settings")
django.setup()

from SystemApp.models import Individual, Vendor, Transaction


def parse():
    module_dir = os.path.dirname(__file__)

    file_lst = glob.glob(module_dir+'/transaction-data/*.csv')

    i = 0
    l = len(file_lst)
    print_progress_bar(i, l, prefix='Progress:', suffix='Complete', length=50)
    for path in file_lst:
        with open(path) as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                # the_date = None
                try:
                    the_date = dtp.parse(row[1])
                except:
                    given_date = row[1].split('/')
                    the_date = dtp.parse(given_date[0]+'/31/'+given_date[2])
                if the_date:
                    amount = row[3]
                    location = row[4]
                    user = Individual.objects.filter(auth_id=int(row[0]))
                    if user:
                        user = user[0]
                    else:
                        user = Individual.objects.create(auth_id=int(row[0]))

                    vendor_name, transaction_name = parse_vendor(row[2])

                    the_vendor = Vendor.objects.filter(store_name=vendor_name)
                    if not the_vendor:
                        the_vendor = Vendor.objects.create(store_name=vendor_name)
                    else:
                        the_vendor = the_vendor[0]

                    Transaction.objects.create(
                        user=user, date=the_date, amount=float(amount),
                        location=location, name=transaction_name, vendor=the_vendor)
            i += 1
            # print('Done: ', i, ' out of ', len(file_lst))
            print_progress_bar(i, l, prefix='Progress:',
                               suffix='Complete', length=50)


def parse_vendor(name):
    name = name.strip()
    split_name = name.split('-')

    if len(split_name) == 1:
        return split_name[0], split_name[0]
    return (i.strip() for i in split_name)


# Print iterations progress
def print_progress_bar(iteration, total, prefix='',
                       suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    st = '\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix) + '\r'
    print(st)
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == '__main__':
    parse()
