from django.contrib import admin
from django.forms import ModelForm
from django.utils.timezone import now
from article.models import Article


class ArticleAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)
        self.fields[
            "publication_date"
        ].required = False  # The admin's .save() method fills in a default.


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = ArticleAdminForm

    fieldsets = (
        (
            None,
            {"fields": ("title", "slug")},
        ),
        (
            "Contents",
            {"fields": ("content",)},
        ),
        (
            "Publication settings",
            {"fields": ("publication_date", "enable_comments")},
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.publication_date:
            # auto_now_add makes the field uneditable.
            # a default in the model fills the field before the post is written (too early)
            obj.publication_date = now()
        obj.save()


admin.site.register(Article, ArticleAdmin)
