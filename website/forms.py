from django import forms
from django.forms.models import modelformset_factory
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['podcast', 'episode', 'content', 'score']

        widgets = {
            'podcast': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'episode': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'content': "Write your review:"
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['episode'].queryset = Episode.objects.none()

        if 'podcast' in self.data:
            try:
                podcast_id = int(self.data.get('podcast'))
                self.fields['episode'].queryset = Episode.objects.filter(podcast_id=podcast_id).order_by("title")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['episode'].queryset = self.instance.podcast.episode_set.order_by("title")

class PodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ['title', 'creator', 'image', 'information']
        exclude = ['podcast_id']
    
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'information': forms.Textarea(attrs={'class': 'form-control'}),
            'creator': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = ['podcast', 'title', 'image', 'information', 'date']
        exclude = ['episode_id', 'user']
    
        widgets = {
            'podcast': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'information': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.TextInput(attrs={'class': 'form-control'}),
            'date': DateInput(),
        }

        date = forms.DateField(
            widget=forms.DateInput(format='%m/%d/%Y'),
            input_formats=('%m/%d/%Y', )
            )

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['title', 'description', 'is_private', 'image']

    
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'required': 'True'}),
            'image': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
        }

        labels = {
            'is_private': "Make list private:"
        }

class ListContentForm(forms.ModelForm):
    class Meta:
        model = ListContent
        fields = ['podcast', 'episode']

        widgets = {
            'podcast': forms.Select(attrs={'class': 'form-control'}),
            'episode': forms.Select(attrs={'class': 'form-control'}),
        }
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['episode'].queryset = Episode.objects.none()

        if 'podcast' in self.data:
            print('here!')
            try:
                podcast_id = int(self.data.get('podcast'))
                self.fields['episode'].queryset = Episode.objects.filter(podcast_id=podcast_id).order_by("title")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['episode'].queryset = self.instance.podcast.episode_set.order_by("title")