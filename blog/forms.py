from django import forms

class EmailPostForm(forms.Form):
    # CharField is rendered as an <input type="text"> element
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # We can override the default element using the widget attribute
    comments = forms.CharField(required=False, widget=forms.Textarea)


