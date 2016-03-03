from gpswrapper import gpspoller
from dbwrapper import dbwrapper
from car import car
import time
# import threading

# CONFIG
pollingDelay = 2
errorPollingDelay = 60
# ENDCONFIG

if __name__ == '__main__':
    gpsd = gpspoller.GpsPoller()
    obd = car.Car()
    dbWrapper = dbwrapper.DbWrapper('10.20.80.193', '8080', 'Admin', '1234')

    reg = "RJ46564"  # TODO: Hent registrering

    trip = {
        'tripid': reg + str(time.localtime()),
        'timestamp': time.localtime(),
        'car_name': reg,
        'data': {}
    }

    timeSinceErrorDetect = 0
    try:
        gpsd.start()
        # obd.start()
        obd.EnableFetch(obd.GetSupportedDataTypes())
        time.sleep(2)  # Data stabilization delay
        while True:
            error = ""
            if timeSinceErrorDetect > errorPollingDelay:
                error = obd.CheckForCarErrors()
                timeSinceErrorDetect = 0
            else:
                timeSinceErrorDetect += pollingDelay

            dataList = obd.FetchData()

            satelliteFix = gpsd.have_fix()
            data = {  # TODO: Finne ut om det er riktig måte å få tilgang til enumeratoren
                'latitude': str(gpsd.get_latitude() * satelliteFix),
                'longitude': str(gpsd.get_longitude() * satelliteFix),
                'fuel_status': dataList[obd.DataTypes.FuelStatus],
                'fuel_rate': dataList[obd.DataTypes.FuelRate],
                'engine_load': dataList[obd.DataTypes.EngineLoad],
                'rpm': dataList[obd.DataTypes.RPM],
                'speed': dataList[obd.DataTypes.Speed],
                'throttle_position': dataList[obd.DataTypes.ThrottlePosition],
                'run_time': dataList[obd.DataTypes.RunTime],
                'intake_air_temp': dataList[obd.DataTypes.IntakeAirTemp],
                'outside_air_temp:': dataList[obd.DataTypes.OutsideAirTemp],
                'oil_temp': dataList[obd.DataTypes.OilTemp],
                'error': error

            }

            trip['timestamp'] = time.localtime()
            trip['data'] = data

            dbWrapper.send(trip)

            time.sleep(pollingDelay)

    except (KeyboardInterrupt, SystemExit):
        print("\nKilling Thread...")
        gpsd.disconnect()
        # car.disconnect()
