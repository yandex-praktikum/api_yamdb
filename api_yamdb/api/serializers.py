from rest_framework import serializers
from django.core.exceptions import ValidationError

from reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field="username",
        read_obly=True
    )

    def validate(self, data):
        request = self.context["request"]
        author = request.user
        title = self.context.get("view").kwargs.get("title_id")
        if (
            request.method == "Post"
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError("Отзыв уже оставлен")
        return data

    class Meta:
        model = Review
        fields = '__all__'