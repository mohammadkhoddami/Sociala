from django import forms 
from .models import Post
#create your forms here 

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)