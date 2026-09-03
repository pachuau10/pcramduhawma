from django import forms
from .models import GuestbookEntry


class GuestbookForm(forms.ModelForm):
    website_confirm = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = GuestbookEntry
        fields = ['name', 'email', 'website', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'retro-input', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'retro-input', 'placeholder': 'Your email (optional)'}),
            'website': forms.URLInput(attrs={'class': 'retro-input', 'placeholder': 'Your website (optional)'}),
            'message': forms.Textarea(attrs={'class': 'retro-textarea', 'rows': 5, 'placeholder': 'Leave a message...'}),
        }

    def clean_website_confirm(self):
        if self.cleaned_data.get('website_confirm'):
            raise forms.ValidationError("Spam detected.")
        return ''

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters.")
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        if len(message) < 5:
            raise forms.ValidationError("Message must be at least 5 characters.")
        if len(message) > 2000:
            raise forms.ValidationError("Message must be less than 2000 characters.")
        return message
