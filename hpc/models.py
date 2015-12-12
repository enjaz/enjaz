from django.db import models

class Abstract(models.Model):
    title = models.CharField(verbose_name="Title", max_length=128)
    authors = models.TextField(verbose_name=u"Name of authors")
    university = models.CharField(verbose_name="University", max_length=128)
    college = models.CharField(verbose_name="College", max_length=128)
    presenting_author = models.CharField(verbose_name="Presenting author", max_length=128)
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(verbose_name="Phone number", max_length=128)
    presentation_preference_choices = (
        ('O', 'Oral'),
        ('P', 'Poster')
        )
    presentation_preference = models.CharField(verbose_name="Presentation preference", max_length=128, choices=presentation_preference_choices)
    attachment = models.FileField(verbose_name=u"Attach the abstract", upload_to="hpc/abstract/")
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title
