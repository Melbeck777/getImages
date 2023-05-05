import zipfile
import sys
import re
import os
from pathlib import Path

# Get file local number
def get_count(dir_path, file_path="-1"):
    count = 1
    numeric_target = re.compile("\d-")
    get_only_numeric = re.compile("\d+")
    for file in Path(dir_path).glob("*"):
        # print(file)
        if os.path.isdir(file):
            continue
        base = os.path.basename(file)

        if numeric_target.search(base) == None:
            continue
        elif file == file_path and numeric_target.search(base):
            return int(get_only_numeric.search(base).group())
        num = int(get_only_numeric.search(base).group())
        print(file,num)
        count = max(count, num+1)
    return count

# Verify images extensions
def verify_extensions(file,extensions):
    for ex in extensions:
        target = re.compile(ex)
        if target.search(file):
            return True
    return False
    

args = sys.argv
target_file_path = Path(args[1])
dir_path = target_file_path.parent


current_num = get_count(dir_path, target_file_path)
image_dir = os.path.join(dir_path, "image", str(current_num))
if os.path.exists(image_dir) == False:
    os.makedirs(image_dir)

# select image files extensions
image_extensions = []
with open("extensions.txt","r",encoding="utf-8") as f:
    image_extensions = f.read().split("\n")

# To zip files and get file namelist.
docx_zip = zipfile.ZipFile(target_file_path)
zipped_files = docx_zip.namelist()



for file in zipped_files:
    # Except not image
    if verify_extensions(file, image_extensions) == False:
        continue
    print(file)
    img_file = docx_zip.open(file)
    img_bytes = img_file.read()
    img_path = os.path.join(image_dir, Path(file).name)
    with open(img_path,mode="wb") as f:
        f.write(img_bytes)
    img_file.close()
docx_zip.close()

base_name = os.path.basename(target_file_path)
if re.search("\d-",base_name) == None:
    to_name = os.path.join(dir_path, "{}-{}".format(str(current_num), base_name))
    os.rename(target_file_path, to_name)
    