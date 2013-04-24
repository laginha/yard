from django.db                  import models
from django.contrib.auth.models import User
from django.conf                import settings
import datetime, rstr


KEY_EXPIRATION_DELTA = getattr(settings, "KEY_EXPIRATION_DELTA", 1)
KEY_PATTERN   = getattr(settings, "KEY_PATTERN", r"[a-z0-9A-Z]{30,40}")


def years_from_now():
    today = datetime.datetime.today()
    delta = datetime.timedelta(days=365*KEY_EXPIRATION_DELTA)
    return today + delta
    
def generate_apikey():
    return rstr.xeger( KEY_PATTERN )
    
    
class Key(models.Model):
    """
    API key for resource access and authentication
    """
    user            = models.ForeignKey(User)
    apikey          = models.CharField(default=generate_apikey, max_length=100, unique=True)
    activation_date = models.DateField(default=datetime.date.today)
    expiration_date = models.DateField(default=years_from_now)
    last_used       = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u"%s" %self.apikey

        
class Consumer(models.Model):
    """
    API Consumer allowed (or not) to use an API key
    """
    key     = models.ForeignKey(Key)
    ip      = models.IPAddressField(blank=True)
    allowed = models.BooleanField(default=True)

    class Meta:
        unique_together = (("key","ip"),)

    def __unicode__(self):
        text = unicode(self.ip) + u" is%s allowed to use key"
        return text % ( "" if self.allowed else " not")
        

