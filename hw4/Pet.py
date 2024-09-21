class Pet:
    species_lifespan = {
        'dog': 13,
        'cat': 15,
        'rabbit': 9,
        'hamster': 3,
        'parrot': 50
    }

    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species

    def age_in_human_years(self):
        if self.species == 'dog' or self.species == 'cat':
            return self.age * 7
        elif self.species == 'rabbit':
            return self.age * 8
        elif self.species == 'hamster':
            return self.age * 25
        elif self.species == 'parrot':
            return self.age * 4
        else:
            return self.age

    @classmethod
    def average_lifespan(cls, species):
        return cls.species_lifespan.get(species, "Unknown lifespan")

pet1 = Pet(name="Buddy", age=4, species="dog")
pet2 = Pet(name="Whiskers", age=3, species="cat")
pet3 = Pet(name="Coco", age=2, species="parrot")

age_buddy_human_years = pet1.age_in_human_years()
age_whiskers_human_years = pet2.age_in_human_years()
age_coco_human_years = pet3.age_in_human_years()

lifespan_buddy = Pet.average_lifespan(pet1.species)
lifespan_whiskers = Pet.average_lifespan(pet2.species)
lifespan_coco = Pet.average_lifespan(pet3.species)

(age_buddy_human_years, lifespan_buddy), (age_whiskers_human_years, lifespan_whiskers), (age_coco_human_years, lifespan_coco)
