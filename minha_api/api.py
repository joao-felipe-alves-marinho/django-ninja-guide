from ninja import NinjaAPI
from django.shortcuts import get_object_or_404
from .models import Pet
from .schemas import PetSchema, CreatePetSchema, UpdatePetSchema

api = NinjaAPI()

@api.get("/pets", response=list[PetSchema])
def get_pets(request):
    return Pet.objects.all()


@api.get("/pets/{pet_id}", response=PetSchema)
def get_pet(request, pet_id: int):
    pet = get_object_or_404(Pet, id=pet_id)
    return pet


@api.post("/pets", response=PetSchema)
def create_pet(request, payload: CreatePetSchema):
    pet = Pet.objects.create(**payload.dict())
    return 201, pet


@api.patch("/pets/{pet_id}", response=PetSchema)
def update_pet(request, pet_id: int, payload: UpdatePetSchema):
    pet = get_object_or_404(Pet, id=pet_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(pet, attr, value)
    pet.save()
    return pet


@api.delete("/pets/{pet_id}")
def delete_pet(request, pet_id: int):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.delete()
    return 204, None