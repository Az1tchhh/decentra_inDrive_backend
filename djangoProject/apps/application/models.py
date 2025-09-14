from django.db import models

from apps.utils.models import DeletedMixin, TimestampMixin


def upload_car_photos(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'car_photos', filename)


def upload_license_photo(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'licence_photo', filename)


def upload_tech_passport_photo(instance, filename):
    from apps.utils.services import upload_to
    return upload_to(instance, 'tech_passports', filename)


# Create your models here.
class DriverApplication(DeletedMixin, TimestampMixin):
    ACCEPTED_STATUS = 'accepted'
    DENIED_STATUS = 'denied'
    PENDING_STATUS = 'pending'

    STATUS_CHOICES = (
        (ACCEPTED_STATUS, 'Accepted'),
        (DENIED_STATUS, 'Denied'),
        (PENDING_STATUS, 'Pending'),
    )
    iin = models.CharField(max_length=12)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    status = models.CharField(choices=STATUS_CHOICES, max_length=255, default=PENDING_STATUS)

    @property
    def is_data_valid(self):
        cause = 'Все в порядке'
        if not self.license.validated_iin or self.license.validated_iin != self.iin:
            cause = 'ИИН не совпадает'
            return cause, False
        if not self.license.validated_name or self.license.validated_name != self.name:
            cause = 'Имя водителя не совпадает'
            return cause, False
        if not self.license.validated_surname or self.license.validated_surname != self.surname:
            cause = 'Фамилия водителя не совпадает'
            return cause, False
        return cause, True


class DriverCarPhoto(DeletedMixin, TimestampMixin):
    application = models.ForeignKey(DriverApplication, on_delete=models.CASCADE, related_name='car_photos')
    image = models.ImageField(upload_to=upload_car_photos, null=True, blank=True)
    problems = models.BooleanField(default=False)
    problem_list = models.TextField(null=True, blank=True)


class DriverLicense(DeletedMixin, TimestampMixin):
    application = models.OneToOneField(DriverApplication, on_delete=models.CASCADE, related_name='license')
    image = models.ImageField(upload_to=upload_license_photo, null=True, blank=True)
    validated_iin = models.CharField(max_length=12, null=True, blank=True)
    validated_name = models.CharField(max_length=255, null=True, blank=True)
    validated_surname = models.CharField(max_length=255, null=True, blank=True)


class CarTechPassport(DeletedMixin, TimestampMixin):
    application = models.ForeignKey(DriverApplication, on_delete=models.CASCADE, related_name='tech_passports')
    image = models.FileField(upload_to=upload_tech_passport_photo, null=True, blank=True)
