# QRcode generator
import pyqrcode
patient = pyqrcode.create('5bbb4bf7cff920610d27b6f8')
patient.png('patient.png', scale=8)
print(patient.terminal(quiet_zone=1))


# QRcode Decoder

from PIL import Image
import zbarlight
file_path = '/home/hash/drone/learn/patient.png'
with open(file_path, 'rb') as image_file:
    image = Image.open(image_file)
    image.load()
codes = zbarlight.scan_codes(['qrcode'], image)
print('QR codes: %s' % codes)
