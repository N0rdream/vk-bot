from django.db import models


class Hashtag(models.Model):
    name = models.CharField(max_length=50)
    message = models.TextField(blank=True)
    attachment = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_hashtag_fields(cls, hashtag):
        hashtag = cls.objects.select_related().filter(name=hashtag).first()
        message = hashtag.message
        attachment = hashtag.attachment
        if not message:
            return None, attachment
        if not attachment:
            return message, None
        return message, attachment


class History(models.Model):
    message_type = models.CharField(max_length=50)
    date = models.IntegerField()
    user_id = models.IntegerField()
    message = models.TextField()
    hashtag = models.ForeignKey(Hashtag, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name_plural = 'History'