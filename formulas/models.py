from core.models import TimestampedModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    career_name = models.CharField(max_length=80, blank=True)

class Subject(models.Model):
    name = models.SlugField(max_length=80, unique=True)

""" class Professor(models.Model):
    name = models.CharField(max_length=60, unique=True) """

class PhotoClassification(models.Model):
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE,
        related_name='photo_classifications'
    )

    # mid term examns what is the limit ?¿, custorm message errors
    exam_number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subject', 'exam_number'], 
                name='subject and exam number must be unique'
            )
        ]


class PhotoContext(models.Model):
    
    class FormulaType(models.TextChoices):
        ONE_FORMULA = 'F1', _('One Formula')
        MULTIPLE_FORMULAS = 'FM', _('Multiple formulas')
        # exercice ?
        EXERCICE_FORMULA = 'FE', _('Exercice formula')
        GRAPHIC_FORMULA = 'FG', _('Graphic formula')

    formula_type = models.CharField(
        max_length=2, 
        choices=FormulaType.choices, 
        blank=True
    )
    professor = models.CharField(max_length=60, blank=True)

class Tag(models.Model):
    name = models.CharField(max_length=60, unique=True)

def user_photos_directory_path(instance, filename):
    return 'user_{0}/photos/{1}'.format(instance.user.id, filename)

class Photo(TimestampedModel):
    file = models.ImageField(
        upload_to=user_photos_directory_path, 
        null=True
    )
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    photo_classification = models.ForeignKey(
        PhotoClassification, 
        on_delete=models.CASCADE,
        related_name='photos',
    )
    photo_context = models.OneToOneField(
        PhotoContext, 
        on_delete=models.CASCADE,
        related_name='photo',
        null = True
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='photos',
    )
    tags = models.ManyToManyField(Tag, related_name='photos')

class Review(models.Model):
    # custorm message errors
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    photo = models.ForeignKey(
        Photo, 
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['photo', 'user'], 
                name='one review per photo'
            )
        ]
        

