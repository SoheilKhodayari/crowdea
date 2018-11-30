from django.forms import ModelForm
from django import forms
from campaign.models import Campaign
from django.core.exceptions import ObjectDoesNotExist
from idea.models import Idea
from datetime import datetime,timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class PostForm(ModelForm):
    current_date = datetime.now().date()
    next_day = current_date + timedelta(1)
    idea_ref = forms.ModelChoiceField(queryset=Idea.objects.all(),
            widget=forms.HiddenInput())
    user = forms.ModelChoiceField(queryset=User.objects.all(),
            widget=forms.HiddenInput())
    title = forms.CharField(widget=forms.HiddenInput())
    idea = forms.CharField(widget=forms.HiddenInput())
    is_active = forms.BooleanField(widget=forms.HiddenInput(), required=False, initial=False)
    campaign_collected_sum = forms.IntegerField(widget=forms.HiddenInput())

    meta_campaign_deadline = forms.DateTimeField(label='Campaign deadline',widget=forms.SelectDateWidget(), 
        help_text='End date of your campaign. Funding cannot be solicited for this campaign beyond this date.'+
            '[Required]', initial=next_day)

    description = forms.CharField(label='Campaign description',widget=forms.Textarea(), 
        help_text='Description of your campaign. Please restrict to 1000 characters [Required]',required=True)

    description.validators.append(MinLengthValidator(limit_value=1, 
        message='Campaign description must not be empty'))

    campaign_target_sum = forms.IntegerField(label='Target funding',widget=forms.NumberInput(), 
        help_text='Target funding of your campaign in Euros. Funding must attain '+
        'this target to be redeemable. [Required]')
    
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