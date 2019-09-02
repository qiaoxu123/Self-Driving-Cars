# Module 1: Basics of 3D Computer Vision

This module introduces the main concepts from the broad field of computer vision needed to progress through perception methods for self-driving vehicles. The main components include camera models and their calibration, monocular and stereo vision, projective geometry, and convolution operations.

## Learning Objectives

- Build a pinhole camera model and define the model parameters to be found in calibration
- Define the projective geometry required to interpret points in 3D as observed in the image plane
- Formulate the equations and constraints for stereo sensors
- Compute disparity from rectified images
- Understand cross-correlation, convolutions, the difference between them, and what they are used for

---

## Lesson 1 Part 1: The Camera Sensor

### Learning Objectives

> - Learn what makes a camera useful for self-driving cars
> - Learn the characteristics of a camera as a sensor, and how images are formed

Hello everyone, and welcome to the visual perception course of the self-driving car specialization. You've probably noticed that most major players in the autonomous driving industry have a camera as their primary sensor in their vehicle sensor suite. The camera is a rich sensor that captures incredible detail about the environment around the vehicle but requires extensive processing to make use of the information that's available in that image. Throughout this course, you will get hands on experience on how to algorithmically manipulate camera images to extract information, useful, not just for autonomous driving but for robotic perception in general. 

In the first module in week one of this course, we will provide you with an overview of important concepts related to cameras and computer vision. This module is only meant as a high level summary of the basics of computer vision. So, we'll move quickly through a large number of topics to develop more in-depth knowledge in this area, have a look at the computer vision courses also available on Coursera. 

In this first video, we will highlight why the camera is a critical sensor for autonomous driving. We will then briefly introduce the concept of image formation and present the pinhole camera model which captures the essential elements of how a camera works in a simple and elegant manner. We'll then show you an example of a historic camera design which used the pinhole principle to create some of the earliest images ever recorded. The pinhole model will form the basis of our discussions in the next video where we investigate how to project points from the world into the camera imaging sensor. 

---

### 1. The Camera Sensor

> - Captures detailed appearance information
> - High rate of information capture
> - Relatively inexpensive

Of all the common self-driving car sensors, the camera is the sensor that provides the most detailed appearance information from objects in the environment. **Appearance information** is particularly useful for scene understanding tasks such as object detection, segmentation and identification. Appearance information is what allows us to distinguish between road signs or traffic lights states, to track turn signals and resolve overlapping vehicles into separate instances. Because of its high resolution output, the camera is able to collect and provide orders of magnitude, more information than other sensors used in self-driving while still being relatively inexpensive. The combination of high valued appearance information and low cost make the camera an essential component of our sensor suite. Let us see how the camera manages to collect this huge amount of information. 

[Reference link1](Sam: Can we add this video of a camera sensor here?
https://www.shutterstock.com/video/clip-1022389735-camerarepair-
sensor-digital-close-up-matrix)

[Reference link2](https://www.shutterstock.com/image-photo/busy-traffic-during-rush-houramsterdam-
1069610642?src=bLnVCTgF8bcUNe81sHDlVw-1-39)

---

### 2. Image Formation

A camera is a passive external receptive sensor. It uses an imaging sensor to capture information conveyed by light rays emitted from objects in the world. This was originally done with film but nowadays we use rather sophisticated silicon chips to gather this information. Light is reflected from every point on an object in all directions, and a portion of these rays travel towards the camera sensor. 

![1566705997582](assets/1566705997582.png)

Look at the car's reflected rays collected by our imaging surface. Do you think we will get a good representation of the car on the image sensor from this ray-pattern? Unfortunately, no. **Using this basic open sensor camera design, we will end up with blurry images because our imaging sensor is collecting light rays from multiple points on the object at the same location on the sensor**. The solution to our problem is to put a barrier in front of the imaging sensor with a tiny hole or aperture in its center. The barrier allows only a small number of light rays to pass through the aperture, reducing the blurriness of the image. 

---

### 3. Pinhole Camera Model

This model is called the pinhole camera model and describes the relationship between a point in the world and it's corresponding projection on the image plane. 

![1566706135569](assets/1566706135569.png)

The two most important parameters in a pinhole camera model are the distance between the pinhole and the image plane which we call the **focal length**, the focal length defines the size of the object projected onto the image and plays an important role in the camera focus when using lenses to improve camera performance. The coordinates of the center of the pinhole, which we call the **camera center,** these coordinates to find the location on the imaging sensor that the object projection will inhabit. Although the pinhole camera model is very simple, it works surprisingly well for representing the image creation process. 

