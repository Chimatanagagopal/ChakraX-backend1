from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Ride, Profile
from .serializers import RideSerializer, ProfileSerializer
from django.contrib.auth import authenticate


class RegisterUser(APIView):
    def post(self, request):
        print("Received data:", request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')

        if not all([username, password, email, phone_number]):
            return Response({'error': 'All fields are required'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        profile = Profile.objects.create(
            user=user,
            username=username,
            email=email,
            phone_number=phone_number
        )

        token = Token.objects.create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'profile': ProfileSerializer(profile).data
        }, status=201)



class LoginUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=400)

        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }, status=200)
        else:
            return Response({'error': 'Invalid credentials.'}, status=401)

class ProfileViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=200)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)


class RideViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rides = Ride.objects.filter(user=request.user).order_by('-ride_time')
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def patch(self, request, ride_id=None):  # now receives ride_id from URL
        rating = request.data.get('rating')
        feedback = request.data.get('feedback')

        try:
            ride = Ride.objects.get(id=ride_id, user=request.user)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found"}, status=404)

        if rating is not None:
            ride.rating = rating
        if feedback is not None:
            ride.feedback = feedback
        ride.save()

        serializer = RideSerializer(ride)
        return Response(serializer.data, status=200)
