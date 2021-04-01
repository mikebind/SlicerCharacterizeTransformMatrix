# SlicerCharacterizeLinearTransform

Have you ever looked at a 4x4 transformation matrix and tried to figure out what it was doing? All the information is in those 12 numbers, but not in an easily understood format. This project is a simple utility module for 3D Slicer ([slicer.org](slicer.org)) which tries to quickly give you any information you might want to know about what a transformation matrix is doing.  For example, is it a rigid transformation or is there scaling?  If there is scaling, what are the scale factors and stretch directions?  Is there rotation?  If so, what is the axis of rotation and how much rotation occurs around that axis?  Alternatively, if we break down the rotation into a sequence of rotations around coordinate axes, what is the rotation about each axis?

## To use
Once installed into 3D Slicer, to use, just open the module and select the transform node you want to know about.  An analysis such as the following will appear in the text box below:

```
Scale factors and stretch directions (eigenvalues and eigenvectors of stretch matrix K):
  f0: +0.012% change in direction [1.00, 0.03, -0.08]
  f1: -2.843% change in direction [-0.08, -0.10, -0.99]
  f2: +3.248% change in direction [0.04, -0.99, 0.10]
This transform is not rigid! Total volume changes by +0.325%, and maximal change in one direction is +3.248%
The rotation matrix portion of this transformation rotates 15.0 degrees ccw (if you look in the direction the vector points) around a vector which points to [0.76, -0.59, -0.27] (RAS)
Broken down into a series of rotations around axes, the rotation matrix portion of the transformation rotates 
  11.8 degrees ccw around the positive R axis, then 
  8.4 degrees cw around the positive A axis, then 
  5.0 degrees cw around the positive S axis
Lastly, this transformation translates, shifting:
  +194.2 mm in the R direction
  +73.4 mm in the A direction
  -1170.3 mm in the S direction
```
This analysis is for the matrix 
```
0.985821 0.0570188 -0.157817 194.155 
-0.0873217 1.01 -0.192319 73.4412 
0.14329 0.203373 0.94 -1170.25 
0 0 0 1 
```

## To Install
1. Clone or download this repository.  If you download it as a zip, unzip and copy the CharacterizeTransformMatrix folder to wherever you would like it to live (a SlicerModules/ subdirectory of your Documents folder is fine).
2. Open Slicer, click the "Edit" menu, then "Application Settings" (or enter Ctrl-2)
3. Click "Modules" on the left.
4. To the right of the "Additional module paths:", click the ">>" button, then click "Add".
5. Navigate to and select the CharacterizeTransformMatrix folder that you cloned or downloaded. 
6. Restart Slicer.
7. Click the magnifying glass just to the right of "Modules:" in the toolbar, and start typing "Characterize", and this module should show up. 
8. Click "Switch to Module". 

## Some Decomposition Details
This module uses polar decomposition to describe the components of a 4x4 transform matrix. The decomposition has the form: `H = T * R * K`, where `H` is the full homogeneous transformation matrix (with 0,0,0,1 as the bottom row), `T` is a translation-only matrix, `R` is a rotation-only matrix, and `K` is a stretch matrix. `K` can further be decompsed into three scale matrices, which can each be characterized by a stretch direction (an eigenvector) and a stretch factor (the associated eigenvalue). Points to be transformed are on the right, so the order of operations is stretching first, then rotation, then translation. 

If you would like access to the decomposed components of the matrix, you can call the relevant logic function of this module as follows: 
```
import CharacterizeTransformMatrix 
decompositionResults = CharacterizeTransformMatrix.CharacterizeTransformMatrixLogic().characterizeLinearTransformNode(transformNode)
```
`decompositionResults` will then be a namedTuple with all the information from the decomposition. For example, `decompositionResults.rotationAngleDegrees` will have the angle the transformation rotates by around the rotation axis.  The named fields of the results are

|Field Name| Description|
| ----------- | ----------- |
| textResults | a line by line list of the analysis text |
| isRigid | boolean, true if largest strech % change is less that 0.1% |
| scaleFactors | numpy vector of scale factors in eigendirections of stretch matrix (with a 4th element which is always 1) |
|scaleDirections| list of 3 scale directions as 4 element vectors (4th element always 0)|
|largestPercentChangeScale | largest scale factor as a percent change (100 * (scaleFactor-1)) |
|volumePercentChangeOverall| total volume % change after all stretching/shrinking|
|scipyRotationObject| scipy `Rotation` object of the rotation component of the transform|
|rotationAxis | RAS vector describing the axis the transform rotates about|
|rotationAngleDegrees| positive if counterclockwise when looking down axis|
|eulerAnglesRAS | sequence of rotation angles about the Right, Anterior, and then Superior axes|
|translationVector| 3-element vector of RAS translation|
|translationOnlyMatrix| identitiy matrix with translation vector in 4th column|
|rotationOnlyMatrix|4x4 rotation matrix `R` from the decomposition|
|stretchOnlyMatrix|4x4 stretch matrix `K` from the decomposition|
|scaleMatrixList|list of three 4x4 symmetric (likely non-uniform) scale matrices (`S1*S2*S3=K`)|
|stretchEigenvectorMatrix|4x4 matrix with the stretch direction eigenvectors as the first 3 columns|

