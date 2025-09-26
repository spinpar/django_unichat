from django.db import models
from django.contrib.auth.models import User

# Modelos Post, Comment e Reply (sem alterações)
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post de {self.author.username} em {self.created_at.strftime("%Y-%m-%d")}'
    
    @property
    def likes_count(self):
        return self.votes.filter(vote_type='like').count()

    @property
    def dislikes_count(self):
        return self.votes.filter(vote_type='dislike').count()
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentário de {self.author.username} no Post {self.post.id}'
    
    @property
    def likes_count(self):
        return self.votes.filter(vote_type='like').count()

    @property
    def dislikes_count(self):
        return self.votes.filter(vote_type='dislike').count()
    
class Reply(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Resposta de {self.author.username} ao comentário {self.comment.id}'
    
    @property
    def likes_count(self):
        return self.votes.filter(vote_type='like').count()

    @property
    def dislikes_count(self):
        return self.votes.filter(vote_type='dislike').count()
    
class Vote(models.Model):
    VOTE_CHOICES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post'), ('user', 'comment'), ('user', 'reply')

    def __str__(self):
        if self.post:
            return f'{self.user.username} voted {self.vote_type} on post {self.post.id}'
        elif self.comment:
            return f'{self.user.username} voted {self.vote_type} on comment {self.comment.id}'
        elif self.reply:
            return f'{self.user.username} voted {self.vote_type} on reply {self.reply.id}'
        return 'Voto inválido'
    
class Event(models.Model):
        author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
        title = models.CharField(max_length=200)
        description = models.TextField()
        image = models.ImageField(upload_to='event_images/', blank=True, null=True) 
        location = models.CharField(max_length=200)
        event_date = models.DateField()
        event_time = models.TimeField()
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f'Evento: {self.title}'