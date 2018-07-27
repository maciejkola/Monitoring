#!/usr/bin/python

# author: mkola

# to add new check:
# 1. update "printonly" function
# 2. update "sendonly" function

import smtplib
import syslog
import sys
import datetime
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from subprocess import Popen,PIPE,STDOUT


#### EDIT THOSE LINES ####
MAILSERVER = ''
MAILSERVER_PORT = ''
LOGIN = ''
PASSWORD = ""
FROM = ''

RECIPIENTS = ['']
# multiple recipients:
#RECIPIENTS = ['yyy@yyy.com', 'xxx@xx.com']
##########################



TODAY = datetime.date.today()
TIME = datetime.datetime.now()



def check_plugin(name, command):
        out = Popen(command,stderr=STDOUT,stdout=PIPE)
        NOTES = out.communicate()[0]
        RETURN_CODE = out.returncode
        CHECK_NAME = name

        if RETURN_CODE == 0:
            CELL_COLOR="white"
            STATUS="OK"
        elif RETURN_CODE == 1:
            CELL_COLOR="yellow"
            STATUS="WARNING"
        elif RETURN_CODE == 2:
            CELL_COLOR="red"
            STATUS="CRITICAL"
        else:
            CELL_COLOR="purple"
            STATUS="UNKNOWN"
        return '<td bgcolor="%s">%s</td><td bgcolor="%s">%s</td><td bgcolor="%s">%s</td>' % (CELL_COLOR, CHECK_NAME, CELL_COLOR, STATUS, CELL_COLOR, NOTES)


def get_plugin_status(plugin):
        NORMAL=0
        WARN=0
        CRIT=0
        UNKNWN=0
        if ">OK<" in str(plugin):
                NORMAL=1
        if ">WARNING<" in str(plugin):
                WARN=1
        if ">CRITICAL<" in str(plugin):
                CRIT=1
        if ">UNKNOWN<" in str(plugin):
                UNKNWN=1

        return [NORMAL, WARN, CRIT, UNKNWN]



