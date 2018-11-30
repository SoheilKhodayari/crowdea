from django.forms import ModelForm
from django import forms
from campaign.models import Campaign
from django.core.exceptions import ObjectDoesNotExist
from idea.models import Idea
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class PostForm(ModelForm):
    idea_ref = forms.ModelChoiceField(queryset=Idea.objects.all(),
            widget=forms.HiddenInput())
    meta_campaign_deadline = forms.DateTimeField()
    class Meta:
        model = Campaign
        fields = '__all__'

    def clean(self): 

        super(PostForm, self).clean()
        idea_ref = self.cleaned_data.get('idea_ref') 
        campaign_desc = self.cleaned_data.get('description')
        campaign_target = self.cleaned_data.get('campaign_target_sum')
        campaign_deadline = self.cleaned_data.get('meta_campaign_deadline')
        
        if idea_ref == "":
            self._errors['idea'] = self.error_class([ 
                'Idea does not exist to create campaign or is invalid. Please navigate to idea and try again.']) 

        if campaign_desc == "":
            self._errors['description'] = self.error_class([ 
                'Campaign Description must not be empty.']) 

        if campaign_target == "":
            self._errors['campaign_target_sum'] = self.error_class([ 
                'Campaign Target amount must be set.']) 

        if campaign_deadline == "":
            self._errors['meta_campaign_deadline'] = self.error_class([ 
                'Deadline date must be at least one day later than today.']) 
        try:
            # ideaobj = Idea.objects.get(pk=idea_ref)
            return self.cleaned_data
        except ObjectDoesNotExist:
            self._errors['idea'] = self.error_class([ 
                'Idea does not exist to create campaign or is invalid. Please navigate to idea and try again.']) 
            return self.cleaned_data
        except TypeError:
            self._errors['meta_campaign_deadline'] = self.error_class([ 
                'Deadline must be yyyy-mm-dd format.']) 
            return self.cleaned_data
        except ValueError:
            self._errors['campaign_target_sum'] = self.error_class([ 
                'Target amount must only contain numbers.'])      
            return self.cleaned_data
        except ValidationError:
            self._errors['meta_campaign_deadline'] = self.error_class([ 
                'Deadline date must be at least one day later than today.']) 
            return self.cleaned_data