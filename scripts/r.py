



import time

import asyncio
import rx
from rx.scheduler.eventloop import AsyncIOScheduler

import rx.operators as op
async_loop = asyncio.get_event_loop()

scheduler = AsyncIOScheduler(async_loop)

# def gen():
#     for k in range(10):
#         time.sleep(0.5)
#         yield k

# test = rx.from_iterable(gen(), scheduler=scheduler)

test = rx.interval(1., scheduler=scheduler)

print('done')
test.subscribe(
   lambda x: print("The value is {0}".format(x)),
   on_error = lambda e: print("Error : {0}".format(e)),
   on_completed = lambda: print("Job Done!"),
   scheduler=scheduler
)

test.pipe(op.delay(1.4), op.map(lambda x:x**2)).subscribe(
   lambda x: print("The square is {0}".format(x)),
   on_error = lambda e: print("Error : {0}".format(e)),
   on_completed = lambda: print("Job Done!"),
   scheduler=scheduler
)


test2 = rx.interval(3., scheduler=scheduler)

print('done')
test2.subscribe(
   lambda x: print("The 2 value is {0}".format(x)),
   on_error = lambda e: print("Error : {0}".format(e)),
   on_completed = lambda: print("Job Done!"),
   scheduler=scheduler
)




async_loop.run_forever()
print("done")
async_loop.close()
# input("Press Enter key to exit\n")