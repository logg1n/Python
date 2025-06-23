from django.db import models

# Create your models here.
class NewsPost(models.Model):
	title = models.CharField("Название новости", max_length=50)
	user = models.CharField("Обозреватель", max_length=25, default='admin')
	short_description = models.CharField("Краткое описание новости", max_length=200)
	text = models.TextField("Новость")
	date = models.DateTimeField("Дата публикации", auto_now=True)

	def __str__(self):
		return f"{self.title}"

	class Meta:
		verbose_name = "Новость"
		verbose_name_plural = "Новости"