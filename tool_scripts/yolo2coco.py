import os
import json
import cv2

yolo_dir = "/Users/jayphone/Desktop/labels" # yolo格式的标注文件所在文件夹
img_dir = "/Users/jayphone/Desktop/images" # 图片文件夹
output_path = "/Users/jayphone/Desktop/coco_labels/output.json" # 转换后的coco格式的标注文件路径

coco_data = {
    "info": {},
    "licenses": [],
    "categories": [
        {"id": 1, "name": "smoke", "supercategory": "object"}
    ],
    "images": [],
    "annotations": []
}

image_id = 1
annotation_id = 1
empty_lines_files = []

for file_name in os.listdir(yolo_dir):
    if file_name.endswith(".txt"):
        with open(os.path.join(yolo_dir, file_name), "r") as f:
            lines = f.readlines()
            if len(lines) == 0: # 如果文件中没有标注信息，则跳过该文件并记录下来
                empty_lines_files.append(file_name)
                continue
            img_name = file_name.replace(".txt", ".jpg")
            img_path = os.path.join(img_dir, img_name)
            img = cv2.imread(img_path)
            if img is None:
                print(f"Error: Failed to read image file {img_path}")
            height, width, channels = img.shape
            print(f'{file_name}: ({width}, {height}, {channels})')
            coco_data["images"].append({
                "id": image_id,
                "file_name": img_name,
                "height": height,
                "width": width
            })
            for line in lines:
                if line.strip() == "": # 如果该行为空行，则跳过
                    continue
                x, y, w, h = map(float, line.split()[1:])
                x1 = max(0, int((x - w / 2) * width))
                y1 = max(0, int((y - h / 2) * height))
                x2 = min(width, int((x + w / 2) * width))
                y2 = min(height, int((y + h / 2) * height))
                coco_data["annotations"].append({
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": 1,
                    "bbox": [x1, y1, x2 - x1, y2 - y1],
                    "area": (x2 - x1) * (y2 - y1),
                    "iscrowd": 0
                })
                annotation_id += 1
            image_id += 1

with open(output_path, "w") as f:
    json.dump(coco_data, f)

if empty_lines_files:
    print("以下文件存在空行，已跳过处理：")
    for file_name in empty_lines_files:
        print(file_name)
