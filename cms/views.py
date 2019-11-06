from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os

from cms.models import Content, Category, Comment, Slider, Service, Feature, CustomerCompanies, CompanyMembers, \
    ContactMessage, ContentTypeChoices
from cms.serializers import ContentSerializer, CategorySerializer, CommentSerializer, SliderSerializer, \
    ServiceSerializer, FeatureSerializer, CustomerCompaniesSerializer, CompanyMembersSerializer, \
    ContactMessageSerializer


class PageList(generics.ListAPIView):
    serializer_class = ContentSerializer

    def get_queryset(self):
        return Content.objects.filter(published_date__lte=now())


class PageDetail(mixins.RetrieveModelMixin,
                 generics.GenericAPIView):
    serializer_class = ContentSerializer

    def get_queryset(self):
        return Content.objects.filter(published_date__lte=now())

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PageCommentList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
        serializer_class = CommentSerializer
        permission_classes = (IsAuthenticatedOrReadOnly,)

        def get_queryset(self):
            all_comment = Comment.objects.filter(content_type=ContentType.objects.get_for_model(Content),
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
                            content_object=Content.objects.get(id=self.kwargs['pk']),
                            content_type=ContentType.objects.get_for_model(Content))


class NewsList(generics.ListAPIView):
    serializer_class = ContentSerializer

    def get_queryset(self):
        return Content.objects.filter(type=ContentTypeChoices.news, published_date__lte=now())


class NewsDetail(mixins.RetrieveModelMixin,
                 generics.GenericAPIView):
    serializer_class = ContentSerializer

    def get_queryset(self):
        return Content.objects.filter(type=ContentTypeChoices.news, published_date__lte=now())

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class NewsCommentList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        all_comment = Comment.objects.filter(content_type=ContentType.objects.get_for_model(Content),
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
                        content_object=Content.objects.get(id=self.kwargs['pk']),
                        content_type=ContentType.objects.get_for_model(Content))


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


class SliderList(generics.ListAPIView):
    serializer_class = SliderSerializer

    def get_queryset(self):
        return Slider.objects.all()


class ServiceList(generics.ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.all()


class FeatureList(generics.ListAPIView):
    serializer_class = FeatureSerializer

    def get_queryset(self):
        return Feature.objects.all()


class CompanyList(generics.ListAPIView):
    serializer_class = CustomerCompaniesSerializer

    def get_queryset(self):
        return CustomerCompanies.objects.all()


class CompanyMemberList(generics.ListAPIView):
    serializer_class = CompanyMembersSerializer

    def get_queryset(self):
        return CompanyMembers.objects.all()


class ContactMessageList(generics.CreateAPIView):
    # use throtelling
    serializer_class = ContactMessageSerializer

    def get_queryset(self):
        return ContactMessage.objects.all()


class ReactAppView(View):

    def get(self, request):
        try:
            print('12312341234')
            print(os.path.join(settings.BASE_DIR, 'humangene_react', 'build', 'index.html'))

            with open('/Users/seyedhasanmousavi/Documents/scm/humangene/humangene-react/build/index.html') as file:
                return HttpResponse(file.read())
        except :
            return HttpResponse(
                """
                index.html not found ! build your React app !!
                """,
                status=501,
            )