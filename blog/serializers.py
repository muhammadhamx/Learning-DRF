from rest_framework import serializers
from .models import Author, Post

# Manual Serializer 
'''class BasicAuthorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    
# Model Serializer  (Manual, flexible)
class AuthorSerializer(serializers.Serializer):
    class Meta:
        model = Author
        fields = '__all__'
    
    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
    
    def validate_email(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Email cannot be empty")
        return value

# Custom Validations    (Automatic, for models)
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at']
        read_only_fields = ['created_at']

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('Title must be longer than 5 characters')
        return value

    def validate(self, data):
        if 'spam' in data.get('content', '').lower():
            raise serializers.ValidationError('Forbidden words: "spam"')
        return data
'''
        
# Nested Serializer (Read-Only)
class NestedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content']


class AuthorSerializer(serializers.ModelSerializer):
    posts = NestedPostSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'posts']
        depth = 1
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['post_count'] = instance.posts.count()
        return data
    
    def to_internal_value(self, data):
        data['name'] = data['name'].strip().title()
        data['email'] = data['email'].lower()
        return super().to_internal_value(data)


# Writable Nested Serializer
class AuthorWritableSerializer(serializers.ModelSerializer):
    posts = NestedPostSerializer(many=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'password', 'posts']

    def create(self, validated_data):
        posts_data = validated_data.pop('posts')
        password = validated_data.pop('password')
        author = Author(**validated_data)
        author.set_password(password)  
        author.save()

        for post_data in posts_data:
            Post.objects.create(author=author, **post_data)
        return author
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance