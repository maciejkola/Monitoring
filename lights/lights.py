#!/usr/bin/env python

import json
import requests
import urllib3
urllib3.disable_warnings()

import RPi.GPIO as GPIO
from time import sleep

import syslog

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

red = 16
yellow = 20
green = 21

def ASK_API_FOR_STATUS():
        # we need to ask API only about HARD states
        # SOFT states are too often switching to red (performance variations, timeouts, etc)
        # HARD state means that icinga has checked 5 times that service is in alert/warning (from 1-4 check it is only SOFT alarm)
        # curl -u <username:pass> -k -H 'X-HTTP-Method-Override: GET' -X POST -d '{"filter": "service.state == 2 && service.state_type == 1 " }' 'https://<icinga_url>:5665/v1/objects/services' | python -m json.tool

        # service.state can be 0 (normal), 1 (warning) or 2 (alert) and there is even 3 (unknown)
        # service.state_type=1 means it is a HARD check

        # we should ignore when service.state is 1 or 2 and service.state_type is 0
        # because that means that there is some problem, but the check is SOFT
        # moreover, "service.acknowledgement != 1" means that we want to show status of a service which was not acknowledged
        # once someone acknowledge a service state, it is no longer alarm for us

        url_services = 'https://<icinga_url>:5665/v1/objects/services'
        url_hosts = 'https://<icinga_url>:5665/v1/objects/hosts'

        user = 'xxx'
        password = 'xxx'

        #First, check for ALERTS:
        alert_payload_services = { "filter": "service.state == 2 && service.state_type == 1 && service.acknowledgement != 1" }
        alerts_response_services = requests.get(url=url_services, auth=(user, password), verify=False, timeout=20, json=alert_payload_services)
        data_services = alerts_response_services.json()

        alert_payload_hosts = { "filter": "host.state == 2 && host.state_type == 1 && host.acknowledgement != 1" }
        alerts_response_hosts = requests.get(url=url_hosts, auth=(user, password), verify=False, timeout=20, json=alert_payload_hosts)
        data_hosts = alerts_response_hosts.json()

        if data_services["results"] != [] or data_hosts["results"] != []:
                status = "red"
                return status


        # check for UNKNOWN - unfortunately icinga2 has a bug (feature?) and unknown SOFT state is recognize immidiately as a HARD
        # to limit unwanted alerts maybe I will need to comment this check in the future:
        unknown_payload_services = { "filter": "service.state == 3 && service.state_type == 1 && service.acknowledgement != 1" }
        unknown_response_services = requests.get(url=url_services, auth=(user, password), verify=False, timeout=20, json=unknown_payload_services)
        data_services = unknown_response_services.json()

        unknown_payload_hosts = { "filter": "host.state == 3 && host.state_type == 1 && host.acknowledgement != 1" }
        unknown_response_hosts = requests.get(url=url_hosts, auth=(user, password), verify=False, timeout=20, json=unknown_payload_hosts)
        data_hosts = unknown_response_hosts.json()

        if data_services["results"] != [] or data_hosts["results"] != []:
                status = "red"
                return status


        warning_payload_services = { "filter": "service.state == 1 && service.state_type == 1 && service.acknowledgement != 1" }
        warnings_response_services = requests.get(url=url_services, auth=(user, password), verify=False, timeout=20, json=warning_payload_services)
        data_services = warnings_response_services.json()

        warning_payload_hosts = { "filter": "host.state == 1 && host.state_type == 1 && host.acknowledgement != 1" }
        warnings_response_hosts = requests.get(url=url_hosts, auth=(user, password), verify=False, timeout=20, json=warning_payload_hosts)
        data_hosts = warnings_response_hosts.json()

        if data_services["results"] != [] or data_hosts["results"] != []:
                status = "yellow"
                return status


        normal_payload_services = { "filter": "service.state == 0 && service.state_type == 1 " }
        normal_response_services = requests.get(url=url_services, auth=(user, password), verify=False, timeout=20, json=normal_payload_services)
        data_services = normal_response_services.json()

        normal_payload_hosts = { "filter": "host.state == 0 && host.state_type == 1 " }
        normal_response_hosts = requests.get(url=url_hosts, auth=(user, password), verify=False, timeout=20, json=normal_payload_hosts)
        data_hosts = normal_response_hosts.json()

        if data_services["results"] != [] and data_hosts["results"] != []:
                status = "green"
                return status

def TURN_LIGHT(color):
        GPIO.setup(red, GPIO.OUT)
        GPIO.setup(yellow, GPIO.OUT)
        GPIO.setup(green, GPIO.OUT)

        if color == "red":
                GPIO.output(red, True)
                GPIO.output(yellow, False)
                GPIO.output(green, False)

        elif color == "yellow":
                GPIO.output(red, False)
                GPIO.output(yellow, True)
                GPIO.output(green, False)

        elif color == "green":
                GPIO.output(red, False)
                GPIO.output(yellow, False)
                GPIO.output(green, True)

        # if status API is something different somehow, we need to light up alaram:
        else:
                GPIO.output(red, True)
                GPIO.output(yellow, False)
                GPIO.output(green, False)


try:
        status = ASK_API_FOR_STATUS()
except requests.exceptions.ConnectionError:
        syslog.syslog("Looks like there is a problem with accessing API")
        print("Looks like there is a problem with accessing API")
        status = "red"
except requests.exceptions.Timeout:
        syslog.syslog("Timeout accessing API")
        print("Timeout accessing API")
        status = "red"

print "Status is %s" % status
TURN_LIGHT(status)
