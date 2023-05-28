from django.urls import path
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('create_wall_configuration/', views.CreateWallConfiguration.as_view(), name="create_conf"),
    path('create_wall_configuration/<int:pk>', views.ListWallConfiguration.as_view(), name="get_conf"),

    path('profiles/<int:profile>/days/<int:day>/', views.ProfileDay.as_view(), name="profile_day"),
    path('profiles/<int:profile>/overview/<int:day>/', views.ProfileOverview.as_view(), name="profile_overview"),

    path('profiles/overview/<int:day>/', views.ProfileOverviewDay.as_view(), name="profile_overview_day"),
    path('profiles/overview/', views.WallOverview.as_view(), name="wall_overview"),



]

urlpatterns = format_suffix_patterns(urlpatterns)