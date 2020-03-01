from django.contrib import admin
from .models import Author, Category, Article, Comment
# Register your models here.

class AuthorModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__", "details"]
    class Meta:
        model = Author
admin.site.register(Author, AuthorModel)

class CategoryModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 10
    class Meta:
        model = Category
admin.site.register(Category, CategoryModel)

class ArticleModel(admin.ModelAdmin):
    list_display = ["__str__", "posted_on"]
    search_fields = ["__str__", "article_author", "category"]
    list_filter = ["posted_on", "category"]
    list_per_page = 10
    class Meta:
        model = Article
admin.site.register(Article, ArticleModel)

class CommentModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 10
    class Meta:
        model = Comment
admin.site.register(Comment, CommentModel)