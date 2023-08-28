import random
import numpy as np
import cv2
import csv
import os

#set to true if you want the solution to be connected in the dataset
Connected_solution=False
def selfmade_transpose(matrix):
    temp = matrix.copy()
    i = 0
    j = 0
    while i<np.shape(matrix)[0]:
        while(j<np.shape(matrix)[1]):
            matrix[i][j]= temp[j][i]
            j+=1
        j=0
        i+=1

def cut_puzzle(puzzle):
    tl=puzzle[0:200,0:200]
    bl= puzzle[200:400,0:200]
    tr = puzzle[0:200,200:400]
    return [tl,tr,bl]

def create_cut_sub_dataset(name,amount,starting_number):
    with open('./simple_puzzle_dataset/' + name + '.csv', 'w') as csv_file:
        if Connected_solution:
            fieldnames = ["top_left", "top_right", "bottom_left", "solution"]
        else:
            fieldnames = ["top_left", "top_right", "bottom_left", "shape", "colour"]
        csv_writer= csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        i = starting_number
        while i < starting_number + amount:
            at_sample = i-starting_number+1
            if at_sample % 25 == 0:
                print(f"\rAt sample {at_sample} of {amount}...", end='', flush=True)
            puzzle, shape_name,colour_name = build_puzzle()
            tl,tr,bl=cut_puzzle(puzzle)
            tl_img = "puzzle_" + str(i) + "_tl"
            tr_img= "puzzle_" + str(i) + "_tr"
            bl_img= "puzzle_" + str(i) + "_bl"
            cv2.imwrite("simple_puzzle_dataset/images/" + tl_img + ".png", np.squeeze(tl))
            cv2.imwrite("simple_puzzle_dataset/images/" + tr_img + ".png", np.squeeze(tr))
            cv2.imwrite("simple_puzzle_dataset/images/" + bl_img + ".png", np.squeeze(bl))
            if Connected_solution:
                solution = colour_name + '_' + shape_name
                csv_writer.writerow(
                    {"top_left": tl_img, "top_right": tr_img, "bottom_left": bl_img, "solution": solution})
            else:
                csv_writer.writerow(
                    {"top_left": tl_img, "top_right": tr_img, "bottom_left": bl_img, "shape": shape_name,
                     "colour": colour_name})
            i += 1
        print(f"\rAt sample {at_sample} of {amount}...", end='', flush=True)

def resolve_colour(colour_matrix, colour, colour_palette):
    if len (colour) == 1:
        return colour[0]
    else:
        if np.equal(colour_palette.get(colour[0]), colour_matrix[1][1]).all():
            return colour[0]
        else:
            return colour[1]
def resolve_shape(shape_matrix,shapes):
    i=0
    while i<2:
        if np.equal(shapes[i][1],shape_matrix[1][1]).all():
            return shapes[i][0]
        i+=1
def shift_colours(colour_matrix,shift):
    temp=np.array([[0,0,0],[0,0,0]])

    #shift second row
    i=0
    while i<2:
        temp[i]=colour_matrix[1][i]
        i+=1
    temp=np.roll(temp,shift,axis=0)
    i=0
    while i<2:
        colour_matrix[1][i]=temp[i]
        i+=1


def shift_shapes(shape_matrix, shift):
    temp = np.zeros((2, 200, 200, 3))

    # shift second row
    i = 0
    while (i < 2):
        temp[i] = shape_matrix[i][1]
        i += 1
    temp = np.roll(temp, shift, axis=0)

    i = 0
    while i < 2:
        shape_matrix[i][1] = temp[i]
        i += 1


def draw_sector(template, colour, puzzle, x_offset, y_offset):
    i = 0
    j = 0
    while (i < 200):
        while (j < 200):
            if template[i][j][0] == 0 and template[i][j][1] == 0 and template[i][j][2] == 0:
                puzzle[i + y_offset][j + x_offset] = colour
            else:
                puzzle[i + y_offset][j + x_offset] = template[i][j]
            j += 1
        j = 0
        i += 1
    return puzzle


def draw_puzzle(shape_matrix, colour_matrix):
    puzzle = np.ones((400, 400, 3), np.uint8) * 255

    # first colomn

    puzzle = draw_sector(shape_matrix[0][0], colour_matrix[0][0], puzzle, 0, 0)
    puzzle = draw_sector(shape_matrix[0][1], colour_matrix[1][0], puzzle, 0, 200)


    # second colomn

    puzzle = draw_sector(shape_matrix[1][0], colour_matrix[0][1], puzzle, 200, 0)
    return puzzle


def build_puzzle():
    colour_palette = {"red": [0, 0, 255], "yellow": [0, 255, 255], "green": [0, 255, 0]
        , "cyan": [255, 255, 0], "blue": [255, 0, 0], "magenta": [255, 0, 255]}

    x = random.randrange(2)
    # one third of the time all the colours are the same
    if x == 2:
        colour = random.sample(colour_palette.keys(), 1)
        colour_order = [colour_palette.get(colour[0]), colour_palette.get(colour[0])]
    # two thirds of the time we have two random colours
    else:
        colour = random.sample(colour_palette.keys(), 2)
        colour_order = [colour_palette.get(colour[0]), colour_palette.get(colour[1])]

    colour_matrix = np.array([colour_order, colour_order])

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
    shapes = [["triangle", triangle_temp],
              ["circle", circle_temp],
              ["hexagon", hexagon_temp],
              ["pentagon", pentagon_temp],
              ["square", square_temp],
              ["right_triangle", right_triangle_temp],
              ["trapeze", trapeze_temp],
              ["rhombus", rhombus_temp],
              ["kite", kite_temp]]
    shapes = random.sample(shapes, 2)
    shape_order = []
    i = 0
    while i < 2:
        shape_order.append(shapes[i][1])
        i += 1
    shape_matrix = np.ndarray((2, 2, 200, 200, 3))
    x=random.randrange(2)

    #one third of the time all the shapes are the same
    if x==2:
        i = 0
        j = 0
        while (i < 2):
            while (j < 2):
                shape_matrix[i][j] = shape_order[0]
                j += 1
            j = 0
            i += 1
    # two thirds the shapes will be random
    else:
        i = 0
        j = 0
        while (i < 2):
            while (j < 2):
                shape_matrix[i][j] = shape_order[i]
                j += 1
            j = 0
            i += 1

    shift_colours(colour_matrix, random.choice([0, 1]))
    shift_shapes(shape_matrix, random.choice([ 0, 1]))

    if random.choice([0, 1])==1:
        selfmade_transpose(shape_matrix)

    if random.choice([0, 1])== 1:
        selfmade_transpose(colour_matrix)
    puzzle = draw_puzzle(shape_matrix, colour_matrix)
    shape_name = resolve_shape(shape_matrix, shapes)
    colour_name = resolve_colour(colour_matrix,colour, colour_palette)
    return [puzzle,shape_name,colour_name]




def main():
    os.makedirs("./simple_puzzle_dataset/images")
    amount_examples_train_dataset = 200
    amount_examples_test_dataset = 50
    create_cut_sub_dataset('train', amount_examples_train_dataset, 0)
    create_cut_sub_dataset('test', amount_examples_test_dataset, amount_examples_train_dataset)




if __name__ == '__main__':
    main()