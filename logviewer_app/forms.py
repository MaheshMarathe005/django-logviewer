from django import forms

class LogSearchForm(forms.Form):
    log_file = forms.ChoiceField(choices=[])  # choices will be set dynamically
    keyword = forms.CharField(required=False, label='Search Keyword')
