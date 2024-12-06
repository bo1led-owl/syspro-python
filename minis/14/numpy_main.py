import matplotlib.pyplot as plt
import numpy as np
import game
import sys
import time

NUM_ITER = 128
field = np.array(game.readField(sys.argv[1]))

start = time.time()
for _ in range(NUM_ITER):
    field = np.array(game.step(field))
end = time.time()
print(f"{end - start}s")

img = plt.imshow(
    list(map(lambda row: list(map(lambda c: not c, row)), field)), cmap="gray"
)
plt.show()
