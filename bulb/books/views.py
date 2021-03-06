# -*- coding: utf-8  -*-
import datetime
import urllib2
import json
import string
import re

from django.conf import settings
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm, ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.files.base import ContentFile

from taggit.models import Tag
from books.models import Book, BookRequest
from accounts.models import get_gender
from templated_email import send_templated_mail

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

    def clean_tags(self):
        """Make sure that only English tags are used."""
        # TODO: Do it on the client side as well by preventing Arabic
        # input to ths field.
        english_regex = re.compile(ur'\b[A-Za-z\']+\b', re.U)
        tags = self.cleaned_data['tags']
        for tag in tags:
            if not re.match(english_regex, tag):
                raise ValidationError(u'يجب أن تكون كل الوسوم إنجليزية')
        return tags

    class Meta:
        model = Book
        fields = ['isbn', 'title', 'contact', 'available_from',
                  'available_until', 'tags', 'description',
                  'cover_url', 'pages', 'authors', 'publisher',
                  'year', 'edition', 'condition']

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

# @login_required
def list_books(request):
    if not request.user.is_authenticated():
        template = 'front/front_base.html'
    else:
        template = 'books_base.html'
         
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

    context = {'template': template, 'page_books': books}
    return render(request, 'books/list.html', context)

@login_required
def show(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    previous_requests = BookRequest.objects.filter(book=book,
                                                  requester=request.user)
    today = datetime.date.today()
    # Since available_until can be None:
    if not book.available_until:
        is_still_available = True
    else:
        is_still_available = today <= book.available_until
    context = {'book': book, 'previous_requests': previous_requests}
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

@login_required
def contribute(request):
    if not request.user.has_perm('books.add_book'):
        raise PermissionDenied

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
                      'pageCount', 'categories', 'publishedDate',
                      'imageLinks']
            if book_details['totalItems'] >= 1:
                for field in fields:
                    if field in book_details['items'][0]['volumeInfo']:
                        book_field = book_details['items'][0]['volumeInfo'][field]
                        if isinstance(book_field, list):
                            # For authors and categories, we need a
                            # string.
                            final_details[field] = ", ".join(book_field)
                        elif field == 'publishedDate':
                            try:
                                final_details[field] = datetime.datetime.strptime(book_field, '%Y-%m-%d').year
                            except ValueError:
                                #Sometimes, only the year is provided.
                                final_details[field] = datetime.datetime.strptime(book_field, '%Y').year
                        elif field == 'imageLinks':
                            final_details[field] = book_field['thumbnail']
                        else:
                            final_details[field] = book_field
                    else:
                        if field == 'pageCount':
                            # Since the number of pages field does not
                            # accept strings, set it to NULL.
                            final_details[field] = None
                        else:
                            final_details[field] = ''
            elif book_details['totalItems'] == 0:
                errors.append('no_data')
            #else: # If the results were more than one.
            #    print "Fix this!", isbn
            #    errors.append('too_many')
            if not errors:
                form = BookForm(instance=Book(isbn=isbn,
                                              title=final_details['title'],
                                              description=final_details['description'],
                                              publisher=final_details['publisher'],
                                              authors=final_details['authors'],
                                              pages=final_details['pageCount'],
                                              year=final_details['publishedDate'],
                                              cover_url = final_details['imageLinks'],
                                              available_from=datetime.date.today(),
                                              contact=request.user.email,))
                context = {'form': form, 'tags': Tag.objects.all()}
                return render(request, 'books/edit.html', context)
        else:
            errors.append('no_isbn')
        return render(request, 'books/submit_isbn.html',
                              {'errors': errors})

    elif request.method == 'POST' and 'is_submit' in request.POST:
        available_to = get_gender(request.user)            
        book = Book(submitter=request.user, available_to=available_to)
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form_object = form.save()
            if form_object.cover_url:
                # TODO: If the cover was previously uploaded (i.e. a
                # previous book with the same ISBN), do not do it
                # again, but this would require more redesign
                opener = urllib2.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                cover_image = opener.open(form_object.cover_url)
                # Make sure we are actually fetching an image.
                if cover_image.headers.type.startswith('image'):
                    cover_object = ContentFile(cover_image.read())
                    form_object.cover.save(str(form_object.pk), cover_object)
                    form_object.save()
            return HttpResponseRedirect(reverse('books:show', args=(form_object.pk,)))
        else:
            context = {'form': form}
            return render(request, 'books/edit.html', context)
    elif request.method == 'GET':
        return render(request, 'books/submit_isbn.html')

@login_required
@permission_required('books.add_bookrequest', raise_exception=True)
def borrow(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    today = datetime.date.today()
    context = {'book': book}
    if request.method == 'POST':
        book_request = BookRequest(book=book, requester=request.user)
        form = BookRequestForm(request.POST, instance=book_request)
        if form.is_valid():
            request_object = form.save()
            review_url = request.build_absolute_uri(reverse('books:review_requests'))
            send_templated_mail(
                    template_name='book_requested',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[book.submitter.email],
                    context={
                        'book': book,
                        'book_request': book_request,
                        'review_url': review_url,
                        })
            return HttpResponseRedirect(reverse('books:my_requests'))
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
            #elif request.user == book.submitter:
            #    context['error'] = 'is_submitter'
        elif request.user == book.holder:
            context['error'] = 'is_holder'
        elif not is_still_available:
            context['error'] = 'expired'
        elif today < book.available_from:
            context['error'] = 'not_yet'
        elif book.available_to != get_gender(request.user):
            context['error'] = 'gender'

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
        book = book_request.book
        if not book_request.book.submitter == request.user:
            raise PermissionDenied

        if request.POST['action'] == "approve":
            # TODO: Make sure that the book isn't already borrowed or
            # held!
            request_url = request.build_absolute_uri(reverse('books:my_requests'))
            send_templated_mail(
                    template_name='request_approved',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[book_request.requester.email],
                    context={
                        'book': book,
                        'book_request': book_request,
                        'request_url': request_url,
                        })
            book_request.status = 'A'
            book.status = 'H'
            book.save()
            book_request.save()

        elif request.POST['action'] == "reject":
            book_request.status = 'R'
            book_request.save()
            search_url = request.build_absolute_uri(reverse('books:search')) + '?q=' + book.isbn
            send_templated_mail(
                    template_name='request_rejected',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[book_request.requester.email],
                    context={'book': book, 'book_request': book_request,
                             'search_url': search_url}
            )
        elif request.POST['action'] == "return":
            book.status = 'A'
            book_request.status = 'S'
            book.save()
            book_request.save()
            # TODO: Ask the submitter whether they want to keep the
            # book in the library or not.  For now, we will just keep
            # it.
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
        book = book_request.book
        if not book_request.requester == request.user:
            raise PermissionDenied
        if 'action' in request.POST:
            if request.POST['action'] == "withdraw" and \
               book_request.status == 'P':
                book_request.status = 'W'
                book_request.save()
            elif request.POST['action'] == "confirm" and \
                 book_request.status == 'A':
                book.status = 'B'
                book.save()
                # TODO: Send niqati
            elif request.POST['action'] == "return" and \
                 book_request.status == 'A':
                book.status = 'R'
                book.save()
                review_url = request.build_absolute_uri(reverse('books:review_requests'))
                send_templated_mail(
                        template_name='book_returned',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[book.submitter.email],
                        context={
                            'book': book,
                            'book_request': book_request,
                            'review_url': review_url,
                            })
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
    book = get_object_or_404(Book, pk=book_id)
    context = {'book': book, 'edit': True, 'tags': Tag.objects.all()}

    if not request.user == book.submitter and \
       not request.user.has_perm('books.change_book'):
        raise PermissionDenied

    if request.method == 'POST':
        modified_book = BookForm(request.POST, instance=book)
        if modified_book.is_valid():
            modified_book.save()
            return HttpResponseRedirect(reverse('books:show', args=(book_id,)))
        else:
            context['form'] = modified_book
    else:
        form = BookForm(instance=book)
        context['form'] = form
    return render(request, 'books/edit.html', context)

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

# TODO: remove this view and the associated url since searching is now done by datatables
#@login_required
def search(request):
    if request.user.is_authenticated():
        template = 'books_base.html'
    else:
        template = 'front/front_base.html'
        
    if request.method == 'GET':
        context = {'page_books': None}
        # Make sure that a query was submitted and that it isn't
        # empty.
        if 'q' in request.GET and request.GET['q']:
            context['q'] = request.GET['q']
            term = request.GET['q']
            additional_books = Book.objects.none()
            if request.user.has_perm('books.view_books'):
                # If the user has the right permissions, they should
                # be able to search all books.
                statuses = ['A', 'H', 'W', 'B', 'R']
            else:
                statuses = ['A']
                if request.user.is_authenticated():
                    # Allow the user to search all the books that he
                    # submitted or borrowed.
                    additional_books = Book.objects.filter(submitter=request.user) | \
                                       Book.objects.filter(holder=request.user)

            title_search = Book.objects.filter(title__contains=term, status__in=statuses) | additional_books.filter(title__contains=term)
            isbn_search = Book.objects.filter(isbn__contains=term, status__in=statuses) | additional_books.filter(isbn__contains=term)

            resulted_books = title_search | isbn_search
            resulted_books = resulted_books.order_by('submission_date')

            context['total_results'] = len(resulted_books)

            # Each page of results should have a maximum of 25
            # activities.
            paginator = Paginator(resulted_books, 25)
            page = request.GET.get('page')

            try:
                page_books = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                page_books = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                page_books = paginator.page(paginator.num_pages)
            context['page_books'] = page_books
        
        context['template'] = template
        return render(request, 'books/search.html', context)
