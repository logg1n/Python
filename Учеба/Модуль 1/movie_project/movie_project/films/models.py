from django.db import models

class Film(models.Model):
    title = models.CharField("Название фильма", max_length=100)
    description = models.TextField("Описание фильма")
    review = models.TextField("Отзыв о фильме")
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    def __str__(self):
        return self.title