![1566706150768](assets/1566706150768.png)

By identifying the focal length and camera's center for a specific camera configuration, we can mathematically describe the location that a ray of light emanating from an object in the world will strike the image plane. This allows us to form a measurement model of image formation for use in state estimation and object detection. A historical example of the pinhole camera model is the camera obscura, which translates to dark room camera in English. Historical evidence shows that this form of imaging was discovered as early as 470 BC in Ancient China and Greece. It's simple construction with a pinhole aperture in front of an imaging surface makes it easy to recreate on your own, and is in fact a safe way to watch solar eclipse if you're so inclined. 

---

### 4. Modern Day Cameras

We've come a long way since the invention of the camera obscura. Current-day cameras allow us to collect extremely high resolution data. 

![1566706253669](assets/1566706253669.png)

They can operate in low-light conditions or at a long range due to the advanced lens optics that gather a large amount of light and focus it accurately on the image plane. The resolution and sensitivity of camera sensors continues to improve, making cameras one of the most ubiquitous sensors on the planet. How many cameras do you think you own? You'd be surprised if you stop to count them all. You'll have cameras in your phones, in your car, on your laptop, they are literally everywhere and in every device we own today. 

![1566706272566](assets/1566706272566.png)

These advances are also extremely beneficial for understanding the environment around a self-driving car. As we discussed in course one, cameras specifically designed for autonomous vehicles need to work well in a wide range of lighting conditions and in distances to objects. These properties are essential to driving safely in all operating conditions. 

---

### 5. Summary

> - The camera is important as a sensor due to the amount of information i can capture, and its relatively small price tag
> - The basic camera model has existed since the 1500s!

In this introductory lesson, you've learned the usefulness of the camera as a sensor for autonomous driving. You also saw the pinhole camera model in its most basic form, which we'll use throughout this course to construct algorithms for visual perception. In the next video, we will describe how an image is formed, a process referred to as projective geometry, which relates objects in the world to their projections on the imaging sensor.

---

## Lesson 1 Part 2: Camera Projective Geometry

### Learning Objectives

> - Learn how to model the camera's projective geometry through coordinate system transformation
> - Learn how to model these transformations using matrix algebra and apply them to a 3D point to get its 2D projection on the image plane
> - Learn how a digital image is represented in software

In this video, you will learn how to model the cameras projective geometry through the coordinate system transformation. These transformations can be used to project points from the world frame to the image frame, building on the pinhole camera model from the previous video. Recall that you've already used transformations extensively in Course 2. You will then model these transformations using matrix algebra and apply them to a 3D point to get it's 2D projection onto the image plane. Finally, you will learn how camera 2D images are represented in software. Equipped with the projection equations in image definitions, you will then be able to create algorithms for detecting objects in 3D and localizing the self-driving car later on in the course. First, let's define the problem we need to solve. 

---

### 1. Projection: World -> Image (Real Camera)

Let's start with a point O world defined at a particular location in the world coordinate frame. We want to project this point from the world frame to the camera image plane. Light travels from the O world on the object through the camera aperture to the sensor surface. 

![1566711309939](assets/1566711309939.png)

You can see that our projection onto the sensor surface through the aperture results in flipped images of the objects in the world. To avoid this confusion, we usually define a virtual image plane in front of the camera center. Let's redraw our camera model with this sensor plane instead of the real image plane behind the camera lens. 

---

### 2. Projection: World -> Image (Simplified Camera)

We will call this model the simplified camera model, and need to develop a model for how to project a point from the world frame coordinates x, y and z to, image coordinates u and v. We begin by defining the following characteristics of the cameras that are relevant to our problem. First, we select a world frame in which to define the coordinates of all objects and the camera. We also define the camera coordinate frame as the coordinate frame attached to the center of our lens aperture known as the optical sensor. 

![1566711477941](assets/1566711477941.png)

As we learned from Course 2, we can define a translation vector and a rotation matrix to model any transformation between a world coordinate frame and another, and in this case, we'll use the world coordinate frame and the camera coordinate frame. **We refer to the parameters of the camera pose as the extrinsic parameters, as they are external to the camera and specific to the location of the camera in the world coordinate frame.** We define our image coordinate frame as the coordinate frame attached to our virtual image plane emanating from the optical center. The image pixel coordinate system however, is attached to the top left corner of the virtual image plane. So we'll need to adjust the pixel locations to the image coordinate frame. Next, we define the focal length is the distance between the camera and the image coordinate frames along the z-axis of the camera coordinate frame. 

---

### 3. Computing the Projection