def printonly():
        NORMAL_COUNT = 0
        WARNING_COUNT = 0
        CRITICAL_COUNT = 0
        UNKNOWN_COUNT = 0

        plugin_output = check_plugin("Memcached (in PHP 7.0 config)", ["/usr/lib64/nagios/plugins/check_memcached.sh", "/opt/plesk/php/7.0/bin/php"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]


        plugin_output = check_plugin("Root Partition", ["/usr/lib64/nagios/plugins/check_disk", "-w", "10%", "-c", "2%", "-p", "/"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        plugin_output = check_plugin("Plesk Partition", ["/usr/lib64/nagios/plugins/check_disk", "-w", "10%", "-c", "2%", "-p", "/var/www"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        plugin_output = check_plugin("Boot Partition", ["/usr/lib64/nagios/plugins/check_disk", "-w", "10%", "-c", "2%", "-p", "/boot"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        plugin_output = check_plugin("Apache Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "httpd"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        plugin_output = check_plugin("Nginx Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "nginx"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        plugin_output = check_plugin("Named Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "named"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        plugin_output = check_plugin("Supervisord Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "supervisord"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        plugin_output = check_plugin("Postfix Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "master"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        plugin_output = check_plugin("NTP Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "ntpd"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        plugin_output = check_plugin("Memcached Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "memcached"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        plugin_output = check_plugin("MySQL Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "mysqld"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        plugin_output = check_plugin("CPU Usage", ["/usr/lib64/nagios/plugins/check_linux_stats.pl", "-C", "-w", "90", "-c", "99", "-s", "3"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        plugin_output = check_plugin("RAM Usage", ["/usr/lib64/nagios/plugins/check_memory.pl"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        plugin_output = check_plugin("OS Updates", ["/usr/lib64/nagios/plugins/check_yum.py"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        plugin_output = check_plugin("Last DB Backup", ["/usr/lib64/nagios/plugins/check_db_backup.py"])
        print plugin_output
        plugin_status =  get_plugin_status(plugin_output)
        print plugin_status
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        print "----------------------------------------------"
        if CRITICAL_COUNT > 0:
                print "Overall status is CRITICAL"
                print [NORMAL_COUNT, WARNING_COUNT, CRITICAL_COUNT, UNKNOWN_COUNT]
        elif UNKNOWN_COUNT > 0:
                print "Overall status is UNKNOWN"
                print [NORMAL_COUNT, WARNING_COUNT, CRITICAL_COUNT, UNKNOWN_COUNT]
        elif WARNING_COUNT > 0:
                print "Overall status is WARNING"
                print [NORMAL_COUNT, WARNING_COUNT, CRITICAL_COUNT, UNKNOWN_COUNT]
        elif NORMAL_COUNT > 0:
                print "Overall status is NORMAL"
                print [NORMAL_COUNT, WARNING_COUNT, CRITICAL_COUNT, UNKNOWN_COUNT]
        else:
                print "Overall status is UNKNOWN"
                print [NORMAL_COUNT, WARNING_COUNT, CRITICAL_COUNT, UNKNOWN_COUNT]




def printandsend():
        NORMAL_COUNT = 0
        WARNING_COUNT = 0
        CRITICAL_COUNT = 0
        UNKNOWN_COUNT = 0

        MEMCACHED_PHP = check_plugin("Memcached (in PHP 7.0 config)", ["/usr/lib64/nagios/plugins/check_memcached.sh", "/opt/plesk/php/7.0/bin/php"])
        plugin_status =  get_plugin_status(MEMCACHED_PHP)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]


        DISK_ROOT = check_plugin("Root Partition", ["/usr/lib64/nagios/plugins/check_disk", "-w", "10%", "-c", "2%", "-p", "/"])
        plugin_status =  get_plugin_status(DISK_ROOT)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        DISK_PLESK = check_plugin("Plesk Partition", ["/usr/lib64/nagios/plugins/check_disk", "-w", "10%", "-c", "2%", "-p", "/var/www"])
        plugin_status =  get_plugin_status(DISK_PLESK)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        DISK_BOOT = check_plugin("Boot Partition", ["/usr/lib64/nagios/plugins/check_disk", "-w", "10%", "-c", "2%", "-p", "/boot"])
        plugin_status =  get_plugin_status(DISK_BOOT)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        APACHE = check_plugin("Apache Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "httpd"])
        plugin_status =  get_plugin_status(APACHE)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        NGINX = check_plugin("Nginx Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "nginx"])
        plugin_status =  get_plugin_status(NGINX)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        NAMED = check_plugin("Named Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "named"])
        plugin_status =  get_plugin_status(NAMED)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        SUPERVISORD = check_plugin("Supervisord Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "supervisord"])
        plugin_status =  get_plugin_status(SUPERVISORD)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        POSTFIX = check_plugin("Postfix Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "master"])
        plugin_status =  get_plugin_status(POSTFIX)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        NTPD = check_plugin("NTP Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "ntpd"])
        plugin_status =  get_plugin_status(NTPD)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        MEMCACHED = check_plugin("Memcached Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "memcached"])
        plugin_status =  get_plugin_status(MEMCACHED)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        MYSQLD = check_plugin("MySQL Service", ["/usr/lib64/nagios/plugins/check_procs", "-c", "1:", "-C", "mysqld"])
        plugin_status =  get_plugin_status(MYSQLD)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        CPU = check_plugin("CPU Usage", ["/usr/lib64/nagios/plugins/check_linux_stats.pl", "-C", "-w", "90", "-c", "99", "-s", "3"])
        plugin_status =  get_plugin_status(CPU)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        RAM = check_plugin("RAM Usage", ["/usr/lib64/nagios/plugins/check_memory.pl"])
        plugin_status =  get_plugin_status(RAM)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        UPDATES = check_plugin("OS Updates", ["/usr/lib64/nagios/plugins/check_yum.py"])
        plugin_status =  get_plugin_status(UPDATES)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        DB_BACKUP = check_plugin("Las DB Backup", ["/usr/lib64/nagios/plugins/check_db_backup.py"])
        plugin_status =  get_plugin_status(DB_BACKUP)
        NORMAL_COUNT = NORMAL_COUNT + plugin_status[0]
        WARNING_COUNT = WARNING_COUNT + plugin_status[1]
        CRITICAL_COUNT = CRITICAL_COUNT + plugin_status[2]
        UNKNOWN_COUNT = UNKNOWN_COUNT + plugin_status[3]

        if CRITICAL_COUNT > 0:
                SUBJECT_STATUS = "CRITICAL"
        elif UNKNOWN_COUNT > 0:
                SUBJECT_STATUS = "UNKNOWN"
        elif WARNING_COUNT > 0:
                SUBJECT_STATUS = "WARNING"
        elif NORMAL_COUNT > 0:
                SUBJECT_STATUS = "NORMAL"
        else:
                SUBJECT_STATUS = "UNKNOWN"

        SUBJECT = SUBJECT_STATUS + ": Daily health status " + TODAY.strftime('%d, %b %Y')

        html = """\
        <html>
                <head></head>
                <body>
                        <p>""" +str(TIME)+ """</p>
                        <table style="width:100%" border="1">
                        <tr>
                                <td width="20%"><b>Item</b></td>
                                <td width="10%"><b>Status</b></td>
                                <td width="70%"><b>Notes</b></td>
                                </tr>

                        <tr>
                                """ +str(MEMCACHED_PHP)+ """
                        </tr>

                        <tr>
                                """ +str(DISK_ROOT)+ """
                        </tr>

                        <tr>
                                """ +str(DISK_PLESK)+ """
                        </tr>

                        <tr>
                                """ +str(DISK_BOOT)+ """
                        </tr>

                        <tr>
                                """ +str(APACHE)+ """
                        </tr>

                        <tr>
                                """ +str(NGINX)+ """
                        </tr>

                        <tr>
                                """ +str(NAMED)+ """
                        </tr>

                        <tr>
                                """ +str(SUPERVISORD)+ """
                        </tr>

                        <tr>
                                """ +str(POSTFIX)+ """
                        </tr>

                        <tr>
                                """ +str(NTPD)+ """
                        </tr>

                        <tr>
                                """ +str(MEMCACHED)+ """
                        </tr>

                        <tr>
                                """ +str(MYSQLD)+ """
                        </tr>

                        <tr>
                                """ +str(CPU)+ """
                        </tr>

                        <tr>
                                """ +str(RAM)+ """
                        </tr>

                        <tr>
                                """ +str(UPDATES)+ """
                        </tr>

                        <tr>
                                """ +str(DB_BACKUP)+ """
                        </tr>

                        </table>
                </body>
        </html>
        """

        message = MIMEMultipart('alternative')
        message['Subject'] = SUBJECT
        message['From'] = FROM
        message['To'] = ", ".join(RECIPIENTS)
        body = MIMEText(html, 'html')

        message.attach(body)

        try:
                server = smtplib.SMTP(MAILSERVER, MAILSERVER_PORT)
                server.starttls()
                server.login(LOGIN, PASSWORD)
                server.sendmail(FROM, RECIPIENTS, message.as_string())
                server.quit()
        except smtplib.SMTPException as e:
                syslog.syslog("Error: %s while connecting to %s port %s" % (str(e), mailserver, mailserver_port))
                print("Error: %s while connecting to %s port %s" % (str(e), mailserver, mailserver_port))
                sys.exit(1)





parser=argparse.ArgumentParser(
    description='''Check System Health ''',
    epilog=""" """)
parser.add_argument('--printonly', action='store_true', help='Print status, without sending anything')
parser.add_argument('--sendonly', action='store_true', help='Send status as e-mail')
args=parser.parse_args()

if not len(sys.argv) > 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

if args.printonly:
        printonly()

if args.sendonly:
        printandsend()
