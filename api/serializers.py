from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *

class ProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    profile = ProfileInfoSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = '__all__'

class MyTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyTag
        fields = '__all__'
        read_only_fields = ['user']

class MyTagDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many = True)

    class Meta:
        model = MyTag
        fields = '__all__'
        read_only_fields = ['user']

class MyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCategory
        fields = '__all__'
        read_only_fields = ['user']

class MyCategoryDetailSerializer(serializers.ModelSerializer):
    categorys = CategorySerializer(many = True)

    class Meta:
        model = MyCategory
        fields = '__all__'
        read_only_fields = ['user']

class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Save
        fields = '__all__'
        read_only_fields = ['user']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        read_only_fields = ['user']

class NewsSerializer(serializers.ModelSerializer):
    #tags = TagSerializer(many=True)
    category = CategorySerializer(many=True)
    user = serializers.SerializerMethodField(method_name='get_username')
    image = serializers.SerializerMethodField(method_name='get_image_url')
    save = serializers.SerializerMethodField(method_name='get_save')
    vote = serializers.SerializerMethodField(method_name='get_vote')

    class Meta:
        model = News
        exclude = ['tags']

    def get_username(self, instance):
        return instance.user.get_full_name() if instance.user else None

    def get_image_url(self, instance):
        request = self.context.get("request")
        return request.build_absolute_uri(instance.image.url) if instance.image else None

    def get_save(self, instance):
        user = self.context.get('request').user
        if user.is_authenticated:
            save = Save.objects.filter(user = user, news=instance)
            if save: return SaveSerializer(save[0]).data
            return None
        return None

    def get_vote(self, instance):
        user = self.context.get('request').user
        if user.is_authenticated:
            vote = Vote.objects.filter(user = user, news=instance)
            if vote: return VoteSerializer(vote[0]).data
        return None

class MyNewsSerializer(serializers.ModelSerializer):
    #news = NewsSerializer()

    class Meta:
        model = MyNews
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'news']

class SaveDetailSerializer(serializers.ModelSerializer):
    news = NewsSerializer()
    class Meta:
        model = Save
        fields = '__all__'
        read_only_fields = ['user']

class VoteDetailSerializer(serializers.ModelSerializer):
    news = NewsSerializer()
    class Meta:
        model = Vote
        fields = '__all__'
        read_only_fields = ['user']