> 1. Project from World coordinates -> Camera coordinates
> 2. Project from Camera coordinates to Image coordinates

Finally, our projection problem reduces to two steps. We first need to project from the world to the camera coordinates, then we project from the camera coordinates to the image coordinates. We can then transform image coordinates to pixel coordinates through scaling and offset. We now have the geometric model to allow us to project a point from that world frame to the image coordinate frame, whenever we want. Let us formulate the mathematical tools needed to perform this projection using linear algebra.  

![1566711572625](assets/1566711572625.png)

First, we begin with the transformation from the world to the camera coordinate frame. This is performed using the rigid body transformation matrix T, which has R and little t in it. The next step is to transform camera coordinates to image coordinates. 

![1566711604799](assets/1566711604799.png)

To perform this transformation, we define the matrix K as a three-by-three matrix. This matrix depends on camera intrinsic parameters, which means it depends on components internal to the camera such as the camera geometry and the camera lens characteristics. 

![1566711692016](assets/1566711692016.png)

Since both transformations are just matrix multiplications, we can define a matrix P as K times R and t, that transforms from the world coordinate frame all the way to the image coordinate frame. 

![1566711706637](assets/1566711706637.png)

The coordinates of point O in the world frame can now be projected to the image plane via the equation O sub image is equal to P times O sub world, which is k times R and t of O sub world. 

![1566711742395](assets/1566711742395.png)

So, let's see what we're still missing to compute this equation. When we expect the matrix dimensions, we noticed that the matrix multiplication cannot be performed. To remedy this problem, we transform the coordinates of the point O into homogeneous coordinates, and this is done by adding a one at the end of the 3D coordinates as we saw in the second state estimation course. So, now the dimensions work and we're all ready to start computing our projections. 

Now, we need to perform the final step, transforming the image coordinates to pixel coordinates. 

![1566712051404](assets/1566712051404.png)

We do so by dividing x and y by z to get homogeneous coordinates in the image plane. You have completed the basic camera projection model. In practice, we usually model more complex phenomena such as non-square pixels, camera access skew, distortion and non unit aspect ratio. Luckily, this only changes the camera K matrix, and the equations you have learned can be used as is with a few additional parameters. 

---

### 4. The Digital Image

Now that we have formulated the coordinates of projection of a 3D point onto the 2D image plane, we want to define what values go into the coordinates in a 2D color image. We will start with a grayscale image. We first define a width N and a height M of an image, as the number of rows and columns the image has. Each point in 3D projects to a pixel on the image defined by the uv coordinates we derived earlier. 

![1566712176793](assets/1566712176793.png)

Zooming in, we can see these pixels is a grid. In grayscale, brightness information is written in each pixel as an unsigned eight bit integer. Some cameras can produce unsigned 16-bit integers for better quality images. 

![1566712207268](assets/1566712207268.png)

For color images, we have a third dimension of value three we call depth. Each channel of this depth represents how much of a certain color exists in the image. Many other color representations are available, but we will be using the RGB representation, so red green blue, throughout this course. In conclusion, an image is represented digitally as an M by N by three array of pixels, with each pixel representing the projection of a 3D point onto the 2D image plane. 

---

### 5. Summary

> - 3D points in the world coordinate frame can be projected
>   to 2D points in the image coordinate frame using projective
>   geometry equations
> - These equations rely on the camera intrinsic parameters, as
>   well as its extrinsic location in the world coordinate frame
> - A color camera image is represented digitally as an MxNx3
>   array of unsigned 8 bit or 16 bit integers

So, in this video, you learned how to project 3D points in the world coordinate frame to 2D points in the image coordinate frame. You saw that the equations that perform this projection rely on camera intrinsic parameters as well as on the location of the camera in the world coordinate frame. As we'll see later throughout the course, this projection model is used in every visual perception algorithm we develop, from object detection to derivable space estimation. Finally, you've learned how images are represented in software as an array representing pixel locations. You're now ready to start working directly with images and software, as you'll do in this week's assessments. In the next video, you will learn how to tailor the camera model to a specific camera by computing its intrinsic and extrinsic camera parameters through a process known as camera calibration.

---

## Lesson 2: Camera Calibration

### Learning Objectives

> - Learn how to find the camera matrix P through a process called camera calibration
> - Learn how to extract the intrinsic parameters from the camera P matrix

So far, we have learnt which camera parameters are needed for projective geometry to work. In this video, we will learn how to get these camera parameters using the mathematical tools of calibration. 

---

### 1. Computing the Projection

