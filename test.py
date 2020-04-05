import json 
import RPi.GPIO as GPIO
from time import sleep
from os import system
from time import time

if __name__ == '__main__':
    #definicja poczatkowa diod
    zie = 36
    zol = 38
    czer = 40
    diodes = [zie, zol, czer]
    GPIO.setmode(GPIO.BOARD)

    for diode in diodes:
        GPIO.setup(diode, GPIO.OUT)
    
    init = True
    
    while (True):
        if int(time()%900) == 0 or init:
            init = False
            
            #zapal wszyskie
            for i in range(5):
            	for diode in diodes:
            	    GPIO.output(diode, GPIO.HIGH)
            	    sleep(0.3)
            	    GPIO.output(diode, GPIO.LOW)
            
            #pobierz dane i je przeanalizuj
            system('curl -X GET --header "Accept: application/json" --header "apikey: BZ3ZjjK5QepQjwFcL24iIuEJ0R3gPkHn" "https://airapi.airly.eu/v2/measurements/installation?installationId=13109" > output.txt')
            file = open('output.txt')
            json_data = file.read()
            file.close()
            
            parsed_json = (json.loads(json_data))
            status = parsed_json['current']['indexes'][0]['level']
            print(status)
            
            #zgas, zapal wszystkie
            for diode in diodes:
                GPIO.output(diode, GPIO.HIGH)
            sleep(1)    
            for diode in diodes:
                GPIO.output(diode, GPIO.LOW)
            
            #zapal odpowiednia
            if status == 'VERY_LOW':
                GPIO.output(zie, GPIO.HIGH)
            
            if status == 'LOW':
                GPIO.output(zie, GPIO.HIGH)
                GPIO.output(zol, GPIO.HIGH)    
            
            if status == 'MEDIUM':
                #zolty
                GPIO.output(zol, GPIO.HIGH)    
            
            if status == 'HIGH':
                #czer
                GPIO.output(czer, GPIO.HIGH)    
            
            if status == 'VERY_HIGH':
                GPIO.output(czer, GPIO.HIGH)    
            
            if status == 'EXTREME':
                GPIO.output(czer, GPIO.HIGH)    
            
            if status == 'AIRMAGEDON':
                GPIO.output(czer, GPIO.HIGH)    
            
            
        sleep(0.2)    
        
