from ninja import ModelSchema
from .models import Pet

class PetSchema(ModelSchema):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'species']


class CreatePetSchema(ModelSchema):
    class Meta:
        model = Pet
        fields = ['name', 'species']


class UpdatePetSchema(ModelSchema):
    class Meta:
        model = Pet
        fields = ['name', 'species']
        fields_optional = '__all__'