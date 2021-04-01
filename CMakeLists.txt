cmake_minimum_required(VERSION 3.13.4)

project(MikeTools)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/MikeTools")
set(EXTENSION_CATEGORY "Utilities")
set(EXTENSION_CONTRIBUTORS "Mike Bindschadler (Seattle Children's Hospital)")
set(EXTENSION_DESCRIPTION "A container for my utility modules with various simple functionalities")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/MikeTools.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/MikeTools/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(CharacterizeTransformMatrix)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
