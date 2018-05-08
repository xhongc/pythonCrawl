from rest_framework import serializers
from api.models import Snippet,LANGUAGE_CHOICE,STYLE_CHOICE

class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False,allow_blank=True,max_length=100)
    code = serializers.CharField(style={'base_template':'txtarea.html'})
    lineos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICE,default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICE,default='friendly')


    def create(self, validated_data):
        return Snippet.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.code = validated_data.get('code',instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance