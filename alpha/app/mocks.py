from django.http import Http404


class Post():
    POSTS = [
        {'id': 1, 'title': 'First post', 'body': 'This is my first  post'},
        {'id': 2, 'title': 'Second post', 'body': 'This is my first  post'},
        {'id': 3, 'title': 'Third post', 'body': 'This is my first  post'},
        {'id': 4, 'title': 'Fourth post', 'body': 'This is my first  post'},
    ]

    @classmethod
    def all(cls):
        return cls.POSTS

    @classmethod
    def find(cls,id):
        try:
            return  cls.POSTS[int(id)-1]
        except:
            raise Http404('Sorry , post #{} not found '.format(id))
