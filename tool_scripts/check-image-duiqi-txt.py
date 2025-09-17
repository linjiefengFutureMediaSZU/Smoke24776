import os

# 图片文件夹路径
img_folder = '/Users/jayphonelin/Desktop/14242/images'
# txt文件夹路径
txt_folder = '/Users/jayphonelin/Desktop/14242/labels'

# 获取txt文件夹中的所有文件名前缀
txt_files = set(os.path.splitext(f)[0] for f in os.listdir(txt_folder))

# 遍历图片文件夹中的所有文件名前缀
for img_file in os.listdir(img_folder):
    img_file_prefix = os.path.splitext(img_file)[0]
    # 如果当前文件名前缀不在txt文件夹中，输出该文件名
    if img_file_prefix not in txt_files:
        print(img_file)
