from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.views.generic import DeleteView, DetailView, ListView,CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q, QuerySet
from .models import Blog


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

    #def get_queryset(self):
        #quseryset = super().get_queryset()
        #return querset,filter(id__lte=50)

    #def get_object(self, queryset=None):
        #object = super().get_object()
        #object = self.model.objects.get(pk=self.kwargs.get('pk'))
        #return object
    #def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        #context['test'] = 'CBV'
        #return context


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = "blog_create.html"
    fields = ("category", "title", "content")
    login_url = "/accounts/login/"

    def form_valid(self, form):
        form.instance.author = self.request.user  # ⭐ 핵심
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blog:detail",kwargs={"pk": self.object.pk})

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



class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog_update.html'
    fields = ('category', 'title', 'content')

    def get_queryset(self):
        queryset = super().get_queryset()

        # 관리자(superuser)는 모든 글 수정 가능
        if self.request.user.is_superuser:
            return queryset

        # 일반 유저는 자기 글만
        return queryset.filter(author=self.request.user)



