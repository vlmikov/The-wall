from rest_framework import serializers
from api.models import ConfigWall
import re
from .constants import max_number_section, max_height


class ConfigWallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigWall
        fields = ['id', 'conf', 'created']
    # id = serializers.IntegerField(read_only=True)
    # conf = serializers.CharField(required=True, allow_blank=False, max_length=250)

    def create(self, validated_data):
        return ConfigWall.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.conf = validated_data.get('conf', instance.conf)
        instance.save()
        return instance

    @staticmethod
    def raise_validation_error(errors, message):
        errors = [str(error) for error in errors]
        errors = ", ".join(errors)
        raise serializers.ValidationError(f'{message} :  {errors}')

    @staticmethod
    def process_input(conf):
        """
        This method remove all additional empty spaces in the input data
        """
        conf = conf.strip()
        conf = re.sub(' +', ' ', conf)
        return conf
    
    def validate(self, value):
        """
        Validate method for input data
        """
        conf = value.get('conf')
        # Remove all additional empty spaces in the input data
        conf = self.process_input(conf)
        # Assign transformed data back in value
        value['conf'] = conf
        # Split input data by new line in order to get list of all profiles
        profiles = conf.split('\n')
        errors_not_integer = []
        errors_value = []
        # loop over every profile
        for indx_profile, profile in enumerate(profiles):
            # Split every profile in order to get list of all section for current profile
            sections = profile.split(' ')
            # if section is greater than max_number section from constants.py
            if len(sections) > max_number_section:
                # Raise validation error
                raise serializers.ValidationError('Too many profiles max ...')

            # loop over sections in current profile
            for indx_section, section in enumerate(sections):
                try:
                    # Check if section is valid integer
                    int(section)
                    # Check if every section is range 0 to wall_length -> from constants.py
                    if int(section) > max_height or int(section) < 0:
                        # If section is out of the range store info in error_value list
                        errors_value.append({'index_profile': indx_profile, 
                                             'index_section': indx_section, 
                                             'value': section, })
                except (Exception,):
                    # If section is not integer value add error info to error_not_integer list
                    response = {'index_profile': indx_profile, 
                                'index_section': indx_section, 
                                'value': section, }

                    errors_not_integer.append(response)

        # Check for error and raise
        if len(errors_not_integer) > 0:
            self.raise_validation_error(errors_not_integer, "Not integer values")
        
        if len(errors_value) > 0:
            self.raise_validation_error(errors_value, "The section value must be between 0 and 30")
           
        return value
