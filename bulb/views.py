# -*- coding: utf-8  -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators import csrf
from django.utils import timezone
from post_office import mail


from accounts.utils import get_user_gender
from core.models import StudentClubYear
from core import decorators
from bulb.models import Category, Book, Request, Point
from bulb.forms import BookForm
from bulb import utils


@login_required
def index(request):
    return render(request, "bulb/index.html")

# TODO
# * Send emails in case of failed indirect request.
# * Don't hard-cord the editing URL in JavaScript.
# * Don't Repeat Yourself when it comes to JavaScript delete, edit and
#   order buttons.
@login_required
def list_book_categories(request):
    categories = Category.objects.distinct().filter(book__isnull=False,
                                                    book__is_available=True,
                                                    book__is_deleted=False)
    context = {'categories': categories}
    return render(request, "bulb/exchange/list_categories.html",
                  context)

@login_required
def show_category(request, code_name):
    category = get_object_or_404(Category, code_name=code_name)
    context = {'category': category}
    return render(request, "bulb/exchange/show_category.html", context)

@decorators.ajax_only
@csrf.csrf_exempt
@login_required
def list_book_previews(request, source, name):
    if source == "category":
        category = get_object_or_404(Category, code_name=name)
        books = Book.objects.current_year().available().filter(category=category)
    elif source == "user":
        done_pks = (Request.objects.filter(owner_status='D', requester_status='D') |\
                    Request.objects.filter(owner_status='D', requester_status='') |\
                    Request.objects.filter(owner_status='', requester_status='D'))\
                    .values_list('book__pk', flat=True)
        condition = request.POST.get('condition')
        user = get_object_or_404(User, username=name)
        if condition == 'available':
            books = Book.objects.current_year().available().of_user(user)
        elif condition == 'done':
            book_pks = (Request.objects.filter(owner_status='D', requester_status='D') |\
                        Request.objects.filter(owner_status='D', requester_status='') |\
                        Request.objects.filter(owner_status='', requester_status='D'))\
                        .values_list('book__pk', flat=True)
            books = Book.objects.current_year().filter(pk__in=done_pks).of_user(user).distinct()
            
    return render(request, "bulb/exchange/list_books.html",
                  {'books': books})

@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
@login_required
def order_instructions(request):
    pk = request.POST.get('pk')
    delivery_type = request.POST.get('delivery_type')
    book = get_object_or_404(Book, pk=pk, is_deleted=False)

    if not utils.can_order_book(request.user, book):
        raise PermissionDenied

    if request.user.book_points.count_total() and \
       delivery_type in ['direct', 'indirect']:
        requester_gender = get_user_gender(request.user)
        owner_gender = get_user_gender(book.submitter)
        if delivery_type == 'indirect' or \
           not requester_gender == owner_gender:
            delivery = 'I'
        elif delivery_type == 'direct':
            delivery = 'D'
        current_year = StudentClubYear.objects.get_current()
        book_request = Request.objects.create(book=book,
                                              delivery=delivery,
                                              requester=request.user)
        Point.objects.create(year=current_year,
                             request=book_request,
                             user=request.user,
                             value=-1)
        book.is_available = False
        book.save()
        email_context = {'book': book,
                         'book_request': book_request}
        my_books_url = reverse('bulb:my_books')
        my_books_full_url = request.build_absolute_uri(my_books_url)
        if delivery == 'I':
            bulb_coordinator = utils.get_bulb_club_for_user(book.submitter).coordinator
            if bulb_coordinator:
                indirect_requests_url = reverse('bulb:indirect_requests')
                indirect_requests_full_url = request.build_absolute_uri(indirect_requests_url)
                email_context['full_url'] = indirect_requests_full_url
                email_context['bulb_coordinator'] = bulb_coordinator
                mail.send([bulb_coordinator.email],
                           template="book_requested_indirectly_to_coordinator",
                           context=email_context)
            owner_template = "book_requested_indirectly_to_owner"
        elif delivery == 'D':
            owner_template = "book_requested_directly_to_owner"

        email_context['full_url'] = my_books_full_url
        mail.send([book.submitter.email],
                   template=owner_template,
                   context=email_context)

    bulb_coordinator = utils.get_bulb_club_for_user(book.submitter).coordinator

    return render(request, "bulb/exchange/components/order_body.html",
                  {'book': book, 'delivery_type': delivery_type,
                   'bulb_coordinator': bulb_coordinator})

@login_required
def show_book(request, pk):
    book = get_object_or_404(Book, pk=pk, is_deleted=False)
    return render(request, "bulb/exchange/show_book.html",
                  {'book': book})

