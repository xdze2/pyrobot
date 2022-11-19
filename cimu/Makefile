	
OUTDIR = ./bin

imu: imu.c
	gcc -o $(OUTDIR)/imu -l pigpiod_if2 imu.c

graph:
	python graph.py