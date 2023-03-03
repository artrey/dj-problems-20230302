from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from demo.models import Post
from demo.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['post'], detail=False, url_path='bulk-create')
    def bulk_create(self, request, *args, **kwargs):
        created_posts = []
        for post_data in request.data:
            s = PostSerializer(data=post_data)
            if not s.is_valid(raise_exception=False):
                continue
            post = s.save(author=self.request.user)
            created_posts.append(post)
        return Response(PostSerializer(created_posts, many=True).data)


