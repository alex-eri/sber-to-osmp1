class Kassa:
    def __init__(self, port, rate):
        devices = pyshtrih.discovery(discovery_callback, port, rate)
        if not devices:
            raise Exception('No devices')
        device = devices[0]
        device.connect()
        self.device = device

    def bill(row):
        s = row['sum']
        s = int(s) * 100
        a = row['account']
        device.open_check(0)
        device.sale(
            (u'Оплата по л/с %s' % a, 1, s), tax1=1
        )
        device.close_check(s)

