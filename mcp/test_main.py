from interface.server import (
    Server, ERR_UNEXPECTED_VALUE,
    ERR_WRONG_VALUE_TYPE, ERR_FIELD_NOT_EXISTS
)


def test_marca_desconhecida():
    error = Server.validation_error('marca', 'Peugeot')
    assert error == ERR_UNEXPECTED_VALUE

def test_km_invalido():
    error = Server.validation_error('km', 'mil')
    assert error == ERR_WRONG_VALUE_TYPE

def test_campo_inexistente():
    error = Server.validation_error('vr_venda', 53_900.00)
    assert error == ERR_FIELD_NOT_EXISTS

def test_sem_erros():
    error = Server.validation_error('placa', 'ABC1D23')
    assert error == 0
