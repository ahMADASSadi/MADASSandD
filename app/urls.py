from django.urls import path


from app.views import HomeGitHubView

app_name = "app"

urlpatterns = [
    path("", HomeGitHubView.as_view(), name="Home"),

]
