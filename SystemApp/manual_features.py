from django.shortcuts import render

from django.db.models import Q

from .models import Transaction, Individual


def provide_profile(request, user_id):
    user = Individual.objects.filter(auth_id=user_id)
    total_expense, total_income, total_housing = total_expense_and_income(user)
    financial_status = total_income - abs(total_expense)

    msg = ''

    if has_kids(user_id):
        msg += 'This guy has kids.\n'

    student_loan = has_been_paying_student_loans(user_id)
    if student_loan:
        msg += 'Has been paying student loan.So far: ${0}'.format(student_loan)

    if has_pets(user_id):
        msg += 'This guy has pets!!!'

    if is_student(user_id):
        msg += 'This guy is a STUDENT!!'

    if is_an_artist(user_id):
        msg += 'This guy is either into art or is an ARTIST!!'

    if is_into_music(user_id):
        msg += 'This guy is into MUSIC!!'

    if is_into_stuffs(user_id):
        msg += 'This guy is into Figurine stuffs, and probably a nerd!!'

    if is_moving(user_id):
        msg += 'This guy is moved or relocated recently!!'

    if likes_peace(user_id):
        msg += 'This guy likes peace and to read!!'

    if is_purposing(user_id):
        msg += 'This guy is planning to get MARRIED... purposing?!!'

    if is_athletic(user_id):
        msg += 'This guy is into SPORTS and/or is an athletic person!!'

    context = {
        'Auth_id': user_id,
        'total_expense': total_expense,
        'total_income': total_income,
        'status': financial_status,
        'total_housing': total_housing,
        'msg': msg
    }
    return render(request, 'SystemApp/pages/profile.html', context=context)


def total_expense_and_income(user):
    total_expense = 0
    total_income = 0
    total_housing = 0
    for t in Transaction.objects.filter(user=user):
        if t.is_expense():
            total_expense += t.amount
            if 'housing rent' in t.name.lower():
                total_housing += abs(t.amount)
        else:
            total_income += t.amount
    return total_expense, total_income, total_housing


def has_kids(user_id):
    kids_related_transactions = Transaction.objects.filter(
        Q(user__auth_id=user_id) & (Q(name__contains='Baby') | Q(name__contains='babies'))
    )
    return bool(kids_related_transactions)


def has_been_paying_student_loans(user_id):
    total = 0
    student_loans_transactions = Transaction.objects.filter(
        user__auth_id=user_id, name__contains="Student Loan"
    )

    for t in student_loans_transactions:
        total += abs(t.amount)

    return total


def has_pets(user_id):
    pets_related_transactions = Transaction.objects.filter(
        Q(user__auth_id=user_id) & Q(name__contains='Pet')
    )
    return bool(pets_related_transactions)


def is_student(user_id):
    student_related_transactions = Transaction.objects.filter(
        Q(user__auth_id=user_id) & (
            Q(name__contains='Science Book') |
            Q(name__contains='Mathematics Book') |
            Q(name__contains='Biology Book')
        )
    )
    return bool(student_related_transactions)


def is_an_artist(user_id):
    art_related_transactions = Transaction.objects.filter(
        Q(user__auth_id=user_id) & (
            Q(name__contains='Art') |
            Q(name__contains='Paint') |
            Q(name__contains='Craft')
        )
    )
    return bool(art_related_transactions)


def is_into_music(user_id):
    music_related_transactions = Transaction.objects.filter(
        Q(user__auth_id=user_id) & (
            Q(name__contains='Guitar') |
            Q(name__contains='Music')
        )
    )
    return bool(music_related_transactions)


def is_into_stuffs(user_id):
    stuffs_related_transactions = Transaction.objects.filter(
        Q(user__auth_id=user_id) & (
            Q(name__contains='Figurine') |
            Q(name__contains='Star')
        )
    )
    return bool(stuffs_related_transactions)


def is_moving(user_id):
    moving_related_transactions = Transaction.objects.filter(
        Q(user__auth_id=user_id) & (
            Q(name__contains='Depot') |
            Q(name__contains='Furniture') |
            Q(name__contains='Move')
        )
    )
    return bool(moving_related_transactions)


def likes_peace(user_id):
    peace_related_transactions = Transaction.objects.filter(
        Q(user__auth_id=user_id) & (
            Q(name__contains='Library') |
            Q(name__contains='Book Store')
        )
    )
    return bool(peace_related_transactions)


def is_purposing(user_id):
    wedding_related_transactions = Transaction.objects.filter(
        Q(user__auth_id=user_id) & (
            Q(name__contains='Wedding') |
            Q(name__contains='Weeding Planner') |
            Q(name__contains='Jewelry')
        )
    )
    return bool(wedding_related_transactions)


def is_athletic(user_id):
    athlete_related_transactions = Transaction.objects.filter(
        Q(user__auth_id=user_id) & (
            Q(name__contains='Dick') |
            Q(name__contains='Sports') |
            Q(name__contains='NFL') |
            Q(name__contains='NBA') |
            Q(name__contains='Athletic') |
            Q(name__contains='Vitamin') |
            Q(name__contains='Bike') |
            Q(name__contains='Gym')

        )
    )
    return bool(athlete_related_transactions)
