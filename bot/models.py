from django.db import models


######################
# Indexes
######################


class Vgroup(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=50)
	description = models.TextField()

	def __str__(self):
		return self.description


class Hashtag(models.Model):
	name = models.CharField(max_length=50)
	message = models.TextField(blank=True)
	attachment = models.CharField(max_length=50, blank=True)
	group = models.ForeignKey(Vgroup, on_delete=models.PROTECT)

	def __str__(self):
		return f'{self.name}, {self.group.name}'


class History(models.Model):
	message_type = models.CharField(max_length=50)
	date = models.IntegerField()
	user_id = models.IntegerField()
	message = models.TextField()
	hashtag = models.ForeignKey(Hashtag, on_delete=models.SET_NULL, null=True, blank=True)
	group = models.ForeignKey(Vgroup, on_delete=models.PROTECT)

	def __str__(self):
		return self.message

	class Meta:
		verbose_name_plural = 'History'