	
OUTDIR = ./bin

imu: imu.c
	gcc -o $(OUTDIR)/imu -l pigpiod_if2 mpu_fct.c imu.c

graph:
	python graph.py