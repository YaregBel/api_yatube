from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, pagination, permissions, viewsets
from posts.models import Post, Group, Comment, Follow
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)
from .permissions import OwnershipPermission

# Определение разрешения для дочерних классов
class PermissionViewset(viewsets.ModelViewSet):
    permission_classes = (OwnershipPermission,)

# Уставление разрешения на только чтение для групп, установка сериализатора.
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# Реализация CRUD запросов для постов, а также их пагинация, сериализация. 
class PostViewSet(PermissionViewset):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user
        )

# Реализация логики создания, чтения, редактирования и удаления комментариев,
# определенного поста.
class CommentViewSet(PermissionViewset):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.get_post_obj().comments.all()

    def get_post_obj(self):
        return get_object_or_404(
            Post,
            pk=self.kwargs.get('post_pk')
        )

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            post=self.get_post_obj()
        )

# Класс реализующийся для создания и просмотра подписок
class FollowViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
