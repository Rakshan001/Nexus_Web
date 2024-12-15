# notifications/forms.py
from django import forms
from django.contrib.auth.models import User

class CustomNotificationForm(forms.Form):
    RECIPIENT_CHOICES = [
        ('all', 'All Users'),
        ('alumni', 'Alumni Only'),
        ('students', 'Students Only'),
        ('specific', 'Specific Users'),
    ]

    recipient_type = forms.ChoiceField(choices=RECIPIENT_CHOICES)
    specific_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'style': 'width: 300px; height: 150px;'})
    )
    title = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        recipient_type = cleaned_data.get('recipient_type')
        specific_users = cleaned_data.get('specific_users')

        if recipient_type == 'specific' and not specific_users:
            raise forms.ValidationError(
                "Please select at least one user when sending to specific users."
            )