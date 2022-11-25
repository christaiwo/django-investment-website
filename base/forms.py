from django import forms
from .models import *



class bankForm(forms.ModelForm):
    class Meta:
        model = bank
        fields = ('routing_no', 'bank_name', 'account_no', 'account_name',)

    def __init__(self, *args, **kwargs):
        super(bankForm, self).__init__(*args, **kwargs)
        self.fields['routing_no'].widget.attrs.update({'class' : 'form-control', 'placeholder':'Routing Number'})
        self.fields['bank_name'].widget.attrs.update({'class' : 'form-control', 'placeholder':'Bank Name'})
        self.fields['account_no'].widget.attrs.update({'class' : 'form-control', 'placeholder':'Account Number'})
        self.fields['account_name'].widget.attrs.update({'class' : 'form-control', 'placeholder':'Account Name'})