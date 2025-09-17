import os

folder_path = "/Users/jayphonelin/Desktop/14242/labels" # 替换为您要遍历的文件夹路径
empty_files = []

# 遍历文件夹
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        filepath = os.path.join(folder_path, filename)
        # 检查文件是否为空
        if os.path.getsize(filepath) == 0:
            empty_files.append(filename)

# 输出空文件的数量和文件名
if len(empty_files) > 0:
    print(f"{len(empty_files)} empty files found:")
    for filename in empty_files:
        print(filename)
else:
    print("No empty files found.")

# 询问是否要删除空文件
if len(empty_files) > 0:
    delete_files = input("Do you want to delete these empty files? (y/n)")
    if delete_files.lower() == "y":
        for filename in empty_files:
            filepath = os.path.join(folder_path, filename)
            os.remove(filepath)
            print(f"{filename} has been deleted.")
    else:
        print("Empty files have not been deleted.")
