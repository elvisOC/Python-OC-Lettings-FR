from django.shortcuts import render
import os


def index(request):
    return render(request, 'index.html')


def sentry_settings(request):
    return {
        "SENTRY_DSN": os.getenv("SENTRY_DSN", ""),
        "SENTRY_ENV": os.getenv("SENTRY_ENV", "development"),
        "GITHUB_SHA": os.getenv("GITHUB_SHA", "local-dev"),
    }
