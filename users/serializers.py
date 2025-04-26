from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserPreferences

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'profile_picture',
                 'bio', 'institution', 'major', 'graduation_year')
        read_only_fields = ('id',)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

    # Create user preferences
        UserPreferences.objects.create(user=user)

        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        help_text="User's email address for login"
    )
    password = serializers.CharField(
        required=True,
        help_text="User's password",
        style={'input_type': 'password'}
    )

    class Meta:
        ref_name = 'UserLogin'  # Explicit name for Swagger documentation


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ('id', 'daily_study_goal',"intensity", 'weekly_study_goal', 'preferred_study_duration',
                  'preferred_break_duration', 'reminder_frequency', 'study_reminders_enabled',
                  'deadline_reminders_enabled', 'assessment_reminders_enabled')
        read_only_fields = ('id',)

class UserProfileSerializer(serializers.ModelSerializer):
    preferences = UserPreferencesSerializer(source='detailed_preferences', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'profile_picture',
                  'bio', 'date_of_birth', 'institution', 'major', 'graduation_year',
                  'preferred_study_time', 'preferences')
        read_only_fields = ('id', 'email')

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        help_text="User's email address for password reset"
    )

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True,
        help_text="New password",
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        required=True,
        help_text="Confirm new password",
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs