from datetime import datetime
from util.duck_model import DuckModel
from faker import Faker
from dados.combustivel import Combustivel
from dados.status import Status
from dados.marca import Marca, MODELOS
from dados.cores import Cor


HOJE = datetime.today()


class Veiculo(DuckModel):
    objects = {}
    primary_key = 'placa'

    @classmethod
    def schema(cls) -> dict:
        return {
            'placa': str,
            'marca': Marca,
            'modelo': str,
            'cor': Cor,
            'ano': int,
            'km': float,
            'compra': datetime,
            'combustivel': Combustivel,
            'unico_dono': bool,
            'status': Status,
        }

    @classmethod
    def populate(cls, count: int):
        fake = Faker('pt_BR')
        # ------------------------------------
        def nunca_trocado(idade: int) -> bool:
            '''
            Retorna True se o dono nunca trocou de carro.
            '''
            chance = (1 / idade) if idade > 0 else 1
            # ... quanto mais velho, menor a chance
            return fake.boolean( min(100, chance*200) )
        # ------------------------------------
        while count:
            marca=fake.random_element(id for id in Marca)
            ano_fabricacao = fake.random_int(2000, HOJE.year)
            idade = HOJE.year - ano_fabricacao
            cls(
                placa=fake.license_plate(),
                marca=marca,
                modelo=fake.random_element(MODELOS[marca]),
                cor=fake.random_element(
                    cor for cor in Cor
                ),
                ano=ano_fabricacao,
                km=fake.random_number(4) * idade,
                compra=fake.date_between_dates(
                    date_start=datetime(ano_fabricacao, 1, 1),
                    date_end=HOJE
                ),
                combustivel=fake.random_element(
                    tipo for tipo in Combustivel
                ),
                unico_dono=nunca_trocado(idade),
                status=fake.random_element(
                    st for st in Status
                ),
            )
            count -= 1
        cls.save()

    @classmethod
    def to_display(cls) -> list[str]:
        return ['placa', 'marca', 'modelo', 'cor', 'ano']
