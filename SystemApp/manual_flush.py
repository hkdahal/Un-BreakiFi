from SystemApp.models import Individual, Vendor


def main():
    print("Deleting Individuals...")
    Individual.objects.all().delete()
    print("Done!\n Deleting Vendors")
    Vendor.objects.all().delete()
    print("Done!\n Database Emtpy now!!")

main()
