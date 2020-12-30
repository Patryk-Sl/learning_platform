from django.contrib.auth.models import User
from django import forms
from .models import Message
from django.utils.encoding import smart_text


class UserFullnameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return smart_text(obj.get_full_name())


class MessageForm(forms.ModelForm):
    user_to = UserFullnameChoiceField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['user_to', 'title', 'text']
