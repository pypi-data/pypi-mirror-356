from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def indicator_api_urls(indicator_dict):
    view_names = [
        "download-indicator-methodo",
        "statistics",
        "values",
        "histogram",
        "top-10",
        "details-table",
        "details-table-export",
        "comparison-histogram",
        "proportions",
    ]
    return {
        view_name: reverse(
            f"indicators-api:{view_name}", kwargs={"name": indicator_dict["name"]}
        )
        for view_name in view_names
    }
