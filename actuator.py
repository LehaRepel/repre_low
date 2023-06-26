#! python
# -*- coding: utf-8 -*-
# noinspection PyPep8Naming
#
# This file is library for communication with Valco Instruments Co. Inc.
# Universal Electric Actuator
# Models EUH, EUD, and EUT
# Firmware revisions EQ and subsequent

import time

import logging
import serial
# import ports
# import config
import sys
# import redis
# from start.helper import get_redis_connect

"""import serial.tools.list_ports
list_of_ports = serial.tools.list_ports.comports()
for obj in list_of_ports:
    if obj.description.find('Actuator') == 0:
        actuator = obj.description[obj.description.find('COM'):-1]"""
# port = ports.actuator
# port = serial.Serial(port=ports.actuator,
#                      baudrate=115200,
#                      bytesize=serial.EIGHTBITS,
#                      parity=serial.PARITY_NONE,
#                      stopbits=serial.STOPBITS_ONE)
# port.close()


class Actuator:
    def __init__(self, port='ttyUSB0', baudrate=115200):
        self.device = serial.Serial(port=port,
                                    baudrate=baudrate,
                                    bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE)

    def transceiver(self, command: str):
        try:
            self.device.open()
        except Exception as e:
            print(e)
            time.sleep(0.1)
            self.device.open()
        """
        Функция посылает команду на Кран-переключатель и возвращает с него ответ
        """
        self.device.write(str.encode(command + '\r\n'))
        # config.logger.info(u'Xmit Actuator: %s.' % command)
        answer = ''
        while self.device.in_waiting == 0:
            time.sleep(0.1)
        while self.device.inWaiting() > 0:
            try:
                answer += self.device.read(1).decode()
            except Exception as e:
                print(e)
                time.sleep(0.1)
                answer += self.device.read(1).decode()
        # config.logger.info(u'Recv Actuator: %s.' % answer[0:-1])
        self.device.close()
        return answer

    def transmitter(self, command: str):
        """
        Функция посылает команду на Кран-переключатель без ожидания ответа
        """
        try:
            self.device.open()
        except Exception as e:
            print(e)
            time.sleep(0.1)
            self.device.open()
        self.device.write(str.encode(command + '\r\n'))
        # config.logger.info(u'Xmit Actuator: %s.' % command)
        self.device.close()

    def test(self):
        """
        Функция тестирования Крана-переключателя, в случае прохождения теста
        устанавливает Кран в положение 24(необходимо для тестирования Насоса)
        :return:
        """
        # config.logger.info(u'Start testing of actuator.')
        print("Test is started")
        ini_test = 0
        if not self.toggle_pos(1):
            ini_test += 1
            # config.logger.error(u'1')
        if not self.toggle_pos(13):
            ini_test += 2
            # config.logger.error(u'2')
        if self.get_moving_time() > 1800:
            ini_test += 4
            # config.logger.error(u'4')
        if not self.toggle_pos(20):
            ini_test += 8
            # config.logger.error(u'8')
        self.toggle_pos(position_number=24)
        # config.logger.info(u'Test is ended. ERROR STATUS: %s.' % ini_test)
        return ini_test

    def go_to_position(self, position_number: int):
        # config.logger.info(u'Going to position %s.' % position_number)
        self.transmitter("GO" + str(position_number))

    def get_current_pos(self, i):
        """
        Функция возвращает текущее положение Крана-переключателя
        :return:
        """
        if i < 5:
            # config.logger.info(u'Interrogating the position of the actuator.')
            try:
                answer = int(self.transceiver("CP").replace("CP", "").replace("\r", ""))
                return answer
            except Exception:
                i += 1
                self.get_current_pos(i)

    def get_moving_time(self):
        """
        Функция возвращает время последнего переключения Крана-переключателя
        :return:
        """
        # config.logger.info(u'Interrogation of the time spent on the previous '
        #                    u'switch.')
        return int(self.transceiver("TM").replace("TM", "").replace("\r", ""))

    def toggle_pos(self, position_number: int, i: int = 0):
        """
        Функция устанавливает Кран-переключатель в положение position_number и
        проверяет верно ли осуществленно переключение, путём возврата True
        или False
        """

        # connection_to_redis = redis.Redis(host='127.0.0.1', port=6379, db=1)
        # flow = '0'
        # while flow != '1':
        #     flow = connection_to_redis.hget("sensors", 'SA').decode()
        #     # print(flow)
        #     time.sleep(0.5)

        time.sleep(2)
        # config.logger.info(u'##### Moving the check switch. #####')
        self.go_to_position(position_number)
        if i < 10:
            if position_number == self.get_current_pos(0):
                # config.logger.info(u'##### The switch was successful. #####')
                return
            else:
                # config.logger.info(u'##### Switching was not successful. #####')
                self.toggle_pos(position_number, i=i + 1)
                return
        else:
            print("Actuator haven't completed last command")
            # config.logger.info(u'Actuator haven\'t completed last command')


if __name__ == "__main__":
    print('Started')

    # if len(sys.argv) > 1:
    #     print(len(sys.argv))
    #     if sys.argv[1] == 'test':
    #         print(sys.argv)
    #         config.set_config_to_main_logger()
    #         Test()
    #     elif sys.argv[1] == 'TogglePos':
    #         print("12")
    #         print(sys.argv)
    #         toggle_pos(int(sys.argv[2]))


