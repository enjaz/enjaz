# -*- coding: utf-8  -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.decorators import csrf
from django.utils import timezone
from post_office import mail


from accounts.utils import get_user_gender
from core.models import StudentClubYear
from core import decorators
from bulb.models import Category, Book, Request, Point, Group, Membership, Session, Report, ReaderProfile
from bulb.forms import BookGiveForm, BookLendForm, BookEditForm, RequestForm, GroupForm, SessionForm, ReportForm, ReaderProfileForm
from bulb import utils


@login_required
def index(request):
    groups = Group.objects.current_year().undeleted().order_by("?")[:6]
    sessions = Session.objects.current_year().undeleted()\
                              .filter(date__gte=timezone.now().date())\
                              .order_by("date")[:5]
    group_count = Group.objects.current_year().undeleted().count()
    group_user_count = (User.objects.filter(reading_group_memberships__isnull=False) | \
                        User.objects.filter(reading_group_coordination__isnull=False)).distinct().count()
    book_sample = Book.objects.current_year().available().order_by("?")[:6]
    latest_books = Book.objects.current_year().undeleted().order_by("-submission_date")[:6]
    book_count = Book.objects.current_year().undeleted().count()
    book_request_count = Request.objects.current_year().count()
    reader_profiles = ReaderProfile.objects.order_by("?")[:10]
    reader_profile_count = ReaderProfile.objects.count()
    context = {'groups': groups, 'group_count': group_count,
               'group_user_count': group_user_count,
               'sessions': sessions,
               'book_sample': book_sample, 'latest_books': latest_books,
               'book_count': book_count,
               'book_request_count': book_request_count,
               'reader_profiles': reader_profiles,
               'reader_profile_count': reader_profile_count}
    return render(request, "bulb/index.html", context)

@login_required
def list_book_categories(request):
    categories = Category.objects.distinct().filter(book__isnull=False,
                                                    book__is_available=True,
                                                    book__is_deleted=False)
    # If we have books, show the All category.
    if Book.objects.current_year().available().exists():
        categories |= Category.objects.filter(code_name="all").distinct()
    context = {'categories': categories}
    return render(request, "bulb/exchange/list_categories.html",
                  context)

@login_required
def books_by_date(request):
    books =  Book.objects.current_year().undeleted().order_by("-submission_date")
    return render(request, "bulb/exchange/books_by_date.html",
                  {'books': books})

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
        books = Book.objects.current_year().available()
        if category.code_name != 'all':
            books = books.filter(category=category)
    elif source == "user":
        condition = request.POST.get('condition')
        user = get_object_or_404(User, username=name)
        if condition == 'available':
            books = Book.objects.current_year().available().of_user(user)
        elif condition == 'borrowed':
            book_pks = Request.objects.filter(book__contribution='L', owner_status='D')\
                                      .values_list('book__pk', flat=True)
            books = Book.objects.current_year().filter(pk__in=book_pks, is_deleted=False).of_user(user).distinct()
        elif condition == 'done':
            book_pks = (Request.objects.filter(book__contribution="G",
                                          owner_status="D") | \
                        Request.objects.filter(book__contribution="L",
                                          owner_status="R"))\
                                       .values_list('book__pk', flat=True)
            books = Book.objects.current_year().filter(pk__in=book_pks, is_deleted=False).of_user(user).distinct()

    return render(request, "bulb/exchange/list_books.html",
                  {'books': books})

@decorators.ajax_only
@decorators.get_only
@login_required
def order_instructions(request, pk):
    book = get_object_or_404(Book, pk=pk, is_deleted=False)
    bulb_coordinator = utils.get_bulb_club_for_user(book.submitter).coordinator
    last_request = book.last_pending_request()
    
    if not (last_request and last_request.requester == request.user) and \
       not utils.can_order_book(request.user, book):
        raise PermissionDenied

    context = {'book': book, 'bulb_coordinator': bulb_coordinator}

    return render(request, "bulb/exchange/components/order_body.html",
                  context)

