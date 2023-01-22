import cv2
import numpy as np
import random




def shift_colours(colour_matrix):
    temp=np.array([[0,0,0],[0,0,0],[0,0,0]])

    #shift second row
    i=0
    while i<3:
        temp[i]=colour_matrix[1][i]
        i+=1
    print(temp)
    temp=np.roll(temp,-1,axis=0)
    print(temp)
    i=0
    while i<3:
        colour_matrix[1][i]=temp[i]
        i+=1

    #shift third row
    temp=np.roll(temp,-1,axis=0)
    i=0
    while i<3:
        colour_matrix[2][i]=temp[i]
        i+=1

def shift_shapes(shape_matrix):
    temp=np.zeros((3,200,200,3))
    
    #shift second row
    i=0
    while(i<3):
       
        temp[i]=shape_matrix[i][1]
        i+=1
    temp=np.roll(temp,-1,axis=0)
   

    i=0
    while i<3:
        shape_matrix[i][1]=temp[i]
        i+=1
    
    #shift third row
    temp=np.roll(temp,-1,axis=0)
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

def template_switch(x,triangle_temp,circle_temp,square_temp):
    if x==1:
        return triangle_temp
    elif x==2:
        return circle_temp
    else:
        return square_temp


def colour_puzzles():
    colour_palette=np.array([[0,0,255],[0,255,255],[0,255,0],[255,255,0],[255,0,0],[255,0,255]])
    #red, yellow,green,cyan,blue and magenta in BGR 


    #choose random colour order
    colour_order=np.zeros([3,3])
    
    x1=random.choice(colour_palette)
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
    colour_matrix=np.array([colour_order,colour_order,colour_order])
    #shift_colours(colour_matrix)
    
   

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
    i=0
    j=0
    while (i<3):
        while (j<3):
            shape_matrix[i][j]=shape_order[i]
            j+=1
        j=0
        i+=1
    shift_shapes(shape_matrix)

    puzzle=draw_puzzle(shape_matrix,colour_matrix)

    cv2.imshow("image1",np.squeeze(puzzle))
    cv2.waitKey()

def main():
    colour_puzzles()


if __name__ == '__main__':
    main()