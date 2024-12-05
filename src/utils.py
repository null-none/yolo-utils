import os


class YoloUtils:
    def __init__(self):
        self.image_width = 1280
        self.image_height = 720

    def seg_to_bbox(self, seg_info):
        # Example input: 5 0.046875 0.369141 0.0644531 0.384766 0.0800781 0.402344 ...
        class_id, *points = seg_info.split()
        points = [float(p) for p in points]
        x_min, y_min, x_max, y_max = (
            min(points[0::2]),
            min(points[1::2]),
            max(points[0::2]),
            max(points[1::2]),
        )
        width, height = x_max - x_min, y_max - y_min
        x_center, y_center = (x_min + x_max) / 2, (y_min + y_max) / 2
        bbox_info = f"{int(class_id)-1} {x_center} {y_center} {width} {height}"
        return bbox_info

    def annotation_to_cv2(self, input_file, output_file):
        with open(input_file, "r") as f:
            lines = f.readlines()

        new_lines = list()
        for line in lines:
            data = line.strip().split(" ")

            class_id = int(data[0])
            x_center = float(data[1])
            y_center = float(data[2])
            width = float(data[3])
            height = float(data[4])

            x_min = int((x_center - (width / 2)) * self.image_width)
            y_min = int((y_center - (height / 2)) * self.image_height)
            x_max = int((x_center + (width / 2)) * self.image_width)
            y_max = int((y_center + (height / 2)) * self.image_height)

            new_data = f"{class_id} {x_min} {y_min} {x_max} {y_max}\n"
            new_lines.append(new_data)

        with open(output_file, "w") as f:
            f.writelines(new_lines)
