from django import forms
from kyrciapp.python.region_dictionary import region_lists
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser
from .python.region_dictionary import choose_region


class SummonerForm(forms.Form):
    summoner_name = forms.CharField(label='Nazwa Gracza', max_length=100)
    region = forms.ChoiceField(choices=[(region, region) for region in region_lists()])


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    region = forms.ChoiceField(choices=[(code, name) for code, name in choose_region()])

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'region') 

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user