from django.urls import path


from app.views import HomeView

app_name = "app"

urlpatterns = [
    path("", HomeView.as_view(), name="Home"),
]
