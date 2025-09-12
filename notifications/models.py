# notifications/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    """
    Modelo para armazenar notificações.
    Usa um campo genérico (GenericForeignKey) para se conectar a qualquer modelo.
    """
    # Quem recebe a notificação.
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text='O usuário que recebe a notificação.'
    )

    # Quem causou a notificação.
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='actions',
        help_text='O usuário que realizou a ação.'
    )

    # A ação que ocorreu (ex: "curtiu", "comentou", "seguiu").
    verb = models.CharField(
        max_length=255,
        help_text='A descrição da ação.'
    )

    # O objeto ao qual a notificação se refere (ex: o Post que foi curtido).
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')

    # Status da notificação
    is_read = models.BooleanField(
        default=False,
        help_text='Indica se a notificação foi visualizada.'
    )

    # Data e hora da notificação
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text='A data e hora em que a notificação foi criada.'
    )

    class Meta:
        # Ordem padrão: as notificações mais recentes aparecem primeiro.
        ordering = ['-timestamp']
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'

    def __str__(self):
        return f'{self.actor.username} {self.verb} {self.target}'