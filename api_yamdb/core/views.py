from django.shortcuts import get_object_or_404

from reviews.models import Review, Title


def get_title_object(self):
    title_id = self.kwargs.get('title_id')
    return get_object_or_404(Title.objects, id=title_id)


def get_review_object(self):
    title = get_title_object(self)
    return get_object_or_404(Review.objects,
                             id=self.kwargs.get('review_id'),
                             title_id=title.id)
