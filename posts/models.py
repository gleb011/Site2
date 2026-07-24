from django.db import models
from users.models import User


class Tag(models.Model):
    title = models.CharField('Title', max_length=100)

    def __str__(self):
        return f'{self.id}_{self.title}'


class Post(models.Model):
    title = models.CharField(verbose_name='Title', max_length=150)
    description = models.TextField(verbose_name='Dedcription', max_length=500, blank=True, null=True)
    poster = models.ImageField('Poster', upload_to='blog/post/', blank=True, null=True)
    owner = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE)
    is_active = models.BooleanField('Is active', default=True) # бачить тільки адмін (імітація видалення поста)
    is_visible = models.BooleanField('Is visible', default=True) # бачить тільки власник
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date create')
    tag = models.ManyToManyField(Tag, verbose_name='Tag', blank=True, null=True)

    def __str__(self):
        return f'{self.id}_{self.title}_({self.owner})'


class Like(models.Model):
    owner = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date create')

    def __str__(self):
        return f'{self.id}_{self.owner.id}_likes_({self.post.id})'


class Review(models.Model):
    owner = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE)
    tread = models.ForeignKey('self', verbose_name='Tread', on_delete=models.CASCADE, related_name='rewiew_tread', blank=True, null=True)
    parent = models.ForeignKey('self', verbose_name='Parent', on_delete=models.CASCADE, related_name='parent_tread', blank=True, null=True)
    text = models.TextField(verbose_name='Dedcription', max_length=500)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date create')

    def __str__(self):
        return f'{self.id}_{self.owner.id}_review_({self.post.id})'


class Repost(models.Model):
    owner = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date create')
    
    def __str__(self):
        return f'{self.id}_{self.owner.id}_repost_({self.post.id})'


class ReviewsLike(models.Model):
    owner = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE)
    review = models.ForeignKey(Review, verbose_name='review', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date create')

    def __str__(self):
        return f'{self.id}_{self.owner.id}_likes_({self.review.id})'