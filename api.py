import requests


class LightTracker:

    def __init__(self, device_id='70B3D5E75E0036AB'):
        self.token = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIyIiwiYXV0aCI6WyJVU0VSX1JFQUQiLCJVU0VSX1VQREFURSIsIlVTRVJfQ1JFQVRFIiwiVVNFUl9ERUxFVEUiLCJSVUxFX1JFQUQiLCJSVUxFX1VQREFURSIsIlJVTEVfQ1JFQVRFIiwiUlVMRV9ERUxFVEUiLCJERVZJQ0VfUkVBRCIsIkRFVklDRV9VUERBVEUiLCJERVZJQ0VfQ1JFQVRFIiwiREVWSUNFX0RFTEVURSIsIkRFVklDRV9UWVBFX1JFQUQiLCJERVZJQ0VfVFlQRV9VUERBVEUiLCJERVZJQ0VfVFlQRV9DUkVBVEUiLCJERVZJQ0VfVFlQRV9ERUxFVEUiLCJST0xFX1JFQUQiLCJST0xFX1VQREFURSIsIlJPTEVfQ1JFQVRFIiwiUk9MRV9ERUxFVEUiLCJEQVNIQk9BUkRfUkVBRCIsIkRBU0hCT0FSRF9VUERBVEUiLCJEQVNIQk9BUkRfQ1JFQVRFIiwiREFTSEJPQVJEX0RFTEVURSIsIlJFUE9SVF9SRUFEIiwiUkVQT1JUX1VQREFURSIsIlJFUE9SVF9DUkVBVEUiLCJSRVBPUlRfREVMRVRFIiwiUE9JTlRfUkVBRCIsIlBPSU5UX1VQREFURSIsIlBPSU5UX0NSRUFURSIsIlBPSU5UX0RFTEVURSIsIk5PVElGSUNBVElPTl9SRUFEIiwiTU9CSUxFX1JFQUQiLCJURU1QTEFURV9SRUFEIiwiVEVNUExBVEVfVVBEQVRFIiwiVEVNUExBVEVfQ1JFQVRFIiwiVEVNUExBVEVfREVMRVRFIl0sImNvbnRleHQiOjEsInJvbGUiOjIsImV4cCI6MTU0NDEwMTcxM30.v5OmQcdMSeX_nx4NzUVhnLyBFZbm0_3jllhlZPN_wRScziZnbrgzg9_i26Pagfbme6jNLpv4h6Y5m5WMQygrTA'

        self.final_token = 'Bearer ' + self.token
        self.headers = {
          'Accept': '*/*',
          'Authorization': self.final_token
        }

        self.params_post = {
            'deviceId': device_id
        }

        self.data = {
          'command': 'ON'
        }

    def check_if_detected(self):
        r = requests.get('https://api-sbb.wolkabout.com/api/devices/70B3D54995B37FEA', params={}, headers=self.headers)
        dict_json = r.json()
        car_detected = next(item for item in dict_json['feeds'] if item["reference"] == "carDetected")
        return car_detected['value'] == "true"

    def reserve(self):
        self.data = {'command': 'ON'}
        while self.check_if_detected():
            pass

        response = requests.post('https://iot-starterkit-kd-iot.app.sbb-aws.net/downlink/message',
                                 params=self.params_post,
                                 data=self.data)
        return response

    def confirm(self):
        self.data = {'command': 'OFF'}
        while not self.check_if_detected():
            pass

        response = requests.post('https://iot-starterkit-kd-iot.app.sbb-aws.net/downlink/message',
                                 params=self.params_post,
                                 data=self.data)
        return response
