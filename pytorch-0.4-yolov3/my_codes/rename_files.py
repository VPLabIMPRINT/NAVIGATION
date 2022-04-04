# This code is for renaming all the files inside the target folder by 
# appending folder name as the preefix of the original file name


import os
from os.path import isfile, join

mypath = "metadata/"
dirs = os.listdir(mypath)
print(dirs)

for dir in dirs:
    print(dir)
    files  = os.listdir(os.path.join(mypath,dir))
    print(files)     # accessing the folders inside mypath
    for file in files:
    #     # print(file)
    #     # subfile = os.listdir(os.path.join(mypath, dir, file))
    #     # print(subfile)

        
        if file.startswith("JPEG"):
            # print("InsideJPEG")
            # do something
            i = 1
            for imgs in os.listdir(os.path.join(mypath, dir, file)): # gets all images inside the folders subfolder(subdire)
                # print(os.path.join(mypath, dir, file, imgs) , mypath + dir + '_' + imgs)

                # os.rename(os.path.join(mypath, dir, file, imgs), os.path.join(mypath, dir, file, dir + '_' + imgs))
                i += 1
                print(i)
    #         # print(sub_dir)
    #         # print(isfile(join(mypath, file, sub_dir)))
    #             # print(list_files)
        elif file.startswith("Ann"):
            # do something
            # j = 1
            for annos in os.listdir(os.path.join(mypath, dir, file)):
                os.rename(os.path.join(mypath, dir, file, annos), os.path.join(mypath, dir, file, dir + '_' + annos))
    #             print(annos)    
            # j += 1
            # print("")
            # i += 1
    # os.rename(os.path.join(path, file), os.path.join(path, str(index)))
