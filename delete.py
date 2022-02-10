import os

def delete(local):
    """
    This function will delete all the files from extract(), make it all clean =)
    """
    folders = []
    for root ,dir, files in os.walk(local):
        for name in files:
            if name[-3:] != "delete.py" or "main.py" :
                os.remove(os.path.join(root, name))
        for folder in dir:
            folders += [os.path.join(root, folder)]
    
    for i in range(len(folders)-1,-1,-1) :
        os.rmdir(folders[i])

local = os.path.dirname(__file__) + "\\"
delete(local)