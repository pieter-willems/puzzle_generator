import cv2
import numpy as np
import random
import csv
import os

All_black=False

def create_cut_sub_dataset(name,amount,starting_number,shape_shift,colour_shift,transpose_shape,transpose_colour,same_shape,same_colour,shapes_colors_connected):
    with open('./dataset/' + name + '.csv', 'w') as csv_file:
        fieldnames = ["top_left","top_middle","top_right","middle_left","middle_middle","middle_right",
                      "bottom_left","bottom_middle","shape","colour"]
        csv_writer= csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        i = starting_number
        while i < starting_number + amount:
            at_sample = i-starting_number+1
            if at_sample % 25 == 0:
                print(f"\rAt sample {at_sample} of {amount}...", end='', flush=True)
            puzzle, shape_name,colour_name = build_puzzle(shape_shift,colour_shift,transpose_shape,transpose_colour,same_shape,same_colour,shapes_colors_connected)
            tl,tm,tr,ml,mm,mr,bl,bm=cut_puzzle(puzzle)

            tl_img = "puzzle_" + str(i) + "_tl"
            tm_img = "puzzle_" + str(i) + "_tm"
            tr_img= "puzzle_" + str(i) + "_tr"

            ml_img = "puzzle_" + str(i) + "_ml"
            mm_img = "puzzle_" + str(i) + "_mm"
            mr_img = "puzzle_" + str(i) + "_mr"

            bl_img= "puzzle_" + str(i) + "_bl"
            bm_img = "puzzle_" + str(i) + "_bm"

            cv2.imwrite("dataset/images/" + tl_img + ".png", np.squeeze(tl))
            cv2.imwrite("dataset/images/" + tm_img + ".png", np.squeeze(tm))
            cv2.imwrite("dataset/images/" + tr_img + ".png", np.squeeze(tr))

            cv2.imwrite("dataset/images/" + ml_img + ".png", np.squeeze(ml))
            cv2.imwrite("dataset/images/" + mm_img + ".png", np.squeeze(mm))
            cv2.imwrite("dataset/images/" + mr_img + ".png", np.squeeze(mr))

            cv2.imwrite("dataset/images/" + bl_img + ".png", np.squeeze(bl))
            cv2.imwrite("dataset/images/" + bm_img + ".png", np.squeeze(bm))

            csv_writer.writerow({"top_left": tl_img,"top_middle": tm_img, "top_right": tr_img,
                                 "middle_left" : ml_img,"middle_middle" : mm_img,"middle_right" : ml_img,
                                 "bottom_left" : bl_img, "bottom_middle" : bm_img,
                                "shape": shape_name, "colour" : colour_name})
            i += 1
        print(f"\rAt sample {at_sample} of {amount}...", end='', flush=True)

def cut_puzzle(puzzle):
    tl = puzzle[0:200, 0:200]
    tm = puzzle[0:200, 200:400]
    tr = puzzle[0:200,400:600]
    ml = puzzle[200:400, 0:200]
    mm = puzzle[200:400, 200:400]
    mr = puzzle[200:400, 400:600]
    bl = puzzle[400:600, 0:200]
    bm = puzzle[400:600, 200:400]
    return [tl, tm,tr,ml,mm,mr,bl,bm]

def resolve_colour(colour_matrix, colour, colour_palette):
    if len (colour) == 1:
        return colour[0]
    else:
        if np.equal(colour_palette.get(colour[0]), colour_matrix[2][2]).all():
            return colour[0]
        elif np.equal(colour_palette.get(colour[1]), colour_matrix[2][2]).all():
            return colour[1]
        else:
            return colour[2]
def resolve_shape(shape_matrix,shapes):
    i=0
    while i<3:
        if np.equal(shapes[i][1],shape_matrix[2][2]).all():
            return shapes[i][0]
        i+=1

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


def shift_colours(colour_matrix,shift):
    temp=np.array([[0,0,0],[0,0,0],[0,0,0]])

    #shift second row
    i=0
    while i<3:
        temp[i]=colour_matrix[1][i]
        i+=1
    temp=np.roll(temp,shift,axis=0)
    i=0
    while i<3:
        colour_matrix[1][i]=temp[i]
        i+=1

    #shift third row
    temp=np.roll(temp,shift,axis=0)
    i=0
    while i<3:
        colour_matrix[2][i]=temp[i]
        i+=1

def shift_shapes(shape_matrix,shift):
    temp=np.zeros((3,200,200,3))
    
    #shift second row
    i=0
    while(i<3):
       
        temp[i]=shape_matrix[i][1]
        i+=1
    temp=np.roll(temp,shift,axis=0)
   

    i=0
    while i<3:
        shape_matrix[i][1]=temp[i]
        i+=1
    
    #shift third row
    temp=np.roll(temp,shift,axis=0)
    i=0
    while i<3:
        shape_matrix[i][2]=temp[i]
        i+=1
    


