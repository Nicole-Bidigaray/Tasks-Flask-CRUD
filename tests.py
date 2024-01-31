import pytest
import requests

#  CRUD
BASE_URL = 'http://127.0.0.1:5000'
tasks = []

def test_create_task():
  new_task_data = {
    "title": "Nova tarefa",
    "description": "Descrição da nova tarefa"
  }
  response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
  assert response.status_code == 200
  response_json = response.json()
  assert "id" in response_json
  task_id = response_json['id']
  assert response_json.get("message") == "Nova tarefa criada com sucesso"
  
  # Verificar se a tarefa foi adicionada corretamente
  response = requests.get(f"{BASE_URL}/tasks/{task_id}")
  assert response.status_code == 200
  task = response.json()
  assert task["title"] == new_task_data["title"]
  assert task["description"] == new_task_data["description"]
  tasks.append(task_id)  # Adicionando ID para uso em outros testes
  
def test_get_tasks():
  response = requests.get(f"{BASE_URL}/tasks")
  assert response.status_code == 200
  response_json = response.json()
  assert "tasks" in response_json
  assert isinstance(response_json["tasks"], list)
  assert response_json["total_tasks"] == len(response_json["tasks"])
  # Verificar estrutura de uma tarefa
  if response_json["tasks"]:
    task = response_json["tasks"][0]
    assert "id" in task
    assert "title" in task
    assert "description" in task
    assert "completed" in task
  
def test_get_task():
  # Criar uma nova tarefa
  new_task_data = {
    "title": "Tarefa para Teste GET",
    "description": "Descrição para Teste GET"
  }
  response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
  assert response.status_code == 200  # 200 é o código para criação bem-sucedida
  task_id = response.json()['id']
  
  # Solicitar a tarefa específica
  response = requests.get(f"{BASE_URL}/tasks/{task_id}")
  assert response.status_code == 200
  task = response.json()
  assert task['id'] == task_id
  assert task['title'] == new_task_data['title']
  assert task['description'] == new_task_data['description']
  
  # Teste para um ID de tarefa inexistente
  response = requests.get(f"{BASE_URL}/tasks/999999")  # Assumindo que 999999 é um ID inválido
  assert response.status_code == 404  # 404 Not Found para IDs inválidos
    
def test_update_task():
    if tasks:
        task_id = tasks[0]
        payload = {
            "title": "Tarefa Atualizada",
            "description": "Descrição atualizada",
            "completed": True
        }
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json

        # Verificando se a tarefa foi realmente atualizada
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['title'] == payload['title']
        assert response_json['description'] == payload['description']
        assert response_json['completed'] == payload['completed']
        
def test_delete_task():
    if tasks:
        task_id = tasks[0]
        # Deletar a tarefa
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code in [200, 204]  # 200 OK ou 204 No Content

        # Verificar se a tarefa foi realmente removida
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404

        # Remover o ID da tarefa da lista para manter a consistência
        tasks.remove(task_id)

    # Teste para deletar uma tarefa inexistente
    response = requests.delete(f"{BASE_URL}/tasks/999999")  # ID inexistente
    assert response.status_code == 404
