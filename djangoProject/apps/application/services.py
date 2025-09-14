from apps.application.models import DriverApplication, DriverCarPhoto, DriverLicense


def add_driver_application(data):
    car_photos = data.pop('car_photos')
    license = data.pop('license')

    application = DriverApplication.objects.create(**data)
    # application.car_photos.set(car_photos)
    car_photos_to_create = []
    for car_photo in car_photos:
        car_photos_to_create.append(DriverCarPhoto(application=application, **car_photo))

    DriverCarPhoto.objects.bulk_create(car_photos_to_create)

    if license:
        DriverLicense.objects.create(application=application, **license)

    return application
