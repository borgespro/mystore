from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'user_type', 'phone', 'address', 'password')

    def is_valid(self, raise_exception=False):
        self.initial_data['username'] = self.initial_data['email']
        self.initial_data['user_type'] = User.CUSTOMER
        return super(UserSerializer, self).is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        instance = super(UserSerializer, self).save(**kwargs)
        instance.set_password(self.initial_data['password'])
        instance.save()
        return instance
