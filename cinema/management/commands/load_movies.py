from django.core.management.base import BaseCommand
from cinema.models import Film
from datetime import datetime

class Command(BaseCommand):
    help = 'Load sample movies into database'

    def handle(self, *args, **options):
        movies = [
            {'tmdb_id': 550, 'title': 'Бойцовский клуб', 'genres': 'Драма, Триллер', 'release_date': '1999-10-15', 'rating': 8.8, 'poster': 'https://image.tmdb.org/t/p/w500/fCayJrkfRaCo5OnQuntVVcjMyT.jpg', 'description': 'Офисный работник находит утешение в подпольном боевом клубе.'},
            {'tmdb_id': 278, 'title': 'Побег из Шоушенка', 'genres': 'Драма', 'release_date': '1994-10-14', 'rating': 9.3, 'poster': 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmJy0nV6mv4MP4oR.jpg', 'description': 'Двое людей в долгосрочном заключении находят мир через письма и дружбу.'},
            {'tmdb_id': 238, 'title': 'Крёстный отец', 'genres': 'Криминал, Драма', 'release_date': '1972-03-24', 'rating': 9.2, 'poster': 'https://image.tmdb.org/t/p/w500/rPdtLWNsZmAtoZl9PK7S2wE3qiS.jpg', 'description': 'Агинг патриарх передает контроль над своей преступной империей сыну.'},
            {'tmdb_id': 240, 'title': 'Крёстный отец: Часть II', 'genres': 'Криминал, Драма', 'release_date': '1974-12-20', 'rating': 9.0, 'poster': 'https://image.tmdb.org/t/p/w500/hfoExvgyCTWYbFaxyLnVCQD5J0V.jpg', 'description': 'Параллельные истории о восхождении Вито Корлеоне и правлении его сына Майкла.'},
            {'tmdb_id': 424, 'title': 'Схема', 'genres': 'Криминал, Драма, Триллер', 'release_date': '1995-12-15', 'rating': 8.4, 'poster': 'https://image.tmdb.org/t/p/w500/eZAsPAiVGKM5sH0UwZW3yUB7rAr.jpg', 'description': 'Два убийцы и азартный игрок входят в плот деньгами после похищения.'},
            {'tmdb_id': 45325, 'title': 'Начало', 'genres': 'Научная фантастика, Триллер', 'release_date': '2010-07-16', 'rating': 8.8, 'poster': 'https://image.tmdb.org/t/p/w500/8ZTVqZf2tgclBv0KNRnQiGDRnzq.jpg', 'description': 'Вор, который крадет корпоративные секреты через технологию сновидений.'},
            {'tmdb_id': 680, 'title': 'Легенда о Геракле', 'genres': 'Боевик, Приключение, Фэнтези', 'release_date': '2014-07-25', 'rating': 6.5, 'poster': 'https://image.tmdb.org/t/p/w500/1W9EZ4ER9R9LdPy8z6z5l5WiKVF.jpg', 'description': 'Дважды рожденный герой принимает его судьбу и становится чемпионом.'},
            {'tmdb_id': 299536, 'title': 'Мстители: Война бесконечности', 'genres': 'Боевик, Приключение, Научная фантастика', 'release_date': '2018-04-27', 'rating': 8.3, 'poster': 'https://image.tmdb.org/t/p/w500/7WsyChQLEftFiDOVRVnzChridUe.jpg', 'description': 'Мстители должны остановить мощного врага от уничтожения вселенной.'},
            {'tmdb_id': 671, 'title': 'Гарри Поттер и философский камень', 'genres': 'Приключение, Фэнтези', 'release_date': '2001-11-04', 'rating': 7.6, 'poster': 'https://image.tmdb.org/t/p/w500/wqnLSKlZ23mo0ZjMeVbMGV9x6Bh.jpg', 'description': 'Молодой волшебник начинает свою магическую школьную карьеру.'},
            {'tmdb_id': 278870, 'title': 'Вторжение', 'genres': 'Ужас, Триллер, Научная фантастика', 'release_date': '2019-06-28', 'rating': 5.9, 'poster': 'https://image.tmdb.org/t/p/w500/87G5BIZx0LJ6Vqh0C9gS8VGfVaR.jpg', 'description': 'Преступники-одиночки вынуждены работать вместе в экстремальном выживании.'},
            {'tmdb_id': 10957, 'title': 'M*A*S*H', 'genres': 'Комедия, Драма, Война', 'release_date': '1970-01-25', 'rating': 7.6, 'poster': 'https://image.tmdb.org/t/p/w500/vI8nYghE3VsVk6kxKdS9i9EuMBj.jpg', 'description': 'История хирургического мобильного госпиталя во время Корейской войны.'},
            {'tmdb_id': 278, 'title': 'Матрица', 'genres': 'Боевик, Научная фантастика', 'release_date': '1999-03-31', 'rating': 8.7, 'poster': 'https://image.tmdb.org/t/p/w500/vgpXmVaVyI5kgoKinsOMHjUGXJX.jpg', 'description': 'Компьютерный хакер узнает истинную природу реальности и роль его в войне.'},
        ]

        for movie in movies:
            Film.objects.get_or_create(
                tmdb_id=movie['tmdb_id'],
                defaults={
                    'title': movie['title'],
                    'genres': movie['genres'],
                    'release_date': movie['release_date'],
                    'rating': movie['rating'],
                    'poster_url': movie['poster'],
                    'description': movie['description'],
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'✅ Загружено {len(movies)} фильмов'))