def draw_sector(template,colour,puzzle,x_offset,y_offset):
    i=0
    j=0
    while(i<200):
        while(j<200):
            if template[i][j][0]==0 and template[i][j][1]==0 and template[i][j][2]==0 and not All_black:
                puzzle[i+y_offset][j+x_offset]=colour
            else:
                puzzle[i+y_offset][j+x_offset]=template[i][j]
            j+=1
        j=0
        i+=1
    return puzzle

def draw_puzzle(shape_matrix,colour_matrix):
    puzzle = np.ones((600, 600, 3), np.uint8) * 255


    #first colomn

    
    puzzle=draw_sector(shape_matrix[0][0],colour_matrix[0][0],puzzle,0,0)
    puzzle=draw_sector(shape_matrix[0][1],colour_matrix[1][0],puzzle,0,200)
    puzzle=draw_sector(shape_matrix[0][2],colour_matrix[2][0],puzzle,0,400)

    #second colomn

   
    puzzle=draw_sector(shape_matrix[1][0],colour_matrix[0][1],puzzle,200,0)
    puzzle=draw_sector(shape_matrix[1][1],colour_matrix[1][1],puzzle,200,200)
    puzzle=draw_sector(shape_matrix[1][2],colour_matrix[2][1],puzzle,200,400)

    #third colomn

   
    puzzle=draw_sector(shape_matrix[2][0],colour_matrix[0][2],puzzle,400,0)
    puzzle=draw_sector(shape_matrix[2][1],colour_matrix[1][2],puzzle,400,200)

    return puzzle


