import csv
import urllib.request
import sys
import datetime
import xml.etree.ElementTree as ET

prefix = ""

host = "billing.example.com"
path = "cgi-bin/osmp.cgi"

url_base = "http://{host}/{path}".format(host=host,path=path)

check = "command=check&account={account}&txn_id={txn_id}&sum={sum}"
pay = "command=pay&account={account}&txn_id={txn_id}&sum={sum}&txn_date={txn_date:%Y%m%d%H%M%S}"

#txn_date=20090815120133

filename = sys.argv[1]

print('Loading %s' % filename)

def push(to,row):
    q = to.format(**row)
    url = '?'.join([url_base,q])
    print(url)
    try:
        re = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print('[http {}]'.format(e.code))
        return
    data = re.read().decode()
    print(data)
    try:
        root = ET.fromstring(data)
    except:
        print('[bad xml]')
        return

    assert root.tag == 'response', 'bad format'
    code = int(root.find('result').text)
    assert code == 0, 'Status %s' % code
    return True




def parse(row):

    row['txn_id'] = prefix + row['txn_id']
    row['txn_date'] = datetime.datetime.strptime( "%s %s" % (row['date'], row['time']), '%d-%m-%Y %H-%M-%S')
    row['sum'] = row['sum'].replace(',','.')

    print(row['txn_date'], row['account'])

    try:
        print('check', end=' ')
        push(check,row)
        print('[ok]')
    except Exception as e:
        print('[failed]', end='')
        print(e)
        return
    try:
        print('pay', end=' ')
        push(pay,row)
        print('[ok]')
    except Exception as e:
        print('[failed]', end=' ')
        print(e)



fieldnames = [
    'date',
    'time',
    'no_ot',
    'no_kas',
    'txn_id',
    'account',
    'fio',
    'address',
    'sum',
    'sum2',
    'commission'
]

import codecs

with codecs.open(filename,encoding='cp1251') as csvfile:
    reader = csv.DictReader(csvfile,fieldnames=fieldnames,delimiter=';')
    for row in reader:
        if "=" in row['date']:
            continue
        parse(row)
