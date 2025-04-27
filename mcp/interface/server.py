from dados.veiculo import Veiculo
from enum import Enum


ERR_FIELD_NOT_EXISTS = 1
ERR_WRONG_VALUE_TYPE = 2
ERR_UNEXPECTED_VALUE = 3


class Server:

    @staticmethod
    def validation_error(field: str, value) -> int:
        schema = Veiculo.schema()
        field_type = schema.get(field)
        if not field_type:
            return ERR_FIELD_NOT_EXISTS
        try:
            field_type(value)
            return 0
        except:
            if field_type.__base__ == Enum:
                return ERR_UNEXPECTED_VALUE
            return ERR_WRONG_VALUE_TYPE

    def __init__(self, **args):
        """
        Recebe a requisição, interpreta os critérios enviados 
        pelo cliente e consulta o banco de dados.
        """
        for key, value in args.items():
            error = self.validation_error(key, value)
            if error:
                raise ValueError(
                    f"Error ({error}): {value} is not a valid value for the field {key}"
                )
        self.data = Veiculo.find(**args)
