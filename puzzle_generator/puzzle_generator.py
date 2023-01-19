import cv2
import numpy as np
import random


def shift_right(colour_matrix):
    print("x1", colour_matrix[1][0])
    print("x2", colour_matrix[2][0])

    #second row
    x=np.array([colour_matrix[1][0][0],colour_matrix[1][0][1],colour_matrix[1][0][2]]) #written like this so that the actual values are put in x and not just a pointer
   
    colour_matrix[1][0]=colour_matrix[1][2]
    colour_matrix[1][2]=colour_matrix[1][1]
    colour_matrix[1][1]=x
  

    #third row
    colour_matrix[2][0]=colour_matrix[2][1]
    colour_matrix[2][1]=colour_matrix[2][2]
    colour_matrix[2][2]=x



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
    puzzle=draw_sector(shape_matrix[0][0],colour_matrix[1][1],puzzle,200,200)
    puzzle=draw_sector(shape_matrix[0][0],colour_matrix[2][1],puzzle,200,400)

    #third colomn

   
    puzzle=draw_sector(shape_matrix[0][0],colour_matrix[0][2],puzzle,400,0)
    puzzle=draw_sector(shape_matrix[0][0],colour_matrix[1][2],puzzle,400,200)

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
    shift_right(colour_matrix)
    
   

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
    
     #create a shape matrix from the random chosen 
    shape_matrix=np.ndarray((3,3,200,200,3))
    i=0
    j=0
    while (i<3):
        while (j<3):
            shape_matrix[i][j]=shape_order[i]
            j+=1
        j=0
        i+=1



    puzzle=draw_puzzle(shape_matrix,colour_matrix)
   

    #draw puzzle
    #puzzle = np.ones((600, 600, 3), np.uint8) * 255
    #first colomn
    #template=template_switch(shape_order[0],triangle_temp,circle_temp,square_temp)
    #puzzle=draw_sector(template,0,0,puzzle,0,0,colour_matrix)
    #puzzle=draw_sector(template,0,200,puzzle,0,1,colour_matrix)
    #puzzle=draw_sector(template,0,400,puzzle,0,2,colour_matrix)
    #second colomn
    #template=template_switch(shape_order[1],triangle_temp,circle_temp,square_temp)
    #puzzle=draw_sector(template,200,0,puzzle,1,0,colour_matrix)
    #puzzle=draw_sector(template,200,200,puzzle,1,1,colour_matrix)
    #puzzle=draw_sector(template,200,400,puzzle,1,2,colour_matrix)
    ##third colomn
    #template=template_switch(shape_order[2],triangle_temp,circle_temp,square_temp)
    #puzzle=draw_sector(template,400,0,puzzle,2,0,colour_matrix)
    #puzzle=draw_sector(template,400,200,puzzle,2,1,colour_matrix)

    cv2.imshow("image1",np.squeeze(puzzle))
    cv2.waitKey()

def main():
    colour_puzzles()


if __name__ == '__main__':
    main()