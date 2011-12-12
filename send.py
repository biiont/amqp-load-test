#!/usr/bin/env python2.7
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('agatis1'))
channel = connection.channel()
channel.queue_declare(queue='hello')

current_evt = 0
current_time = start_time = time.time()
for i in range(0, 1000000):
    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
    if i % 5000 == 0:
        last_evt = current_evt
        last_time = current_time
        current_evt = i
        current_time = time.time()
        speed = (current_evt - last_evt) / (current_time - last_time)
        print "Send event %d (%d msg/sec)" % (i, speed)

print "Average speed %d msg/sec" % (last_evt / (current_time - start_time))

channel.basic_publish(exchange='',
                  routing_key='hello',
                  body='Quit.')

connection.close()
