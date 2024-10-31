from django import forms
from .models import Alumni

class AlumniUpdateForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = [
            'first_name', 'last_name', 'phone_number', 'graduation_year', 'location', 
            'profile_picture', 'batch', 'usn', 'linkedin_url', 'current_position', 
            'company_name', 'bio', 'achievements', 'dob', 'personal_email'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(AlumniUpdateForm, self).__init__(*args, **kwargs)
        # Remove the Bootstrap class addition, as it's not needed now
        # for field in self.fields.values():
        #     field.widget.attrs.update({'class': 'form-control'})
