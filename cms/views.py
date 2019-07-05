from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from cms.models import Page, News, Category, Comment
from cms.serializers import PageSerializer, NewsSerializer, CategorySerializer, CommentSerializer


class PageList(generics.ListAPIView):
    serializer_class = PageSerializer

    def get_queryset(self):
        return Page.objects.filter(published_date__lte=now())


class PageDetail(mixins.RetrieveModelMixin,
                 generics.GenericAPIView):
    serializer_class = PageSerializer

    def get_queryset(self):
        return Page.objects.filter(published_date__lte=now())

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PageCommentList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
        serializer_class = CommentSerializer
        permission_classes = (IsAuthenticatedOrReadOnly,)

        def get_queryset(self):
            all_comment = Comment.objects.filter(content_type=ContentType.objects.get_for_model(Page),
                                                 object_id=self.kwargs['pk'],
                                                 enabled=True,
                                                 is_approved=True).select_related('user', ).order_by('-created_at')
            return all_comment

        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)

        def post(self, request, *args, **kwargs):
            return self.create(request, *args, **kwargs)

        def perform_create(self, serializer):
            serializer.save(user=self.request.user,
                            content_object=Page.objects.get(id=self.kwargs['pk']),
                            content_type=ContentType.objects.get_for_model(Page))


class NewsList(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.filter(published_date__lte=now())


class NewsDetail(mixins.RetrieveModelMixin,
                 generics.GenericAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.filter(published_date__lte=now())

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class NewsCommentList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        all_comment = Comment.objects.filter(content_type=ContentType.objects.get_for_model(News),
                                             object_id=self.kwargs['pk'],
                                             enabled=True,
                                             is_approved=True).select_related('user',).order_by('-created_at')
        return all_comment

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        content_object=News.objects.get(id=self.kwargs['pk']),
                        content_type=ContentType.objects.get_for_model(News))


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

