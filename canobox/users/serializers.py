# accounts/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # JWT payload에 role도 포함시킴
        token['role'] = 'admin' if (user.is_staff or user.is_superuser) else 'user'
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # 응답 JSON에 role 추가
        data['role'] = 'admin' if (self.user.is_staff or self.user.is_superuser) else 'user'
        data['username'] = self.user.username
        data['user_id'] = self.user.id
        data['name'] = self.user.name

        return data