@decorators.ajax_only
@login_required
def add_book(request):
    if request.method == 'POST':
        current_year = StudentClubYear.objects.get_current()
        instance = Book(submitter=request.user,
                        year=current_year)
        form = BookForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            book = form.save()
            return {"message": "success"}
    elif request.method == 'GET':
        form = BookForm()

    context = {'form': form}
    return render(request, 'bulb/exchange/edit_book.html', context)

@decorators.ajax_only
@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if not utils.can_edit_book(request.user, book):
        raise PermissionDenied

    context = {'book': book}
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            return {"message": "success"}
    elif request.method == 'GET':
        form = BookForm(instance=book)

    context['form'] = form
    return render(request, 'bulb/exchange/edit_book.html', context)

@login_required
def requests_by_me(request):
    context = {}
    context['pending'] = Request.objects.filter(requester=request.user,
                                                requester_status='')
    context['canceled'] = Request.objects.filter(requester=request.user,
                                                 requester_status='C')
    context['rejected'] = Request.objects.filter(requester=request.user,
                                                 owner_status='C')
    context['failed'] = Request.objects.filter(requester=request.user,
                                               owner_status='F')
    context['done'] = Request.objects.filter(requester=request.user,
                                             requester_status='D')
    return render(request, 'bulb/exchange/requests_by_me.html', context)

@login_required
def my_books(request):
    return render(request, 'bulb/exchange/my_books.html')

@decorators.ajax_only
@decorators.post_only
@login_required
def pending_book(request):
    pk = request.POST.get('pk')
    book = get_object_or_404(Book, pk=pk)

    if not utils.can_edit_book(request.user, book):
        raise PermissionDenied

    return render(request, 'bulb/exchange/pending_book.html',
                  {'book': book})

@decorators.ajax_only
@login_required
def list_my_pending_books(request):
    done_pks = (Request.objects.filter(owner_status='D', requester_status='D') |\
                Request.objects.filter(owner_status='D', requester_status='') |\
                Request.objects.filter(owner_status='', requester_status='D'))\
                .values_list('book__pk', flat=True)
    books = Book.objects.current_year().exclude(pk__in=done_pks).filter(is_available=False, is_deleted=False).of_user(request.user).distinct()
    bulb_coordinator = utils.get_bulb_club_for_user(request.user).coordinator
    context =  {'books': books,
                'bulb_coordinator': bulb_coordinator}
    return render(request, 'bulb/exchange/list_my_pending_books.html', context)

@decorators.ajax_only
@decorators.post_only
@login_required
def pending_request(request):
    pk = request.POST.get('pk')
    book = get_object_or_404(Book, pk=pk)

    if not utils.can_edit_book(request.user, book):
        raise PermissionDenied

    return render(request, 'bulb/exchange/pending_book.html',
                  {'book': book, 'bulb_coordinator': bulb_coordinator})

@decorators.ajax_only
@login_required
def list_my_pending_requests(request):
    done_pks = (
        Request.objects.filter(requester=request.user,
                               owner_status='D',
                               requester_status='D') |\
        Request.objects.filter(requester=request.user,
                               owner_status='D',
                               requester_status='') |\
        Request.objects.filter(requester=request.user,
                               owner_status='',
                               requester_status='D')\
               ).values_list('book__pk', flat=True)
    books = Book.objects.current_year()\
                        .filter(is_available=False, is_deleted=False)\
                        .filter(request__requester=request.user)\
                        .exclude(pk__in=done_pks)\
                        .distinct()
    bulb_coordinator = utils.get_bulb_club_for_user(request.user).coordinator
    context =  {'books': books,
                'bulb_coordinator': bulb_coordinator}
    return render(request, 'bulb/exchange/list_my_pending_requests.html', context)

