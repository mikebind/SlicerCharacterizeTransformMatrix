import os
import unittest
import logging
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
import numpy as np

#
# CharacterizeTransformMatrix
#

class CharacterizeTransformMatrix(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "CharacterizeTransformMatrix"  # TODO: make this more human readable by adding spaces
    self.parent.categories = ["MikeTools"]  # TODO: set categories (folders where the module shows up in the module selector)
    self.parent.dependencies = []  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["Mike Bindschadler (Seattle Children's Hospital)"]  # TODO: replace with "Firstname Lastname (Organization)"
    # TODO: update with short description of the module and a link to online module documentation
    self.parent.helpText = """
This module uses polar decomposition to describe the components of a 4x4 transform matrix. The decomposition has the form:
H = T * R * K, where H is the full homogeneous transformation matrix (with 0,0,0,1 as the bottom row), T is a translation-only matrix,
R is a rotation-only matrix, and K is a stretch matrix. K can further be decompsed into three scale matrices, which can each be
characterized by a stretch direction (an eigenvector) and a stretch factor (the associated eigenvalue). Points 
to be transformed are on the right, so the order of operations is stretching first, then rotation, then translation.

If you would like access to the decomposed components of the matrix, you can call the relevant logic function of this module as follows:

import CharacterizeTransformMatrix

decompositionResults = CharacterizeTransformMatrix.CharacterizeTransformMatrixLogic().characterizeLinearTransformNode(transformNode)

decompositionResults will then be a namedTuple with all the information from the decomposition.

See more information in <a href="https://github.com/mikebind/SlicerCharacterizeLinearTransform">module documentation</a>.
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
This file was originally developed by Mike Bindschadler and funded by Seattle Children's Hosptial.  The decomposition approach closely follows an example originally found <a href="https://colab.research.google.com/drive/1ImBB-N6P9zlNMCBH9evHD6tjk0dzvy1_"> here</a>.
"""

    # Additional initialization step after application startup is complete
    slicer.app.connect("startupCompleted()", registerSampleData)

#
# Register sample data sets in Sample Data module
#

def registerSampleData():
  """
  Add data sets to Sample Data module.
  """
  # It is always recommended to provide sample data for users to make it easy to try the module,
  # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

  import SampleData
  iconsPath = os.path.join(os.path.dirname(__file__), 'Resources/Icons')

  # To ensure that the source code repository remains small (can be downloaded and installed quickly)
  # it is recommended to store data sets that are larger than a few MB in a Github release.

  # CharacterizeTransformMatrix1
  SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='CharacterizeTransformMatrix',
    sampleName='CharacterizeTransformMatrix1',
    # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
    # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
    thumbnailFileName=os.path.join(iconsPath, 'CharacterizeTransformMatrix1.png'),
    # Download URL and target file name
    uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
    fileNames='CharacterizeTransformMatrix1.nrrd',
    # Checksum to ensure file integrity. Can be computed by this command:
    #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
    checksums = 'SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95',
    # This node name will be used when the data set is loaded
    nodeNames='CharacterizeTransformMatrix1'
  )

  # CharacterizeTransformMatrix2
  SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='CharacterizeTransformMatrix',
    sampleName='CharacterizeTransformMatrix2',
    thumbnailFileName=os.path.join(iconsPath, 'CharacterizeTransformMatrix2.png'),
    # Download URL and target file name
    uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
    fileNames='CharacterizeTransformMatrix2.nrrd',
    checksums = 'SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97',
    # This node name will be used when the data set is loaded
    nodeNames='CharacterizeTransformMatrix2'
  )

#
# CharacterizeTransformMatrixWidget
#

class CharacterizeTransformMatrixWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self.logic = None
    self._parameterNode = None
    self._updatingGUIFromParameterNode = False

  def setup(self):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.setup(self)

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/CharacterizeTransformMatrix.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
    # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
    # "setMRMLScene(vtkMRMLScene*)" slot.
    uiWidget.setMRMLScene(slicer.mrmlScene)

    # Create logic class. Logic implements all computations that should be possible to run
    # in batch mode, without a graphical user interface.
    self.logic = CharacterizeTransformMatrixLogic()

    # Connections

    

    # These connections ensure that whenever user changes some settings on the GUI, that is saved in the MRML scene
    # (in the selected parameter node).
    self.ui.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onTransformNodeChange)
    

    # Make sure parameter node is initialized (needed for module reload)
    #self.initializeParameterNode()

  def onTransformNodeChange(self):
    """ Update the text area with info about newly selected transform node
    """
    transformNode = self.ui.inputSelector.currentNode()
    if transformNode is None:
      self.ui.transformDescriptionTextEdit.setPlainText("No transform node selected")
      return
    elif not transformNode.IsLinear():
      self.ui.transformDescriptionTextEdit.setPlainText("Selected transform is composite or not linear")
      return
    # Otherwise, transform node exists and is linear
    results = self.logic.characterizeLinearTransformNode(transformNode)
    resultsText = results.textResults
    resultsText = '\n'.join(resultsText)
    self.ui.transformDescriptionTextEdit.setPlainText(resultsText)


  def cleanup(self):
    """
    Called when the application closes and the module widget is destroyed.
    """
    self.removeObservers()

  


