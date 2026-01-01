from rest_framework import serializers
from django.contrib.auth import get_user_model
from payments.models import Wallet, Transaction
from bookings.models import Booking, GPUSlot
from mentors.models import Mentor, MentorSession

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'college_name', 'department', 'year_of_study', 'user_type']

class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone_number', 'college_name', 'department', 'year_of_study']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        Wallet.objects.create(user=user)
        return user

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'free_minutes', 'created_at', 'updated_at']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_type', 'transaction_id', 'description', 'timestamp']

class GPUSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPUSlot
        fields = ['id', 'name', 'is_available']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'gpu_slot', 'start_time', 'end_time', 'is_active', 'created_at']

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['id', 'user', 'expertise', 'experience_years', 'bio', 'hourly_rate']

class MentorSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorSession
        fields = ['id', 'student', 'mentor', 'start_time', 'end_time', 'is_confirmed', 'notes']
