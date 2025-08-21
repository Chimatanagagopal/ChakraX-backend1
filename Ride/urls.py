from django.urls import path
from .views import RideViewSet, ProfileViewSet, RegisterUser, LoginUser

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register-user'),
    path('login/', LoginUser.as_view(), name='login-user'),
    path('profiles/', ProfileViewSet.as_view(), name='profile-detail'),

    # Ride endpoints
    path('rides/', RideViewSet.as_view(), name='ride-list'),           # GET (list), POST (create)
    path('rides/<int:ride_id>/', RideViewSet.as_view(), name='ride-update'),  # PATCH (update rating/feedback)
]
