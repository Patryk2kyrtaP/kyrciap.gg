from django import forms
from kyrciapp.python.region_dictionary import region_lists

class SummonerForm(forms.Form):
    summoner_name = forms.CharField(label='Nazwa Gracza', max_length=100)
    region = forms.ChoiceField(choices=[(region, region) for region in region_lists()])
