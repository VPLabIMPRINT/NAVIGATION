import numpy as np
from scipy.io import loadmat,savemat

annots = loadmat("data/color150.mat")
print(annots['colors'])

colors = [[0,0,0],[255,255,255]]
count = -1
for a in annots['colors']:
	count += 1
	if count <= 1:
		continue
	else:
		colors.append(a.tolist())

annots['colors'] = np.array(colors).astype(np.uint64)
savemat('data/color150_binary_new.mat',annots)