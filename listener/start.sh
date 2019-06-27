nohup python UDPListener.py > /root/server/UDPListener.log  2>&1 &
nohup celery -A tasks worker -l info  > /root/server/celery.log  2>&1 &