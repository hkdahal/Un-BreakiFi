import csv
import dateutil.parser as dtp
import django
import glob
import os
import sys


curr_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(curr_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UnBreakiFi.settings")


if 'setup' in dir(django):
    django.setup()

from SystemApp.models import Individual, Vendor, Transaction, Features
import SystemApp.manual_features as F


def parse():
    my_dir = os.path.dirname(os.path.realpath(__file__))
    file_lst = glob.glob(my_dir+'/transaction-data/*.csv')
    if file_lst:
        save_to_db(file_lst)


def save_to_db(file_lst, uploaded=False):
    i = 0
    l = len(file_lst)
    users = set()
    for path in file_lst:
        if uploaded:
            reader = csv.reader(path)
            user = read_and_save(reader)
        else:
            with open(path) as csvfile:
                reader = csv.reader(csvfile)
                user = read_and_save(reader)
        users.add(user)
        i += 1
        print_progress_bar(i, l, prefix='Progress:', suffix='Complete',
                           length=50)
    return users


def update_features(user):
    if user:
        feature = Features(user=user)
        feature.student = F.is_student(user.auth_id)
        feature.has_kids = F.has_kids(user.auth_id)
        feature.student_loan = F.has_been_paying_student_loans(user.auth_id)
        feature.pets = F.has_pets(user.auth_id)
        feature.an_artist = F.is_an_artist(user.auth_id)
        feature.moved = F.is_moving(user.auth_id)
        feature.peaceful = F.likes_peace(user.auth_id)
        feature.proposing = F.is_proposing(user.auth_id)
        feature.athletic = F.is_athletic(user.auth_id)
        feature.divorced = F.is_divorced(user.auth_id)
        feature.outgoing = F.is_outgoing(user.auth_id)
        feature.figurine_stuffs = F.is_into_stuffs(user.auth_id)
        feature.student = F.is_student(user.auth_id)
        feature.save()


def read_and_save(reader):
    user = None
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
    update_features(user=user)
    return user.auth_id


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


def manual_flush():
    print("Deleting Individuals...")
    Individual.objects.all().delete()
    print("Done!\nDeleting Vendors")
    Vendor.objects.all().delete()
    print("Done!\nDatabase Emtpy now!!")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '--parse':
            parse()
        elif sys.argv[1] == '--delete':
            sure = input('Are you sure you want to delete?\n[Y]es or [N]o: ')
            if sure.lower() == 'y':
                manual_flush()
            else:
                print('Not deleted')
        else:
            print('wrong argument given: ', sys.argv[1], '\nUsage: \n\t--parse : parse csv files \n\t--delete : delete all the data from the database\n')
    else:
        print('Must provide 1 argument')
