import random
import os
import cv2
import numpy as np
import csv

c = 0

def create_sub_dataset(name,amount,starting_number,count):
    with open('./test_puzzle_dataset/' + name + '.csv', 'w') as csv_file:
        fieldnames = ["image_name","shape"]
        csv_writer= csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        i = starting_number
        while i < starting_number + amount:
            puzzle, shape_name = generate_puzzle()
            image_name = count
            cv2.imwrite("test_puzzle_dataset/images/"  + str(image_name) + ".png", np.squeeze(puzzle))
            csv_writer.writerow({"image_name": image_name, "shape": shape_name})
            count += 1
            i += 1
        return count
def draw_puzzle(puzzle,colour,shape):
    i = 0
    j = 0
    while (i < 200):
        while (j < 200):
            # if shape[i][j][0] == 0 and shape[i][j][1] == 0 and shape[i][j][2] == 0:
            #     puzzle[i][j] = colour
            # else:
            puzzle[i][j] = shape[i][j]
            j += 1
        j = 0
        i += 1
    return puzzle
def generate_puzzle():

    #colour section
    colour_palette = np.array([[0, 0, 255], [0, 255, 255], [0, 255, 0], [255, 255, 0], [255, 0, 0], [255, 0, 255]])
    # red, yellow,green,cyan,blue and magenta in BGR

    colour = random.choice(colour_palette)

    #shape section
    # create triangle template
    triangle_temp = np.ones((200, 200, 3), np.uint8) * 255
    pt1 = (100, 50)
    pt2 = (50, 150)
    pt3 = (150, 150)
    tri_points = np.array([pt1, pt2, pt3])
    cv2.drawContours(triangle_temp, [tri_points], -1, (0, 0, 0), -1)

    # create circle template
    circle_temp = np.ones((200, 200, 3), np.uint8) * 255
    cv2.circle(circle_temp, (100, 100), 63, (0, 0, 0), -1)

    # create square template
    square_temp = np.ones((200, 200, 3), np.uint8) * 255
    cv2.rectangle(square_temp, (50, 50), (150, 150), (0, 0, 0), -1)

    # create right triangle
    right_triangle_temp = np.ones((200, 200, 3), np.uint8) * 255
    pt1 = (50, 50)
    pt2 = (50, 150)
    pt3 = (150, 150)
    tri_points = np.array([pt1, pt2, pt3])
    cv2.drawContours(right_triangle_temp, [tri_points], -1, (0, 0, 0), -1)

    # create trapeze template
    trapeze_temp = np.ones((200, 200, 3), np.uint8) * 255
    pt1 = (65, 50)
    pt2 = (135, 50)
    pt3 = (175, 150)
    pt4 = (25, 150)
    quad_points = np.array([pt1, pt2, pt3, pt4])
    cv2.drawContours(trapeze_temp, [quad_points], -1, (0, 0, 0), -1)

    # create rhombus template
    rhombus_temp = np.ones((200, 200, 3), np.uint8) * 255
    pt1 = (100, 50)
    pt2 = (150, 100)
    pt3 = (100, 150)
    pt4 = (50, 100)
    quad_points = np.array([pt1, pt2, pt3, pt4])
    cv2.drawContours(rhombus_temp, [quad_points], -1, (0, 0, 0), -1)

    # create kite template
    kite_temp = np.ones((200, 200, 3), np.uint8) * 255
    pt1 = (100, 50)
    pt2 = (150, 70)
    pt3 = (100, 150)
    pt4 = (50, 70)
    quad_points = np.array([pt1, pt2, pt3, pt4])
    cv2.drawContours(kite_temp, [quad_points], -1, (0, 0, 0), -1)

    # create pentagon template
    pentagon_temp = np.ones((200, 200, 3), np.uint8) * 255
    pt1 = (100, 50)
    pt2 = (150, 90)
    pt3 = (130, 150)
    pt4 = (70, 150)
    pt5 = (50, 90)
    pent_points = np.array([pt1, pt2, pt3, pt4, pt5])
    cv2.drawContours(pentagon_temp, [pent_points], -1, (0, 0, 0), -1)

    # create hexagon template
    hexagon_temp = np.ones((200, 200, 3), np.uint8) * 255
    pt1 = (100, 50)
    pt2 = (150, 76)
    pt3 = (150, 124)
    pt4 = (100, 150)
    pt5 = (50, 124)
    pt6 = (50, 76)
    hex_points = np.array([pt1, pt2, pt3, pt4, pt5, pt6])
    cv2.drawContours(hexagon_temp, [hex_points], -1, (0, 0, 0), -1)

    # choose random order of random shapes
    shapes = [[0, triangle_temp],
              [1, circle_temp],
              [2, hexagon_temp],
              [3, pentagon_temp],
              [4, square_temp],
              [5, right_triangle_temp],
              [6, trapeze_temp],
              [7, rhombus_temp],
              [8, kite_temp]]
    shape = random.choice(shapes)

    test_puzzle = np.ones((200, 200, 3), np.uint8) * 255

    test_puzzle=draw_puzzle(test_puzzle,colour,shape[1])
    return [test_puzzle,shape[0]]
def main():
    test_puzzle,shape = generate_puzzle()
    os.makedirs("./test_puzzle_dataset/images")
    amount_examples_train_dataset = 800
    amount_examples_test_dataset = 200
    count=0
    count = create_sub_dataset('train',amount_examples_train_dataset,0,count)
    count = create_sub_dataset('test',amount_examples_test_dataset,amount_examples_train_dataset,count)


if __name__ == '__main__':
    main()