@login_required
def indicators(request):
    if not utils.is_bulb_coordinator_or_deputy(request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied

@decorators.ajax_only
@csrf.csrf_exempt
@login_required
def list_indirect_requests(request):
    if not utils.is_bulb_coordinator_or_deputy(request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied

    condition = request.POST.get('condition')
    bulb_club = utils.get_bulb_club_of_user(request.user)
    if condition == 'to_receive':
        # Get all requests that are:
        # * for indirect delivery,
        # * have not been acted upon for owner (i.e. not canceled nor given)
        # * have not been canceled nor received by requester.
        pks = Request.objects.filter(delivery='I',
                                     owner_status='',
                                     book__submitter__common_profile__college__gender=bulb_club.gender)\
                             .exclude(requester_status__in=['D', 'C'])\
                             .values_list('book__pk', flat=True)
        side = 'owner'
    elif condition == 'to_give':
        # Get all requests that are:
        # * for indirect delivery,
        # * have been received from owner,
        # * have not been acted upon for requester (i.e. not canceled nor received)
        pks = Request.objects.filter(delivery='I',
                                     owner_status='D',
                                     requester_status='',
                                     requester__common_profile__college__gender=bulb_club.gender)\
                             .values_list('book__pk', flat=True)
        side = 'requester'
    books = Book.objects.filter(pk__in=pks, is_deleted=False).distinct()

    context = {'books': books,
               'bulb_club': bulb_club,
               'side': side}

    return render(request, 'bulb/exchange/list_indirect_requests.html', context)

@login_required
def indirect_requests(request):
    if not utils.is_bulb_coordinator_or_deputy(request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied

    return render(request, 'bulb/exchange/indirect_requests.html')

@login_required
def disputed_requests(request):
    if not utils.is_bulb_coordinator_or_deputy(request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied

@login_required
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def control_book(request):
    action = request.POST.get('action')
    book_pk = request.POST.get('book_pk')
    book = get_object_or_404(Book, pk=book_pk)
    if action == 'delete':
        # TODO: Notify pending requests.
        pass
    return {"message": "success"}

@login_required
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def control_request(request):
    action = request.POST.get('action')
    request_pk = request.POST.get('pk')
    book_request = get_object_or_404(Request, pk=request_pk)
    book = book_request.book

    if action.startswith('owner_'):
        if not utils.can_edit_book(request.user, book):
            raise PermissionDenied
        if action == 'owner_done':
            book.is_available = False
            book.save()
            book_request.owner_status = 'D'
            book_request.owner_status_date = timezone.now()
            book_request.save()

            # If no previous points have been created (i.e. by
            # requested confirmation), create one.
            request_points = Point.objects.filter(request=book_request,
                                                  user=book.submitter,
                                                  is_counted=True)
            if not request_points.exists():
                Point.objects.create(year=current_year,
                                     request=book_request,
                                     user=book.submitter,
                                     value=1)

        elif action == 'owner_failed':
            book.is_available = False
            book.save()
            book_request.owner_status = 'F'
            book_request.owner_status_date = timezone.now()
            book_request.save()
            requests_by_me_url = reverse('bulb:requests_by_me')
            full_url = request.build_absolute_uri(requests_by_me_url)
            email_context = {'book': book,
                             'book_request': book_request,
                             'full_url': full_url}
            mail.send([book_request.requester.email],
                       template="book_request_failed_to_requester",
                       context=email_context)

        elif action == 'owner_canceled':
            book.is_available = True
            book.save()
            book_request.owner_status = 'C'
            book_request.owner_status_date = timezone.now()
            # Return the poin to the requester
            book_request.cancel_related_user_point(book_request.requester)
            book_request.save()
            list_book_categories_url = reverse('bulb:list_book_categories')
            full_url = request.build_absolute_uri(list_book_categories_url)
            email_context = {'book': book,
                             'book_request': book_request,
                             'full_url': full_url}
            mail.send([book_request.requester.email],
                       template="book_request_canceled_to_requester",
                       context=email_context)
            # Also, email Bulb coordinator.
            if book_request.delivery == 'I':
                bulb_coordinator = utils.get_bulb_club_for_user(request.user).coordinator
                if bulb_coordinator:
                    email_context['bulb_coordinator'] = bulb_coordinator
                    mail.send([bulb_coordinator.email],
                              template="indirect_book_request_canceled_to_coordinator",
                              context=email_context)

    if action.startswith('requester_'):
        if not request.user == book_request.requester and \
           not request.user.is_superuser:
            raise PermissionDenied

        if action == 'requester_canceled':
            # You cannot delete a request after it has been approved
            # by both parties.
            if book_request.owner_status == 'D' or\
               book_request.requester_status == 'D':
                raise Exception(u'لا يمكنك إلغاء طلب منجز.')
            book.is_available = True
            book.save()
            book_request.owner_status = 'C'
            book_request.owner_status_date = timezone.now()
            book_request.cancel_related_user_point(request.user)
            book_request.save()

            email_context = {'book': book,
                             'book_request': book_request}
            mail.send([book_request.requester.email],
                       template="book_request_canceled_to_owner",
                       context=email_context)
            # Also, email Bulb coordinator.
            if book_request.delivery == 'I':
                bulb_coordinator = utils.get_bulb_club_for_user(request.user).coordinator
                if bulb_coordinator:
                    email_context['bulb_coordinator'] = bulb_coordinator
                    mail.send([bulb_coordinator.email],
                              template="indirect_book_request_canceled_to_coordinator",
                              context=email_context)
    return {"message": "success"}

@login_required
def student_report(request, username=None):
    if username and \
       not request.user.is_superuser and\
       not utils.is_bulb_coordinator_or_deputy(request.user):
        raise PermissionDenied

    if username:
        bulb_user = get_object_or_404(User, username=username)
    else:
        bulb_user = request.user

    return render(request, 'bulb/exchange/student_report.html',
                  {'bulb_user': bulb_user})
