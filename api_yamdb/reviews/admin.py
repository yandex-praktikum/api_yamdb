from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]


admin.site.register(User, UserAdmin)


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]


admin.site.register(Category, CategoryAdmin)


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre


class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]


admin.site.register(Genre, GenreAdmin)


class TitleResource(resources.ModelResource):
    class Meta:
        model = Title


class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]


admin.site.register(Title, TitleAdmin)


class ReviewResource(resources.ModelResource):
    title = Field(attribute='title_id', column_name='title_id')

    class Meta:
        model = Review


class ReviewAdmin(ImportExportModelAdmin):
    resource_classes = [ReviewResource]


admin.site.register(Review, ReviewAdmin)


class CommentResource(resources.ModelResource):
    review = Field(attribute='review_id', column_name='review_id')
    created = Field(attribute='created_id', column_name='pub_date')

    class Meta:
        model = Comment


class CommentAdmin(ImportExportModelAdmin):
    resource_classes = [CommentResource]


admin.site.register(Comment, CommentAdmin)
