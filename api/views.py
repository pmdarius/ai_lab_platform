from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import random

from payments.models import Wallet, Transaction
from bookings.models import Booking, GPUSlot
from mentors.models import Mentor, MentorSession

from .serializers import (
    UserSerializer, UserSignUpSerializer, WalletSerializer,
    TransactionSerializer, GPUSlotSerializer, BookingSerializer,
    MentorSerializer, MentorSessionSerializer
)

User = get_user_model()

# Store OTPs in memory (in production, use Redis or database)
otp_store = {}

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def signup(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def request_otp(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = str(random.randint(100000, 999999))
        otp_store[email] = otp
        
        # Send OTP via email
        try:
            send_mail(
                'Your OTP for KSRCE AI Lab',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({'error': f'Failed to send OTP: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'message': 'OTP sent to your email'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_otp(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        if email not in otp_store or otp_store[email] != otp:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            del otp_store[email]
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def balance(self, request):
        wallet = Wallet.objects.get(user=request.user)
        return Response({
            'balance': wallet.balance,
            'free_minutes': wallet.free_minutes
        })

    @action(detail=False, methods=['post'])
    def recharge(self, request):
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance += float(amount)
        wallet.save()
        
        # Create transaction record
        Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type='recharge',
            description=f'Wallet recharge of ₹{amount}'
        )
        
        return Response({
            'message': 'Wallet recharged successfully',
            'new_balance': wallet.balance
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def transactions(self, request):
        wallet = Wallet.objects.get(user=request.user)
        transactions = Transaction.objects.filter(wallet=wallet).order_by('-timestamp')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

class GPUSlotViewSet(viewsets.ModelViewSet):
    queryset = GPUSlot.objects.all()
    serializer_class = GPUSlotSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def available(self, request):
        slots = GPUSlot.objects.filter(is_available=True)
        serializer = GPUSlotSerializer(slots, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_booking(self, request):
        gpu_slot_id = request.data.get('gpu_slot_id')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        
        if not all([gpu_slot_id, start_time, end_time]):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            gpu_slot = GPUSlot.objects.get(id=gpu_slot_id)
            booking = Booking.objects.create(
                user=request.user,
                gpu_slot=gpu_slot,
                start_time=start_time,
                end_time=end_time,
                is_active=True
            )
            return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
        except GPUSlot.DoesNotExist:
            return Response({'error': 'GPU slot not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

class MentorViewSet(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def book_session(self, request):
        mentor_id = request.data.get('mentor_id')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        
        if not all([mentor_id, start_time, end_time]):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            mentor = Mentor.objects.get(id=mentor_id)
            session = MentorSession.objects.create(
                student=request.user,
                mentor=mentor,
                start_time=start_time,
                end_time=end_time
            )
            return Response(MentorSessionSerializer(session).data, status=status.HTTP_201_CREATED)
        except Mentor.DoesNotExist:
            return Response({'error': 'Mentor not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def my_sessions(self, request):
        sessions = MentorSession.objects.filter(student=request.user).order_by('-start_time')
        serializer = MentorSessionSerializer(sessions, many=True)
        return Response(serializer.data)
