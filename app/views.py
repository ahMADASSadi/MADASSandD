import requests

from django.views.generic import TemplateView
from django.core.cache import cache

# Create your views here.


class HomeView(TemplateView):
    template_name = "app/index.html"

    def get_context_data(self, **kwargs):
        profile_key = "profile"
        repo_key = "repo"
        context = super().get_context_data(**kwargs)

        github_username = "ahMADASSadi"

        url = f"https://api.github.com/users/{github_username}"
        repo_url = url + "/repos"

        user_info = cache.get(profile_key)
        if user_info is None:
            try:
                response = requests.get(url, timeout=1)
                response.raise_for_status()
                data = response.json()

                user_info = {
                    "login": data.get("login"),
                    "name": data.get("name"),
                    "bio": data.get("bio"),
                    "email": data.get("email"),
                    "avatar_url": data.get("avatar_url"),
                    "html_url": data.get("html_url"),
                }

                cache.set(profile_key, user_info, timeout=60 * 10)

            except requests.exceptions.RequestException as e:
                print(f"Error fetching GitHub profile data: {e}")
            user_info = {"error": "Could not retrieve GitHub profile data"}

        context["user_info"] = user_info

        repos_info = cache.get(repo_key)
        if repos_info is None:
            try:
                response = requests.get(repo_url, timeout=1)
                response.raise_for_status()
                data = response.json()
                repos_info = [
                    {
                        "id": repo.get("id"),
                        "title": repo.get("name"),
                        "description": repo.get("description"),
                        "technologies": "N/A",  # Or parse from topics if available
                        "githubLink": repo.get("html_url"),
                    }
                    for repo in data
                    if repo.get("description")
                ]

                cache.set(repo_key, repos_info, timeout=60 * 10)

            except requests.exceptions.RequestException:
                context["repos"] = None

        context["repos"] = repos_info

        skills = [
            {"name": "Python", "color": "#3776AB"},
            {"name": "Django", "color": "#092E20"},
            {"name": "Django RestAPI", "color": "#EF4444"},
            {"name": "FastAPI", "color": "#009688"},
            {"name": "PostgreSQL", "color": "#4169E1"},
            {"name": "MongoDB", "color": "#00533B"},
            {"name": "Celery", "color": "#A9CC54", "text_color": "gray-900"},
            {"name": "Redis", "color": "#AA0A00"},
            {"name": "Docker", "color": "#328EEF"},
            {"name": "RabbitMQ", "color": "#FF8C00"},
        ]
        context["skills"] = skills
        return context
