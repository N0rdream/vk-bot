from django.db import models


class Hashtag(models.Model):
    name = models.CharField(max_length=50)
    message = models.TextField(blank=True)
    vk_attachment_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class History(models.Model):
    message_type = models.CharField(max_length=50)
    vk_timestamp = models.IntegerField()
    user_id = models.IntegerField()
    message = models.TextField()
    hashtag = models.ForeignKey(Hashtag, on_delete=models.SET_NULL, null=True, blank=True)
    answered = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    @classmethod
    def save_message(
        cls, message_type, vk_timestamp, user_id, message, 
        hashtag_obj=None, answered=False
    ):
        record = cls(
            message_type=message_type,
            vk_timestamp=vk_timestamp,
            user_id=user_id,
            message=message,
            answered=answered
        )
        if hashtag_obj is not None:
            record.hashtag = hashtag_obj
        record.save()

    @classmethod
    def has_hashtag(cls, hashtag, user_id, vk_timestamp, tdelta):
        return cls.objects.filter(
            hashtag__name=hashtag,
            user_id=user_id,
            vk_timestamp__lte=vk_timestamp,
            vk_timestamp__gte=vk_timestamp - int(tdelta) * 60,
            answered=True
        ).exists()


    class Meta:
        verbose_name_plural = 'History'