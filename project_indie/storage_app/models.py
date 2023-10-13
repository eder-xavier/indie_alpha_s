from django.contrib.auth import get_user_model
from django.db import models

CustomUser = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(max_length=200, blank=True)
    following = models.ManyToManyField(CustomUser, related_name='followers', blank=True)

    def __str__(self):
        return self.user.username

class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following_relationships')
    followed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower_relationships')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file)

class Publication(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.TextField(blank=False, null=True, max_length=30)
    text = models.TextField(blank=True, null=True, max_length=639)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    attachments = models.ManyToManyField('Attachment', related_name='publications')
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_publications', blank=True)


    def get_likes_count(self):
        return self.likes.count()
    
    def __str__(self):
        return f"Post by {self.author.username}"




class Comment(models.Model):
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_comments', blank=True)

    def get_likes_count(self):
        return self.likes.count()


#class Reply(models.Model):
#    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
#    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#    text = models.TextField()
#   created_at = models.DateTimeField(auto_now_add=True)
#    likes = models.ManyToManyField(CustomUser, related_name='liked_replies', blank=True)

#   def get_likes_count(self):
#        return self.likes.count()

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} liked {self.publication}"

#class Friendship(models.Model):
#    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friendships_started')
#    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friendships_received')
#
#    def __str__(self):
#        return f"{self.from_user} -> {self.to_user}"
    
class Friendship(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friendship_requests_sent')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friendship_requests_received')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.from_user} -> {self.to_user}'