from rest_framework import serializers
from .models import CustomUser, UserProfile
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_id', 'name', 'gender', 'age', 'region', 'email']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        instance.username = validated_data.get('username', instance.username)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()

        profile = instance.profile
        profile.user_id = profile_data.get('user_id', profile.user_id)
        profile.name = profile_data.get('name', profile.name)
        profile.gender = profile_data.get('gender', profile.gender)
        profile.age = profile_data.get('age', profile.age)
        profile.region = profile_data.get('region', profile.region)
        profile.email = profile_data.get('email', profile.email)
        profile.save()

        return instance

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    password1 = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    user_id = serializers.CharField()
    name = serializers.CharField()
    gender = serializers.CharField()
    age = serializers.IntegerField()
    region = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("This username is already taken.")
        return data

    def create(self, validated_data):
        user = CustomUser(username=validated_data['username'])
        user.set_password(validated_data['password1'])
        user.save()

        UserProfile.objects.create(
            user=user,
            user_id=validated_data['user_id'],
            name=validated_data['name'],
            gender=validated_data['gender'],
            age=validated_data['age'],
            region=validated_data['region'],
            email=validated_data['email'],
        )

        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'profile': {
                    'user_id': validated_data['user_id'],
                    'name': validated_data['name'],
                    'gender': validated_data['gender'],
                    'age': validated_data['age'],
                    'region': validated_data['region'],
                    'email': validated_data['email'],
                }
            }
        }

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'profile': {
                'user_id': self.user.profile.user_id,
                'name': self.user.profile.name,
                'gender': self.user.profile.gender,
                'age': self.user.profile.age,
                'region': self.user.profile.region,
                'email': self.user.profile.email,
            }
        }
        
        return data