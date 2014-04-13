# -*- coding: utf-8  -*-
import datetime
import urllib2
import json
import string

from django.conf import settings
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm, ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from books.models import Book, BookRequest

class BookForm(ModelForm):
    def clean(self):
        cleaned_data = super(BookForm, self).clean()
        if 'available_until' in cleaned_data and 'available_from' \
           in cleaned_data and cleaned_data['available_until']: # Not None
            if cleaned_data['available_from'] > cleaned_data['available_until']:
                msg = u'تاريخ انتهاء الإعارة بعد تاريخ بدئها!'
                # Add an error message to specific fields.
                self._errors["available_from"] = self.error_class([msg])
                self._errors["available_until"] = self.error_class([msg])
                # Remove invalid fields
                del cleaned_data["available_from"]
                del cleaned_data["available_until"]
        return cleaned_data

    class Meta:
        model = Book
        fields = ['isbn', 'title', 'contact', 'available_from',
                  'available_until', 'tags', 'description', 'pages',
                  'authors', 'publisher', 'year', 'edition',
                  'condition']

class BookRequestForm(ModelForm):
    def clean(self):
        cleaned_data = super(BookRequestForm, self).clean()
        if 'borrow_from' in cleaned_data and 'borrow_until' in cleaned_data:
            if cleaned_data['borrow_from'] > cleaned_data['borrow_until']:
                msg = u'تاريخ انتهاء الاستعارة بعد تاريخ بدئها!'
                self._errors["borrow_from"] = self.error_class([msg])
                self._errors["borrow_until"] = self.error_class([msg])
        return cleaned_data

    class Meta:
        model = BookRequest
        fields = ['borrow_from', 'borrow_until']

def get_gender(user):
    try:
        section = user.my_profile.college.section
    except (ObjectDoesNotExist, AttributeError):
        # If the user was auto-generated, it will raise this
        # error.  Let's assume the user is male.
        return 'M'
    if section in [u'M', u'KM']:
        return 'M'
    elif section in [u'F', u'KF']:
        return 'F'

def list_books(request):
    if request.user.has_perm('books.view_books'):
        books = Book.objects.all()
    else:
        # Normally, only currently available books should shown.
        today = datetime.date.today()
        if request.user.is_authenticated():
            # Additionally, if the user is logged in, they should see
            # the books they're holding and or contributing.
            user_books = Book.objects.filter(submitter=request.user) | \
                         Book.objects.filter(holder=request.user)
        else:
            user_books = Book.objects.none()

        available_books = Book.objects.filter(status='A',
                                              available_from__lte=today)
        available_books = available_books.exclude(available_until__lt=today)

        books = available_books | user_books

    filter_by = request.GET.get('filter')
    if filter_by == 'mine':
        if request.user.is_authenticated():
            books = books.filter(submitter=request.user)
    elif filter_by == "available":
        books = books.filter(status='A')

    order = request.GET.get('order')
    if order == 'status':
        sorted_books = books.order_by('-status')
    else:
        sorted_books = books.order_by('-submission_date')

    #Each page of results should have a maximum of 25 activities.
    paginator = Paginator(sorted_books, 25)
    page = request.GET.get('page')

    try:
        page_books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_books = paginator.page(paginator.num_pages)

    context = {'page_books': page_books}
    return render(request, 'books/list.html', context)

