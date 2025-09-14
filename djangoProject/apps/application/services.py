from apps.application.models import DriverApplication, DriverCarPhoto, DriverLicense
from model import predict


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


def model_validation(obj: DriverApplication):
    loc_photos = obj.car_photos.all()
    for loc_photo in loc_photos:  # TODO function for model call for each photo
        try:
            verdict, confidence = predict.predict(loc_photo.image.url)
        except Exception as e:
            verdict, confidence = True, 0
        if verdict:
            response = {
                'has_problem': True,
                'problem_type': 'DENT'
            }
            if response['problem_type'] == 'DENT':
                loc_photo.problems = True
                loc_photo.problem_list = 'Вмятина'
                loc_photo.save()

    #TODO parsing license service call
    license_parse = {
        'iin': obj.iin,
        'name': obj.name,
        'surname': obj.surname,
    }

    driver_license = DriverLicense.objects.get(application_id=obj.id)
    driver_license.validated_iin = license_parse['iin']
    driver_license.validated_surname = license_parse['surname']
    driver_license.validated_name = license_parse['name']

    driver_license.save()

    return obj
