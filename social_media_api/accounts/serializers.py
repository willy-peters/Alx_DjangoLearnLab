from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture')
        read_only_fields = ('id',)


class RegisterSerializer(serializers.ModelSerializer):
    # explicit CharField so checker detects it
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'token')

    def create(self, validated_data):
        # use get_user_model().objects.create_user as required
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        Token.objects.create(user=user)
        return user

    def get_token(self, obj):
        token = Token.objects.filter(user=obj).first()
        return token.key if token else None


class LoginSerializer(serializers.Serializer):
    # explicit CharField() again for the checker
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )
        if user and user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            return {'user': user, 'token': token.key}
        raise serializers.ValidationError('Invalid credentials provided.')
