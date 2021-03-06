## CSC320 Winter 2020 
## Assignment 1
## (c) Kyros Kutulakos
##
## DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
## AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION 
## BY THE INSTRUCTOR IS STRICTLY PROHIBITED. VIOLATION OF THIS 
## POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY

##
## DO NOT MODIFY THIS FILE ANYWHERE EXCEPT WHERE INDICATED
##

# import basic packages
import numpy as np
import scipy.linalg as sp
import cv2 as cv

# If you wish to import any additional modules
# or define other utility functions, 
# include them here

#########################################
## PLACE YOUR CODE BETWEEN THESE LINES ##
#########################################


#########################################

#
# The Matting Class
#
# This class contains all methods required for implementing 
# triangulation matting and image compositing. Description of
# the individual methods is given below.
#
# To run triangulation matting you must create an instance
# of this class. See function run() in file run.py for an
# example of how it is called
#
class Matting:
    #
    # The class constructor
    #
    # When called, it creates a private dictionary object that acts as a container
    # for all input and all output images of the triangulation matting and compositing 
    # algorithms. These images are initialized to None and populated/accessed by 
    # calling the the readImage(), writeImage(), useTriangulationResults() methods.
    # See function run() in run.py for examples of their usage.
    #
    def __init__(self):
        self._images = { 
            'backA': None, 
            'backB': None, 
            'compA': None, 
            'compB': None, 
            'colOut': None,
            'alphaOut': None, 
            'backIn': None, 
            'colIn': None, 
            'alphaIn': None, 
            'compOut': None, 
        }

    # Return a dictionary containing the input arguments of the
    # triangulation matting algorithm, along with a brief explanation
    # and a default filename (or None)
    # This dictionary is used to create the command-line arguments
    # required by the algorithm. See the parseArguments() function
    # run.py for examples of its usage
    def mattingInput(self): 
        return {
            'backA':{'msg':'Image filename for Background A Color','default':None},
            'backB':{'msg':'Image filename for Background B Color','default':None},
            'compA':{'msg':'Image filename for Composite A Color','default':None},
            'compB':{'msg':'Image filename for Composite B Color','default':None},
        }
    # Same as above, but for the output arguments
    def mattingOutput(self): 
        return {
            'colOut':{'msg':'Image filename for Object Color','default':['color.tif']},
            'alphaOut':{'msg':'Image filename for Object Alpha','default':['alpha.tif']}
        }
    def compositingInput(self):
        return {
            'colIn':{'msg':'Image filename for Object Color','default':None},
            'alphaIn':{'msg':'Image filename for Object Alpha','default':None},
            'backIn':{'msg':'Image filename for Background Color','default':None},
        }
    def compositingOutput(self):
        return {
            'compOut':{'msg':'Image filename for Composite Color','default':['comp.tif']},
        }
    
    # Copy the output of the triangulation matting algorithm (i.e., the 
    # object Color and object Alpha images) to the images holding the input
    # to the compositing algorithm. This way we can do compositing right after
    # triangulation matting without having to save the object Color and object
    # Alpha images to disk. This routine is NOT used for partA of the assignment.
    def useTriangulationResults(self):
        if (self._images['colOut'] is not None) and (self._images['alphaOut'] is not None):
            self._images['colIn'] = self._images['colOut'].copy()
            self._images['alphaIn'] = self._images['alphaOut'].copy()

    # If you wish to create additional methods for the 
    # Matting class, include them here

    #########################################
    ## PLACE YOUR CODE BETWEEN THESE LINES ##
    #########################################

    #########################################
            
    # Use OpenCV to read an image from a file and copy its contents to the 
    # matting instance's private dictionary object. The key 
    # specifies the image variable and should be one of the
    # strings in lines 54-63. See run() in run.py for examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # leave the matting instance's dictionary entry unaffected and return
    # False, along with an error message
    def readImage(self, fileName, key):
        success = True
        msg = 'Read'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        try:
            image = cv.imread(fileName)
            image = image.astype(np.float64)
            self._images[key] = image
        except:
            success = False
            msg = "Image read failed"

        #########################################
        return success, msg

    # Use OpenCV to write to a file an image that is contained in the 
    # instance's private dictionary. The key specifies the which image
    # should be written and should be one of the strings in lines 54-63. 
    # See run() in run.py for usage examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # return False, along with an error message
    def writeImage(self, fileName, key):
        success = True
        msg = 'Write'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        try:
            cv.imwrite(fileName, self._images[key])
        except:
            success = False
            msg = "Image write failed"

        #########################################
        return success, msg

    # Method implementing the triangulation matting algorithm. The
    # method takes its inputs/outputs from the method's private dictionary 
    # ojbect. 
    def triangulationMatting(self):
        """
        success, errorMessage = triangulationMatting(self)
        
        Perform triangulation matting. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
        """

        success = False
        msg = 'Matting'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        backA = self._images["backA"]
        backB = self._images["backB"]
        compA = self._images["compA"]
        compB = self._images["compB"]

        # error checking
        if backA is None or backB is None or compA is None or compB is None:
            msg = "Missing background or foreground images"
            return success, msg

        mSize = backA.shape
        alpha = np.zeros(mSize[:2])
        foreground = np.zeros(mSize)

        for i in range(mSize[0]):
            for j in range(mSize[1]):
                try:
                    C_delta = np.array([
                        [compA[i][j][2] - backA[i][j][2]], #R_A
                        [compA[i][j][1] - backA[i][j][1]], #G_A
                        [compA[i][j][0] - backA[i][j][0]], #B_A
                        [compB[i][j][2] - backB[i][j][2]], #R_B
                        [compB[i][j][1] - backB[i][j][1]], #G_B
                        [compB[i][j][0] - backB[i][j][0]]  #B_B
                    ])
                except:
                    msg = "Assign C_delta error"
                    return success, msg

                try:
                    B_0 = np.array([
                        [1, 0, 0, -backA[i][j][2]], #R
                        [0, 1, 0, -backA[i][j][1]], #G
                        [0, 0, 1, -backA[i][j][0]], #B
                        [1, 0, 0, -backB[i][j][2]], #R
                        [0, 1, 0, -backB[i][j][1]], #G
                        [0, 0, 1, -backB[i][j][0]]  #B
                    ])
                except:
                    msg = "Assign B_0 error"
                    return success, msg

                try:
                    result = np.matmul(np.linalg.pinv(B_0),C_delta)
                except:
                    msg = "Matrix calculation error"
                    return success, msg
                alpha[i][j] = result[3][0]
                foreground[i][j] = np.array([
                    [result[2][0], result[1][0], result[0][0]]
                ])

        self._images['colOut'] = foreground
        self._images['alphaOut'] = alpha * 255
        # cv.imshow("foreground", foreground)
        # cv.imshow("alpha", alpha * 255)
        success = True
        

        #########################################

        return success, msg

        
    def createComposite(self):
        """
        success, errorMessage = createComposite(self)
        
        Perform compositing. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
        """

        success = False
        msg = 'Composite'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        alpha = self._images['alphaIn'] / 255
        col = self._images['colIn']
        back = self._images['backIn']
        mSize = back.shape
        comp = np.zeros(mSize)


        for i in range(mSize[0]):
            for j in range(mSize[1]):
                pCol = col[i][j]
                pAlpha = alpha[i][j]
                pBack = back[i][j]
                try:
                    comp[i][j] = pAlpha * pCol + (1 - pAlpha) * pBack
                except:
                    msg = "Comp calculation error"
                    return success, msg

        self._images['compOut'] = comp 
        # cv.imshow("comp", comp)
        success = True
        #########################################

        return success, msg


