import pyshtrih

def discovery_callback(*a,**kw):
    print(a)
    print(kw)

class Kassa:
    def __init__(self, port, rate):
        devices = pyshtrih.discovery(discovery_callback, port, rate)
        if not devices:
            raise Exception('No devices')
        device = devices[0]
        device.connect()
        self.device = device

    def bill(self, row):
        s = row['sum']
        s = int(s) * 100
        a = row['account']

        cashier = pyshtrih.FD({1021: u'Кассир: Лебедева С.Н.'})
        self.device.open_check(0)
        self.device.send_tlv_struct(cashier.dump())
        self.device.sale(
            (u'Расчетный счёт л/с%s' % a, 1000, s)
        )
        self.device.close_check(payment_type4=s)