Let's remember the projection equations we've learnt so far. The homogeneous coordinates of point O in 3D space can be transformed to the camera plane, with the camera projection matrix P, which includes both extrinsic and intrinsic parameters. 

![1566739031283](assets/1566739031283.png)

Remember, the projected coordinates need to be converted to homogeneous form to get the u and v pixel locations in pixel coordinates. We do this by dividing the image coordinates by the z-component. Finally, u and v can then be multiplied with an arbitrary scale s. We multiply by s, as it will be useful later on when we formulate the calibration problem. It is important to note that scale plays a challenging role in understanding monocular image information, as once points are projected from the 3D world onto the 2D image plane, scale information is lost. Points in 3D space along a ray from the camera center, all project to the same location on the image plane, and it is therefore not possible to directly associate a depth to a point given only image information. 

![1566739144783](assets/1566739144783.png)

---

### 2. Camera Calibration : Problem Formulation

The camera calibration problem is defined as finding these unknown intrinsic and extrinsic camera parameters, shown here in red given n known 3D point coordinates and their corresponding projection to the image plane. Our approach will comprise of getting the P matrix first and then decomposing it into the intrinsic parameters K and the extrinsic rotation parameters R and translation parameters t. 

![1566739202989](assets/1566739202989.png)

For calibration, we use a scene with known geometry to get the location of our 3D points from the 2D image, resolving the scale issue by measuring the actual 3D distance between the points that are observed in the image. 

![1566739295081](assets/1566739295081.png)

The most commonly used example would be a 3D checkerboard, with squares of known size providing a map of fixed point locations to observe. We define our word coordinate frame, in yellow and compute our 3D point coordinates and their projections in the image. Associating 3D points to 2D projections can be done either manually, by clicking on the purple points, for example or automatically, with checkerboard detectors. We can then set up a system of equations to solve for the unknown parameters of P. Now, let us form the system of linear equations that needs to be solved. 

![1566739338215](assets/1566739338215.png)

First, we expand the projection equations to three equations through matrix multiplication. 

![1566739368841](assets/1566739368841.png)

To get zero on the right-hand side of these equations, we move the right hand side to the left-hand side for each one. Then, we substitute the third equation into equations one and two, and end up with two equations per point. 

![1566739430512](assets/1566739430512.png)

Therefore, if we have n points, we have 2n associated equations. Putting these equations in matrix form gives us the shown homogeneous linear system. 

![1566739448060](assets/1566739448060.png)

Since this is a homogeneous linear system, we can use the pseudo-inverse or even better, the singular value decomposition to get the least squares solution. 

---

### 3. Camera Calibration : Linear Methods

> - **Advantages of such a simple linear system are:**
>   - Easy to formulate
>   - Closed form solution
> -  **Disadvantages of such a simple linear system are:**
>   - Does not directly provide camera parameters
>   - Does not model radial distortion and other complex
>     phenomena
>   - Does not allow for constraints such as known focal length to
>     be imposed
>

Our simple linear calibration approach has several advantages. It's easy to formulate, has a closed form solution, and often provides really good initial points for non-linear calibration approaches. Can you think of some disadvantages of a simple linear system? One disadvantage of solving for P, is that we do not directly get the intrinsic and extrinsic camera parameters. Furthermore, our linear model does not take into account complex phenomena, such  as radial and tangential distortion. Finally, since we are solving via the linear least squares method, we cannot impose constraints on our solution, such as requiring the focal length to be non-negative. 

---

### 4. Factoring and Factorizing the P matrix

The camera projection matrix P by itself, is useful for projecting 3D points into 2D, but it has several drawbacks. It doesn't tell you the cameras pose and it doesn't tell you about the camera's internal geometry. Fortunately, we can factorize P into intrinsic parameter matrix K and extrinsic rotation parameters R and translation parameters t, using a linear algebra operation known as the RQ factorization. 

![1566824661844](assets/1566824661844.png)

Let us see how we perform this factorization. First, we alter the representation of P to be a function of the camera center C. C is the point that projects to zero when multiplied by P. We multiply K into the matrix to form two sub-matrices, KR and minus KRC. We will refer to the combination of K and R as the M matrix. 

![1566824736332](assets/1566824736332.png)

We can now express our projection matrix P as M and minus MC. From here, we use the fact that any square matrix can be factored into an upper triangular matrix R and an orthogonal basis to decompose M into upper triangular R and orthogonal basis Q. In linear algebra, this procedure is known as RQ factorization, which is a variant of the more commonly referred to QR factorization. In QR factorization, we have the orthogonal Q first and then the upper triangular R. Note here that the R and the output of RQ factorization, is a different variable than our rotation matrix R. So, don't get those confused. 

