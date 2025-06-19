import json
from app import app
from models import db, Plant

class TestPlant:
    '''Flask application in app.py'''

    def test_plants_get_route(self):
        '''has a resource available at "/plants".'''
        response = app.test_client().get('/plants')
        assert response.status_code == 200

    def test_plants_get_route_returns_list_of_plant_objects(self):
        '''returns JSON representing Plant objects at "/plants".'''
        with app.app_context():
            p = Plant(name="Douglas Fir", image="https://example.com/fir.jpg", price=100.00)
            db.session.add(p)
            db.session.commit()

            response = app.test_client().get('/plants')
            data = json.loads(response.data.decode())

            assert isinstance(data, list)
            assert any(isinstance(record, dict) and 'id' in record and 'name' in record for record in data)

            db.session.delete(p)
            db.session.commit()

    def test_plants_post_route_creates_plant_record_in_db(self):
        '''allows users to create Plant records through the "/plants" POST route.'''
        response = app.test_client().post(
            '/plants',
            json={
                "name": "Live Oak",
                "image": "https://example.com/live_oak.jpg",
                "price": 250.00,
            }
        )

        assert response.status_code == 201 or response.status_code == 200  # depending on implementation

        with app.app_context():
            plant = Plant.query.filter_by(name="Live Oak").first()
            assert plant is not None
            assert plant.name == "Live Oak"
            assert plant.image == "https://example.com/live_oak.jpg"
            assert plant.price == 250.00

            db.session.delete(plant)
            db.session.commit()

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        with app.app_context():
            p = Plant(name="Maple", image="https://example.com/maple.jpg", price=120.00)
            db.session.add(p)
            db.session.commit()

            response = app.test_client().get(f'/plants/{p.id}')
            assert response.status_code == 200

            db.session.delete(p)
            db.session.commit()

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        with app.app_context():
            p = Plant(name="Cedar", image="https://example.com/cedar.jpg", price=180.00)
            db.session.add(p)
            db.session.commit()

            response = app.test_client().get(f'/plants/{p.id}')
            data = json.loads(response.data.decode())

            assert isinstance(data, dict)
            assert data["id"] == p.id
            assert data["name"] == "Cedar"

            db.session.delete(p)
            db.session.commit()

                