def build_puzzle(shape_shift,colour_shift,transpose_shape,transpose_colour,same_shape,same_colour,shapes_colors_connected):

    colour_palette = {"red": [0, 0, 255], "yellow": [0, 255, 255], "green": [0, 255, 0]}

    x = random.randrange(2)
    # one third of the time all the colours are the same
    if x == 2 and same_colour:
        colour = random.sample(colour_palette.keys(), 1)
        colour_order = [colour_palette.get(colour[0]), colour_palette.get(colour[0]),colour_palette.get(colour[0])]
    # two thirds of the time we have two random colours
    else:
        colour = random.sample(colour_palette.keys(), 3)
        colour_order = [colour_palette.get(colour[0]), colour_palette.get(colour[1]),colour_palette.get(colour[2])]


    #create a 3x3 matrix of the chosen colours
    colour_matrix=np.array([colour_order,colour_order,colour_order])

    #create triangle template
    triangle_temp=np.ones((200,200,3),np.uint8)*255
    pt1 = (100, 50)
    pt2 = (50, 150)
    pt3 = (150, 150)
    tri_points=np.array([pt1,pt2,pt3])
    cv2.drawContours(triangle_temp, [tri_points], -1, (0,0,0), -1)

    #create circle template
    circle_temp=np.ones((200,200,3),np.uint8)*255
    cv2.circle(circle_temp,(100,100), 63, (0,0,0), -1)

    #create square template
    square_temp=np.ones((200,200,3),np.uint8)*255
    cv2.rectangle(square_temp,(50,50),(150,150),(0,0,0),-1)

    #create right triangle
    right_triangle_temp=np.ones((200,200,3),np.uint8)*255
    pt1=(50,50)
    pt2=(50,150)
    pt3=(150,150)
    tri_points = np.array([pt1, pt2, pt3])
    cv2.drawContours(right_triangle_temp, [tri_points], -1, (0, 0, 0), -1)

    #create trapeze template
    trapeze_temp = np.ones((200, 200, 3), np.uint8) * 255
    pt1 = (65, 50)
    pt2 = (135, 50)
    pt3 = (175, 150)
    pt4 = (25, 150)
    quad_points = np.array([pt1, pt2, pt3, pt4])
    cv2.drawContours(trapeze_temp, [quad_points], -1, (0, 0, 0), -1)

    #create rhombus template
    rhombus_temp = np.ones((200, 200, 3), np.uint8) * 255
    pt1 = (100, 50)
    pt2 = (150, 100)
    pt3 = (100, 150)
    pt4 = (50, 100)
    quad_points = np.array([pt1, pt2, pt3, pt4])
    cv2.drawContours(rhombus_temp, [quad_points], -1, (0, 0, 0), -1)

    #create kite template
    kite_temp = np.ones((200, 200, 3), np.uint8) * 255
    pt1 = (100, 50)
    pt2 = (150, 70)
    pt3 = (100, 150)
    pt4 = (50, 70)
    quad_points = np.array([pt1, pt2, pt3, pt4])
    cv2.drawContours(kite_temp, [quad_points], -1, (0, 0, 0), -1)

    #create pentagon template
    pentagon_temp = np.ones((200, 200, 3), np.uint8) * 255
    pt1 = (100, 50)
    pt2 = (150, 90)
    pt3 = (130, 150)
    pt4 = (70,150)
    pt5 = (50, 90)
    pent_points = np.array([pt1, pt2, pt3, pt4,pt5])
    cv2.drawContours(pentagon_temp, [pent_points], -1, (0, 0, 0), -1)

    #create hexagon template
    hexagon_temp = np.ones((200, 200, 3), np.uint8) * 255
    pt1 = (100, 50)
    pt2 = (150, 76)
    pt3 = (150, 124)
    pt4 = (100, 150)
    pt5 = (50, 124)
    pt6 = (50, 76)
    hex_points = np.array([pt1, pt2, pt3, pt4, pt5,pt6])
    cv2.drawContours(hexagon_temp, [hex_points], -1, (0, 0, 0), -1)

    #choose random order of random shapes
    shapes=[["triangle",triangle_temp],
             ["circle",circle_temp],
             ["square",square_temp]]
    shapes=random.sample(shapes,3)
    shape_order=[]
    i=0
    while i<3:
        shape_order.append(shapes[i][1])
        i+=1
    if( not shapes_colors_connected):
        x = random.randrange(2)
    shape_matrix=np.ndarray((3,3,200,200,3))
    #make all the shapes in the shape matrix the same 1/3 of the time
    if(x==2 and same_shape):
        i=0
        j=0
        while (i<3):
            while (j<3):
                shape_matrix[i][j]=shape_order[0]
                j+=1
            j=0
            i+=1
    #otherwise the shapes will be random for 2/3 of the time
    else:
        i=0
        j=0
        while (i<3):
            while (j<3):
                shape_matrix[i][j]=shape_order[i]
                j+=1
            j=0
            i+=1



    #elif(not choices.one_colour and not choices.one_shape):
    if(shapes_colors_connected):
        x=random.choices(shape_shift)
        shift_colours(colour_matrix, x)
        shift_shapes(shape_matrix, x)
        if (bool(random.getrandbits(1)) and transpose_shape):
            selfmade_transpose(shape_matrix)
            selfmade_transpose(colour_matrix)

    else:
        shift_colours(colour_matrix,random.choice(colour_shift))
        shift_shapes(shape_matrix,random.choice(shape_shift))
        if(bool(random.getrandbits(1)) and transpose_shape):
                selfmade_transpose(shape_matrix)
        if(bool(random.getrandbits(1)) and transpose_colour):
                selfmade_transpose(colour_matrix)

    puzzle=draw_puzzle(shape_matrix,colour_matrix)
    shape_name=resolve_shape(shape_matrix,shapes)
    colour_name = resolve_colour(colour_matrix,colour,colour_palette)

    return [puzzle,shape_name,colour_name]

def main():

    #when set to true an example will be generated and displayed
    show_example = False

    #settings for creating a dataset, if create_dataset is true a dataset will be created.
    #there is also the possibility of choosing how many training examples and test examples are generated.
    create_dataset = True
    amount_examples_train_dataset = 200
    amount_examples_test_dataset = 50


    #settings adjusting what kind of puzzles can be generated
    #give a list of shift values that are allowed. Normal values [-1,0,1] 0 is no shift, -1 left, +1 right.
    shape_shift=[-1,0,1]
    colour_shift=[-1,0,1]

    #allows transposition for colours and shapes
    transpose_shape=True
    transpose_colour=True

    #if set to true allows the puzzle to all have the same shape or same colour
    same_shape=True
    same_colour=True

    #makes the colour matrix do whatever the shape matrix does
    shapes_colors_connected=False


    if show_example:
        puzzle, shape_name, colour_name = build_puzzle(shape_shift,colour_shift,transpose_shape,transpose_colour,same_shape,same_colour,shapes_colors_connected)
        cv2.imshow(shape_name,np.squeeze(puzzle))
        cv2.waitKey()


    if create_dataset:
        print(os.getcwd())
        os.makedirs("./dataset/images")

        create_cut_sub_dataset('train', amount_examples_train_dataset, 0,shape_shift,colour_shift,transpose_shape,transpose_colour,same_shape,same_colour,shapes_colors_connected)
        create_cut_sub_dataset('test', amount_examples_test_dataset, amount_examples_train_dataset,shape_shift,colour_shift,transpose_shape,transpose_colour,same_shape,same_colour,shapes_colors_connected)


if __name__ == '__main__':
    main()