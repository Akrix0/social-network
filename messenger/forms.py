from django import forms
from django.core.exceptions import ValidationError
from messenger.models import Message, Chat
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageForm(forms.ModelForm):
    reply_to = forms.IntegerField(required=False)

    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': "Write down message...",
                'class': 'form-control',
                'id': 'message-input'
            })
        }

    def __init__(self, *args, chat=None, **kwargs):
        self.chat = chat
        super().__init__(*args, **kwargs)

    def clean_reply_to(self):
        reply_id = self.cleaned_data.get('reply_to')
        if reply_id in (None, ''):
            return None
        if self.chat is None:
            raise ValidationError("Chat is required to validate a reply.")
        try:
            return Message.objects.get(id=reply_id, chat=self.chat)
        except Message.DoesNotExist:
            raise ValidationError("Reply message does not exist in this chat.")


class GroupForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['users', 'background', 'title']
        widgets = {
            'users': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
            'title': forms.TextInput(attrs={
                'placeholder': "Write down group title...",
                'class': 'form-control',
            }),
            'background': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            friends_qs = User.objects.filter(id__in=[u.id for u in user.get_friends()])
            self.fields['users'].queryset = friends_qs


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['background']
        widgets = {
            'background': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
