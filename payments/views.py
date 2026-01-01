from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import razorpay
import json

from .models import Wallet, Transaction

# Initialize Razorpay client
try:
    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
except:
    razorpay_client = None

class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        """Create a Razorpay order for wallet recharge"""
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if not razorpay_client:
                return Response({'error': 'Payment gateway not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            amount_in_paise = int(float(amount) * 100)
            order_data = {
                'amount': amount_in_paise,
                'currency': 'INR',
                'receipt': f'wallet_recharge_{request.user.id}',
                'payment_capture': 1
            }
            order = razorpay_client.order.create(data=order_data)
            return Response({
                'order_id': order['id'],
                'amount': amount,
                'key_id': settings.RAZORPAY_KEY_ID
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def verify_payment(self, request):
        """Verify Razorpay payment and update wallet"""
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')
        amount = request.data.get('amount')

        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature, amount]):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if not razorpay_client:
                return Response({'error': 'Payment gateway not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Verify signature
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # Update wallet
            wallet = Wallet.objects.get(user=request.user)
            wallet.balance += float(amount)
            wallet.save()

            # Create transaction record
            Transaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type='recharge',
                transaction_id=razorpay_payment_id,
                description=f'Wallet recharge via Razorpay - Order {razorpay_order_id}'
            )

            return Response({
                'message': 'Payment verified and wallet updated',
                'new_balance': wallet.balance
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Payment verification failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
