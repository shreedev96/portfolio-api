from fastapi.testclient import TestClient
from main import app
from dotenv import load_dotenv
import os

client=TestClient(app)

load_dotenv()
API_KEY=os.getenv("SECRET_API_KEY")

def test_read_root():

    response=client.get('/')

    assert response.status_code==200
    assert response.json()=={"message":"Welcome to the Investment Portfolio API!"}
    

def test_get_investment():

    fake_investment = {
        "name": "Apple Stock",
        "type": "Stock",
        "amount": 500
    }

    create_response = client.post(
        "/investment/add",
        json=fake_investment
    )

    created_data = create_response.json()
    investment_id = created_data["data"]["id"]
    response = client.get(f"/investment/{investment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == investment_id
    assert data["name"] == fake_investment["name"]

def test_create_investment():

    fake_investment={
        "name": "Test Google Stock",
        "type": "Stock",
        "amount": 250.50
    }

    response=client.post('/investment/add',json=fake_investment)

    assert response.status_code==200
    data=response.json()
    investment=data["data"]
    assert investment["name"]==fake_investment["name"]
    assert investment["investment_type"]==fake_investment["type"]
    assert investment["amount"]==fake_investment["amount"]
    assert "id" in investment

def test_delete_investment():

    fake_investment = {
        "name": "Delete Test",
        "type": "Stock",
        "amount": 100
    }
    create_response = client.post(
        "/investment/add",
        json=fake_investment
    )
    created_data = create_response.json()
    investment_id = created_data["data"]["id"]
    headers = {
        "x-api-key": API_KEY
    }
    response = client.delete(
        f"/investment/delete/{investment_id}",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Deleted the investment"

def test_get_invalid_investment():

    response = client.get("/investment/999999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Investment not found"

def test_delete_with_invalid_api_key():
    headers = {
        "x-api-key": "wrong_key"
    }
    response = client.delete("/investment/delete/1",headers=headers
    )
    assert response.status_code == 401

def test_delete_without_api_key():

    response = client.delete("/investment/delete/1")
    assert response.status_code == 401

def test_create_invalid_investment():

    fake_investment = {
        "name": "Invalid Investment"
    }
    response = client.post("/investment/add",json=fake_investment)
    assert response.status_code == 422

def test_update_investment():

    fake_investment = {
        "name": "Old Stock",
        "type": "Stock",
        "amount": 100
    }

    create_response = client.post(
        "/investment/add",
        json=fake_investment
    )

    investment_id = create_response.json()["data"]["id"]
    updated_data = {
        "name": "Updated Stock",
        "type": "ETF",
        "amount": 500
    }
    response = client.put(f"/investment/update/{investment_id}",json=updated_data)
    assert response.status_code == 200

def test_update_invalid_investment():

    updated_data = {
        "name": "Updated",
        "type": "ETF",
        "amount": 500
    }

    response = client.put("/investment/update/999999",json=updated_data)
    assert response.status_code == 404

def test_export_csv():

    response = client.get("/investment/exportToCsv")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "attachment" in response.headers["content-disposition"]

def test_get_all_investments():

    response = client.get("/investment/getAll")
    assert response.status_code == 200
    data = response.json()
    assert "investments" in data
    