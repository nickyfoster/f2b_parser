import json
import socket
from influxdb import InfluxDBClient
import pygeohash as pgh
import urllib.request


class TCPServer:
    BUFFER_SIZE = 1024

    def __init__(self, host='127.0.0.1', port=7070):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.running = True
        self.data = None
        self.client = InfluxDBClient('0.0.0.0', port=8086, database='f2b_logs')

    def run_server(self):
        print(f"Starting TCP server on port {self.port}")
        self.sock.bind((self.host, self.port))
        self.sock.listen(10)
        conn, addr = self.sock.accept()
        print('connected:', addr)

        self.listen_socket(conn)

    def listen_socket(self, conn):
        while self.running:
            self.data = conn.recv(self.BUFFER_SIZE)
            if self.data:
                self.get_data(self.data)
        self.conn.close()
        print("Server stopped")

    def get_data(self, data):
        try:
            data = json.loads(data)
        except Exception as e:
            print(e)
            return None
        if "**NO MATCH**" in data.values():
            return None
        else:
            parsed_data = self.parse_data(data)
            self.update_db(parsed_data)

    def parse_data(self, data):
        with urllib.request.urlopen(f"https://api.ipgeolocationapi.com/geolocate/{data['ip']}") as url:
            ip_data = json.loads(url.read().decode())
            data['lat'] = ip_data['geo']['latitude']
            data['lon'] = ip_data['geo']['longitude']
            data['geohash'] = self.convert_latlon_to_geohash(data)
            return data

    def convert_latlon_to_geohash(self, data):
        return pgh.encode(latitude=data['lat'], longitude=data['lon'])

    def update_db(self, parsed_data):
        data = [{
            "measurement": "geossh",
            "fields": {
                "value": 1
            },
            "tags": {
                "geohash": parsed_data["geohash"],
                "username": parsed_data["username"],
                "port": parsed_data["port"],
                "ip": parsed_data["ip"]
            }
        }]
        self.client.write_points(points=data)


if __name__ == '__main__':
    server = TCPServer()
    server.run_server()
