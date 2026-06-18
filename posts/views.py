from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser
from django.views import View
from posts.models import Post
from users.models import User


class Post_list_base(View):
    anonimys = AnonymousUser()

    def redirect_to_login(self):
        if self.request.user == self.anonimys:
            return redirect('login')

    def get_user_data(self):
        user = User.objects.filter(id=self.request.user.id).first()
        return user
        

    def get_data(self):
        context = {
            'user_data': self.get_user_data(),
        }
        return context

    def get(self, request):
        self.redirect_to_login()
        context = self.get_data()
        print(context)
        return render(request, self.template_name, context)


class HomePage(Post_list_base):
    template_name = 'posts/home.html'
    page_title = 'Home'

    def get_data(self):
        context = super().get_data()

        post_list = Post.objects.filter(is_active=True, is_visible=True).order_by('-date')

        context.update({
            'page_title': self.page_title,
            'post_list': post_list,
        })
        
        return context
