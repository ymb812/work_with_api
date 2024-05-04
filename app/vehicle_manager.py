import requests
import math


class Vehicle:
    def __init__(self, id=None, name=None, model=None, year=None, color=None, price=None, latitude=None,
                 longitude=None):
        self.id = id
        self.name = name
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f'<Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>'


class VehicleManager:
    def __init__(self, url):
        self.url = url


    def api_request(self, method: str, endpoint: str | int, data=None):
        if method == 'GET':
            response = requests.get(f'{self.url}/{endpoint}')
        elif method == 'POST':
            response = requests.post(f'{self.url}/{endpoint}', json=data)
        elif method == 'PUT':
            response = requests.put(f'{self.url}/{endpoint}', json=data)
        elif method == 'DELETE':
            response = requests.delete(f'{self.url}/{endpoint}')
            return response

        else:
            raise Exception(f'Unexpected method {method}')
        return response.json()


    def get_vehicles(self):
        return [Vehicle(**vehicle_data) for vehicle_data in self.api_request('GET', 'vehicles')]


    def filter_vehicles(self, **kwargs):
        filtered_vehicles = []

        vehicles = self.get_vehicles()
        for vehicle in vehicles:
            matched = True

            for key, value in kwargs.items():
                if hasattr(vehicle, key):
                    if getattr(vehicle, key) != value:
                        matched = False
                        break
                else:
                    matched = False
                    break

            if matched:
                filtered_vehicles.append(vehicle)

        return filtered_vehicles


    def get_vehicle(self, id: int):
        return Vehicle(**self.api_request('GET', f'vehicles/{id}'))


    def add_vehicle(self, vehicle: Vehicle):
        data = vars(vehicle)
        return Vehicle(**self.api_request('POST', 'vehicles', data))


    def update_vehicle(self, vehicle: Vehicle):
        data = vars(vehicle)
        return Vehicle(**self.api_request('PUT', f'vehicles/{vehicle.id}', data))


    def delete_vehicle(self, id: int):
        return self.api_request('DELETE', f'vehicles/{id}')


    def get_distance(self, id1: int = None, id2: int = None, vehicle1: Vehicle = None, vehicle2: Vehicle = None):
        if (not id1 or not id2) and (not vehicle1 or not vehicle2):
            raise Exception('One pair of params is needed')

        if not vehicle1:
            vehicle1 = Vehicle(**self.api_request('GET', f'vehicles/{id1}'))

        if not vehicle2:
            vehicle2 = Vehicle(**self.api_request('GET', f'vehicles/{id2}'))

        lat1, lon1 = vehicle1.latitude, vehicle1.longitude
        lat2, lon2 = vehicle2.latitude, vehicle2.longitude
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = math.sin(delta_lat / 2) * math.sin(delta_lat / 2) + math.cos(math.radians(lat1)) * math.cos(
            math.radians(lat2)) * math.sin(delta_lon / 2) * math.sin(delta_lon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return 6371000 * c


    def get_nearest_vehicle(self, id):
        nearest_vehicle = None
        min_distance = float('inf')

        vehicles = self.get_vehicles()
        target_vehicle = self.get_vehicle(id=id)
        if not target_vehicle:
            return None

        for vehicle in vehicles:
            if vehicle.id != id:
                dist = self.get_distance(vehicle1=target_vehicle, vehicle2=vehicle)
                if dist < min_distance:
                    min_distance = dist
                    nearest_vehicle = vehicle

        return nearest_vehicle
