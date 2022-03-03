from django_filters import FilterSet, CharFilter
from .models import Comment


class CommentFilter(FilterSet):

    class Meta:
        model = Comment
        fields = ('user', 'post')

