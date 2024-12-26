from rest_framework import serializers
from drf.models import User
from drf.common_methods import create_jwt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'json_web_token')
        read_only_fields = ('json_web_token', )

    def create(self, validated_data):
        jwt_token = create_jwt(validated_data['email'])
        validated_data['json_web_token'] = jwt_token
        return super().create(validated_data)