![1566824822540](assets/1566824822540.png)

Let's now see how we can use the output of RQ factorization of the matrix M to retrieve K, R, and t by aligning these two expressions. The intrinsic calibration matrix K is the output R of the RQ factorization of M. The rotation matrix R is the orthogonal basis Q. Finally, we can extract the translation vector directly from K in the last column of the P matrix. RQ factorization is a great tool to compute K, R, and t from the camera P matrix. However, some mathematical assumptions need to be performed to guarantee a unique solution for these matrices. We will explore these assumptions in further detail with this lesson's practice Jupiter notebook. Monocular camera calibration is a well-established tool that has excellent implementations in C++, Python and MATLAB. You can test out some of the most common implementations by following the links we've included in the supplemental materials. 

![1566824838015](assets/1566824838015.png)

---

### 5. Summary

> - The camera matrix P can be found through a process known as camera calibration
> - The intrinsic and extrinsic camera parameters can be extracted from the P matrix using RQ factorization

So, to summarize. In this lesson, you've learned that the camera projection matrix P can be found through a process known as camera calibration. You've learnt that this matrix can be factored into the camera intrinsic matrix K and the camera's extrinsic parameters R and t, through RQ factorization. Next up, we'll discuss how to get depth from two camera sensors through stereovision. We'll see you then.

---

### 6. Calibration Tools – MOVE TO  SUPPLEMENTAL MATERIALS

- OpenCV:  https://docs.opencv.org/master/d4/d94/tutorial_camera_calibration.html
- Matlab: https://www.mathworks.com/help/vision/ug/single-camera-calibrator-app.html
- ROS: http://wiki.ros.org/camera_calibration

---

## Lesson 3 Part 1: Visual Depth Perception - Stereopsis

### Learning Objectives

> - Learn the geometry of a stereo sensor, and how the two camera are related
> - Learn how to derive the location of a point in 3D given its projection on the two images of a stereo sensor

Self-driving cars require accurate depth perception for the safe operation of our autonomous vehicles. If you don't know how far away the cars are in front of you, how can you avoid them while driving? Lidar and Radar sensors are usually thought of as the primary 3D sensors available for perception tasks. However, we can get depth information from two or more cameras using multi-view geometry. Specifically, we'll be describing the process of getting depth from two axis aligned cameras a setup known as the stereo cameras. In this video, we will cover the geometry of the stereo sensor as well as how to derive the 3D coordinates of a point given its projection onto two images of the stereo sensor. 

---

### 1. Stereopsis

Stereopsis, the process of stereo vision, was first described by Charles Wheatstone back in 1838. He recognized that because each eye views the visual world from a slightly different horizontal position that each eye's image differs from the other. Objects at different distances from the eye project images into the two eyes that differ in their horizontal position giving depth cues of horizontal disparity that are also known as binocular disparity. However, historical evidence suggests that stereopsis was discovered much earlier than this. In fact some drawings by Leonardo da Vinci depict accurate geometry of depth through stereopsis. 

![1566825324854](assets/1566825324854.png)

Up to the 19th century, the phenomenon of stereopsis was primarily used for entertainment. Anaglyphs were used to provide a stereoscopic 3D effect when viewed with 2D color glass, where each lens employs different chromatically opposite colors, usually red and cyan. 

![1566825375687](assets/1566825375687.png)

Nowadays, we use stereopsis with complex algorithms to derive depth from two images using a similar concept to Da Vincis drawings. 

---

### 2. Stereo Camera

Now, let us delve into the geometry of a stereo sensor. A stereo sensor is usually created by two cameras with parallel optical axes. To simplify the problem even more, most manufacturers align the cameras in 3D space so that the two image planes are aligned with only an offset in the x-axis. 

![1566825508934](assets/1566825508934.png)

Given a known rotation and translation between the two cameras and a known projection of a point O in 3D to the two camera frames resulting in pixel locations OL and OR respectively, we can formulate the necessary equations to compute the 3D coordinates of the point O. To make our computation easier, we will state some assumptions. First, we assume that the two cameras used to construct the stereo sensors are identical. Second, we will assume that while manufacturing the stereo sensor, we tried as hard as possible to keep the two cameras optical axes aligned. 

![1566825585830](assets/1566825585830.png)

Let's now define some important parameters of the stereo sensor. The focal length is, once again, the distance between the camera center and the image plane. Second, the baseline is defined as the distance along the shared x-axis between the left and right camera centers. By defining a baseline to represent the transformation between the two camera coordinate frames, we are assuming that the rotation matrix is identity and there is only a non-zero x component in the translation vector. The R and T transformation therefore boils down to a single baseline parameter B. 

