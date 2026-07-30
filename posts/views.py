from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser
from django.views import View
from posts.models import Post, Like, Repost, Review
from users.models import User


class Post_base(View):
    '''
        Variable "template_name" is required
        - template_name = name of template curent page (from dir "templates" (ex: page_dir/page_name.html))
    '''
    anonimys = AnonymousUser()

    def get_user_data(self):
        if self.request.user == self.anonimys:
            return None
        user = self.request.user
        return user

    def get_data(self):
        context = {
            'user_data': self.get_user_data(),
        }
        return context

    def get(self, request):
        context = self.get_data()
        return render(request, self.template_name, context)


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
        return render(request, self.template_name, context)


class HomePage(Post_list_base):
    template_name = 'posts/home.html'
    page_title = 'Home page'

    def get_data(self):
        context = super().get_data()

        post_list = Post.objects.filter(is_active=True, is_visible=True).order_by('-date')

        context.update({
            'page_title': self.page_title,
            'post_list': post_list,
        })
        
        return context


class CreatePost(View):
    anonimys = AnonymousUser()
    template_name = 'posts/post_create.html'
    page_title = 'Creating post'

    def get_user_data(self):
        user = User.objects.filter(id=self.request.user.id).first()
        return user
    
    def get(self, request):
        context = {
            'page_title': self.page_title,
            'user_data': self.get_user_data(),
        }

        context = context
        return render(request, self.template_name, context)
    
    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        poster = request.POST.get('poster')

        if not title:
            context = {
                'page_title': self.page_title,
                'errors': 'Немає Title',
                'user_data': self.get_user_data(),
            }
            return render(request, self.template_name, context)

        if request.user == self.anonimys:
            context = {
                'page_title': self.page_title,
                'errors': 'Треба авторизація',
                'user_data': self.get_user_data(),
            }
            return render(request, self.template_name, context)

        post = Post.objects.create(
            title = title, 
            description = description,
            poster = poster,
            owner = request.user
        )

        return redirect('home_page')


class LikePost(View):
    def post(self, request):
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        owner = request.user

        likes = Like.objects.filter(post=post)

        if owner in [like.owner for like in likes]:
            obj = Like.objects.get(post=post, owner=owner)
            obj.delete()
        else:
            like = Like.objects.create(
                owner=owner,
                post=post
            )

        return redirect('home_page')


class RepostPost(View):
    def post(self, request):
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        owner = request.user


        reposts = Repost.objects.filter(post=post)

        if owner in [repost.owner for repost in reposts]:
            obj = Repost.objects.get(post=post, owner=owner)
            obj.delete()
        else:
            repost = Repost.objects.create(
                owner=owner,
                post=post
            )

        return redirect('home_page')
    

class PostDetail(View):
    anonimys = AnonymousUser()
    template_name = 'posts/post_detail.html'

    def get_user_data(self):
        user = User.objects.filter(id=self.request.user.id).first()
        return user

    def likes_count(self, post):
        likes_cont = Like.objects.filter(post=post)
        return len(likes_cont)
    
    def is_liked(self, post):
        if self.request.user == self.anonimys:
            return False
        return Like.objects.filter(post=post, owner=self.request.user).exists()
    
    def reviews_count(self, post):
        return Review.objects.filter(post=post).count()
    
    def reposts_count(self, post):
        return Repost.objects.filter(post=post).count()

    def is_reposted(self, post):
        if self.request.user == self.anonimys:
            return False
        return Repost.objects.filter(post=post, owner=self.request.user).exists()
        

    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        review_list = Review.objects.filter( post=post,).order_by('-date')

        page_title = post.title
        context = {
            'user_data': self.get_user_data(),
            'page_title': page_title,
            'post': {
                'post_info': post,
                'post_likes': {
                    'is_like': self.is_liked(post), 
                    'likes_count': self.likes_count(post),
                },
                'post_repost': { 
                    'is_repost': self.is_reposted(post),
                    'repost_count': self.reposts_count(post),
                },
                'post_reviews': {
                    'reviews_count': self.reviews_count(post),
                    'reviews_list': review_list,
                },
            },
        }

        context = context
        return render(request, self.template_name, context)
    

class ReviewPost(View):
    def post(self, request):
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        owner = request.user
        text = request.POST.get('text')
        print(f'Post ID: {post_id}, Owner: {owner}, Text: {text}')

        review = Review.objects.create(
            owner=owner,
            post=post,
            text=text,
        )

        return redirect('home_page')