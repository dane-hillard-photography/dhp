from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    phone = forms.CharField(max_length=20, required=False)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
