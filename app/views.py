import requests
import pprint

from django.views.generic import TemplateView, ListView
from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from django.core.cache import cache

# Create your views here.


class HomeGitHubView(TemplateView):
    template_name = "app/index.html"  # The template for the home page

    def get_context_data(self, **kwargs):
        profile_key = "profile"
        repo_key = "repo"
        context = super().get_context_data(**kwargs)

        github_username = "ahMADASSadi"  # Your GitHub username
        # Ensure this token is added securely in your settings
        github_token = settings.GITHUB_TOKEN

        url = f'https://api.github.com/users/{github_username}'
        repo_url = url+'/repos'

        user_info = cache.get(profile_key)
        if user_info is None:
            try:
                response = requests.get(url, timeout=1)
                response.raise_for_status()
                data = response.json()

                user_info = {
                    'login': data.get('login'),
                    'name': data.get('name'),
                    'bio': data.get('bio'),
                    'email': data.get('email'),
                    'avatar_url': data.get('avatar_url'),
                    'html_url': data.get('html_url'),
                }

                cache.set(profile_key, user_info, timeout=60*10)

            except requests.exceptions.RequestException as e:

                print(f"Error fetching GitHub profile data: {e}")
                user_info = {
                    'error': 'Could not retrieve GitHub profile data'
                }

        context['user_info'] = user_info

        repos_info = cache.get(repo_key)
        if repos_info is None:
            try:
                response = requests.get(repo_url, auth=("username", github_token), timeout=1)
                response.raise_for_status()
                data = response.json()
                repos_info = [
                    {
                        'name': repo.get('name'),
                        'description': repo.get('description'),
                        'url': repo.get('url')
                    }
                    for repo in data if repo.get('description')
                ]

                cache.set(repo_key, repos_info, timeout=60*10)

            except requests.exceptions.RequestException as e:

                context['repos'] = None

        context['repos'] = repos_info

        return context
