from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models
from slugify import slugify

from .utils import get_timestamp_path


class Client(AbstractUser):
    friends = models.ManyToManyField(
        'Client',
        blank=True
    )
    is_active = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='Activated?'
    )
    slug = models.SlugField(
        unique=True
    )

    # Optional
    avatar = models.ImageField(
        blank=True,
        upload_to=get_timestamp_path,
        verbose_name='Avatar'
    )
    phone_valid = RegexValidator(
        regex=r'^\+?7?\d{9,15}$'
    )
    phone_number = models.CharField(
        validators=[phone_valid],
        max_length=17,
        blank=True,
        verbose_name='Phone'
    )
    birthday = models.DateTimeField(
        blank=True,
        verbose_name='Birthday'
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


class Rubric(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='rubric'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'rubric'
        verbose_name_plural = 'rubrics'
        ordering = ['title']


class Public(models.Model):
    users = models.ManyToManyField(
        Client,
        blank=True
    )
    rubric = models.ForeignKey(
        Rubric,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='title'
    )
    desc = models.TextField(
        blank=True,
        verbose_name='description',
        max_length=600
    )
    photo = models.ImageField(
        blank=True,
        upload_to=get_timestamp_path,
        verbose_name='photo'
    )
    author = models.CharField(
        verbose_name='author',
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='slug'
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'public'
        verbose_name_plural = 'publics'
        ordering = ['title']


class Like(models.Model):
    user = models.ForeignKey(Client,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Post(models.Model):
    likes = GenericRelation(Like)
    public = models.ForeignKey(
        Public,
        on_delete=models.CASCADE,
        blank=True
    )
    content = models.TextField(
        verbose_name='content'
    )
    image = models.ImageField(
        blank=True,
        upload_to=get_timestamp_path,
        verbose_name='image'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='created_at'
    )

    @property
    def total_likes(self):
        return self.likes.count()

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']


class Comments(models.Model):
    pass


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        Client,
        related_name='from_user',
        on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        Client,
        related_name='to_user',
        on_delete=models.CASCADE)
