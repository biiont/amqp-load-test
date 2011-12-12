#!/usr/bin/env python2.7
import sys
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('agatis1'))
channel = connection.channel()
channel.queue_declare(queue='hello')

print ' [*] Waiting for messages. To exit press CTRL+C'

i = 0

def callback(ch, method, properties, body):
    global i
    global last_evt
    global last_time
    global current_evt
    global current_time
    i += 1
    if i % 5000 == 0:
        last_evt = current_evt
        last_time = current_time
        current_evt = i
        current_time = time.time()
        speed = (current_evt - last_evt) / (current_time - last_time)
        print "Got %d events (%d msg/sec)" % (i, speed)
    if body == 'Quit.':
        print "Average speed %d msg/sec" % (last_evt / (current_time - start_time))
        sys.exit();

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
current_evt = 0
current_time = start_time = time.time()
channel.start_consuming()
