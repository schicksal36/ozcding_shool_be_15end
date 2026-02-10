from typing import Self
import blog
from blog.forms import CommentForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.views.generic import (DeleteView, DetailView, ListView, CreateView, UpdateView)
from django.urls import reverse_lazy,reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Blog, Comment
from .forms import BlogForm, CommentForm


class BlogListView(ListView):
    #model = Blog
    queryset =Blog.objects.all().order_by() #정렬, ordering = ('-created_at') 이랑같은의미
    template_name = 'blog_list.html'
    paginate_by = 10
    #o0rdering = ('-created_at')역순정렬 

    def get_queryset(self):
        queryst = super().get_queryset()
        qwer = self.request.GET.get('qwer')
        if qwer:
            queryst = queryst.filter(

            Q(title__icontains=qwer) | 
            Q(content__icontains=qwer) | 
            Q(author__username__icontains=qwer)
            ) 
        return queryst

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    #queryset = Blog.objects.all().prefetch_related('comments','comments__author')
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Blog, pk=kwargs.get('blog_pk'))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
        #return super().get(request,*args,**kwargs)
    
    def get_queryset(self):  # ❌ get_queryst → ✅ get_queryset
        return self.model.objects.filter(
            blog=self.object
        ).prefetch_related('author')  # ❌ prefeth_related → ✅ prefetch_related

    #def get_queryset(self):
        #quseryset = super().get_queryset()
        #return querset,filter(id__lte=50)

    #def get_object(self, queryset=None):
        #object = super().get_object()
        #object = self.model.objects.get(pk=self.kwargs.get('pk'))
        #return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['blog'] = self.object
        return context
    
    #def post(self, request, *args, **kwargs):
        #self.object = self.get_object()

        #comment_form = CommentForm(request.POST)

        #if not comment_form.is_valid():
            #context = self.get_context_data()
            #context['comment_form'] = comment_form
            #return self.render_to_response(context)

        #if not self.request.user.is_authenticated:
            #raise Http404    
        
        #comment = comment_form.save(commit=False)
        #comment.blog_id = self.kwargs['pk']
        #comment.blog = self.object  
        #comment.blog = self.get.object    
        #comment.author = self.request.user
        #comment.save()

        #return HttpResponseRedirect(reverse_lazy('blog:detail', kwargs={'pk': self.kwargs['pk']}))



class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = "blog_form.html"
    #fields = ("category", "title", "content")
    form_class = BlogForm
    login_url = "/accounts/login/"


    def form_valid(self, form):
        form.instance.author = self.request.user  # ⭐ 핵심
        return super().form_valid(form)

    #def get_success_url(self):
        #return reverse_lazy("blog:detail",kwargs={"pk": self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '작성'
        context['btn_name'] = '생성'
        return context

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog_form.html'
    #fields = ('category', 'title', 'content')
    form_class = BlogForm 

    def get_queryset(self):
        queryset = super().get_queryset()

        # 관리자(superuser)는 모든 글 수정 가능
        if self.request.user.is_superuser:
            return queryset

        # 일반 유저는 자기 글만
        return queryset.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # ✅ 여기
        context['sub_title'] = '수정'
        context['btn_name'] = '수정'
        return context
    
    def form_valid(self, form): 
        print(form.cleaned_data)
        return super().form_valid(form) 



class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    def get_queryset(self):
        queryset = super().get_queryset()

        # 관리자(superuser)는 모든 글 삭제 가능
        if self.request.user.is_superuser:
            return queryset
        # 일반 유저는 자기 글만
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('blog:list')

    
    #def get_object(self, queryset=None):
        #self.object = super().get_object(queryset)
        #if self.object.author != self.request.user:
            #raise Http404
        #return self.object

    #def get_success_url(self):
        #return reverse_lazy('cb_blog_detail',kwargs={'pk': self.object.pk})
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm   # from_class ❌

    def form_valid(self, form):  # from_valid ❌
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.blog = self.get_blog()
        self.object.save()       # seve ❌
        return HttpResponseRedirect(
            reverse('blog:detail', kwargs={'blog_pk': self.object.blog.pk})
        )

    def get_blog(self):
        pk = self.kwargs['blog_pk']
        blog = get_object_or_404(Blog, pk=pk)
        return blog
 