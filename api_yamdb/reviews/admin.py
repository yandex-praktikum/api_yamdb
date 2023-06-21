from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from reviews.models import (Categories,
                            Genres,
                            Titles,
                            TitleGenre,
                            Reviews,
                            Comments)
from users.models import User


class UserResource(resources.ModelResource):

    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]


admin.site.register(User, UserAdmin)


class CategoriesResource(resources.ModelResource):

    class Meta:
        model = Categories


class CategoriesAdmin(ImportExportModelAdmin):
    resource_classes = [CategoriesResource]


admin.site.register(Categories, CategoriesAdmin)


class GenresResource(resources.ModelResource):

    class Meta:
        model = Genres


class GenresAdmin(ImportExportModelAdmin):
    resource_classes = [GenresResource]


admin.site.register(Genres, GenresAdmin)


class TitlesResource(resources.ModelResource):

    class Meta:
        model = Titles


class TitlesAdmin(ImportExportModelAdmin):
    resource_classes = [TitlesResource]


admin.site.register(Titles, TitlesAdmin)


class TitleGenreResource(resources.ModelResource):
    title = Field(attribute='title_id', column_name="title_id")
    genre = Field(attribute='genre_id', column_name="genre_id")

    class Meta:
        model = TitleGenre


class TitleGenreAdmin(ImportExportModelAdmin):
    resource_classes = [TitleGenreResource]


admin.site.register(TitleGenre, TitleGenreAdmin)


class ReviewsResource(resources.ModelResource):
    title = Field(attribute='title_id', column_name="title_id")

    class Meta:
        model = Reviews


class ReviewsAdmin(ImportExportModelAdmin):
    resource_classes = [ReviewsResource]


admin.site.register(Reviews, ReviewsAdmin)


class CommentsResource(resources.ModelResource):
    review = Field(attribute='review_id', column_name="review_id")
    created = Field(attribute='created_id', column_name="pub_date")

    class Meta:
        model = Comments


class CommentsAdmin(ImportExportModelAdmin):
    resource_classes = [CommentsResource]


admin.site.register(Comments, CommentsAdmin)
