
from rich.pretty import pprint
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt



def integrate(x):
    zero = np.mean(x[:100])
    return np.cumsum(x - zero)


def dbl_integrate(x):
    zero = np.mean(x[:100])
    return np.cumsum(np.cumsum(x - zero))



data_filepath = "./data.txt"

print(f'Read file {data_filepath}...', flush=True)
data = np.loadtxt(data_filepath, delimiter = "\t", comments="#")
print(f"{len(data)} lines", flush=True)

time_sec = data[:, 0] * 1e-6


wz =  data[:, 7]

axy = data[:, 1]**2 + data[:, 2]**2

def moving_average(x, w: int):
    return np.convolve(x, np.ones(w), 'valid') / w


# Acc
plt.figure()
for k in [1000, 500, 250, 50]:
    plt.plot(moving_average(wz, k), label=f"wz {k}", alpha=0.5, linewidth=1);

plt.legend();
plt.xlabel('time [sec]'); plt.ylabel('wz');
graph_path = f"{Path(data_filepath).stem}_wz.png"
plt.tight_layout();
plt.savefig(graph_path);
print(f"Graph saved to {graph_path}")



# Acc
plt.figure()
for k in [1000, 500, 250, 50]:
    plt.plot(moving_average(axy, k), label=f"wz {k}", alpha=0.5, linewidth=1);

plt.legend();
plt.xlabel('time [sec]'); plt.ylabel('axy');
graph_path = f"{Path(data_filepath).stem}_axy.png"
plt.tight_layout();
plt.savefig(graph_path);
print(f"Graph saved to {graph_path}")