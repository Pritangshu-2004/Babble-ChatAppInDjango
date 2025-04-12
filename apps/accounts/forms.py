from django import forms
from .models import Profile

# Define avatar choices
AVATAR_CHOICES = [
    ('avatar1', 'Avatar 1'),
    ('avatar2', 'Avatar 2'),
    ('avatar3', 'Avatar 3'),
    ('avatar4', 'Avatar 4'),
]

class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ChoiceField(choices=AVATAR_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Profile  # Replace with your actual model
        fields = ['profile_picture', 'avatar']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'avatar']