from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    # CharField is rendered as an <input type="text"> element
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # We can override the default element using the widget attribute
    comments = forms.CharField(required=False, widget=forms.Textarea)


# We can use models to build forms as well
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # By default, all fields are added to the form but we can select specific fields
        # by providing a 'fields' tuple or exclude specific ones using an 'exclude' tuple
        fields = ('name', 'email', 'body')

