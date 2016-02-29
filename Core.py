
# import gpspoller
# import icar
# import dbwrapper
import time
import threading

if __name__ == '__main__':
    # gpsp = GpsPoller()
    # TODO: Hent data fra icar
    # dbWrapper = DbWrapper('10.20.80.193', '8080', 'Admin', '1234')

    reg = "RJ46564"  # TODO: Hent registrering

    trip = {
        'tripid': reg + str(time.localtime()),
        'timestamp': time.localtime(),
        'car_name': reg,
        'data': {}
    }
    try:
        # gpsp.start()
        while True:
            time.sleep(2)  # Data stabilization delay

            # satelliteFix = 0 if gpsd.fix.mode==1 else 1
            data = {
                # 'latitude': str(gpsd.fix.latitude * satelliteFix),
                # 'longitude': str(gpsd.fix.longitude * satelliteFix),
                # 'fuel_status': ,
                # 'fuel_rate': ,
                # 'engine_load': ,
                # 'rpm': ,
                # 'speed': ,
                # 'throttle_position': ,
                # 'run_time': ,
                # 'intake_air_temp': ,
                # 'outside_air_temp: ,
                # 'oil_temp':
            }

            trip['timestamp'] = time.localtime()
            trip['data'] = data

            # dbWrapper.send(trip)

            time.sleep(2)

    except (KeyboardInterrupt, SystemExit):
        print("\nKilling Thread...")
        # gpsp.running = False
        # gpsp.join()





