from flask import Flask, render_template, redirect
import Crypto 
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from pyfirmata import Arduino
from pyfirmata import util
import Adafruit_DHT
from wyliodrin import *
from time import sleep
import os
import random
import requests
from base64 import b64decode,b64encode

# server
template_dir = os.path.abspath('/wyliodrin')
app = Flask(__name__, template_folder = template_dir)

# arduino
board = Arduino('/dev/ttyACM0')
reader = util.Iterator(board)
reader.start()

# dht11 temp + umiditate
sensor = Adafruit_DHT.DHT11
pin_temp_humid = 16
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_temp_humid)

# umid sol
pin_humid = board.get_pin("a:0:o")

# luminozitate
pin_potent = board.get_pin("a:1:o")

# date
@app.route('/current')
def current():
    humidity_soil = None
    humidity_air = None
    luminosity = None
    temperature = None
    
    if (humidity_soil == None) :
        val = pin_humid.read()
        if (val != None) :
            humidity_soil = (val / 3.3) * 100
        else: 
            humidity_soil = -3 # random() * 100
            
    print(humidity_soil)
    
    if (luminosity == None) :
        val = pin_potent.read()
        if (val != None) :
            luminosity = val * 100
        else: 
            luminosity = -3 # random() * 100
            
    print(luminosity)
    
    if (humidity_air == None or temperature == None) :
        humidity_air, temperature = Adafruit_DHT.read_retry(sensor, pin_temp_humid)
        
    print(temperature)
    print(humidity_air)
    
    payload = {
                'luminosity': luminosity,
                'humidity_soil': humidity_soil, 
                'humidity_air' : humidity_air, 
                'temperature': temperature
    }
    
    r = requests.get(http-address, verify = True)
    msg = r.text
    private_key_file = location-of-file-in-system
    f = open(private_key_file, 'rb')
    key_from_file = f.read()
    decoded_key = b64decode(key_from_file)
    publicKey = RSA.importKey(decoded_key)
    cipher = Cipher_PKCS1_v1_5.new(publicKey)
    msg = msg.encode('UTF-8')
    print type(msg)
    enc = cipher.encrypt(msg)
    f.close()
    requests.post(http-address, verify=True, data = enc)
    return render_template('current.html', hs = humidity_soil, ha = humidity_air, l = luminosity, t = temperature)

if __name__ == '__main__':
   app.run(ip-address, debug = True)
    
