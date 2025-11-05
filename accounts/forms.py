from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
    }))
    
    
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password')

    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():

            # Skip password fields (already have custom attrs)
            if name in ['password', 'confirm_password']:
                continue

            # Add Bootstrap class and placeholders for other fields
            field.widget.attrs.update({
            'class': 'form-control',
            'placeholder': f'Enter {field.label}'
            })

    
    def clean(self):
        #cleaned_data is a dictionary of all validated and cleaned values.
        cleaned_data = super().clean()

        #This pulls both field values from the dictionary.
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        #Checks Password and Confirm Password is equal.
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data


        