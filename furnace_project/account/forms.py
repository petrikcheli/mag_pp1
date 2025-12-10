from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']    

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class FurnaceInputForm(forms.Form):
    Si = forms.FloatField(initial=0.53)
    Mn = forms.FloatField(initial=0.19)
    S = forms.FloatField(initial=0.014)
    P = forms.FloatField(initial=0.043)
    Ti = forms.FloatField(initial=0.068)
    Cr = forms.FloatField(initial=0.021)
    V = forms.FloatField(initial=0.0)
    C = forms.FloatField(initial=5.13)

    T_iron = forms.FloatField(initial=1405)
    C_iron = forms.FloatField(initial=0.9)

    rd = forms.FloatField(initial=0.35)

    coke_rate = forms.FloatField(initial=420)
    coke_ash = forms.FloatField(initial=11.9)
    coke_sulfur = forms.FloatField(initial=0.5)
    coke_volatiles = forms.FloatField(initial=0.6)
    coke_moisture = forms.FloatField(initial=4.2)

    hot_blast_temp = forms.FloatField(initial=1140)
    blast_humidity = forms.FloatField(initial=6.36)
    oxygen_content = forms.FloatField(initial=24.1)

    gas_consumption = forms.FloatField(initial=115)
    gas_CH4 = forms.FloatField(initial=100)
    gas_C2H6 = forms.FloatField(initial=0)
    gas_CO2 = forms.FloatField(initial=0)
    gas_C_CH4 = forms.FloatField(initial=1)
    gas_H2_CH4 = forms.FloatField(initial=2)

    limestone_rate = forms.FloatField(initial=0)
    limestone_moisture = forms.FloatField(initial=0)
    limestone_loss_on_ignition = forms.FloatField(initial=42)

    slag_rate = forms.FloatField(initial=260)
    slag_sulfur = forms.FloatField(initial=1.03)
    slag_heat_capacity = forms.FloatField(initial=1.26)

    top_gas_temp = forms.FloatField(initial=328)
    top_CO2 = forms.FloatField(initial=17.5)
    top_CO = forms.FloatField(initial=24.1)
    top_H2 = forms.FloatField(initial=7.0)
    top_N2 = forms.FloatField(initial=51.4)

    ore_rate = forms.FloatField(initial=1716)
    pellets_rate = forms.FloatField(initial=0)
    ore_moisture = forms.FloatField(initial=0)