from django import forms
from .models import Post

class PostForm(forms.ModelForms):
	class Meta:
		model = Post
		fields = ('name', 'email', 'subject', 'message')

		widget = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'email': forms.TextInput(attrs={'class': 'form-control'}),
			'subject': forms.TextInput(attrs={'class': 'form-control'}),
			'message': forms.TextInput(attrs={'class': 'form-control'}),

		}