def show(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    today = datetime.date.today()
    # Since available_until can be None:
    if not book.available_until:
        is_still_available = True
    else:
        is_still_available = today <= book.available_until
    context = {'book': book}
    # Don't show the book unnless:
    # * The user is the original submitter,
    # * The user is the current holder,
    # * The user has the 'view_books' permission, or
    # * The book is available.
    if request.user in [book.submitter, book.holder] or request.user.has_perm('books.view_books'):
        context['extra'] = True
    elif is_still_available and today >= book.available_from and \
         book.status == 'A':
        pass
    else:
        raise PermissionDenied

    if request.user.is_authenticated():
        context['user_gender'] = get_gender(request.user)

    context['submitter_gender'] = get_gender(book.submitter)

    return render(request, 'books/show.html', context)

@permission_required('books.add_book', raise_exception=True)
def contribute(request):
    if request.method == 'POST' and 'is_isbn' in request.POST:
        errors = []
        if 'isbn' in request.POST:
            isbn = request.POST['isbn']
            # Remove any dashes, we only need numbers:
            isbn = isbn.replace('-', '')
            # Make sure that the user only posted numbers
            are_numbers = all([i in string.digits for i in isbn])
            if not are_numbers:
                errors.append('not_numbers')
            # Make sure that the ISBN is of a valid length:
            if not len(isbn) in [10, 13]:
                if 13 > len(isbn) > 10 or len(isbn) < 10:
                    errors.append('short_length')
                elif len(isbn) > 13:
                    errors.append('long_length')
            if errors:
                return render(request, 'books/submit_isbn.html',
                              {'errors': errors})

            google_url_query = 'https://www.googleapis.com/books/v1/volumes?key=%s&q=isbn:%s'

            book_query = urllib2.urlopen(google_url_query % (settings.GOOGLE_BOOKS_KEY, isbn)).read()
            book_details = json.loads(book_query)
            final_details = {}
            fields = ['title', 'publisher', 'description', 'authors',
                      'pageCount', 'categories', 'publishedDate']
            if book_details['totalItems'] == 1:
                for field in fields:
                    if field in book_details['items'][0]['volumeInfo']:
                        book_field = book_details['items'][0]['volumeInfo'][field]
                        if isinstance(book_field, list):
                            # For authors and categories
                            final_details[field] = ", ".join(book_field)
                        elif field == 'publishedDate':
                            try:
                                final_details[field] = datetime.datetime.strptime(book_field, '%Y-%m-%d').year
                            except ValueError:
                                #Sometimes, only the year is provided.
                                final_details[field] = datetime.datetime.strptime(book_field, '%Y').year
                        else:
                            final_details[field] = book_field
                    else:
                        if field == 'pageCount':
                            final_details[field] = None
                        else:
                            final_details[field] = ''
            elif book_details['totalItems'] == 0:
                errors.append('no_data')
            else: # If the results were more than one.
                print "Fix this!", isbn
                errors.append('too_many')
            if not errors:
                form = BookForm(instance=Book(isbn=isbn,
                                              title=final_details['title'],
                                              description=final_details['description'],
                                              publisher=final_details['publisher'],
                                              authors=final_details['authors'],
                                              pages=final_details['pageCount'],
                                              year=final_details['publishedDate'],
                                              available_from=datetime.date.today(),
                                              contact=request.user.email,))
                context = {'form': form}
                return render(request, 'books/edit.html', context)
        else:
            errors.append('no_isbn')
        return render(request, 'books/submit_isbn.html',
                              {'errors': errors})

    elif request.method == 'POST' and 'is_submit' in request.POST:
        avaliable_to = get_gender(request.user)            
        book = Book(submitter=request.user, avaliable_to=avaliable_to)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form_object = form.save()
            return HttpResponseRedirect(reverse('books:show', args=(form_object.pk,)))
        else:
            context = {'form': form}
            return render(request, 'books/edit.html', context)
    elif request.method == 'GET':
        return render(request, 'books/submit_isbn.html')

@permission_required('books.add_bookrequest', raise_exception=True)
def borrow(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    today = datetime.date.today()
    context = {'book': book}
    if request.method == 'POST':
        book_request = BookRequest(book=book, requester=request.user)
        form = BookRequestForm(request.POST, instance=book_request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('books:show', args=(book.pk,)))
        else:
            context['form'] = form
            return render(request, 'books/borrow.html', context)
    else:
        # Since available_until can be None:
        if not book.available_until:
            is_still_available = True
        else:
            is_still_available = today <= book.available_until

        # Check if there are pending requests
        if not book.status == 'A':
            # Check if the book is actually available (not held,
            # borrowed or expired).
            # TODO: Make it  possible to borrow a book  in the future,
            # after the book is returned.
            context['error'] = 'not_available'
        elif request.user == book.submitter:
            context['error'] = 'is_submitter'
        elif request.user == book.holder:
            context['error'] = 'is_holder'
        elif not is_still_available:
            context['error'] = 'expired'
        elif today < book.available_from:
            context['error'] = 'not_yet'

        # If the more serious errors arenot present, we can check for
        # warnings and prepare the form:
        if not 'error' in context:
            previous_requests = BookRequest.objects.filter(status='P')
            if previous_requests:
                context['warning'] = 'pending_requests'
            form = BookRequestForm()
            context['form'] = form

        return render(request, 'books/borrow.html', context)

@login_required
def review_requests(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        book_request = BookRequest.objects.get(pk=pk)
        if not book_request.book.submitter == request.user:
            raise PermissionDenied
        if request.POST['action'] == "approve":
            # TODO: Make sure that the book isn't already borrowed or
            # held!
            book_request.status = 'A'
            book = book_request.book
            book.status = 'H'
            book.save()
            book_request.save()
        elif request.POST['action'] == "reject":
            book_request.status = 'R'
            book_request.save()
        return HttpResponseRedirect(reverse('books:review_requests'))
    else:
        user_books = Book.objects.filter(submitter=request.user)
        context = {'books': user_books}
        return render(request, 'books/review_requests.html', context)

@login_required
def my_requests(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        book_request = BookRequest.objects.get(pk=pk)
        if not book_request.requester == request.user:
            raise PermissionDenied
        if request.POST['action'] == "withdraw" and book_request.status == 'P':
            book_request.status = 'W'
            book_request.save()
        elif request.POST['action'] == "confirm" and book_request.status == 'A':
            book = book_request.book
            book.status = 'B'
            book.save()
            # TODO: Send niqati
        else:
            context = {'error': True}
            return render(request, 'books/my_requests.html', context)
        return HttpResponseRedirect(reverse('books:my_requests'))
    else:
        book_requests = BookRequest.objects.filter(requester=request.user)
        context = {'book_requests': book_requests}
        return render(request, 'books/my_requests.html', context)

@login_required
def edit(request, book_id):
    pass

@login_required
def withdraw(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {'book': book}
    if request.method == 'POST':
        if not book.submitter == request.user and \
           not request.user.has_perm('books.delete_book'):
            raise PermissionDenied
        if book.status in [u'H', u'A'] and 'confirm' in request.POST:
            book.status = 'W'
            book.save()
            return HttpResponseRedirect(reverse('books:withdraw', args=(book_id,))+'?done=1')
            # TODO: Check if there any pending book requests and email
            # them accordingly.
        else:
            # If the book is already borrowed, the sumbitter shouldn't
            # be able to withdraw it until it is returned.
            context['error'] = True
    elif request.method == 'GET':
        if 'done' in request.GET:
            context['done'] = True

    return render(request, 'books/withdraw.html', context)
