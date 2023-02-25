from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, View
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from .models import Comment
from django.views.decorators.http import require_POST


# Create your views here.

class PostComment(View):
    template_name = 'blog/post/comment.html'
    http_method_names = ['post'] 
    
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED) 
        comment = None

        # A comment was posted
        form = CommentForm(data=request.POST)
        if form.is_valid():
            # Create a Comment object without saving it to the database 
            comment = form.save(commit=False)
            # Assign the post to the comment
            comment.post = post
            # Save the comment to the database
            comment.save()
        
        return render(request, self.template_name,
                            {'post': post,
                                'form': form,
                                'comment': comment})

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

class PostShare(View):
    template_name = "blog/post/share.html"

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        form = EmailPostForm()

        return render(request, self.template_name, {'post': post, 'form': form})

    def post(self, request, post_id):
        # Form was submitted
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        form = EmailPostForm(request.POST)
        sent = False
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read "\
                    f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
                                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, "isaacrobertoluwaseun@gmail.com", [cd['to']])

            sent = True

        return render(request, self.template_name, {'post': post, 'form': form, "sent": sent})


def post_list(request):
    published = Post.published.all()

    page_limit = request.GET.get("limit", 3)
    page_number = request.GET.get('page', 1)

    paginator = Paginator(published, page_limit)
    try:
        posts = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        posts = paginator.page(paginator.num_pages)
    
    return render(
        request,
        "blog/post/list.html",
        {"posts": posts}
    )

def post_detail(request, year, month, day, post):
    
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year, 
        publish__month=month, 
        publish__day=day
    )

    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "form": form, "comments": comments}
    )