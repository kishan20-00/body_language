import cv2
import math
import numpy as np
dot_radius = 5 
dot_color = (4, 255, 0)
dot_thickness = -1

center_points = []
object_points = []

def is_valid_point(new_center, existing_points, min_distance):
    for point in existing_points:
        distance = math.sqrt((new_center[0] - point[0]) ** 2 + (new_center[1] - point[1]) ** 2)
        if distance < min_distance:
            return False
    return True

min_distance = 50
object_distance = 50

def store_center_point(cx, cy):
    new_center = (cx, cy)
    
    if is_valid_point(new_center, center_points, min_distance):
        center_points.append(new_center)
        print(f"Stored point: {new_center}")
    else:
        print(f"Point {new_center} is too close to an existing point. Not stored.")

def object_store_center_point(cx, cy):
    new_center = (cx, cy)
    
    if is_valid_point(new_center, object_points, object_distance):
        object_points.append(new_center)
        print(f"Stored point: {new_center}")
    else:
        print(f"Point {new_center} is too close to an existing point. Not stored.")

def resize_image(img, scale_percent) :
    # Calculate new size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # Resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def draw_box(img, result, class_list) :
    # Get information from result
    xyxy= result.boxes.xyxy.numpy()
    confidence= result.boxes.conf.numpy()
    class_id= result.boxes.cls.numpy().astype(int)
    # Get Class name
    class_name = [class_list[x] for x in class_id]
    # Pack together for easy use
    sum_output = list(zip(class_name, confidence,xyxy))
    # Copy image, in case that we need original image for something
    out_image = img.copy()
    for run_output in sum_output :
        # Unpack
        label, con, box = run_output
        # Choose color
        box_color = (0, 0, 255)
        text_color = (255,255,255)
        # Draw object box
        first_half_box = (int(box[0]),int(box[1]))
        second_half_box = (int(box[2]),int(box[3]))
        cv2.rectangle(out_image, first_half_box, second_half_box, box_color, 2)
        # Create text
        text_print = '{label} {con:.2f}'.format(label = label, con = con)
        # Locate text position
        text_location = (int(box[0]), int(box[1] - 10 ))
        # Get size and baseline
        labelSize, baseLine = cv2.getTextSize(text_print, cv2.FONT_HERSHEY_SIMPLEX, 1, 2) 
        # Draw text's background
        cv2.rectangle(out_image 
                        , (int(box[0]), int(box[1] - labelSize[1] - 10 ))
                        , (int(box[0])+labelSize[0], int(box[1] + baseLine-10))
                        , box_color , cv2.FILLED) 
        # Put text
        cv2.putText(out_image, text_print ,text_location
                    , cv2.FONT_HERSHEY_SIMPLEX , 1
                    , text_color, 2 ,cv2.LINE_AA)
    return out_image


def draw_box_people(img, result, class_list,image_center_points) :
    temp_center_points=image_center_points
    print(len(image_center_points))
    if(len(image_center_points)==0 and len(center_points)!=0):
        center_points.clear()
    # Get information from result
    xyxy= result.boxes.xyxy.numpy()
    confidence= result.boxes.conf.numpy()
    class_id= result.boxes.cls.numpy().astype(int)
    # Get Class name
    class_name = [class_list[x] for x in class_id]
    # Pack together for easy use
    sum_output = list(zip(class_name, confidence,xyxy))
    # Copy image, in case that we need original image for something
    out_image = img.copy()
    for run_output in sum_output :
        # Unpack
        label, con, box = run_output
        
        if(label == "people"):
            x1, y1 = int(box[0]), int(box[1])
            x2, y2 = int(box[2]), int(box[3])

            x = (x1 + x2) // 2
            y = (y1 + y2) // 2
            print(x)
            print(y)

            store_center_point(x,y)

    for point in temp_center_points:
        cv2.circle(out_image, ((point[0]), point[1]), dot_radius, dot_color, dot_thickness)

    return out_image,center_points

def draw_box_object(img, result, class_list,image_object_points) :
    temp_object_points=image_object_points
    print(len(image_object_points))
    if(len(image_object_points)==0 and len(object_points)!=0):
        object_points.clear()
        
    xyxy= result.boxes.xyxy.numpy()
    confidence= result.boxes.conf.numpy()
    class_id= result.boxes.cls.numpy().astype(int)
    
    class_name = [class_list[x] for x in class_id]
    
    sum_output = list(zip(class_name, confidence,xyxy))
    # Copy image, in case that we need original image for something
    out_image = img.copy()
    for run_output in sum_output :
        # Unpack
        label, con, box = run_output
        
        if(label != "people"):
            x1, y1 = int(box[0]), int(box[1])
            x2, y2 = int(box[2]), int(box[3])

            x = (x1 + x2) // 2
            y = (y1 + y2) // 2
            print(x)
            print(y)

            object_store_center_point(x,y)

    for point in temp_object_points:
        cv2.circle(out_image, ((point[0]), point[1]), dot_radius, dot_color, dot_thickness)

    return out_image,object_points