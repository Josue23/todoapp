from todo import app, tarefas


def test_listar_tarefas_deve_retornar_status_200():
    with app.test_client() as cliente:
        resposta = cliente.get('/task')
        assert resposta.status_code == 200


def test_listar_tarefas_deve_ter_formato_json():
    with app.test_client() as cliente:
        resposta = cliente.get('/task')
        assert resposta.content_type == 'application/json'


def test_lista_de_tarefas_vazia_retorna_lista_vazia():
  with app.test_client() as cliente:
    resposta = cliente.get('/task')
    assert resposta.data == b'[]\n'
