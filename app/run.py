from vehicle_manager import VehicleManager, Vehicle


if __name__ == '__main__':
    manager = VehicleManager(url='https://test.tspb.su/test-task')

    # point 1
    print('1. Get all vehicles:')
    print(manager.get_vehicles(), '\n')

    # point 2
    print('2. Filter vehicles:')
    print(manager.filter_vehicles(year=2019, color='red'), '\n')

    # point 3
    print('3. Get vehicle by id:')
    print(manager.get_vehicle(id=1), '\n')

    # point 4 - there is an API error: doesn't work without id
    print('4. Add new vehicle:')
    print(manager.add_vehicle(Vehicle(
        #id=333,
        name='Toyota',
        model='Camry',
        year=2022,
        color='black',
        price=22000,
        latitude=55.753215,
        longitude=37.620393)
    ), '\n')

    # point 5
    print('5. Update vehicle by id:')
    print(manager.update_vehicle(Vehicle(
        id=1,
        name='Toyota',
        model='Camry',
        year=2022,
        color='silver',
        price=22222,
        latitude=55.753215,
        longitude=37.620393
    )), '\n')

    # point 6
    print('6. Delete vehicle by id:')
    print(manager.delete_vehicle(id=1), '\n')

    # point 7
    print('7. Get Distance between the vehicles:')
    print('Distance between Camry and Sorento:')
    print(manager.get_distance(id1=1, id2=10), '\n')
    print('Distance between Camry and Tesla:')
    print(manager.get_distance(id1=1, id2=18), '\n')

    # point 8
    print('8. Get the nearest vehicle to the vehicle by id:')
    print('The nearest vehicle to Camry:')
    print(manager.get_nearest_vehicle(id=1), '\n')
