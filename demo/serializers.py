from rest_framework import serializers

from demo.models import Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'text', 'created_at', 'author', 'tags']
        read_only_fields = ['author']
        # extra_kwargs = {
        #     'tags': {'required': False},
        #     'author': {'read_only': True},
        # }

    tags = TagSerializer(many=True)
    # tags = serializers.ListSerializer(child=serializers.CharField(), default=list)

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        post = super().create(validated_data)
        for tag_params in tags:
            tag_obj, created = Tag.objects.get_or_create(**tag_params)
            post.tags.add(tag_obj)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        post = super().update(instance, validated_data)
        tag_objs = []
        for tag_params in tags:
            tag_obj, created = Tag.objects.get_or_create(**tag_params)
            tag_objs.append(tag_obj)
        post.tags.set(tag_objs)
        return post
