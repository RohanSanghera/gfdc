from  get_shapes import remove_lines

def get_coords_lines(start, sq_size, spacing):

    distance = spacing + sq_size

    coords = []
    i = 0
    while i <= 10:

        coords.append(start + i * distance)
        i = i + 1

    return(coords)
   
def build_grid(square_side, line_properties, gray):

    line = line_properties["size"]
    line_start_left = line_properties["start_left"]
    line_start_top = line_properties["start_top"]
    line_thickness = line_properties["thickness"]

    spacing = (line/2 - 5*square_side)/5
    gray_no_lines = remove_lines(line, line_start_left, line_start_top, line_thickness, gray)

    x_coords = get_coords_lines(line_start_left, square_side, spacing)
    y_coords = get_coords_lines(line_start_top, square_side, spacing)

    return x_coords, y_coords, gray_no_lines