import cv2
import numpy as np
import random
import argparse
import sys

def selfmade_transpose(matrix):
    temp=matrix.copy()
    i=0
    j=0
    while(i<np.shape(matrix)[0]):
        while(j<np.shape(matrix)[1]):
            matrix[i][j]=temp[j][i]
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
            if template[i][j][0]==0 and template[i][j][1]==0 and template[i][j][2]==0:
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


def build_puzzle(choices):
    colour_palette=np.array([[0,0,255],[0,255,255],[0,255,0],[255,255,0],[255,0,0],[255,0,255]])
    #red, yellow,green,cyan,blue and magenta in BGR 


    #choose random colour order
    colour_order=np.zeros([3,3])
    
    x1=random.choice(colour_palette)

    #make the colour order one colour if chosen by user argument
    if(choices.one_colour):
        colour_order[0]=x1
        colour_order[1]=x1
        colour_order[2]=x1

    #otherwise the colour order is random
    else:
        colour_order[0]=x1
        while(1):
      
            x2=random.choice(colour_palette)
            if np.array_equiv(x1,x2)==False:
                break
        colour_order[1]=x2
        while(1):
            x3=random.choice(colour_palette)
            if np.array_equiv(x3,x1)==False and np.array_equiv(x3,x2)==False:
                break
        colour_order[2]=x3

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

    #choose random order of random shapes
    shapes=[triangle_temp,circle_temp,square_temp]
    shape_order=random.sample(shapes,3)
    
    #create a shape matrix from randomly chosen shapes
    shape_matrix=np.ndarray((3,3,200,200,3))
    #make all the shapes in the shape matrix the same if chosen by user argument
    if(choices.one_shape):
        i=0
        j=0
        while (i<3):
            while (j<3):
                shape_matrix[i][j]=shape_order[0]
                j+=1
            j=0
            i+=1
    #otherwise the shapes will be random
    else:
        i=0
        j=0
        while (i<3):
            while (j<3):
                shape_matrix[i][j]=shape_order[i]
                j+=1
            j=0
            i+=1

    #change colour and shape matrix based on choices
    if len(sys.argv)>1:
        print("no")
        if choices.colourshift is not None and choices.one_colour is False:
            shift_colours(colour_matrix,choices.colourshift)
        if choices.shapeshift is not None and choices.one_shape is False:
            shift_shapes(shape_matrix,choices.shapeshift)
        if choices.transpose_colour:
            selfmade_transpose(colour_matrix)
        if choices.transpose_shapes:
            selfmade_transpose(shape_matrix)
    elif(not choices.one_colour and not choices.one_shape):
        print("yes")
        shift_colours(colour_matrix,random.choice([-2,-1,0,1,2]))
        shift_shapes(shape_matrix,random.choice([-2,-1,0,1,2]))
        if(bool(random.getrandbits(1))):
            selfmade_transpose(colour_matrix)
        if(bool(random.getrandbits(1))):
            selfmade_transpose(shape_matrix)
    puzzle=draw_puzzle(shape_matrix,colour_matrix)
    
    cv2.imshow("image1",np.squeeze(puzzle))
    cv2.waitKey()

def main():
    #parser for user arguments
    parser=argparse.ArgumentParser(description='choose what kind of random puzzles you want with the help of arguments. If none are given, they will be random.')
    parser.add_argument("--shift_colours",type=int,choices=[-2,-1,1,2],dest="colourshift",help="decide how the colours will be shifted in the puzzle. Negative values will shift to the left, positive values to the right.")
    parser.add_argument("--shift_shapes",type=int,choices=[-2,-1,1,2],dest="shapeshift",help="decide how the shapes will be shifted in the puzzle. Negative values will shift to the left, positive values to the right.")
    parser.add_argument("--one_colour",action="store_true",help="the shapes of the puzzle will consist of one colour instead of three random colours")
    parser.add_argument("--one_shape",action="store_true",help="the shapes of the puzzle will be one type of shape instead of three random shapes") 
    parser.add_argument("--transpose_colour",action="store_true",help="will transpose the colours of the puzzle ")
    parser.add_argument("--transpose_shapes",action="store_true",help="will transpose the shapes of the puzzle")
    x=None
    parsed_args=parser.parse_args()
    if parsed_args.colourshift is not None:
        print("hey amigo")
    if not len(sys.argv) > 1:
        print(len(sys.argv))
    parsed_args=parser.parse_args()
    print(parsed_args)
    build_puzzle(parsed_args)


if __name__ == '__main__':
    main()