---

### 3. Stereo Sensor: Assumptions

>- Sensor is constructed from two identical cameras
>- The two cameras have parallel optical axes
>- Project to Bird’s eye view for easier geometry

Before proceeding, we will project the previous figure to bird's eye view for easier visualization. Now, let's define the quantities we would like to compute. We want to compute the x and z coordinates of the point O with respect to the left camera frame. 

![1566825748206](assets/1566825748206.png)

The y coordinate can be estimated easily after the x and z coordinates are computed. Remember, we are given the baseline, focal length, and the coordinates of the projection of the point O onto the left and right image planes. We can see two similar triangles formed by the left camera measurement as follows. The triangle formed by the depth z and the position x is similar to the triangle formed by the focal length f and the left measurement x component xl. From this similarity we can construct the equation z over equals x over xl. The same can be done for the right measurements but with the offset for the baseline included. In this case, the two triangles are defined by z, and the distance x minus b and the focal length f and the right measurement x component xr. Similarly, we can get a second equation relating z to x via the right camera parameters in measurements. 

---

### 4. Computing 3D Point Coordinates

From these two equations, we can now derive the 3D coordinates of the point O. We define the disparity d to be the difference between the image coordinates of the same pixel in the left and right images. We can easily transform between image and pixel coordinates using the x and y offsets u Naught and v Naught. We then use the two equations from the similar triangle relations to solve for the value of z as follows. 

![1566825901850](assets/1566825901850.png)

From there we use the value of z to compute x with the following expression. Finally, we can repeat the process in the y direction with the same derivation to arrive at the following expression for y. The three components of the point position are now explicitly available from the two sets of pixel measurements available to us. 

![1566825931095](assets/1566825931095.png)

Now that we have established the equations needed for 3D coordinate computation from the stereo sensor, two problems arise to be able to perform this computation. First, we need to compute the focal length baseline and x and y offsets. That is, we need to calibrate the stereo camera system. Second, we need to find the correspondence between each left and right image pixel pair to be able to compute their disparity. Fortunately, the calibration problem can be solved using stereo camera calibration. 

![1566826024305](assets/1566826024305.png)

This is an extension of the monocular process we discussed in the previous video, for which well-established implementations are available. The correspondence problem however, requires specialized algorithms to efficiently perform the matching and compute the disparity between left and right image pixels, which we'll discuss further in the next video. The output depth from stereopsis suffers from some limitations particularly as points move further away from the stereo camera. However, given a good disparity estimation algorithm, the output is still useful for self-driving cars as a dense source of depth information and closer range which exceeds the density we can get from common Lidar sensors. 

---

### 5. Summary

> - Stereopsis as a phenomenon was well known as early as the 19th century
> - Given the geometric transformation between the two cameras of a stereo sensor, and the disparity, you can estimate the 3D location of pixel

To summarize this lesson, you've learned some historical background on stereopsis. You also learned the equations required to estimate 3D coordinates of a pixel given the geometric transformation between the two cameras sensors and the disparity between pixels. In the next lesson we'll learn more about disparity generating algorithms and show full examples on how to compute that disparity from a stereo image pair using Python and OpenCV. Will see you then.

---

## Lesson 3 Part 2: Visual Depth Perception - Computing the Disparity

### Learning Objectives

> - Learn how to estimate the disparity through stereo matching
> - Learn how to constrain disparity estimation through epipolar constraints

It's great to see you again. Welcome back. So far we have learned the essential equations to extract 3D information from a stereo pair. However, we were faced with some unknown parameters that we have to estimate. In this lesson you will learn how to estimate these missing parameters such as the disparity through stereo matching. You will also learn that efficient disparity estimation is possible due to epipolar constraints. Let's get started. 

---

### 1. Computing 3D Point Coordinates

Recall from the previous video that we identified two primary issues with the visual depth estimation from stereo images. The first is that the camera parameters focal length F baseline B and camera pixel centers U_naught and V_naught, need to be estimated from stereo camera calibration. Similar to monocular camera calibration, stereo calibration is a well-studied problem with lots of user-friendly free software capable of performing in. This lesson we'll be targeting the second problem, mainly stereo matching to compute disparities. 

![1566826354735](assets/1566826354735.png)

