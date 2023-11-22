from rest_framework import serializers

from form.models import Template, Field


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ("name", "field_type", )


class TemplateSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(read_only=True, many=True)
    # fields = serializers.PrimaryKeyRelatedField(queryset=Field.objects.all(), many=True)


    class Meta:
        model = Template
        fields = ("id", "name", "fields", )


# class TemplateSearchSerializer(serializers.ModelSerializer):
#     fields = serializers.CharField()
#
#     class Meta:
#         model = Template
#         fields = ("id", "name", "fields", )

