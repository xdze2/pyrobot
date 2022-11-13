

from rich.pretty import pprint
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


data_filepath = "./data.txt"

print(f'Read file {data_filepath}...', flush=True)
data = np.loadtxt(data_filepath, delimiter = "\t", comments="#")
print(f"{len(data)} lines", flush=True)

time_sec = data[:, 0] * 1e-6


plt.figure()
plt.plot(time_sec, data[:, 1], label="ax");
plt.plot(time_sec, data[:, 2], label="ay");
plt.plot(time_sec, data[:, 3], label="az");
plt.legend();
plt.xlabel('time [sec]'); plt.ylabel('acc [mg]');
graph_path = f"{Path(data_filepath).stem}.png"
plt.tight_layout();
plt.savefig('graph.png');
print(f"Graph saved to {graph_path}")



dt = np.diff(time_sec)
print('dt avg (sec)=', np.mean(dt))
print('dt min', np.min(dt))
print('dt max', np.max(dt))



def dbl_integrate(x):
    zero = np.mean(x[:100])
    return np.cumsum(np.cumsum(x - zero))

plt.figure()
plt.plot(dbl_integrate(data[:, 1]), label="x");
plt.plot(dbl_integrate(data[:, 2]), label="y");
plt.plot(dbl_integrate(data[:, 3]), label="z");
plt.legend();
plt.xlabel('time [sec]'); plt.ylabel('pos [m]');
graph_path = f"{Path(data_filepath).stem}.png"
plt.tight_layout();
plt.savefig('graph_x.png');
print(f"Graph saved to {graph_path}")