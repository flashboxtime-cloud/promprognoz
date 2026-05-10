from typing import Required
from django.urls import path, include
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Post, Comment, PostView
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = Post.objects.filter(is_published = True)

    html_content = "<h1>Список опубликованных постов</h1>"
    html_content += "<ul>"

    if not posts:
        html_content += "<li>Нет опубликованных постов</li>"
    else:
        for post in posts:
            
            html_content += f"<a href = '{post.id}/'><li><strong>Автор: {post.author.username}</strong> Лайки: {post.total_likes()}</li></a>"
    
    html_content += "</ul>"

    return HttpResponse(html_content)

def post_detail(request, post_id):

    post = get_object_or_404(Post, pk = post_id, is_published = True)

    already_viewed = get_object_or_404(Post, pk = post_id, is_published = True)

    if not already_viewed:
        PostView.objects.create(post=post, _user=request.user)

    html_content = f"<h1>{post.title}</h1>"
    html_content += f"<p><strong>Автор:</strong> {post.author.username}</p>"
    html_content += f"<p><strong>Опубликовано:</strong> {post.created_at.strftime('%d.%m.%Y %H:%M')}</p>"
    html_content += f"<p><strong> Лайки: </strong> {post.total_likes()}</p>"
    html_content += "<hr>"
    like_url = reverse('posts:add_like', args=[post_id])


    html_content += f"<p>{post.content}</p>"
    html_content += f"<a href='{like_url}'><p>❤️ Поставить лайк</p></a>"
    comments = post.comments.all()
    comment_url = reverse('posts:add_comment', args=[post.id])

    html_content += "<hr>"
    html_content += "<h3>Комментарии</h3>"

    # Форма добавления комментария
    html_content += f"""
    <form method="post" action="{comment_url}">
        <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', '')}">
        <textarea name="text" rows="4" cols="50" placeholder="Введите комментарий"></textarea><br>
        <button type="submit">Отправить</button>
    </form>
    """

    # Список комментариев
    if not comments:
        html_content += "<p>Комментариев пока нет.</p>"
    else:
        for comment in comments:
            html_content += (
                f"<p><strong>{comment.author.username}</strong>: "
                f"{comment.text}</p>"
            )

    menu_url = reverse('posts:post_list')

    html_content += f"<a href='{menu_url}'><p>Главное меню</p></a>"

    html_content += f"<p><strong>Просмотры:</strong> {post.views.count()}</p>"

    return HttpResponse(html_content)

#@login_required
def add_like(request, post_id):
    post = get_object_or_404(Post, pk = post_id, is_published = True)

    post.likes.add(request.user)

    return HttpResponseRedirect(reverse('posts:post_detail', args =[post_id]))

#@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk = post_id, is_published = True)

    if request.method == "POST":
        text = request.POST.get("text")
        
        if text:
            Comment.objects.create(
                post = post,
                author = request.user,
                text = text
            )

    return HttpResponseRedirect(reverse('posts:post_detail', args = [post_id]))