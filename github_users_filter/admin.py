import datetime

from django.contrib import admin

from rangefilter.filter import DateTimeRangeFilter

from models import GithubUser, SearchApiCallLog, GithubUserStats, SearchApiStats
from github_users_filter.utils import get_current_datetime_ist


class GithubUserAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'username', 'email', 'created_at', 'location', 'company')

    list_filter = (('created_at', DateTimeRangeFilter), 'location', )

    search_fields = ('email', )


class SearchApiCallLogAdmin(admin.ModelAdmin):
    list_display = ('for_date', 'count')


class GithubUserStatsAdmin(admin.ModelAdmin):
    change_list_template = 'github_user_stats.html'

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super(GithubUserStatsAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        current_datetime = get_current_datetime_ist().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start_date = current_datetime - datetime.timedelta(days=current_datetime.weekday())
        month_start_date = current_datetime - datetime.timedelta(days=(current_datetime.day - 1))

        today_count = qs.filter(created_at__gte=current_datetime).count()
        this_week_count = qs.filter(created_at__gte=week_start_date).count()
        this_month_count = qs.filter(created_at__gte=month_start_date).count()

        response.context_data['summary'] = [
            {"title": "Today", "value": today_count},
            {"title": "This week", "value": this_week_count},
            {"title": "This month", "value": this_month_count}
        ]

        return response


class SearchApiStatsAdmin(admin.ModelAdmin):
    change_list_template = 'search_query_stats.html'

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super(SearchApiStatsAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        current_datetime = get_current_datetime_ist().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start_date = current_datetime - datetime.timedelta(days=current_datetime.weekday())
        month_start_date = current_datetime - datetime.timedelta(days=(current_datetime.day - 1))

        today_count = sum(qs.filter(for_date__gte=current_datetime).values_list('count', flat=True))
        this_week_count = sum(qs.filter(for_date__gte=week_start_date).values_list('count', flat=True))
        this_month_count = sum(qs.filter(for_date__gte=month_start_date).values_list('count', flat=True))

        response.context_data['summary'] = [
            {"title": "Today", "value": today_count},
            {"title": "This week", "value": this_week_count},
            {"title": "This month", "value": this_month_count}
        ]

        return response


admin.site.register(GithubUser, GithubUserAdmin)
admin.site.register(SearchApiCallLog, SearchApiCallLogAdmin)
admin.site.register(GithubUserStats, GithubUserStatsAdmin)
admin.site.register(SearchApiStats, SearchApiStatsAdmin)
