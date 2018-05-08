from django.contrib import admin

# Register your models here.
from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'count_text']    # admin 페이지에 보여줄 column list
    list_display_links = ['title']    # title 을 link column으로...

    def count_text(self, post):
        return '{} 글자'.format(len(post.text))

    count_text.short_description = '내용 글자 수'

admin.site.register(Post, PostAdmin)

