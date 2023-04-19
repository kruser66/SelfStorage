from django.db import models

# Create your models here.
class Notify(models.Model):
    username = models.CharField('Имя клиента', max_length=100)
    email = models.EmailField()
    sending_data = models.DateField('Плановая дата отправки', db_index=True)
    subject = models.CharField('Тема сообщения', max_length=200)
    message = models.TextField('Текст сообщения')
    rental_info = models.CharField('Информация о заказе', max_length=200)
    expired_at = models.DateField('Срок окончания заказа', db_index=True)
    executed = models.BooleanField(default=False)   
    
    class Meta:
        verbose_name = 'уведомление'
        verbose_name_plural = 'уведомления'

    def __str__(self):
        return f'{self.sending_data} {self.username} {self.email}'
