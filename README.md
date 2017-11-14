# Tori
Blender add-ons for creating tori of varying configurations

**N.B. As the master branch now checks for SciPy at run-time, and gracefully disables the functionality that depends on SciPy if it is unavailable, the 0.2 branch will no longer receive any updates, since I've kept it only to have a non-SciPy version. It may be deleted without prior notice.**

-----

## Installation
1. Click the **Clone or download** button and save the zip file to your harddrive, but do not unzip it.
2. Open up Blender and hit Ctrl+Alt+U or click _File_ -> _User Preferences_
3. Click _Add-ons_
4. Click _Install Add-on from File..._
5. Select the file you downloaded in step 1 and click _Install Add-on from File..._
6. The name _Add Mesh: Tori_ should appear in the list of add-ons. Click the check box next to it, to enable it.
7. _(Optional):_ To make the change persist, click _Save User Settings_
8. Close the user preferences window.

-----

## Usage

### EllipticTorus
Click _Add_ -> _Mesh_ -> _Elliptic Torus_ or press Shift+A followed by M then click _Elliptic Torus_.  
This creates an elliptic torus with the cross-section correctly following the ellipse. It does so by calculating the normal of the ellipse and rotating the cross-section accordingly.

#### Settings
_Ring's Major Semi-Axis_ is half the length of the major axis of the ellipse.  
_Ring's Minor Semi-Axis_ is half the length of the major axis of the ellipse.  
_Ring Segments_ is the number of segements into which the ring is divided.  
_Ring Spacing_ defines how to calculate the distance between the the cross-sections along the ring.  
_Cross-Section's Major Semi-Axis_ is half the length of the major axis of the cross-section.  
_Cross-Section's Minor Semi-Axis_ is half the length of the minor axis of the cross-section.  
_Cross-Section Segments_ is the number of segements into which the cross-section is divided.  
_Cross-Section Twists_ is the number of half twists to do along the ring, i.e. a setting of 1 produces a Möbius band with an interior.  
_Cross-Section Initial Rotation_ rotates the cross-section on the Y axis **before** aligning it with the ring's normal and moving it to its position. This is the starting rotation, from which the twisting is calculated.  
_Cross-Section Spacing_ defines how to calculate the distance between the vertices of the cross-section.  
_Tube Thickness Method_ defines how to calculate the tube thickness.  

Setting the major and minor semi-axes to the same value, makes a circle.

Setting the major semi-axis to a smaller value than the minor semi-axis is perfectly fine. While semantically an error, it doesn't pose a mathematical problem; if you do this with the ring, it will be stretched on the Y axis rather than on the X axis, and if you do this on the cross-section, it will be taller than it is wide.

##### Spacing
Equal Area spacing just uses the standard equations for an ellipse, which cause the sectors of the ellipse to have an equal area.  
Equiangular Normal places the vertices of the ellipse such that the angle between the normals to the ellipse is constant.  
Equirectangular Radius places vertices of the ellipse the such that the angle between the radii is constant.  

##### Tube thickness
Equal Cross-Sections leaves the cross-sections at the size defined by the cross-section axes settings. However, if the ring is highly eccentric and/or has a very low segment count, this will cause the tube to be visibly thinner near accute angles and visibly thicker near obtuse angles.  
Constant Tube Thickness scales the cross-sections to accommodate for the varying thickness with highly eccentric rings and rings with a low segment count. However, if you then subdivide using a smoothing algorithm like Catmull-Clark, this may backfire and actually make the tube visibly thicker at accute angles and visible thinner at obtuse angles.

I've not been able to find an all purpose algorithm, and these are the best I've been able to come up with so far. You need to choose on a case by case basis.
