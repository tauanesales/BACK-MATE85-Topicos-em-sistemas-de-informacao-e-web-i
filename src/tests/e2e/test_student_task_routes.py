import pytest
from core.application import client
from core.base_student_task import (
    alternative_description,
    alternative_name,
    completed,
    completion_date,
    deadline_date,
    description,
    last_notified,
    name,
    student_form,
    task_id,
)

valid_form = {
    "nome": name,
    "descricao": description,
    "completada": completed,
    "data_prazo": deadline_date,
    "last_notified": last_notified,
    "data_conclusao": completion_date,
}
student_id = None


@pytest.mark.dependency()
def test_create_task():
    """
    Test route for creating a new task.
    """
    global student_id

    url = "/tarefas/"

    # Must have at least one student at the database for testing task routes.
    response = client.post("/alunos/", json=student_form)
    assert 200 <= response.status_code <= 299

    student_id = response.json()["id"]
    valid_form["aluno_id"] = student_id

    # Test sending a form with bad information.
    invalid_form_cases = [
        {"nome": ""},  # Empty name
        {"nome": " " * 20},  # Blank name
        {"nome": "N"},  # Short name
    ]
    for invalid_form in invalid_form_cases:
        form = valid_form.copy()
        form.update(invalid_form)

        assert client.post(url, json=form).status_code >= 400

    # Test sending a incomplete form.
    for key in valid_form.keys():
        if valid_form[key] is None:
            continue

        form = valid_form.copy()
        form.pop(key)

        assert client.post(url, json=form).status_code >= 400

    # Test sending a valid form.
    assert 200 <= client.post(url, json=valid_form).status_code <= 299

    # Test sending an alternative valid form.
    form = valid_form.copy()
    form["nome"] = alternative_name
    form["descricao"] = alternative_description
    assert 200 <= client.post(url, json=form).status_code <= 299

    # Test sending the same form but for a student that does NOT exists on database.
    form = valid_form.copy()
    form["aluno_id"] = student_id + 10**4
    assert client.post(url, json=form).status_code >= 400


@pytest.mark.dependency(depends=["test_create_task"])
def test_get_task():
    """
    Test route for getting the task from the database.
    """
    expected = {"nome": name, "descricao": description, "aluno_id": student_id}

    response = client.get(f"/tarefas/{task_id}")
    assert 200 <= response.status_code <= 299

    result = response.json()

    for key, value in expected.items():
        assert result.get(key, "") == value


@pytest.mark.dependency(depends=["test_create_task"])
def test_get_tasks_by_student_id():
    """
    Test route for getting the tasks from the database by the ID of a student.
    """
    expected = [
        {"nome": name, "descricao": description, "aluno_id": student_id},
        {
            "nome": alternative_name,
            "descricao": alternative_description,
            "aluno_id": student_id,
        },
    ]

    response = client.get(f"/tarefas/aluno/{student_id}")
    assert 200 <= response.status_code <= 299

    result = sorted(response.json(), key=lambda x: x["id"])

    for row in range(len(result)):
        for key, value in expected[row].items():
            assert result[row].get(key, "") == value


@pytest.mark.dependency(depends=["test_create_task"])
def test_update_task():
    """
    Test route for updating the task's information on the database.
    """
    url = f"/tarefas/{task_id}"

    new_data = {
        "nome": "Th1s is 4 nic3 s#per ultr@ titl3!! =)",
        "descricao": "Th1s is 4 nic3 s#per ultr@ d3scr1ption!! =)",
    }

    # Update user's information.
    form = valid_form.copy()
    form.update(new_data)

    response = client.put(url, json=form)
    assert 200 <= response.status_code <= 299

    # Get the user's information and check the changes.
    response = client.get(url)
    assert 200 <= response.status_code <= 299

    result = response.json()

    for key, value in new_data.items():
        assert result.get(key, "") == value


@pytest.mark.dependency(depends=["test_create_task"])
def test_delete_task():
    """
    Test route for deleting the task from the database.
    """
    url = f"/tarefas/{task_id}"

    # Try to get the user.
    response = client.get(url)
    assert 200 <= response.status_code <= 299

    # Update user's information.
    response = client.delete(url)
    assert 200 <= response.status_code <= 299

    # Try to get the deleted user.
    response = client.get(url)
    assert response.status_code >= 400