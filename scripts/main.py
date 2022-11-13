import asyncio

import numpy as np
import pigpio
import rx
import rx.operators as op
from rx.scheduler.eventloop import AsyncIOScheduler

from pyrobot.drive import Mobility
from pyrobot.gpio_mapping import SonarGpio
from pyrobot.hardware.sonar import UltraSoundSensor
from pyrobot.rgb_leds import ColorMap, HsvColor, RgbUnderlighting

gpio = pigpio.pi()

distance_sensor = UltraSoundSensor(
    gpio_echo=SonarGpio.ECHO, gpio_trig=SonarGpio.TRIG, gpio=gpio
)

mob = Mobility()


cm = ColorMap(0, 1500, "gist_heat")
leds = RgbUnderlighting()


async_loop = asyncio.get_event_loop()
scheduler = AsyncIOScheduler(async_loop)


print("init done")

distance_measure = rx.interval(0.100, scheduler=scheduler).pipe(
    op.map(lambda t: (t, distance_sensor.measure_cm())),
    op.scan(lambda acc, x: (x[0], 0.5 * acc[1] + 0.5 * x[1])),  # moving average
)
(
    distance_measure.pipe(
        op.buffer_with_time(0.5), op.map(lambda grp: np.mean([u[1] for u in grp]))
    ).subscribe(
        lambda dist_avg: leds.change_color(cm.get_rgb(dist_avg), "front"),
        on_error=lambda e: print("Error : {0}".format(e)),
        on_completed=lambda: print("Job Done!"),
        scheduler=scheduler,
    )
)
distance_measure.subscribe(
    lambda x: print(x),
)


# test.pipe(op.delay(1.4), op.map(lambda x:x**2)).subscribe(
#    lambda x: print("The square is {0}".format(x)),
#    on_error = lambda e: print("Error : {0}".format(e)),
#    on_completed = lambda: print("Job Done!"),
#    scheduler=scheduler
# )


# test2 = rx.interval(3., scheduler=scheduler)

# print('done')
# test2.subscribe(
#    lambda x: print("The 2 value is {0}".format(x)),
#    on_error = lambda e: print("Error : {0}".format(e)),
#    on_completed = lambda: print("Job Done!"),
#    scheduler=scheduler
# )


async_loop.run_forever()
print("done")
async_loop.close()
