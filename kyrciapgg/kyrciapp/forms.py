from django import forms
from kyrciapp.python.region_dictionary import region_lists
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SummonerForm(forms.Form):
    summoner_name = forms.CharField(label='Nazwa Gracza', max_length=100)
    region = forms.ChoiceField(choices=[(region, region) for region in region_lists()])


class SignUpForm(UserCreationForm):
    # Możesz dodać dodatkowe pola
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )
        
        
