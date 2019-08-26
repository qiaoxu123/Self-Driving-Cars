# Part2：State Estimation and Localization for Self-Driving Cars

Welcome to State Estimation and Localization for Self-Driving Cars! You’re joining thousands of learners currently enrolled in the course. I'm excited to have you in the class and look forward to your contributions to the learning community.

To begin, I recommend taking a few minutes to explore the course site. Review the material we’ll cover each week, and preview the assignments you’ll need to complete to pass the course. Click **Discussions** to see forums where you can discuss the course material with fellow students taking the class.

If you have questions about course content, please post them in the forums to get help from others in the course community. For technical problems with the Coursera platform, visit the [Learner Help Center](http://learner.coursera.help/).

Good luck as you get started, and I hope you enjoy the course!

---

## Module 1: Least Squares

The method of least squares, developed by Carl Friedrich Gauss in 1795, is a well known technique for estimating parameter values from data. This module provides a review of least squares, for the cases of unweighted and weighted observations. There is a deep connection between least squares and maximum likelihood estimators (when the observations are considered to be Gaussian random variables) and this connection is established and explained. Finally, the module develops a technique to transform the traditional 'batch' least squares estimator to a recursive form, suitable for online, real-time estimation applications.

### 学习目标

- Understand the squared error optimization criterion and its use
- Explain how least squares is employed in parameter estimation problems
- Apply the unweighted and weighted least squares methods to parameter estimation
- Apply a recursive version of least squares to update parameter estimates as new measurements arrive
- Explain how Jacobian matrices are used

---

## Module 2: State Estimation - Linear and Nonlinear Kalman Filters

Any engineer working on autonomous vehicles must understand the Kalman filter, first described in a paper by Rudolf Kalman in 1960. The filter has been recognized as one of the top 10 algorithms of the 20th century, is implemented in software that runs on your smartphone and on modern jet aircraft, and was crucial to enabling the Apollo spacecraft to reach the moon. 

This module derives the Kalman filter equations from a least squares perspective, for linear systems. The module also examines why the Kalman filter is the best linear unbiased estimator (that is, it is optimal in the linear case). The Kalman filter, as originally published, is a linear algorithm; however, all systems in practice are nonlinear to some degree. Shortly after the Kalman filter was developed, it was extended to nonlinear systems, resulting in an algorithm now called the ‘extended’ Kalman filter, or EKF. The EKF is the ‘bread and butter’ of state estimators, and should be in every engineer’s toolbox. This module explains how the EKF operates (i.e., through linearization) and discusses its relationship to the original Kalman filter. The module also provides an overview of the unscented Kalman filter, a more recently developed and very popular member of the Kalman filter family.

### 学习目标

- Describe the relationship between least squares and the linear Kalman filter
- Explain the (in)sensitivity of the Kalman filter to new data and the need for process noise
- Describe how the linear Kalman filter can be extended to nonlinear systems via linearization
- Describe how the EKF uses first-order linearization to turn a nonlinear problem into a linear one
- Contrast the linearization approach of the EKF with that of the UKF, and explain why the UKF is superior for many problems
- Assess the performance of the extended Kalman filter and its variants

---

## Module 3: GNSS/INS Sensing for Pose Estimation

To navigate reliably, autonomous vehicles require an estimate of their pose (position and orientation) in the world (and on the road) at all times. Much like for modern aircraft, this information can be derived from a combination of GPS measurements and inertial navigation system (INS) data. This module introduces sensor models for inertial measurement units and GPS (and, more broadly, GNSS) receivers; performance and noise characteristics are reviewed. The module describes ways in which the two sensor systems can be used in combination to provide accurate and robust vehicle pose estimates.

### 学习目标

- Explain the operation of the two most common sensors used for pose estimation in autonomous driving, inertial meaurement units and GNSS receivers.
- Understand the concept of coordinate acceleration and the fundamental equation of inertial navigation.
- Apply gyroscope and accelerometer measurement models in the context of navigation.
- Describe the process of trilateration and justify why four satellites must be visible to obtain a 3D position fix from a GPS (GNSS) receiver.
- Understand why ionospheric delays and multipath effects can degrade the performance of GPS.

---

## Module 4: LIDAR Sensing

LIDAR (light detection and ranging) sensing is an enabling technology for self-driving vehicles. LIDAR sensors can ‘see’ farther than cameras and are able to provide accurate range information. This module develops a basic LIDAR sensor model and explores how LIDAR data can be used to produce point clouds (collections of 3D points in a specific reference frame). Learners will examine ways in which two LIDAR point clouds can be registered, or aligned, in order to determine how the pose of the vehicle has changed with time (i.e., the transformation between two local reference frames).

### 学习目标

- Explain how LIDAR sensors are able to generate range data from time-of-flight measurements
- Understand inverse and forward sensor models for a basic scanning LIDAR
- Apply standard transfomations (translation, rotation, and scaling) to LIDAR point cloud data
- Summarize how the problem of motion distortion can affect LIDAR scans acquired from a moving vehicle
- Utilize the iterative closest point (ICP) algorithm to align point clouds from consecutive LIDAR scans

---

## Module 5: Putting It together - An Autonomous Vehicle State Estimator

This module combines materials from Modules 1-4 together, with the goal of developing a full vehicle state estimator. Learners will build, using data from the CARLA simulator, an error-state extended Kalman filter-based estimator that incorporates GPS, IMU, and LIDAR measurements to determine the vehicle position and orientation on the road at a high update rate. There will be an opportunity to observe what happens to the quality of the state estimate when one or more of the sensors either 'drop out' or are disabled.

### 学习目标

- Apply filtering-based state estimation to determine the pose of a vehicle on the roadway
- Use LIDAR scan registration (to an existing map) to improve state estimates
- Test the effects of the loss of one or more sensors on the vehicle pose estimate