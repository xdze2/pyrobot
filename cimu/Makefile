	
OUTDIR = ./bin

imu: imu.c
	gcc -o $(OUTDIR)/imu -l pigpiod_if2 mpu_fct.c imu.c


imuZ: imuZ.c
	gcc -o $(OUTDIR)/imuZ -l pigpiod_if2 mpu_fct.c imuZ.c

graph:
	python graph.py


format:
	clang-format -i imuZ.c
	clang-format -i mpu_fct.c
	clang-format -i mpu_fct.h