As a reminder, disparity is the difference in the image location of the same 3D point as observed by two different cameras. To compute the disparity we need to be able to find the same point in the left and right stereo camera images. This problem is known as the stereo correspondence problem. The most naive solution for this problem is an exhaustive search, where we searched the whole rate image for every pixel in the left image. Such a solution is extremely inefficient and will usually not run in real time to be used on self-driving cars. It's also unlikely to succeed as many pixels will have similar local characteristics, making it difficult to match them correctly. Luckily for us, we can use stereo geometry to constrain our search problem from 2D over the entire image space to a 1D line. 

![1566826494141](assets/1566826494141.png)

---

### 2. Epipolar Constraint for Correspondence

Let's revisit our stereo camera setup and see why such a simplification is valid. We've already determined, how a single point is projected to both cameras. Now, let's move our 3D point along the line connecting it with the left cameras center. Its projection on the left camera image plane does not change. However, what can you notice about the projection on the right camera plane, the projection moves along the horizontal line. This is called an epipolar line and follows directly from the fixed lateral offset and image plane alignment of the two cameras in a stereo pair. We can constrain our correspondence search to be along the epipolar line, reducing the search from 2D to 1D. 

![1566826804093](assets/1566826804093.png)

---

### 3. Non-Parallel Optical Axes

One thing to note is that horizontal epipolar lines only occur if the optical axes of the two cameras are parallel. 

![1566826883869](assets/1566826883869.png)



---

### 4. Disparity Computation

In the case of non parallel optical axis, the epipolar lines are skewed. In such cases we will have to result to multiple view geometry rather than the stereo equations we have developed, which is out of the scope of this lesson. In the case of two calibrated use such as our stereo camera, a skewed epipolar line is not a huge problem. In fact, we can work the optical axis to be parallel through a process known as stereo rectification. After rectification we arrive back to our horizontal epipolar line. We will not go through how to perform rectification as implementations are available in standard computer vision packages such as OpenCV and MATLAB. 

![1566826980556](assets/1566826980556.png)

---

### 5. A Basic Stereo Algorithm

To put it all together we will go over our first basic stereo algorithm. For each epipolar line take a pixel on this line in the left image, compare these left image pixels to every pixel in the right image on the same epipolar line. Next, select the right image pixel that matches the left pixel the most closely which can be done by minimizing the cost. 

![1566827050683](assets/1566827050683.png)

---

### 6. Stereo Matching

For example, a very simple cost here can be the squared difference in pixel intensities. Finally, we can compute the disparity by subtracting the right image location from the left one. Stereo matching is a very well-studied problem in computer vision. Many more complex costs and search regions can be defined, which attempts to improve either computational efficiency or disparity accuracy. 

![1566827112851](assets/1566827112851.png)

There are a wide range of approaches including both local and global methods, which differ in the main image region considered when identifying correspondences and computing disparities. As with most problems in computer vision, the stereo vision algorithms are evaluated on a public benchmark. The most famous of which is the middlebury stereo benchmark. If you are interested, many of the top-performing stereo matching algorithms have results published there and have code available too. 

---

### 7. Summary

> - Disparity estimation can be performed through stereo matching algorithms
> - Efficient solutions exist as the problem is constrained with epipolar constraints

With this lesson, you should now know how a stereo sensor generates depth from images through disparity estimation. This week's assignment will give a chance to compute your own disparity maps and to use them to create your own distance to impact driver assist module. In the next lesson, we will describe image filtering, an important concept we will later use when designing convolutional neural networks for visual perception. Thanks for watching. See you next time.

---

## Lesson 4: Image Filtering

### Learning Objectives

> - Learn to perform image filtering through cross-correlation and convolution operations
> - Learn some uses for these operations in context of image understanding

Welcome to the last video of this module. A brief introduction to computer vision. You're almost there. Today, we will learn the last introductory piece required to begin developing basic perception algorithms for self-driving cars. Specifically, we will be talking about image filtering through cross correlation and convolution operations. We will also discuss some of the common uses for these operations and relate them to the self-driving task. 

---

### 1. Image Filtering

First, let us begin with the motivation on why we would use image filtering. The image formation process is susceptible to lots of different noise sources. Here you can see the camera man, a very famous photo created at MIT that is used for testing computer vision algorithms. 

Now let us add salt and pepper noise to this image, by randomly turning some of its pixels white and others black. How can we retrieve a reasonable visual appearance of the original image from such a noisy one? Image filtering is as simple and efficient method to eliminate noise. You will also see that depending on the filter, a variety of operations can be performed on images in an efficient manner. But first, let us see ho w image filtering helps reduce salt and pepper noise as a motivating example. 

![1566905614885](assets/1566905614885.png)

