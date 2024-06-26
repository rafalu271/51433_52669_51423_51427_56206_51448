from rest_framework import serializers
from .models import User
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  def validate(self, attrs):
    password = attrs.get('password')

    try: 
    # django's validation rules for password
      validate_password(password)
    except ValueError as err:
      raise serializers.ValidationError(" ".join(err.messages))

    email = attrs.get('email')

    try:
    # django's validation rules for email
      validate_email(email)
    except ValueError:
      raise serializers.ValidationError("Invalid email address")

    return attrs
  
  def create(self, validated_data):
    # remove password from validated_data and store it password variable
    password = validated_data.pop('password')
    # make_password is a django function which hashes the password
    user = User.objects.create_user(
      email=validated_data['email'], password=password
    )
    return user
  
  class Meta:
    # Serializer configuration options
    model = User
    fields = ('email', 'password')