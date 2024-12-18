from .models import Book, Author, BookInstance, Genre

# Функция отображения для домашней страницы сайта.
def index(request):

    # Генерация "количеств" некоторых главных объектов:
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.
    num_books_word=Book.objects.filter(title__icontains='дети').count()
    num_genres=Genre.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными внутри переменной контекста context:
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors, 'num_genres':num_genres, 'num_books_word':num_books_word, 'num_visits':num_visits},
    )


from django.views import generic
class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'
    context_object_name = 'author'


from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm, CustomAuthenticationForm
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Хранение пароля в зашифрованном виде
            user.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('EA:index')
        else:
            print(form.errors)  # Вывод ошибок формы для отладки
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


from .forms import SearchForm
def search(request):
    form = SearchForm()
    results = []

    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        results = (Book.objects.filter(title__icontains=query) | Book.objects.filter(author__first_name__icontains=query) | Book.objects.filter(author__last_name__icontains=query) | Book.objects.filter(genre__name__icontains=query))


    return render(request, 'search.html', {'form': form, 'results': results})


def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('EA:index')
            else:
                form.add_error(None, 'Неверный логин или пароль.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

from django.contrib.auth import login, authenticate, logout
def logout_user(request):
    logout(request)
    return render(request,'registration/logged_out.html')


# API-эндпоинты(конечные точки веб-сервиса, к которой клиентское приложение обращается для выполнения определённых операций или получения данных.):
from rest_framework import generics
from .serializers import BookSerializer, AuthorSerializer

class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorListAPIView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorDetailAPIView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


from rest_framework.permissions import IsAdminUser
class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # permission_classes = [IsAdminUser]


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title', None)
        genre = self.request.query_params.get('genre', None)
        author = self.request.query_params.get('author', None)

        if title:
            queryset = queryset.filter(title__icontains=title)
        if genre:
            queryset = queryset.filter(genre__name__icontains=genre)
        if author:
            queryset = queryset.filter(author__first_name__icontains=author) | queryset.filter(author__last_name__icontains=author)

        return queryset


class BookSearchAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title', None)
        genre = self.request.query_params.get('genre', None)
        author = self.request.query_params.get('author', None)

        if title:
            queryset = queryset.filter(title__icontains=title)
        if genre:
            queryset = queryset.filter(genre__name__icontains=genre)
        if author:
            queryset = queryset.filter(author__first_name__icontains=author) | queryset.filter(
                author__last_name__icontains=author)

        return queryset