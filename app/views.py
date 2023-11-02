from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.
def index(req):
    films=Kino.objects.all()
    data = {'kino':films}
    return render(req,'index.html',data)

def film(req,id):
    film = Kino.objects.get(id=id)
    forma = CommentForm()
    commentsall = film.comment_set.filter(active=True)
    if req.POST:
        commentnew = Comment.objects.create()
        commentnew.name=req.POST.get('name')
        commentnew.body=req.POST.get('body')
        commentnew.kino=film
        commentnew.save()
        #функция для проверки
        mat = ['жопа','сука','хрен','дерьмо']
        for i in mat:
            if i in commentnew.body:
                commentnew.delete()
                messages.error(req, 'Ваш комментарий был удален из-за нарушения правил.', extra_tags='deleted')
                return redirect('film', id=id)
        commentnew.active=True
        commentnew.save()
        messages.error(req, 'Ваш комментарий добавлен', extra_tags='added')


    data = {'forma':forma,'commentsall':commentsall, 'kino':film}
    return render(req,'film.html',data)