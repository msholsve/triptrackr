from gpswrapper import gpspoller
from dbwrapper import dbwrapper
#from car import carsim as car
from car import car
import datetime, time, json

# CONFIG
pollingDelay = 1.5
errorPollingDelay = 20
debug = False
carDataNames={
    car.Car.DataTypes.FuelStatus:           'fuel_status',
    car.Car.DataTypes.FuelLevel:            'fuel_level',
    car.Car.DataTypes.FuelRate:             'fuel_rate',
    car.Car.DataTypes.EngineLoad:           'engine_load',
    car.Car.DataTypes.EngineCoolantTemp:    'coolant_temp',
    car.Car.DataTypes.IntakePreassure:      'intake_pressure',
    car.Car.DataTypes.FuelRailPressure:     'fuel_pressure',
    car.Car.DataTypes.RPM:                  'rpm',
    car.Car.DataTypes.Speed:                'speed',
    car.Car.DataTypes.ThrottlePosition:     'throttle_position',
    car.Car.DataTypes.RunTime:              'run_time',
    car.Car.DataTypes.IntakeAirTemp:        'intake_air_temp',
    car.Car.DataTypes.OutsideAirTemp:       'outside_air_temp',
    car.Car.DataTypes.OilTemp:              'oil_temp',
}
# ENDCONFIG


if __name__ == '__main__':
    gpsd = gpspoller.GpsPoller()
    obd = car.Car()
    obdFetchEnabled = False
    if not obd.connected:
        print('OBD not connected on startup.')

    dbWrapper = dbwrapper.DbWrapper('10.20.80.193', '8080', 'Admin', '1234')

    reg = "RJ46564"  # TODO: Hent registrering

    timeStamp = str(datetime.datetime.now())

    trip = {
        'tripid': '{0}:{1}'.format(reg,timeStamp),
        'timestamp': timeStamp,
        'car_name': reg,
        'data': {}
    }
    error = []
    timeSinceErrorDetect = errorPollingDelay+1
    try:
        while True:
            if not obdFetchEnabled and obd.connected:
                obd.enableFetch(obd.getSupportedDataTypes())
                obdFetchEnabled = True

            if timeSinceErrorDetect > errorPollingDelay:
                if obd.connected:
                    error = obd.checkForCarErrors()
                timeSinceErrorDetect = 0
            else:
                timeSinceErrorDetect += pollingDelay

            carDataList = {}
            if obd.connected:
                carDataList = obd.fetchData()

            satelliteFix = gpsd.gotSatLink()
            position = gpsd.getPosition()
            data = {
                'time': str(gpsd.getTime()),
                'latitude': str(position[0] * satelliteFix),
                'longitude': str(position[1] * satelliteFix),
                'error': error
            }

            for dataType, value in carDataList.items():
                data[carDataNames[dataType]] = value[0]

            trip['timestamp'] = str(datetime.datetime.now())
            trip['data'] = data

            if debug:
                print(json.dumps(trip, sort_keys=True, indent=4))
            dbWrapper.send(trip)
            if debug:
                print("Data sent!")

            if not obd.connected:
                obd.Reconnect()
            time.sleep(pollingDelay)

    except (KeyboardInterrupt, SystemExit):
        print("\nKilling Thread...")
        obd.close()
        gpsd.disconnect()
