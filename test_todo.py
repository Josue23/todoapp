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
        'descricao': 'descricao'}),
        content_type='application/json')
    # é realizada a análise e transformação para objeto python da resposta
    data = json.loads(resposta.data.decode('utf-8'))
    assert data['id'] == 1
    assert data['titulo'] == 'titulo'
    assert data['descricao'] == 'descricao'
    # qaundo a comparação é com True, False ou None, utiliza-se o "is"
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


def test_listar_tarefas_deve_apresentar_tarefas_nao_finalizadas_primeiro():
    tarefas.clear()
    tarefas.append({'id': 1, 'titulo': 'tarefa 1', 'descricao': 'tarefa de numero 1',
                    'estado': True})
    tarefas.append({'id': 2, 'titulo': 'tarefa 2', 'descricao': 'tarefa de numero 2',
                    'estado': False})
    with app.test_client() as cliente:
        resposta = cliente.get('/task')
        data = json.loads(resposta.data.decode('utf-8'))
        primeira_task, segunda_task = data
        assert primeira_task['titulo'] == 'tarefa 2'
        assert segunda_task['titulo'] == 'tarefa 1'


# Removendo tarefas
def test_deletar_tarefa_utiliza_verbo_delete():
    tarefas.clear()
    with app.test_client() as cliente:
        resposta = cliente.delete('/task/1')
        assert resposta.status_code != 405


def test_remover_tarefa_existente_retorna_204():
    tarefas.clear()
    tarefas.append({'id': 1, 'titulo': 'titulo',
                    'descricao': 'descricao', 'estado': False})
    cliente = app.test_client()
    resposta = cliente.delete('/task/1', content_type='application/json')
    assert resposta.status_code == 204
    assert resposta.data == b''


def test_remover_tarefa_existente_remove_tarefa_da_lista():
    tarefas.clear()
    tarefas.append({'id': 1, 'titulo': 'titulo',
                    'descricao': 'descricao', 'estado': False})
    cliente = app.test_client()
    cliente.delete('/task/1', content_type='application/json')
    assert len(tarefas) == 0


def test_remover_tarefa_nao_existente():
    tarefas.clear()
    cliente = app.test_client()
    resposta = cliente.delete('/task/1', content_type='application/json')
    assert resposta.status_code == 404


# Detalhando tarefas
def test_detalhar_tarefa_existente():
    tarefas.clear()
    tarefas.append({'id': 1, 'titulo': 'titulo',
                    'descricao': 'descricao', 'entregue': False})
    cliente = app.test_client()
    resposta = cliente.get('/task/1', content_type='application/json')
    data = json.loads(resposta.data.decode('utf-8'))
    assert resposta.status_code == 200
    assert data['id'] == 1
    assert data['titulo'] == 'titulo'
    assert data['descricao'] == 'descricao'
    assert data['entregue'] is False


def test_detalhar_tarefa_nao_existente():
    tarefas.clear()
    cliente = app.test_client()
    resposta = cliente.get('/task/1', content_type='application/json')
    assert resposta.status_code == 404


# Entregando tarefas
def test_atualizando_uma_tarefa_existente():
    tarefas.clear()
    tarefas.append({'id': 1, 'titulo': 'titulo',
                    'descricao': 'descricao', 'estado': False})
    cliente = app.test_client()
    resposta = cliente.put('/task/1', data=json.dumps(
        {'titulo': 'titulo atualizado',
         'descricao': 'descricao atualizada', 'estado': True}
    ),
        content_type='application/json')
    data = json.loads(resposta.data.decode('utf-8'))
    assert resposta.status_code == 200
    assert data['id'] == 1
    assert data['titulo'] == 'titulo atualizado'
    assert data['descricao'] == 'descricao atualizada'
    assert data['estado'] is True


def test_atualizando_uma_tarefa_nao_existente():
    tarefas.clear()
    cliente = app.test_client()
    resposta = cliente.put('/tarefa/1', data=json.dumps(
        {'titulo': 'titulo atualizado',
         'decricao': 'descricao atualizada', 'estado': True}
    ),
        content_type='application/json')
    assert resposta.status_code == 404


def test_atualizando_uma_tarefa_com_campos_invalidos():
    tarefas.clear()
    tarefas.append({'id': 1, 'titulo': 'titulo',
                    'descricao': 'descricao', 'estado': False})
    cliente = app.test_client()
    # sem estado
    resposta = cliente.put('/tarefa/1', data=json.dumps(
        {'titulo': 'titulo atualizado',
         'decricao': 'descricao atualizada'}
    ),
        content_type='application/json')
    assert resposta.status_code == 400
    # sem descrição
    resposta = cliente.put('/tarefa/1', data=json.dumps(
        {'titulo': 'titulo atualizado',
         'estado': False}
    ),
        content_type='application/json')
    assert resposta.status_code == 400
    # sem titulo
    resposta = cliente.put('/tarefa/1', data=json.dumps(
        {'descricao': 'descricao atualizado',
         'estado': False}
    ),
        content_type='application/json')
    assert resposta.status_code == 400
