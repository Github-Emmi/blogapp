from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from blogapp.models import CustomUser, Comment
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model= CustomUser
        fields= UserCreationForm.Meta.fields + ("username",)
        
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model= CustomUser
        fields= UserChangeForm.Meta.fields      
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('email','name','body')
        widgets = {
            'name': forms.TextInput(attrs={"class":"form-control","placeholder":"Enter your name"}),
            'email': forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter your email"}),
            'body': forms.Textarea(attrs={"class":"form-control","cols":"30", "rows":"10","placeholder":"Leave a comment"}),
        }
        
class ShareForm(forms.Form):
    name= forms.CharField(label="Name:", max_length=50, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter your name"}))
    email=forms.EmailField(label="Email:",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off","placeholder":"Enter your email"}))
    to=forms.EmailField(label="Recipient Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off","placeholder":"Enter recipient email"}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","placeholder":"comment about the post"}))
        
class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Looking for something?"}))        