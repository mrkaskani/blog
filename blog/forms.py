from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'body', 'image', 'tags', 'publish')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'body': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

    def save(self, *args, **kwargs):
        return super(PostForm, self).save(*args, **kwargs)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

    def save(self, *args, **kwargs):
        return super(CommentForm, self).save(*args, **kwargs)
