from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'retro-input', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'retro-input', 'placeholder': 'you@example.com'}),
            'subject': forms.TextInput(attrs={'class': 'retro-input', 'placeholder': 'Subject (optional)'}),
            'message': forms.Textarea(attrs={'class': 'retro-textarea', 'rows': 5, 'placeholder': 'Your message...'}),
        }

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        if len(message.strip()) < 10:
            raise forms.ValidationError("Message must be at least 10 characters.")
        if len(message) > 5000:
            raise forms.ValidationError("Message must be less than 5000 characters.")
        return message
