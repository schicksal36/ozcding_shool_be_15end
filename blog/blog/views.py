# ==================== 상세 주석 및 코드 설명 ====================
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from blog.forms import BlogForm
from .models import Blog

def blog_list(request):
    blogs = Blog.objects.all().order_by("created_at")
    qwer = request.GET.get("qwer")
    if qwer:
        blogs = blogs.filter(
            Q(title__icontains=qwer) |
            Q(content__icontains=qwer) |
            Q(author__username__icontains=qwer)
        )
    paginator = Paginator(blogs, 10)
    page = request.GET.get("page")
    page_object = paginator.get_page(page)
    context = {
        "object_list": page_object.object_list,
        "page_object": page_object,
    }
    return render(request, "blog_list.html", context)

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {
        "test": "TEST",
        "blog": blog,
    }
    return render(request, "blog_detail.html", context)

@login_required()
def blog_create(request):
    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return redirect(reverse("blog_detail", kwargs={"blog_pk": blog.pk}))
    context = {
        "form": form,
    }
    return render(request, "blog_form.html", context)

@login_required()
def blog_update(request, pk):
    if request.user.is_superuser:
        blog = get_object_or_404(Blog, pk=pk)
    else:
        blog = get_object_or_404(Blog, pk=pk, author=request.user)

    form = BlogForm(
        request.POST or None,
        request.FILES or None,
        instance=blog
    )

    if form.is_valid():
        blog = form.save()
        return redirect(reverse("blog:detail", kwargs={"blog_pk": blog.pk}))

    return render(request, "blog_form.html", {
        "blog": blog,
        "form": form,
    })

@login_required()
@require_http_methods(["POST"])
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()
    return redirect(reverse("blog_list"))
