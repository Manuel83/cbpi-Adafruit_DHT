# -*- coding: utf-8 -*-
from modules import cbpi
from modules.core.hardware import  SensorPassive
from modules import cbpi
from modules.core.props import Property

import Adafruit_DHT

@cbpi.sensor
class AdafruitDHTSensor(SensorPassive):


    gpio = Property.Select("GPIO", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], description="GPIO to which the actor is connected")
    type = Property.Select("TYPE", options=["humidity", "temperature"])

    def get_unit(self):
        '''
        :return: Unit of the sensor as string. Should not be longer than 3 characters
        '''

        if self.type == "humidity":
            return "%"
        if self.type == "temperature":
            return "°C"

    def read(self):
        
        self.api.app.logger.info("Read Adafruit_DHT")
        self.api.app.logger.info("GPIO %s type %s" % (self.gpio, self.type))
        try:
            sensor = Adafruit_DHT.DHT22
            pin = int(self.gpio)
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            self.api.app.logger.info(humidity)
            self.api.app.logger.info(temperature)
            if self.type == "humidity":
                self.data_received(round(humidity, 2))
            if self.type == "temperature":
                if self.get_config_parameter("unit", "C") == "C":
                    self.data_received(round(temperature, 2))
                else:
                    self.data_received(round(9.0 / 5.0 * temperature + 32, 2))                
        except Exception as e:
            self.api.app.logger.error("Adafruit_DHT ERROR")
