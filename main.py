import cv2
import imutils
from get_shapes import get_square_size, get_line_size
from grid import build_grid
from Classification import calculate_black_percentage, pct_classification, get_test_result

def grading(image_path):
    print('image_path')
    use_ratio = False
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Could not read image at {image_path}")
            return "ERROR - IMAGE NOT UPLOADED"
        img = imutils.resize(img, width=1000)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        phone = False

        try:
            h, w = get_square_size(gray, phone, img)
            square_side = (h + w)/2

        except:
            use_ratio = True

        line, line_start_left, line_start_top = get_line_size(gray, phone, img)
        line_thickness = 10
        line_properties = {"size": line, "start_left": line_start_left, "start_top": line_start_top, "thickness": line_thickness}
        ratio = 14.926

        if use_ratio == True:
            square_side = line/ratio
        use_ratio = False
        
        if line_start_left >= 0:
            x_coords, y_coords, gray_no_lines = build_grid(square_side, line_properties, gray)
            percentage = calculate_black_percentage(x_coords, y_coords, gray_no_lines)
            classification = pct_classification(percentage)

            if 5 not in classification and use_ratio == False:
                use_ratio = True
                square_side = line / ratio
                x_coords, y_coords, gray_no_lines = build_grid(square_side, line_properties, gray)
                percentage = calculate_black_percentage(x_coords, y_coords, gray_no_lines)
                classification = pct_classification(percentage)

            return get_test_result(classification)

        else:
            print("ERROR: Can't see edge of the line in", image_path)
            return None

    except Exception as e:
        print("An error occurred:", str(e))
        return None
