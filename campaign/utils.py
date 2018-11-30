from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime

def validate_campaign_target(date):
    current_date = datetime.now().date()
    if date.date() <= current_date:
        raise ValidationError(
            _('Campaign %(date)s must be at least one day later'),
            params={'date': date},
        )