@decorators.ajax_only
@login_required
@csrf.csrf_exempt
def confirm_book_order(request, pk):
    book = get_object_or_404(Book, pk=pk, is_deleted=False)
    bulb_coordinator = utils.get_bulb_club_for_user(book.submitter).coordinator
    current_year = StudentClubYear.objects.get_current()
    instance = Request(requester=request.user, book=book)
    if request.method == 'POST':
        form = RequestForm(request.POST, instance=instance)
        # TODO: In case the user lost thier balance after this form
        # was shown, no error message will be shown.  Show it?
        if book.contribution == 'G':
            balance_test = request.user.book_points.count_total_giving
        elif book.contribution == 'L':
            balance_test = request.user.book_points.count_total_lending

        if form.is_valid() and balance_test():
            book_request = form.save()
            current_year = StudentClubYear.objects.get_current()
            Point.objects.create(year=current_year,
                                 category=book.contribution,
                                 request=book_request,
                                 user=request.user,
                                 value=-1)
            book.is_available = False
            book.save()
            email_context = {'book': book,
                             'book_request': book_request}
            my_books_url = reverse('bulb:my_books')
            my_books_full_url = request.build_absolute_uri(my_books_url)
            if book_request.delivery == 'I':
                owner_template = "book_requested_indirectly_to_owner"
                if bulb_coordinator:
                    indirect_requests_url = reverse('bulb:indirect_requests')
                    indirect_requests_full_url = request.build_absolute_uri(indirect_requests_url)
                    email_context['full_url'] = indirect_requests_full_url
                    email_context['bulb_coordinator'] = bulb_coordinator
                    cc = utils.get_indirect_request_cc(book)
                    mail.send([bulb_coordinator.email],
                              cc=cc,
                              template="book_requested_indirectly_to_coordinator",
                              context=email_context)
            elif book_request.delivery == 'D':
                owner_template = "book_requested_directly_to_owner"

            email_context['full_url'] = my_books_full_url
            mail.send([book.submitter.email],
                      template=owner_template,
                      context=email_context)
            requests_by_me_url = reverse('bulb:requests_by_me')
            full_url = request.build_absolute_uri(requests_by_me_url)
            return {"message": "success", "list_url": full_url}            

    elif request.method == 'GET':
        form = RequestForm(instance=instance)

    return render(request, "bulb/exchange/confirm_book_order.html",
                  {'book': book, 'form': form})

@login_required
def show_book(request, pk):
    book = get_object_or_404(Book, pk=pk, is_deleted=False)
    return render(request, "bulb/exchange/show_book.html",
                  {'book': book})

@decorators.ajax_only
@login_required
@decorators.get_only
def confirm_book_deletion(request, pk):
    book = get_object_or_404(Book, pk=pk, is_deleted=False)
    if not utils.can_edit_book(request.user, book):
        raise PermissionDenied

    return render(request, "bulb/exchange/confirm_book_deletion.html",
                  {'book': book})

@decorators.ajax_only
@decorators.post_only
@login_required
@csrf.csrf_exempt
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk, is_deleted=False)
    if not utils.can_edit_book(request.user, book):
        raise Exception(u"لا تستطيع حذف الكتاب")

    # Book owners cannot delete a book if it has any pending requests,
    # but superusers and Bulb coordinators can, and in that case,
    # notify the book owner, then check for pending requests notify
    # the requester accordingly.
    if request.user != book.submitter:
        pending_request = book.last_pending_request()
        bulb_coordinator = utils.get_bulb_club_for_user(book.submitter).coordinator
        if bulb_coordinator:
            cc_coordinator = [bulb_coordinator.email]
        else:
            cc_coordinator = []
        email_context = {'book': book,
                         'book_request': pending_request,
                         'bulb_coordinator': bulb_coordinator}
        mail.send([book.submitter.email],
                  cc=cc_coordinator,
                  template="book_deleted_to_owner",
                  context=email_context)
        if pending_request:
            pending_request.cancel_related_user_point(pending_request.requester)
            mail.send([pending_request.requester.email],
                      cc=cc_coordinator,
                      template="book_deleted_to_requester",
                      context=email_context)

    book.is_deleted = True
    book.save()
    show_category_url = reverse('bulb:show_category',
                                args=(book.category.code_name,))
    full_url = request.build_absolute_uri(show_category_url)
    return {"message": "success", "list_url": full_url}

