import os
my_path = '/media/vplab/My Passport/Sadbhavana/IMPRINT/VPOD/test/'
dirs = os.listdir(my_path)
# sub_dirs = os.listdir(os.path.join(my_path, dirs))
sets = []
# sets=[('1043','train'), ('1044','train')]
# print(type(sets[0]))

for file in dirs:
        sets.append((file , 'train'))

print(sets)
print(len(sets))