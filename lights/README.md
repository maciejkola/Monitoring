This is the way of visualizing Icinga2 status on a traffic lights / tower light indicator.
The script should be run from cron on a raspberry pi. It conects to Icinga2 API and then checks the overall status. If there is any alert/warning/unknown - it lights proper bulb.

Tower Lights:
![alt text](https://github.com/maciejkola/Monitoring/blob/master/lights/lights.jpg)

Box inside:
![alt text](https://github.com/maciejkola/Monitoring/blob/master/lights/box_inside.jpg)

Scheme:
![alt text](https://github.com/maciejkola/Monitoring/blob/master/lights/scheme.png)
