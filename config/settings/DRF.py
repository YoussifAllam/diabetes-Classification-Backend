REST_FRAMEWORK: dict = {
    "DEFAULT_THROTTLE_RATES": {
        "user": "100/hour",
        "anon": "10/minute",
    },
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 1,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}
