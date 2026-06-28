from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from autoslug import AutoSlugField

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
    def was_edited(self):
        if (self.updated_at - self.created_at).total_seconds() > 1:
            return True
        return False

class UserProfile(AbstractUser):
    bio = models.CharField(max_length=200, blank=True, null=True, verbose_name='Bio', default='Bio is not set.')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar', default='default/default_avatar.png')
    mobile = PhoneNumberField(blank=True, null=True, verbose_name='Mobile Number')
    slug = AutoSlugField(populate_from='username', unique=True, verbose_name='Slug')
    birthday = models.DateField(blank=True, null=True, verbose_name='Birthday')

    def __str__(self):
        return self.username
    
    def delete(self, *args, **kwargs):
        if self.avatar and self.avatar.name != 'default/default_avatar.png':
            self.avatar.delete(save=False)

        super().delete(*args, **kwargs)

    def get_friends(self):
        following_ids = Follow.objects.filter(follower=self).values_list(
            "following_id", flat=True
        )
        mutual_ids = Follow.objects.filter(
            follower_id__in=following_ids,
            following=self,
        ).values_list("follower_id", flat=True)
        return UserProfile.objects.filter(id__in=mutual_ids)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['username']

class Follow(BaseModel):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following', verbose_name='Follower')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followers', verbose_name='Following')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        constraints = [
            models.UniqueConstraint(
                fields=('follower', 'following'),
                name='accounts_follow_follower_following_uniq',
            ),
        ]

    def __str__(self):
        return f"{self.follower} → {self.following}"
    
    @classmethod
    def is_friends(cls, user1, user2):
        return (
            Follow.objects.filter(follower=user1, following=user2).exists()
            and Follow.objects.filter(follower=user2, following=user1).exists()
        )

    @classmethod
    def follow_user(cls, follower, following):
        follow_obj, created = Follow.objects.get_or_create(
            follower=follower, following=following
        )
        return created

    @classmethod
    def unfollow_user(cls, follower, following):
        Follow.objects.filter(follower=follower, following=following).delete()