#
# CharacterizeTransformMatrixLogic
#

class CharacterizeTransformMatrixLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self):
    """
    Called when the logic class is instantiated. Can be used for initializing member variables.
    """
    ScriptedLoadableModuleLogic.__init__(self)


  def characterizeLinearTransformNode(self, transformNode, verbose=True):
    H = slicer.util.arrayFromTransformMatrix(transformNode)
    # H is 4x4 numpy array transformation matrix
    outputs = self.characterizeLinearTransformMatrix(H, verbose=verbose)
    return outputs #outputs is a namedtuple

  def characterizeLinearTransformMatrix(self, H, verbose=True):
    import numpy as np
    import scipy
    T,R,K,S,f,X = self.polarDecompose(H)
    textResults = []
    #### Stretch
    # Report scale factors and stretch directions, determine if rigid, largest percent change, volumePercentChange
    line = 'Scale factors and stretch directions (eigenvalues and eigenvectors of stretch matrix K):'
    textResults.append(line)
    if verbose:
      print(line) 
    percentChanges = []
    scaleDirections = []
    for idx, (factor, axis) in enumerate(zip(f[:3], X.T[:3])):
      percentChange = 100 * (factor-1)
      percentChanges.append(percentChange)
      scaleDirections.append(axis)
      line = '  f%i: %+0.3f%% change in direction [%0.2f, %0.2f, %0.2f]' % (idx, percentChange, *axis[:3])
      textResults.append(line)
      if verbose:
        print(line)
    largestPercentChangeIdx = np.argmax(np.abs(percentChanges))
    largestPercentChange = percentChanges[largestPercentChangeIdx]
    volumePercentChange = (np.prod(f)-1) * 100
    if np.abs(largestPercentChange) < 0.1:
      isRigid = True
      line = 'This transform is essentially rigid (largest percent scale changes is %+0.3f%%, volume percent change is %+0.3f%%).' % (largestPercentChange, volumePercentChange)
      textResults.append(line)
      if verbose:
        print(line)
    else: 
      isRigid = False
      line = 'This transform is not rigid! Total volume changes by %+0.3f%%, and maximal change in one direction is %+0.3f%%'%(volumePercentChange,largestPercentChange)
      textResults.append(line)
      if verbose:
        print(line)
    #### Rotation
    # Create Rotation object from matrix
    r = scipy.spatial.transform.Rotation.from_matrix(R[:3,:3])
    #
    # What is rotation axis and rotation angle about that axis?
    rv = r.as_rotvec() # the conversion ensures angle is >=0 and <=pi, axis is inverted as needed to make this true
    rotation_angle_deg = 180/np.pi*np.linalg.norm(rv) # length of rotvec is rotation angle in radians
    if rotation_angle_deg < 1e-4 :
      # No rotation!
      line = 'There is essentially no rotation (rotation angle =  %0.1g degrees (less than < 1e-4 degrees threshold)).'%(rotation_angle_deg)
      textResults.append(line)
      if verbose:
        print(line)
      # expected outputs need to be filled with NaNs
      rotation_axis = [np.NaN]*3 # no rotation axis
      euler_angles_xyz = [np.NaN]*3 # no rotations...
    else:
      # There is rotation
      # If you look in the direction of the rotation axis vector, positive angles mean counter-clockwise rotation.
      # (as_rotvec() always returns non-negative angles, the rotation axis is inverted as necessary)
      # If you point your LEFT thumb in the direction of the rotation axis, your fingers curl in the positive rotation direction
      rotation_axis = rv/np.linalg.norm(rv) # unit vector version of rotation axis
      #
      line = 'The rotation matrix portion of this transformation rotates %0.1f degrees %s (if you look in the direction the vector points) around a vector which points to [%0.2f, %0.2f, %0.2f] (RAS)' % (np.abs(rotation_angle_deg), 'ccw' if rotation_angle_deg>=0 else 'cw', *rotation_axis)
      textResults.append(line)
      if verbose:
        print(line)
      #
      # What is the best way to understand these as a sequence of rotations around coordinate axes?
      euler_angles_xyz = r.as_euler('xyz',degrees=True)
      # The results are the rotation angles about the positive x axis, then y, then z (in that order,
      # and without the axes moving with the volume ("extrinsic" axes, not "intrinsic"))
      # Same as above, positive angles mean ccw rotation if looking in the positive direction along the
      # axis.  
      Rrot,Arot,Srot = euler_angles_xyz
      line = 'Broken down into a series of rotations around axes, the rotation matrix portion of the transformation rotates \n  %0.1f degrees %s around the positive R axis, then \n  %0.1f degrees %s around the positive A axis, then \n  %0.1f degrees %s around the positive S axis' % (np.abs(Rrot), 'ccw' if Rrot>=0 else 'cw', np.abs(Arot), 'ccw' if Arot>=0 else 'cw', np.abs(Srot), 'ccw' if Srot>=0 else 'cw')
      textResults.append(line)
      if verbose:
        print(line)
        
    #### Translation
    translationVector = T[:3,3]
    line = 'Lastly, this transformation translates, shifting:\n  %+0.1f mm in the R direction\n  %+0.1f mm in the A direction\n  %+0.1f mm in the S direction' %(*translationVector,)
    textResults.append(line)
    if verbose:
      print(line)
    #### Return values as named tuple
    import collections
    resultsNamedTupleClass = collections.namedtuple('TransformMatrixAnaylsisResults',
        ['textResults','isRigid','scaleFactors','scaleDirections','largestPercentChangeScale','volumePercentChangeOverall',
        'scipyRotationObject','rotationAxis','rotationAngleDegrees','eulerAnglesRAS', 'translationVector',
        'translationOnlyMatrix','rotationOnlyMatrix','stretchOnlyMatrix','scaleMatrixList','stretchEigenvectorMatrix'
        ])
    results = resultsNamedTupleClass(
      textResults=textResults, isRigid=isRigid, scaleFactors=f, scaleDirections=scaleDirections,
      largestPercentChangeScale=largestPercentChange, volumePercentChangeOverall=volumePercentChange, 
      scipyRotationObject=r, rotationAxis=rotation_axis, rotationAngleDegrees=rotation_angle_deg, 
      eulerAnglesRAS=euler_angles_xyz, translationVector=translationVector, translationOnlyMatrix=T, 
      rotationOnlyMatrix=R, stretchOnlyMatrix=K, scaleMatrixList=S, stretchEigenvectorMatrix=X )
    return results

  def separateTranslation(self, H):
    T = np.eye(4)
    T[:3,3] = H[:3,3]
    L = H.copy()
    L[:3,3] = 0
    assert np.allclose(H, T @ L), 'T*L should equal H, but it does not!'
    return T, L 

  def polarDecompose(self, H):
    from scipy.linalg import polar
    T, L = self.separateTranslation(H) # T is translation matrix, 
    R, K = polar(L) # R is rotation matrix, K is stretch matrix
    # The determinant of a rotation matrix must be positive
    if np.linalg.det(R) < 0:
      R[:3,:3] = -R[:3,:3]
      K[:3,:3] = -K[:3,:3]
    # Check answer still OK
    assert np.allclose(L, R @ K), 'R*K should equal L, but it does not!'
    assert np.allclose(H, T @ R @ K), 'T*R*K should equal H, but it does not!'
    # Decompose stretch matrix K into scale matrices
    f, X = np.linalg.eig(K) # eigenvalues and eigenvectors of stretch matrix
    S = []
    for factor, axis in zip(f[:3], X.T[:3]):
      #if not np.isclose(factor, 1):
      scale = np.eye(4) + np.outer(axis,axis) * (factor - 1)
      S.append(scale)
    # Check answers still OK
    scale_prod = np.eye(4)
    for scale in S:
      scale_prod = scale_prod @ scale
    if not np.allclose( K, scale_prod):
      print('Product of scale matrices should equal stretch matrix K, but it does not!')
    if not np.allclose( H, T @ R @ scale_prod):
      print('T*R*(product of scale matrices) should equal stretch matrix K, but it does not!')
    # Return all interesting outputs
    return T, R, K, S, f, X






#
# CharacterizeTransformMatrixTest
#

class CharacterizeTransformMatrixTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear()

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_CharacterizeTransformMatrix1()

  def test_CharacterizeTransformMatrix1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")

    self.delayDisplay('Test passed')
