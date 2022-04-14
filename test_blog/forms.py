from django import forms

from.models import Comment, Post


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
        }


class LogInForm(forms.Form):
    '''Форма входа в систему'''

    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control mt-2",
            'id': "inputPassword",
        })
    )


class PostForm(forms.ModelForm):
    '''Форма создания поста'''

    class Meta:
        model = Post
        fields = ('h1', 'title', 'url', 'description', 'content')
        labels = {
            'h1': 'H1',
            'title': 'Title',
            'url': 'Url',
            'description': 'Description',
            'content': 'Content'
        }
        widgets = {
            'description': forms.Textarea(attrs={'style':
                                              'resize: vertical;'}),
            'content': forms.Textarea(attrs={'style':
                                                     'resize: vertical;'})
        }
