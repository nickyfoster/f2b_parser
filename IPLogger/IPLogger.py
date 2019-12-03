from ipwhois import IPWhois

# GET https://api.ipgeolocationapi.com/geolocate/0.0.0.0

class IPLogger:
    def __init__(self):
        self.obj = IPWhois("146.185.181.37")
        self.ret = self.obj.lookup_rdap(depth=1)
        print(self.ret['asn_country_code'])
        print(self.ret['asn_description'])

    def get_ip_from_log(self):
        pass

    def get_logfile(self):
        pass

    def get_ip_data(self, data):
        pass

    def save_ip_data(self):
        pass
