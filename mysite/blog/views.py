from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Post, Comment
from django.core.paginator import Paginator
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForms
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector



def post_searh(request):
    form = SearchForms()
    query = None
    results = []
    if 


@never_cache
def post_share(request, post_id):
    post = get_object_or_404(Post, id = post_id, status = Post.Status.PUBLISHED)
    sent=False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} рекомендую прочитать " \
                      f"{post.title}"
            message = f"Прочитай {post.title} по ссылке {post_url}\n\n" \
                    f"{cd['name']} прокомментировал: {cd['comments']}"
            send_mail(subject, message, 'serikov.artur20@gmail.com',[cd['to']])
            sent=True
    else:
        form=EmailPostForm()
    return render(request, 'blog/post/share.html',{'post':post, 'form':form, 'sent':sent})


@never_cache
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id = post_id, status = Post.Status.PUBLISHED)
       # Получение поста по id и статусу PUBLISHED или возврат ошибки 404, если пост не найден
    comment = None
    form = CommentForm(data = request.POST)# Создание формы с данными из запроса POST
    if form.is_valid():

        comment = form.save(commit= False)# Создание объекта Comment без сохранения его в базе данных
        comment.post = post # Установка связи между комментарием и постом
        comment.active = True
        comment.save()# Сохранение комментария в базе данных
    
    # Рендеринг шаблона с контекстом, содержащим пост, форму и комментарий
    return render(request, "blog/post/comment.html", {'post':post, 'form':form, 'comment':comment})







class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'





@never_cache
def post_list(request, tag_slug = None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in = [tag])
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts, 'tag': tag})

@never_cache
def post_detail(request, id):
    try:
        post = Post.published.get(id = id) # Получаем пост с указанным id и статусом PUBLISHED.
        comments = post.comments.filter(active=True) # Фильтруем комментарии к посту, чтобы отображались только активные.
        form=CommentForm()
    except Post.DoesNotExist:
        raise Http404("No Post found")

    return render (request,
                   'blog/post/detail.html',
                  {'post': post,
                   'comments':comments,
                   'form':form})