from rest_framework import serializers

from apps.application.models import DriverApplication, DriverCarPhoto, DriverLicense


class DriverCarPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverCarPhoto
        fields = ('id',
                  'image',
                  'problems',
                  'problem_list')


class DriverCarPhotoCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = DriverCarPhoto
        fields = (
            'image',
        )


class DriverLicenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverLicense
        fields = ('id',
                  'validated_iin',
                  'validated_name',
                  'validated_surname')


class DriverLicenceCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = DriverLicense
        fields = (
            'image',
        )


class DriverApplicationSerializer(serializers.ModelSerializer):
    car_photos = DriverCarPhotoSerializer(many=True)
    license = DriverLicenceSerializer()

    class Meta:
        model = DriverApplication
        fields = ('id',
                  'iin',
                  'name',
                  'surname',
                  'license',
                  'car_photos',
                  'status')


class DriverApplicationCreateSerializer(serializers.ModelSerializer):
    car_photos = DriverCarPhotoCreateSerializer(many=True)
    license = DriverLicenceCreateSerializer()

    class Meta:
        model = DriverApplication
        fields = (
            'iin',
            'name',
            'surname',
            'car_photos',
            'license'
        )
