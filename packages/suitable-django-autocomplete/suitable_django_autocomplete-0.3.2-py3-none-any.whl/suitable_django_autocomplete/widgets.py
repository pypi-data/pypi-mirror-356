from django import forms
from django.urls import reverse_lazy


class AutocompleteWidget(forms.TextInput):
    """A suitable autocomplete widget for Django forms using web components."""

    template_name = "suitable_django_autocomplete/autocomplete.html"

    def __init__(self, url=None, attrs=None, min_length=2, debounce_delay=300,
                 value_field='value', label_field='label', initial_display_value=None,
                 host_attrs=None):
        self.url = url
        self.min_length = min_length
        self.debounce_delay = debounce_delay
        self.value_field = value_field
        self.label_field = label_field
        self.initial_display_value = initial_display_value
        self.host_attrs = host_attrs or {}
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"].update(
            {
                "url": self.url or reverse_lazy("autocomplete"),
                "min_length": self.min_length,
                "debounce_delay": self.debounce_delay,
                "value_field": self.value_field,
                "label_field": self.label_field,
                "initial_display_value": self.initial_display_value,
                "host_attrs": self.host_attrs,
            }
        )
        return context

    # When migrating to 5.2 only, use this to module load instead of in template. Nice.
    # class Media:
    #     js = [
    #         Script(
    #             "suitable_django_autocomplete/autocomplete.js",
    #             **{
    #                 "type": "module",
    #             },
    #         ),
    #     ]
