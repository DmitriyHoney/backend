from django.db import models
from address.models import AddressInfo
from citizen.utils import create_image_thumb
from municipality.models import Municipality
from users.models import User


class ProblemPhoto(models.Model):
    title = models.CharField(verbose_name="Заголовок фотографии", blank=True, default="", max_length=255)
    photo = models.ImageField(verbose_name="Изображение", upload_to="images/problems")
    photo_small = models.ImageField(verbose_name="Изображение thumb", upload_to="thumbs", blank=True)
    problem = models.ForeignKey('Problem', verbose_name="Проблема", on_delete=models.CASCADE)
    additional = models.ForeignKey('ProblemAdditional', verbose_name="Дополнение к проблеме", null=True, blank=True,
                                   on_delete=models.CASCADE)

    def create_photo_thumb(self):
        self.photo_small.delete(save=True)
        if self.photo:
            create_image_thumb(self, self.photo, self.photo_small)


class ProblemComment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    parent_comment = models.ForeignKey('self', verbose_name="Родительский комментарий", null=True,
                                       on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    problem = models.ForeignKey('Problem', verbose_name="Проблема", on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now=True)


class ProblemCategory(models.Model):
    name = models.CharField(verbose_name="Наименоввание", max_length=255)
    parent_category = models.ForeignKey('self', verbose_name="Родительская категория", null=True, blank=True, related_name="parent",
                                        on_delete=models.CASCADE)

    def __str__(self):
        return f'pk: {self.pk}, name: {self.name}, parent_name: {self.parent_category.name if self.parent_category else None}'


class Problem(models.Model):
    NEW = 1
    UNDER_CONSIDERATION = 2
    IN_WORK = 3
    NOT_VALIDATED = 4
    COMPLETED = 5

    STATUS = (
        (NEW, 'Новый'),
        (UNDER_CONSIDERATION, 'На рассмотрении'),
        (IN_WORK, 'В работе'),
        (NOT_VALIDATED, 'Не прошёл модерацию'),
        (COMPLETED, 'Решена')
    )
    title = models.CharField(verbose_name="Описание проблемы", max_length=255, blank=True)
    description = models.TextField(verbose_name="Подробное описание проблемы", blank=True)
    status = models.CharField(verbose_name="Статус", choices=STATUS, default=NEW, max_length=255, blank=True)
    is_draft = models.BooleanField(verbose_name="Черновик", default=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT, related_name='problem_authors')
    operator = models.ForeignKey(User, verbose_name="Оператор принявший проблему", related_name='problem_operators',
                                 on_delete=models.SET_NULL, null=True)
    address = models.OneToOneField(AddressInfo, verbose_name="Адрес", on_delete=models.CASCADE)
    mo = models.ForeignKey(Municipality, verbose_name="МО", on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(ProblemCategory, verbose_name="Категория", null=True, blank=True, on_delete=models.CASCADE,
                                 related_name="problem_category")
    subcategory = models.ForeignKey(ProblemCategory, verbose_name="Под категория", null=True, blank=True,
                                    on_delete=models.CASCADE, related_name="problem_subcategory",)
    # organization = models.ForeignKey(Organization, verbose_name="Организация", on_delete=models.SET_NULL, null=True)

    def change_status(self, new_status):
        ProblemHistory.objects.create(problem=self, status=self.status)
        self.status = new_status
        self.save()

    class Meta:
        verbose_name = 'Проблема'
        verbose_name_plural = 'Проблемы'

    def __str__(self):
        return f'({self.pk}) - {self.title}'


class ProblemHistory(models.Model):
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    status = models.CharField(verbose_name="Статус", choices=Problem.STATUS, max_length=255)
    problem = models.ForeignKey('Problem', verbose_name="Проблема", on_delete=models.CASCADE)


class ProblemAdditional(models.Model): # Дополнение от пользователя/заявителя
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    description = models.TextField(verbose_name="Текст дополнения")
    is_checked_applicant = models.BooleanField(default=False, verbose_name="Проверено заявителем")
    problem = models.ForeignKey('Problem', verbose_name="Проблема", on_delete=models.CASCADE)


class ProblemLikeDislike(models.Model):
    LIKE = 1
    DISLIKE = 2
    STATUS = (
        (LIKE, 'За'),
        (DISLIKE, 'Против')
    )
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    status = models.CharField(verbose_name="Статус лайка, дизлайка", choices=STATUS, max_length=255)
    problem = models.ForeignKey('Problem', verbose_name="Проблема", on_delete=models.CASCADE)
