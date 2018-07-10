from django.contrib import admin

from models import GithubUser, SearchApiCallLog


class GithubUserAdmin(admin.ModelAdmin):
    pass


class SearchApiCallLogAdmin(admin.ModelAdmin):
    pass


admin.site.register(GithubUser, GithubUserAdmin)
admin.site.register(SearchApiCallLog, SearchApiCallLogAdmin)
