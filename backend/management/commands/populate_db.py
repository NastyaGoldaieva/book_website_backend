from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from backend.models import Author, Publisher, Genre, Book, UserProfile
from decimal import Decimal
from datetime import date


class Command(BaseCommand):
    help = 'Populate database with sample book data'

    def handle(self, *args, **options):
        self.stdout.write('Populating database with sample data...')

        authors_data = [
            {
                'name': 'Джоан Роулінг',
                'biography': 'Британська письменниця, авторка серії романів про Гаррі Поттера.',
                'birth_date': date(1965, 7, 31)
            },
            {
                'name': 'Джордж Орвелл',
                'biography': 'Англійський письменник і журналіст, автор антиутопічного роману "1984".',
                'birth_date': date(1903, 6, 25)
            },
            {
                'name': 'Агата Крісті',
                'biography': 'Англійська письменниця, відома своїми детективними творами.',
                'birth_date': date(1890, 9, 15)
            },
            {
                'name': 'Стеніслав Лем',
                'biography': 'Польський філософ, футуролог і письменник-фантаст.',
                'birth_date': date(1921, 9, 12)
            },
            {
                'name': 'Ліна Костенко',
                'biography': 'Українська поетеса, письменниця, одна з найвідоміших представників шістдесятників.',
                'birth_date': date(1930, 3, 19)
            },
            {
                'name': 'Джон Толкін',
                'biography': 'Англійський письменник, поет, філолог, професор Оксфордського університету.',
                'birth_date': date(1892, 1, 3)
            }
        ]

        authors = {}
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                name=author_data['name'],
                defaults=author_data
            )
            authors[author_data['name']] = author
            self.stdout.write(f'Created author: {author.name}')

        publishers_data = [
            {
                'name': 'А-БА-БА-ГА-ЛА-МА-ГА',
                'description': 'Українське видавництво дитячої літератури, засноване у 1992 році.',
                'contact_info': 'Київ, вул. Хрещатик, 1\n+380 44 123 4567'
            },
            {
                'name': 'Видавництво Старого Лева',
                'description': 'Один з найбільших українських видавничих домів, заснований у 1994 році.',
                'contact_info': 'Львів, вул. Вірменська, 7\n+380 32 234 5678'
            },
            {
                'name': 'Наш Формат',
                'description': 'Українське видавництво, що спеціалізується на сучасній українській та перекладній літературі.',
                'contact_info': 'Київ, вул. Велика Васильківська, 72\n+380 44 345 6789'
            },
            {
                'name': 'КМ-Букс',
                'description': 'Видавництво, що спеціалізується на художній літературі та наукових виданнях.',
                'contact_info': 'Київ, вул. Б. Хмельницького, 42\n+380 44 456 7890'
            }
        ]

        publishers = {}
        for publisher_data in publishers_data:
            publisher, created = Publisher.objects.get_or_create(
                name=publisher_data['name'],
                defaults=publisher_data
            )
            publishers[publisher_data['name']] = publisher
            self.stdout.write(f'Created publisher: {publisher.name}')

        genres_data = [
            {'name': 'Фентезі', 'description': 'Жанр фантастичної літератури з елементами чарівності та міфології.'},
            {'name': 'Антиутопія', 'description': 'Жанр, що описує уявне суспільство з негативними рисами.'},
            {'name': 'Детектив', 'description': 'Жанр, що зосереджується на розслідуванні злочинів.'},
            {'name': 'Наукова фантастика', 'description': 'Жанр, що описує уявні технології та наукові відкриття.'},
            {'name': 'Поезія', 'description': 'Жанр літератури, що використовує ритм та образність мови.'},
            {'name': 'Роман', 'description': 'Велика прозова твір зі складною сюжетною лінією.'}
        ]

        genres = {}
        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(
                name=genre_data['name'],
                defaults=genre_data
            )
            genres[genre_data['name']] = genre
            self.stdout.write(f'Created genre: {genre.name}')

        books_data = [
            {
                'title': 'Гаррі Поттер і філософський камінь',
                'author': authors['Джоан Роулінг'],
                'publisher': publishers['А-БА-БА-ГА-ЛА-МА-ГА'],
                'genre': genres['Фентезі'],
                'description': 'Перша книга серії про Гаррі Поттера. Хлопчик-сирота дізнається, що він є волшебником і відправляється до школи чарівництва Хогвартс.',
                'price': Decimal('250.00'),
                'publication_date': date(1997, 6, 26),
                'isbn': '9786175853541',
                'stock': 15
            },
            {
                'title': 'Гаррі Поттер і тайна кімната',
                'author': authors['Джоан Роулінг'],
                'publisher': publishers['А-БА-БА-ГА-ЛА-МА-ГА'],
                'genre': genres['Фентезі'],
                'description': 'Друга книга серії. Гаррі повертається в Хогвартс на другий рік навчання, де відкривається таємна кімната.',
                'price': Decimal('260.00'),
                'publication_date': date(1998, 7, 2),
                'isbn': '9786175853558',
                'stock': 12
            },
            {
                'title': '1984',
                'author': authors['Джордж Орвелл'],
                'publisher': publishers['Видавництво Старого Лева'],
                'genre': genres['Антиутопія'],
                'description': 'Класична антиутопія про тоталітарне суспільство, де кожен крок людини знаходиться під наглядом Великого Брата.',
                'price': Decimal('180.00'),
                'publication_date': date(1949, 6, 8),
                'isbn': '9786176798322',
                'stock': 8
            },
            {
                'title': 'Ферма тварин',
                'author': authors['Джордж Орвелл'],
                'publisher': publishers['Видавництво Старого Лева'],
                'genre': genres['Антиутопія'],
                'description': 'Алегорія на радянську тоталітарну систему у вигляді історії про тварин, які повстали проти господарів.',
                'price': Decimal('160.00'),
                'publication_date': date(1945, 8, 17),
                'isbn': '9786176798339',
                'stock': 6
            },
            {
                'title': 'Убивство у "Східному експресі"',
                'author': authors['Агата Крісті'],
                'publisher': publishers['Наш Формат'],
                'genre': genres['Детектив'],
                'description': 'Знаменитий детектив Еркюль Пуаро розслідує вбивство, скоєне у поїзді "Східний експрес", що застряг у снігах.',
                'price': Decimal('190.00'),
                'publication_date': date(1934, 1, 1),
                'isbn': '9786177682057',
                'stock': 10
            },
            {
                'title': 'Соляріс',
                'author': authors['Стеніслав Лем'],
                'publisher': publishers['КМ-Букс'],
                'genre': genres['Наукова фантастика'],
                'description': 'Філософський роман про спроби контакту з розумним океаном на планеті Соляріс, який матеріалізує найглибші таємниці людей.',
                'price': Decimal('210.00'),
                'publication_date': date(1961, 1, 1),
                'isbn': '9789669483024',
                'stock': 5
            },
            {
                'title': 'Маруся Чурай',
                'author': authors['Ліна Костенко'],
                'publisher': publishers['Видавництво Старого Лева'],
                'genre': genres['Поезія'],
                'description': 'Історичний роман у віршах про трагічне життя української поетеси та співачки Марусі Чурай.',
                'price': Decimal('150.00'),
                'publication_date': date(1979, 1, 1),
                'isbn': '9786176798650',
                'stock': 12
            },
            {
                'title': 'Володар перснів: Хранителі Персня',
                'author': authors['Джон Толкін'],
                'publisher': publishers['А-БА-БА-ГА-ЛА-МА-ГА'],
                'genre': genres['Фентезі'],
                'description': 'Перша частина епічної трилогії про боротьбу за знищення Персня Всевладдя у вигаданому світі Середзем\'ї.',
                'price': Decimal('320.00'),
                'publication_date': date(1954, 7, 29),
                'isbn': '9786175853565',
                'stock': 7
            }
        ]

        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            if created:
                self.stdout.write(f'Created book: {book.title}')
            else:
                self.stdout.write(f'Book already exists: {book.title}')

        try:
            user, created = User.objects.get_or_create(
                username='testuser',
                defaults={
                    'email': 'test@example.com',
                    'first_name': 'Тест',
                    'last_name': 'Користувач'
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                UserProfile.objects.create(user=user, phone='+380501234567', address='Київ, вул. Тестова, 1')
                self.stdout.write('Created test user: testuser / testpass123')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not create test user: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))