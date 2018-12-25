def connect():
    try:
        print("nodemcu wifi connect")
        import network

        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)

        ssid = "SSID"
        password = "PASSWORD"

        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect(ssid, password)
            while not sta_if.isconnected():
                pass
        print('network config:', sta_if.ifconfig())
    except:
        print("An  error occur while connecting the WIFI")
        return
