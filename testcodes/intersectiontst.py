
def intersectionpt(p1,p2,p3,p4):
    

    # line p1 p2 
    a1 = p2[1] - p1[1] 
    b1 = p1[0] - p2[0] 
    c1 = a1*(p1[0]) + b1*(p1[1])


    #line p3 p4

    a2 = p4[1] - p3[1] 
    b2 = p3[0] - p4[0] 
    c2 = a2*(p3[0])+ b2*(p3[1])
 

    #determinant

    determinant = a1*b2 - a2*b1

    if (determinant == 0) :

        #The lines are parallel. This is simplified 
        # by returning a pair of FLT_MAX 
        print('The points are parallel')
        return (0,0) 
    else:
        mx = (b2*c1 - b1*c2)/determinant; 
        my = (a1*c2 - a2*c1)/determinant; 
        return (mx, my); 
         







