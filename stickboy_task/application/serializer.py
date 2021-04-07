from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):

	


	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email','password','is_staff','id')
		read_only_fields = ('is_active', 'last_login', 'groups', 'user_permissions', 'is_superuser',
                            'last_update_userid', 'last_update_date')
		extra_kwargs = {
            'password': {'write_only': True},}
	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		
		return user	


class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField(max_length=255)
	password = serializers.CharField(max_length=255, write_only=True)


	def validate(self,data):

		email = data.get("email",None)
		password =data.get("password",None)
		user = authenticate(email=email, password=password)
		
		if user is None:
			raise serializers.ValidationError('user not found')

		

		return{
			'email':user.email,
			
		}

class ChangePasswordSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    old_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password','confirm_password']



    def update(self, instance, validated_data):

        instance.password = validated_data.get('password', instance.password)

        if not validated_data['new_password']:
              raise serializers.ValidationError({'new_password': 'not found'})

        if not validated_data['old_password']:
              raise serializers.ValidationError({'old_password': 'not found'})

        if not instance.check_password(validated_data['old_password']):
              raise serializers.ValidationError({'old_password': 'wrong password'})

        if validated_data['new_password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({'passwords': 'passwords do not match'})

        if validated_data['new_password'] == validated_data['confirm_password'] and instance.check_password(validated_data['old_password']):
            # instance.password = validated_data['new_password'] 
            print(instance.password)
            instance.set_password(validated_data['new_password'])
            print(instance.password)
            instance.save()
            return instance
        return instance

class LoginSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:

		model = User
		fields = "__all__"

	def update(self, instance, validated_data):
		instance.password = validated_data.get('password', instance.password)

		instance.set_password(validated_data['password'])
		print(instance.password)
		instance.save()
		return instance