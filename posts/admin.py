from django.contrib import admin
from posts.models import Post, Tag, Like, Review, Repost, ReviewsLike

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'is_active', 'is_visible', 'date')
    search_fields = ('id', 'title', 'owner__username')
    list_filter = ('is_active', 'is_visible', 'date')
    list_editable = ('is_active', 'is_visible')
    ordering = ('-date',)
    list_per_page = 25

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'post', 'date')
    search_fields = ('owner__username', 'text')
    list_filter = ('date',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'post', 'date')
    list_filter = ('date',)

@admin.register(Repost)
class RepostAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'post', 'date')
    list_filter = ('date',)

@admin.register(ReviewsLike)
class ReviewsLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'review', 'date')
    list_filter = ('date',)
