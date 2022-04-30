from django.db import models

class search(models.Model):
    search=models.CharField(max_length=500)
    created=models.DateTimeField(auto_now=True)
    #changing saved objects to strings in admin page(searches model)
    def __str__(self):
        return '{}'.format(self.search)

    #change the name in admin page
    class Meta:
        verbose_name_plural="searches"

# Create your models here.
