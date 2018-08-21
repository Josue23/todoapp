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


def test_criar_tarefa_aceita_post():
  with app.test_client() as cliente:
    resposta = cliente.post('/task')
    assert resposta.status_code != 405


def test_criar_tarefa_retorna_tarefa_inserida():
  tarefas.clear()
  cliente = app.test_client()
  # realiza a requisição utilizando o verbo POST
  resposta = cliente.post('/task', data=json.dumps({
    'titulo': 'titulo',
    'descricao': 'descricao'
  }),
  content_type='application/json'
  )
  # é realizada a análise e transformação para objeto python da resposta
  data = json.loads(resposta.data.decode('utf-8'))
  assert data['id'] == 1
  assert  data['titulo'] == 'titulo'
  assert data['descricao'] == 'descricao'
  # quando a comparação é com True, False ou None, utiliza-se o "is"
  assert data['estado'] is False


def test_criar_tarefa_codigo_de_status_retornado_deve_ser_201():
    with app.test_client() as cliente:
        resposta = cliente.post('/task', data=json.dumps({
            'titulo': 'titulo',
            'descricao': 'descricao'}),
            content_type='application/json')
        assert resposta.status_code == 201


def test_criar_tarefa_insere_elemento_no_banco():
    tarefas.clear()
    cliente = app.test_client()
    # realiza a requisição utilizando o verbo POST
    cliente.post('/task', data=json.dumps({
        'titulo': 'titulo',
        'descricao': 'descricao'}),
        content_type='application/json')
    assert len(tarefas) > 0


def test_criar_tarefa_sem_descricao():
    cliente = app.test_client()
    # o código de status deve ser 400 indicando um erro do cliente
    resposta = cliente.post('/task', data=json.dumps({'titulo': 'titulo'}),
                            content_type='application/json')
    assert resposta.status_code == 400


def test_criar_tarefa_sem_titulo():
    cliente = app.test_client()
    # o código de status deve ser 400 indicando um erro do cliente
    resposta = cliente.post('/task', data=json.dumps(
        {'descricao': 'descricao'}),
        content_type='application/json')
    assert resposta.status_code == 400