@decorators.ajax_only
@login_required
def add_book(request, contribution):

    if contribution  == 'lend':
        BookForm = BookLendForm
        contribution = 'L'
    elif contribution  == 'give':
        BookForm = BookGiveForm
        contribution = 'G'

    if request.method == 'POST':
        current_year = StudentClubYear.objects.get_current()
        instance = Book(submitter=request.user,
                        year=current_year,
                        contribution=contribution)
        form = BookForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            book = form.save()
            show_book_url = reverse('bulb:show_book', args=(book.pk,))
            full_url = request.build_absolute_uri(show_book_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = BookForm()

    context = {'form': form}
    return render(request, 'bulb/exchange/edit_book_form.html', context)

@decorators.ajax_only
@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if not utils.can_edit_book(request.user, book):
        raise Exception(u"لا تستطيع تعديل الكتاب")

    context = {'book': book}
    if request.method == 'POST':
        form = BookEditForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            show_book_url = reverse('bulb:show_book', args=(book.pk,))
            full_url = request.build_absolute_uri(show_book_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = BookEditForm(instance=book)

    context['form'] = form
    return render(request, 'bulb/exchange/edit_book_form.html', context)

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
@csrf.csrf_exempt
def pending_book(request):
    pk = request.POST.get('pk')
    book_request = get_object_or_404(Request, pk=pk)

    if not utils.can_edit_book(request.user, book_request.book):
        raise PermissionDenied

    return render(request, 'bulb/exchange/pending_book.html',
                  {'book': book_request.book})

@decorators.ajax_only
@decorators.post_only
@login_required
@csrf.csrf_exempt
def pending_request(request):
    pk = request.POST.get('pk')
    book_request = get_object_or_404(Request, pk=pk)

    return render(request, 'bulb/exchange/pending_request.html',
                  {'book_request': book_request})

@decorators.ajax_only
@login_required
@csrf.csrf_exempt
def list_my_books(request):
    bulb_coordinator = utils.get_bulb_club_for_user(request.user).coordinator
    condition = request.POST.get('condition')
    if condition == 'pending':
        pks = Request.objects.filter(status="",
                                     owner_status__in=["", "F"])\
                          .values_list('book__pk', flat=True)
    elif condition == 'borrowed':
        pks = Request.objects.filter(status__in=["", "D"],
                                     book__contribution="L",
                                     owner_status="D")\
                          .values_list('book__pk', flat=True)
    elif condition == 'done':
        pks = (Request.objects.filter(book__contribution="G",
                                      owner_status="D") | \
               Request.objects.filter(book__contribution="L",
                                      owner_status="R"))\
                      .values_list('book__pk', flat=True)

    books = Book.objects.filter(pk__in=pks, is_deleted=False).of_user(request.user).distinct()

    context =  {'books': books,
                'bulb_coordinator': bulb_coordinator}
    return render(request, 'bulb/exchange/list_my_books.html', context)    


@decorators.ajax_only
@login_required
@csrf.csrf_exempt
def list_my_requests(request):
    bulb_coordinator = utils.get_bulb_club_for_user(request.user).coordinator
    condition = request.POST.get('condition')
    if condition == 'pending':
        requests = Request.objects.filter(requester=request.user,
                                          status="",
                                          requester_status__in=["", "F"])
    elif condition == 'borrowing':
        requests = Request.objects.filter(requester=request.user,
                                          book__contribution="L",
                                          status__in=["", "D"],
                                          requester_status="D")
    elif condition == 'done':
        requests = Request.objects.filter(requester=request.user,
                                          book__contribution="G",
                                          requester_status="D") | \
                   Request.objects.filter(requester=request.user,
                                          book__contribution="L",
                                          requester_status="R")

    context =  {'requests': requests,
                'bulb_coordinator': bulb_coordinator}
    return render(request, 'bulb/exchange/list_direct_requests.html', context)    

@login_required
def indicators(request):
    if not utils.is_bulb_coordinator_or_deputy(request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied

    books = Book.objects.current_year()
    book_requests = Request.objects.current_year()
    groups = Group.objects.current_year()
    sessions = Session.objects.current_year()
    users = (User.objects.filter(book_giveaways__isnull=False) |
             User.objects.filter(request__isnull=False) |
             User.objects.filter(reading_group_coordination__isnull=False) |
             User.objects.filter(reading_group_memberships__isnull=False) |
             User.objects.filter(reader_profile__isnull=False)
    ).filter(common_profile__is_student=True).distinct()
    book_users = User.objects.filter(common_profile__is_student=True,
                                     book_points__is_counted=True)\
                             .annotate(point_count=Count('book_points'))\
                             .filter(point_count__gte=3)
    book_contributing_male_users = User.objects.filter(common_profile__college__gender='M',
                                                       book_giveaways__isnull=False).distinct().count()
    book_contributing_female_users = User.objects.filter(common_profile__college__gender='F',
                                                         book_giveaways__isnull=False).distinct().count()
    group_male_users = (User.objects.filter(reading_group_memberships__isnull=False,
                                            common_profile__college__gender='M') | \
                        User.objects.filter(reading_group_coordination__isnull=False,
                                            common_profile__college__gender='M')).distinct().count()
    group_female_users = (User.objects.filter(reading_group_memberships__isnull=False,
                                              common_profile__college__gender='F') | \
                          User.objects.filter(reading_group_coordination__isnull=False,
                                              common_profile__college__gender='F')).distinct().count()

    context = {'groups': groups,
               'sessions': sessions,
               'books': books,
               'book_requests': book_requests,
               'book_users': book_users,
               'users': users,
               'book_contributing_male_users': book_contributing_male_users,
               'book_contributing_female_users': book_contributing_female_users,
               'group_male_users': group_male_users,
               'group_female_users': group_female_users}
    return render(request, 'bulb/indicators.html', context)

@decorators.ajax_only
@csrf.csrf_exempt
@login_required
def list_indirect_requests(request):
    if not utils.is_bulb_coordinator_or_deputy(request.user) and \
       not utils.is_bulb_member(request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied

    condition = request.POST.get('condition')
    bulb_club = utils.get_bulb_club_of_user(request.user)
    if condition == 'to_receive':
        # Get all requests that are:
        # * for indirect delivery,
        # * have not been acted upon for owner (i.e. not canceled nor given)
        # * have not been canceled nor received by requester.
        requests = Request.objects.filter(delivery='I',
                                          owner_status='',
                                          requester_status='',
                                          book__submitter__common_profile__college__gender=bulb_club.gender)
        side = 'owner'
    elif condition == 'to_give':
        # Get all requests that are:
        # * for indirect delivery,
        # * have been received from owner,
        # * have not been acted upon for requester (i.e. not canceled nor received)
        requests = Request.objects.filter(delivery='I',
                                          owner_status='D',
                                          requester_status='',
                                          requester__common_profile__college__gender=bulb_club.gender)
        side = 'requester'
    elif condition == 'to_return_to_owner':
        # Get all requesters that are:
        # * for indirect delivery,
        # * for lending,
        # * have been returned by the requester but not to the owner
        requests = Request.objects.filter(delivery='I',
                                          book__contribution='L',
                                          requester_status='R',
                                          owner_status='D',
                                          borrowing_end_date__lte=timezone.now(),
                                          book__submitter__common_profile__college__gender=bulb_club.gender)
        side = 'owner'
    elif condition == 'to_claim_from_requester':
        # Get all requesters that are:
        # * for indirect delivery,
        # * for lending,
        # * haven't been returned by the requesters,
        requests = Request.objects.filter(delivery='I',
                                          book__contribution='L',
                                          requester_status='D',
                                          borrowing_end_date__lte=timezone.now(),
                                          requester__common_profile__college__gender=bulb_club.gender)
        side = 'requester'
    elif condition == 'failed_requester':
        # Get all requesters that are:
        # * for indirect delivery,
        # * for lending,
        # * haven't been returned by the requesters,
        requests = Request.objects.filter(delivery='I',
                                          requester_status='F',
                                          requester__common_profile__college__gender=bulb_club.gender)
        side = 'requester'
    elif condition == 'failed_owner':
        requests = Request.objects.filter(delivery='I',
                                          owner_status='F',
                                          book__submitter__common_profile__college__gender=bulb_club.gender)
        side = 'owner'
    elif condition == 'done':
        # Get all requesters that are:
        # * for indirect delivery,
        # * either the requester's status is done and the requester's gender is the same as the bulb's,
        # * or the owner's status is done and the owner's gender is the same as bulb's.
        # * exclude requests that are supposed to be in the claim/return lists. 
        requests = Request.objects.filter(delivery='I',
                                          owner_status='D',
                                           book__submitter__common_profile__college__gender=bulb_club.gender)\
                                  .exclude(book__contribution='L',
                                           borrowing_end_date__lte=timezone.now()) | \
                   Request.objects.filter(delivery='I',
                                          requester_status='D',
                                          requester__common_profile__college__gender=bulb_club.gender)\
                                  .exclude(book__contribution='L',
                                           borrowing_end_date__lte=timezone.now()) | \
                   Request.objects.filter(delivery='I',
                                          book__contribution='L',
                                          status='R',
                                          requester__common_profile__college__gender=bulb_club.gender)

        side = None

    context = {'requests': requests,
               'bulb_club': bulb_club,
               'side': side}

    return render(request, 'bulb/exchange/list_indirect_requests.html', context)

@login_required
def indirect_requests(request):
    if not utils.is_bulb_coordinator_or_deputy(request.user) and \
       not utils.is_bulb_member(request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied

    return render(request, 'bulb/exchange/indirect_requests.html')

@login_required
def disputed_requests(request):
    if not utils.is_bulb_coordinator_or_deputy(request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied

@decorators.ajax_only
@decorators.post_only
@login_required
@csrf.csrf_exempt
def control_request(request):
    action = request.POST.get('action')
    request_pk = request.POST.get('pk')
    book_request = get_object_or_404(Request, pk=request_pk)
    book = book_request.book
    bulb_coordinator = utils.get_bulb_club_for_user(request.user).coordinator
    if bulb_coordinator:
        cc_coordinator = [bulb_coordinator.email]
    else:
        cc_coordinator = []
    email_context = {'book': book,
                     'book_request': book_request,
                     'bulb_coordinator': bulb_coordinator}

    if action.startswith('owner_'):
        if not utils.can_edit_owner_status(request.user, book):
            raise Exception(u"لا يمكنك اتخاذ إجراء باسم صاحب الكتاب.")
        previous_owner_status = book_request.owner_status
        if action == 'owner_done' and previous_owner_status != 'D':
            book.is_available = False
            book_request.owner_status = 'D'
            book_request.owner_status_date = timezone.now()

            # If the book requester had already confirmed the request,
            # consider the reuqest done.  Otherwise, keep it pending
            # (to be shown in the requester's pending requests list).
            # In that case, when seven days have passed since the
            # request was submitted, a cron job would mark it as done
            # (to be removed from the requester's pending requests
            # list).
            if book_request.requester_status == 'D':
                book_request.status = 'D'

            # If no previous points have been created (i.e. by
            # requester's confirmation), create one.
            book_request.create_related_points()

        elif action == 'owner_returned' and previous_owner_status != 'R':
            book.is_available = True
            book_request.owner_status = 'R'
            book_request.owner_status_date = timezone.now()
            # If the book requester had already confirmed returning
            # the book, consider the reuqest returned.  Otherwise,
            # keep it pending (to be shown in the requester's pending
            # requests list).  In that case, when seven days have
            # passed since the request was submitted, a cron job would
            # mark it as done (to be removed from the requester's
            # pending requests list).
            if book_request.requester_status == 'R':
                book_request.status = 'R'

        elif action == 'owner_failed' and previous_owner_status != 'F':
            book_request.owner_status = 'F'
            book_request.owner_status_date = timezone.now()

            requests_by_me_url = reverse('bulb:requests_by_me')
            full_url = request.build_absolute_uri(requests_by_me_url)
            email_context['full_url'] = full_url

            if book_request.delivery == 'I':
                # If Bulb coordinator failed to comminicate with the
                # owner, make the book available again and email both
                # the owner and the requester that the request has
                # been canceled.
                book.is_available = True
                book_request.status = 'C'
                # Return the point to the book requester
                book_request.cancel_related_user_point(book_request.requester)
                mail.send([book_request.requester.email],
                          cc=cc_coordinator,
                          template="indirect_book_request_failed_to_requester",
                          context=email_context)
                mail.send([book.submitter.email],
                          cc=cc_coordinator,
                          template="indirect_book_request_failed_to_owner",
                          context=email_context)
            elif book_request.delivery == 'D':
                # Just to make sure
                book.is_available = False
                mail.send([book_request.requester.email],
                           template="book_request_failed_to_requester",
                           context=email_context)

        elif action == 'owner_canceled' and previous_owner_status != 'C':
            book.is_available = True
            book_request.owner_status = 'C'
            book_request.owner_status_date = timezone.now()

            # If one party canceled the request (in this case: the
            # book owner), and ther other hasn't confirmed it, that's
            # enough to consider the whole request canceled.
            # Otherwise, it will be handled in the conflicts section.
            if book_request.requester_status != 'D':
                book_request.status = 'C'

            # Return the point to the book requester
            book_request.cancel_related_user_point(book_request.requester)
            list_book_categories_url = reverse('bulb:list_book_categories')
            full_url = request.build_absolute_uri(list_book_categories_url)
            email_context['full_url'] = full_url
            mail.send([book_request.requester.email],
                      cc=cc_coordinator,
                      template="book_request_canceled_to_requester",
                      context=email_context)
            # Also, email Bulb coordinator.
            if book_request.delivery == 'I' and bulb_coordinator:
                cc = utils.get_indirect_request_cc(book)
                mail.send([bulb_coordinator.email],
                          cc=cc,
                          template="indirect_book_request_canceled_to_coordinator",
                          context=email_context)
    elif action.startswith('requester_'):
        if not utils.can_edit_requester_status(request.user, book_request):
            raise Exception(u"لا يمكنك اتخاذ إجراء باسم مقدم الطلب.")

        previous_requester_status = book_request.requester_status
        if action == 'requester_done' and previous_requester_status != 'D':
            book.is_available = False
            book_request.requester_status = 'D'
            book_request.requester_status_date = timezone.now()

            # If the book owner had already confirmed the request,
            # consider the reuqest done.  Otherwise, keep it pending
            # (to be shown in the owner's pending books list).  In the
            # case, when seven days have passed since the request was
            # submitted, a cron job would mark it as done (to be
            # removed from the owner's pending book list).
            if book_request.owner_status == 'D':
                book_request.status = 'D'

            # If no previous points have been created (i.e. by
            # requester's confirmation), create one.
            book_request.create_related_points()

        elif action == 'requester_returned' and previous_requester_status != 'R':
            book.is_available = True
            book_request.requester_status = 'R'
            book_request.requester_status_date = timezone.now()
            # If the book requester had already confirmed returning
            # the book, consider the reuqest returned.  Otherwise,
            # keep it pending (to be shown in the requester's pending
            # requests list).  In that case, when seven days have
            # passed since the request was submitted, a cron job would
            # mark it as done (to be removed from the requester's
            # pending requests list).
            if book_request.owner_status == 'R':
                book_request.status = 'R'

        elif action == 'requester_failed' and previous_requester_status != 'F':
            book_request.requester_status = 'F'
            book_request.requester_status_date = timezone.now()

            my_books_url = reverse('bulb:my_books')
            full_url = request.build_absolute_uri(my_books_url)
            email_context['full_url'] = full_url

            if book_request.delivery == 'I':
                # If Bulb coordinator failed to comminicate with the
                # owner, make the book available again and email both
                # the owner and the requester that the request has
                # been canceled.
                book.is_available = True
                book_request.status = 'C'
                # Return the point to the book requester
                book_request.cancel_related_user_point(book.submitter)
                mail.send([book_request.requester.email],
                          cc=cc_coordinator,
                          template="indirect_book_request_failed_to_requester",
                          context=email_context)
                mail.send([book.submitter.email],
                          cc=cc_coordinator,
                          template="indirect_book_request_failed_to_owner",
                          context=email_context)
            elif book_request.delivery == 'D':
                # Just to make sure
                book.is_available = False
                mail.send([book.submitter.email],
                          cc=cc_coordinator,
                          template="book_request_failed_to_owner",
                          context=email_context)

        elif action == 'requester_canceled' and previous_requester_status != 'C':
            # You cannot delete a request after it has been approved
            # by the requester.
            if book_request.requester_status == 'D':
                raise Exception(u'لا يمكنك إلغاء طلب منجز.')

            book.is_available = True
            book_request.requester_status = 'C'
            book_request.requester_status_date = timezone.now()

            # If one party canceled the request (in this case: the
            # book requester), and ther other hasn't confirmed it,
            # that's enough to consider the whole request canceled.
            # Otherwise, it will be handled in the conflicts section.
            if book_request.owner_status != 'D':
                book_request.status = 'C'

            # Return the point to the book requester
            book_request.cancel_related_user_point(request.user)

            mail.send([book.submitter.email],
                      template="book_request_canceled_to_owner",
                      context=email_context)

            # Also, email Bulb coordinator.
            if book_request.delivery == 'I' and bulb_coordinator:
                cc = utils.get_indirect_request_cc(book)
                mail.send([bulb_coordinator.email],
                          cc=cc,
                          template="indirect_book_request_canceled_to_coordinator",
                          context=email_context)

    book.save()
    book_request.save()
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

@decorators.ajax_only
@decorators.post_only
@login_required
@csrf.csrf_exempt
def convert_balance(request):
    try:
        giving = int(request.POST.get('giving'))
    except ValueError:
        raise Exception(u"أدخل رقما!")

    if giving > request.user.book_points.count_total_giving():
        raise Exception(u"لا تستطيع تحويل أكثر مما تملك من رصيد اقتناء")

    # Start converting the last, counted, positive-one point.
    for giving_point in request.user.book_points.current_year().giving().counted().filter(value=1).order_by("-submission_date")[:giving]:
        giving_point.value = 2
        giving_point.category = 'L'
        giving_point.save()

    return {"message": "success",
            "total_lending": request.user.book_points.count_total_lending(),
            "total_giving": request.user.book_points.count_total_giving()}

# Reading Groups

@login_required
def list_groups(request):
    return render(request, 'bulb/groups/list_groups.html')

@decorators.ajax_only
@csrf.csrf_exempt
@login_required
def list_group_previews(request):
    groups = Group.objects.current_year().undeleted().for_user_city(request.user).order_by('?')
    return render(request, "bulb/groups/list_group_previews.html",
                  {'groups': groups})

@decorators.ajax_only
@login_required
def add_group(request):
    if request.method == 'POST':
        current_year = StudentClubYear.objects.get_current()
        instance = Group(coordinator=request.user,
                         year=current_year)
        form = GroupForm(request.POST, request.FILES, instance=instance, user=request.user)
        if form.is_valid():
            group = form.save()
            show_group_url = reverse('bulb:show_group', args=(group.pk,))
            full_url = request.build_absolute_uri(show_group_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = GroupForm(user=request.user)

    context = {'form': form}
    return render(request, 'bulb/groups/edit_group_form.html', context)

@decorators.ajax_only
@login_required
def edit_group(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk)

    if not utils.can_edit_group(request.user, group):
        raise Exception(u"لا تستطيع تعديل المجموعة")

    context = {'group': group}
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=group, user=request.user)
        if form.is_valid():
            group = form.save()
            show_group_url = reverse('bulb:show_group', args=(group.pk,))
            full_url = request.build_absolute_uri(show_group_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = GroupForm(instance=group, user=request.user)

    context['form'] = form
    return render(request, 'bulb/groups/edit_group_form.html', context)

@login_required
def show_group(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk, is_deleted=False)
    return render(request, "bulb/groups/show_group.html",
                  {'group': group})

@decorators.ajax_only
@decorators.post_only
@login_required
@csrf.csrf_exempt
def delete_group(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk, is_deleted=False)
    if not utils.can_edit_group(request.user, group):
        raise Exception(u"لا تستطيع حذف المجموعة")    

    group.is_deleted = True
    group.save()
    list_groups_url = reverse('bulb:list_groups')
    full_url = request.build_absolute_uri(list_groups_url)
    return {"message": "success", "list_url": full_url}

@login_required
def list_memberships(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk, is_deleted=False)

    if not utils.can_edit_group(request.user, group):
        raise PermissionDenied

    return render(request, "bulb/groups/list_memberships.html",
                  {'group': group})

@decorators.ajax_only
@login_required
def add_session(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk, is_deleted=False)
    if not utils.can_edit_group(request.user, group):
        raise Exception(u"لا تستطيع تعديل المجموعة")    

    if request.method == 'POST':
        instance = Session(group=group)
        form = SessionForm(request.POST, instance=instance)
        if form.is_valid():
            session = form.save()
            show_group_url = reverse('bulb:show_group', args=(group.pk,))
            full_url = request.build_absolute_uri(show_group_url)
            email_context = {'session': session, 'full_url': full_url}
            # If the coordinator is not already a group member, email
            # them as well.
            bulb_coordinator = utils.get_bulb_club_for_user(session.group.coordinator).coordinator
            for membership in group.membership_set.filter(is_active=True):
                # Bulb coordinator will be handled later.
                if bulb_coordinator == membership.user:
                    continue
                email_context['member'] = membership.user
                mail.send([membership.user.email],
                           template="reading_group_session_just_submitted",
                           context=email_context)

            # Notify Bulb coordinator and their deputies.
            email_context['member'] = bulb_coordinator
            cc = utils.get_session_submitted_cc(group)
            mail.send([bulb_coordinator.email],
                      cc=cc,
                      template="reading_group_session_just_submitted",
                      context=email_context)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = SessionForm()

    context = {'form': form, 'group': group}
    return render(request, 'bulb/groups/edit_session_form.html', context)

@decorators.ajax_only
@login_required
def edit_session(request, group_pk, session_pk):
    group = get_object_or_404(Group, pk=group_pk, is_deleted=False)
    session = get_object_or_404(Session, pk=session_pk,
                                is_deleted=False, group__pk=group_pk)
    if not utils.can_edit_group(request.user, session.group):
        raise Exception(u"لا تستطيع تعديل المجموعة")

    response = {"message": "success"}
    context = {'session': session, 'group': group}

    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            session = form.save()
            show_group_url = reverse('bulb:show_group', args=(group.pk,))
            full_url = request.build_absolute_uri(show_group_url)
            response['show_url'] = full_url
            return response
    elif request.method == 'GET':
        form = SessionForm(instance=session)

    context['form'] = form
    return render(request, 'bulb/groups/edit_session_form.html', context)

@decorators.ajax_only
@decorators.post_only
@login_required
@csrf.csrf_exempt
def delete_session(request, group_pk, session_pk):
    session = get_object_or_404(Session, pk=session_pk,
                                is_deleted=False, group__pk=group_pk,
                                group__is_deleted=False)
    if not utils.can_edit_group(request.user, session.group):
        raise Exception(u"لا تستطيع حذف المجموعة")    

    session.is_deleted = True
    session.save()

    show_group_url = reverse('bulb:show_group', args=(session.group.pk,))
    full_url = request.build_absolute_uri(show_group_url)

    return {"message": "success", "show_url": full_url}

def show_report(request, group_pk, session_pk):
    report = get_object_or_404(Report, session__group__pk=group_pk,
                               session__pk=session_pk)
    return render(request, "bulb/groups/show_report.html",
                  {'report': report})

@decorators.ajax_only
@login_required
def add_report(request, group_pk, session_pk):
    session = get_object_or_404(Session, pk=session_pk,
                                group__pk=group_pk,
                                group__is_deleted=False)

    if not utils.can_edit_group(request.user, session.group):
        raise Exception(u"لا تستطيع تعديل المجموعة")

    response = {"message": "success"}

    if request.method == 'POST':
        instance = Report(session=session)
        form = ReportForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            report = form.save()
            show_report_url = reverse('bulb:show_report', args=(session.group.pk, session.pk))
            full_url = request.build_absolute_uri(show_report_url)
            response['show_url'] = full_url
            return response
    elif request.method == 'GET':
        form = ReportForm()

    context = {'form': form, 'session': session}
    return render(request, 'bulb/groups/edit_report_form.html', context)

@decorators.ajax_only
@login_required
def edit_report(request, group_pk, session_pk):
    report = get_object_or_404(Report, session__pk=session_pk,
                               session__group__pk=group_pk,
                               session__group__is_deleted=False)
    if not utils.can_edit_group(request.user, report.session.group):
        raise Exception(u"لا تستطيع تعديل المجموعة")

    response = {"message": "success"}
    context = {'report': report}
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            report = form.save()
            show_report_url = reverse('bulb:show_report', args=(report.session.group.pk,
                                                               report.session.pk))
            full_url = request.build_absolute_uri(show_report_url)
            response['show_url'] = full_url
            return response
    elif request.method == 'GET':
        form = ReportForm(instance=report)

    context['form'] = form
    return render(request, 'bulb/groups/edit_report_form.html', context)

@decorators.ajax_only
@decorators.post_only
@login_required
@csrf.csrf_exempt
def control_membership(request):
    action = request.POST.get('action')
    group_pk = request.POST.get('group_pk')
    group = get_object_or_404(Group, pk=group_pk)
    user_pk = request.POST.get('user_pk')
    if user_pk:
        user = get_object_or_404(User, pk=user_pk)

    response = {"message": "success"}

    if action == 'deactivate':
        if not utils.can_edit_group(request.user, group):
            raise Exception("You cannot deactivate users.")
        Membership.objects.filter(group=group, user=user).update(is_active=False)
    elif action == 'activate':
        if not utils.can_edit_group(request.user, group):
            raise Exception("You cannot activate users.")
        Membership.objects.filter(group=group, user=user).update(is_active=True)
    elif action == 'join':
        # Make sure that the user can indeed be added to the group
        if not utils.can_join_group(request.user, group):
            raise Exception(u"لا تستطيع الانضمام لهذه المجموعة.")
        Membership.objects.create(group=group, user=request.user)

        # Notify group coordinator
        list_memberships_url = reverse('bulb:list_memberships', args=(group.pk,))
        full_list_memberships_url = request.build_absolute_uri(list_memberships_url)
        email_context = {'member': request.user,
                         'group': group,
                         'full_url': full_list_memberships_url}
        mail.send([group.coordinator.email],
                   template="new_reading_group_member_to_group_coordinator",
                   context=email_context)

        show_group_url = reverse('bulb:show_group', args=(group.pk,))
        full_show_url = request.build_absolute_uri(show_group_url)
        response['show_url'] = full_show_url
    elif action == 'leave':
        # Make sure that the user can indeed be added to the group
        if not Membership.objects.filter(group=group, user=request.user).exists():
            raise Exception("لا تستطيع مغادرة هذه المجموعة.")
        Membership.objects.get(group=group, user=request.user).delete()
        show_group_url = reverse('bulb:show_group', args=(group.pk,))
        full_url = request.build_absolute_uri(show_group_url)
        response['show_url'] = full_url

    return response

@decorators.ajax_only
@login_required
@csrf.csrf_exempt
def new_member_introduction(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk)
    return render(request, 'bulb/groups/new_member_introduction.html',
                  {'group': group})

# Readers

@login_required
def list_reader_profiles(request):
    reader_profiles = ReaderProfile.objects.all()
    return render(request, 'bulb/readers/list_reader_profiles.html',
                  {'reader_profiles': reader_profiles})

@login_required
def show_reader_profile(request, reader_pk):
    reader_profile = get_object_or_404(ReaderProfile, pk=reader_pk)
    group_coordination = Group.objects.current_year().undeleted().filter(coordinator=reader_profile.user)
    group_membership_pks = Membership.objects.current_year().active().filter(user=reader_profile.user).values_list('group__pk', flat=True)
    group_memberships = Group.objects.current_year().undeleted().filter(pk__in=group_membership_pks)
    return render(request, 'bulb/readers/show_reader_profile.html',
                  {'reader_profile': reader_profile,
                   'group_coordination': group_coordination,
                   'group_memberships': group_memberships})

@decorators.ajax_only
@login_required
def add_reader_profile(request):
    if request.method == 'POST':
        instance = ReaderProfile(user=request.user)
        form = ReaderProfileForm(request.POST, instance=instance)
        if form.is_valid():
            reader_profile = form.save()
            show_reader_profile_url = reverse('bulb:show_reader_profile', args=(reader_profile.pk,))
            full_url = request.build_absolute_uri(show_reader_profile_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = ReaderProfileForm()

    context = {'form': form}
    return render(request, 'bulb/readers/edit_reader_profile_form.html', context)

@decorators.ajax_only
@login_required
def edit_reader_profile(request, reader_pk):
    reader_profile = get_object_or_404(ReaderProfile, pk=reader_pk)

    if not utils.can_edit_reader_profile(request.user, reader_profile):
        raise Exception(u"لا تستطيع تعديل المجموعة")

    context = {'reader_profile': reader_profile}
    if request.method == 'POST':
        form = ReaderProfileForm(request.POST, instance=reader_profile)
        if form.is_valid():
            form.save()
            show_reader_profile_url = reverse('bulb:show_reader_profile', args=(reader_profile.pk,))
            full_url = request.build_absolute_uri(show_reader_profile_url)
            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = ReaderProfileForm(instance=reader_profile)

    context['form'] = form
    return render(request, 'bulb/readers/edit_reader_profile_form.html', context)