If we look at the image array, we noticed that salt and pepper noise usually results in outlier pixels, low-value pixels in a high-value neighborhood or high-value pixels in a low-value neighborhood. One idea to reduce this noise is to compute the mean of the whole neighborhood, and replace the outlier pixel with this mean value. Let us define G as the output of our filter operation. The equation of the mean can be described in terms of k, u and v. Here, 2k plus one is the filter size. In this case, the size of our neighborhood which is three leads to a k that's equal to one. u and v are the center pixel image coordinates. Computing the mean results in 80 for the top neighborhood and 10 for the bottom one. The final step is to replace the center pixel of each of those neighborhoods by the corresponding mean. We have successfully reduced the noise and smooth the image array values in this neighborhood. 

---

### 2. Cross-Correlation

The mean equation can be generalized by adding a weight to every pixel in the neighborhood. The weight matrix H is called a kernel. This generalized form is termed cross-correlation, as it defines a correlation between each pixel and every other pixel in the neighborhood. For the mean filter defined above, we now represented with the following kernel. A three-by-three matrix filled with the value one-ninth. Another kernel for noise reduction is the Gaussian kernel, where the center pixel is weighted more than the neighboring pixels and the weights follow a Gaussian distribution. 

![1566905764966](assets/1566905764966.png)

Now let's apply these kernels to our camera man image. 

![1566905783607](assets/1566905783607.png)

We can see that our kernels successfully reduces the salt and pepper noise. However, it also blurred our image, an inevitable consequence of these linear filters. This blur can be reduced by tuning the parameters specific to each type of filter. 

---

### 3. Convolution

Now, we will define another useful operation used for image filtering. A convolution is a cross-correlation, where the filter is flipped both horizontally and vertically before being applied to the image.

![1566905898494](assets/1566905898494.png)

To apply the convolution, we take each row of our kernel, flip it and replace it at its corresponding symmetric position from the middle row. Mathematically convolution can be described as the following equation. 

![1566906732323](assets/1566906732323.png)

Note that we simply manipulated the image coordinates instead of flipping the kernel. What are the advantages of using a convolution over a kernel? Unlike correlation, convolution is associative, meaning the order of multiplication of kernels does not matter. We can therefore apply as many consecutive linear kernels to an image as we want by precomputing the combined convolution of all the kernels, and then performing a single convolution of the resulting kernel with the image. 

![1566906801030](assets/1566906801030.png)

As an example, we apply two linear kernels, H and F, by computing H times F and then applying it to the image. This results in a substantial reduction in runtime, especially if we need to process images in real-time while moving in a vehicle. 

---

### 4. Applications: Template Matching

Now let's present some important applications of cross-correlation and convolution operations. Cross-correlation can be used for template matching. Template matching is the problem where we are given a pattern or a template, and we want to find its location in the image. This can be done by finding the location of the highest value of the output of cross-correlation, between the template and the image. 

![1566906898634](assets/1566906898634.png)

To visualize this better, let's superimpose the colorized output of cross-correlation on top of our target image. Here red is a high cross-correlation response, while blue is a very low response. The location of the template and the image is then the u, v coordinates of the pixel with the highest value from the output of the cross-correlation. We can check that our correlation is correct by superimposing the template on the u, v coordinates we just found. This method can be used as a starting point for the identification of signs, and even for lean detection, although challenges arise with the approach in practice. 

---

### 5. Applications: Gradient Computation

Another important application that can be performed using convolutions, is image gradient computation. Image gradients can be computed by a convolution with a kernel that performs finite difference. We can rotate our kernel in different orientations to get vertical, horizontal or even diagonal gradients of an image at a pixel. Image gradients are extremely useful for detection of edges and corners, and are used extensively in self-driving for image feature and object detection, for example. 

![1566906958771](assets/1566906958771.png)

---

### 6. Summary

> - Cross-Correlation and Convolution are two operations that can be used to apply a filter to an image
> - Cross-Correlation can be used to match image regions, while convolutions can be used for edge detection

In this lesson, you learned how to perform cross-correlation and convolution as well as some of the uses of these operations. These operations will prove to be very useful later on in the course when we discuss convolution neural networks. Next week we will deal deeper into image processing to learn how to distill useful information from these high dimensional objects. Well done. You've completed the first week of this course. By now you should know how to represent a digital image. How points in 3D relate to pixels in an image. How to compute 3D point coordinates from a pair of images, and how to process images using cross-correlation and convolution operations. For this week's assignment, we will use what we've learnt as building blocks for a simple distance to impact perception module for self-driving cars. Good luck.