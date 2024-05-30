from django.contrib import admin
from .models import Post

@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status"]
    search_fields = ["title"]
    list_filter = ['status', 'author']
    raw_id_fields = ["author"] # созданеи поиска по автору (окошко дополниельное )
    prepopulated_fields = {'slug':('title',)} # формированря слага через тайтл  




# Register your models here.
