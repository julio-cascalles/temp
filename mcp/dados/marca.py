from enum import Enum


class Marca(Enum):
    CHEVROLET = 'Chevrolet'
    FIAT = 'Fiat'
    VOLKSWAGEN = 'Volkswagen'
    FORD = 'Ford'
    TOYOTA = 'Toyota'
    HONDA = 'Honda'
    HYUNDAI = 'Hyundai'
    NISSAN = 'Nissan'
    RENAULT = 'Renault'
    JEEP = 'Jeep'

MODELOS = {
    Marca.CHEVROLET: ['Onix', 'Tracker', 'S10'],
    Marca.FIAT: ['Palio', 'Strada', 'Toro'],
    Marca.VOLKSWAGEN: ['Gol', 'T-Cross', 'Polo'],
    Marca.FORD: ['Fiesta', 'EcoSport', 'Ranger'],
    Marca.TOYOTA: ['Corolla', 'Hilux', 'Etios'],
    Marca.HONDA: ['Civic', 'HR-V', 'Fit'],
    Marca.HYUNDAI: ['HB20', 'Creta', 'Kona'],
    Marca.NISSAN: ['Versa', 'Kicks', 'Frontier'],
    Marca.RENAULT: ['Sandero', 'Duster', 'Captur'],
    Marca.JEEP: ['Renegade', 'Compass', 'Wrangler']    
}
