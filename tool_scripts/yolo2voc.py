import os
import xml.etree.ElementTree as ET
from PIL import Image

# 设置数据文件夹路径、类别名称和输出文件夹路径
data_folder = '/Users/jayphone/Desktop/whole'
class_name = 'smoke'
output_folder = '/Users/jayphone/Desktop/xml_labels'

# 遍历数据文件夹内所有文件
for file_name in os.listdir(data_folder):
    # 判断文件是否是yolo格式的标注文件
    if file_name.endswith('.txt'):
        # 读取标注文件内容
        with open(os.path.join(data_folder, file_name), 'r') as f:
            lines = f.readlines()
        # 如果标注文件存在空行，则删除对应文件名的图片并输出删除成功的信息
        if '' in lines:
            print(f"Empty line in {file_name}, deleting corresponding image.")
            os.remove(os.path.join(data_folder, file_name.replace('.txt', '.jpg')))
        # 否则，将标注文件转换成voc格式的xml文件
        else:
            # 读取对应的图片文件
            img_file_name = os.path.join(data_folder, file_name.replace('.txt', '.jpg'))
            img = Image.open(img_file_name)
            width, height = img.size
            root = ET.Element("annotation")
            folder = ET.SubElement(root, "folder")
            folder.text = data_folder
            filename = ET.SubElement(root, "filename")
            filename.text = file_name.replace('.txt', '.jpg')
            source = ET.SubElement(root, "source")
            database = ET.SubElement(source, "database")
            database.text = "Unknown"
            size = ET.SubElement(root, "size")
            width_elem = ET.SubElement(size, "width")
            height_elem = ET.SubElement(size, "height")
            depth = ET.SubElement(size, "depth")
            width_elem.text = str(width)
            height_elem.text = str(height)
            depth.text = '3'
            for line in lines:
                x, y, w, h = map(float, line.split()[1:])
                xmin = int((x - w/2) * width)
                ymin = int((y - h/2) * height)
                xmax = int((x + w/2) * width)
                ymax = int((y + h/2) * height)
                object = ET.SubElement(root, "object")
                name = ET.SubElement(object, "name")
                name.text = class_name
                bndbox = ET.SubElement(object, "bndbox")
                xmin_elem = ET.SubElement(bndbox, "xmin")
                ymin_elem = ET.SubElement(bndbox, "ymin")
                xmax_elem = ET.SubElement(bndbox, "xmax")
                ymax_elem = ET.SubElement(bndbox, "ymax")
                xmin_elem.text = str(xmin)
                ymin_elem.text = str(ymin)
                xmax_elem.text = str(xmax)
                ymax_elem.text = str(ymax)
            # 将xml文件保存到输出文件夹
            xml_file_name = file_name.replace('.txt', '.xml')
            tree = ET.ElementTree(root)
            tree.write(os.path.join(output_folder, xml_file_name))
