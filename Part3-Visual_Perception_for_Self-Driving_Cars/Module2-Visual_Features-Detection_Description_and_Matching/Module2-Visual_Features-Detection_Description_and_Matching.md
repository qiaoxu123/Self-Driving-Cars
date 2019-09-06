# Module 2: Visual Features - Detection, Description and Matching

**Visual features are used to track motion through an environment and to recognize places in a map.** This module describes how features can be detected and tracked through a sequence of images and fused with other sources for localization as described in Course 2. Feature extraction is also fundamental to object detection and semantic segmentation in deep networks, and this module introduces some of the feature detection methods employed in that context as well.

## Learning Objectives

- Apply feature detection methods to driving images
- Distinguish between different feature detectors and descriptors
- Match image features using **brute-force matching**
- Perform improved image feature matching with maximum likelihood and KLT
- Formulate and solve visual odometry for a self-driving car dataset
- Improve VO performance through outlier rejection

---

## Lesson 1: Image Features

### Learning Objectives

> - Learn feature extraction, the first step of using image features for applications
> - Learn what characteristics make good image features
> - Learn about different algorithms used to extract features in images

Hello again, and welcome to the second week of the course. This week, we will be learning about image features, which are distinctive points of interest in the image. We use image features for several computer vision applications in self-driving cars. For example, we can use these feature points to localize our car across image frames or to get a global location in a predefined map. All of these tasks share a general framework comprising of feature detection, description, and finally matching. In this video, we will cover the first step of this framework namely feature extraction. You will learn what comprises good image features and different algorithms that perform feature extraction. 

---

### 1. Image Features: A General Process

Let's begin describing this process by taking a real application, **image stitching**. We're given two images from two different cameras, and we would like to stitch them together to form a panorama. 

First, we need to identify distinctive points in our images. We call this point **image features**. Second, we associate a descriptor for each feature from its neighborhood. Finally, we use these descriptors to match features across two or more images. For our application here, we can use the matched features in an image stitching algorithm to align the two images and create lovely panorama. Take a look at the details of the stitched panorama. You can see the two images have been stitched together from some of the artifacts at the edge of the image. 

![1567085985248](assets/1567085985248.png)

---

### 2. Feature Detection

So how do we do it? Don't worry. We'll explain each of the above three steps in detail. But first, let's begin by defining what an image feature really is. Features are points of interest in an image. This definition is pretty vague, as it poses the following question. 

![1567086107911](assets/1567086107911.png)

What is considered an interesting point? Points of interest should be distinctive, and identifiable, and different from its immediate neighborhood. Features should also be repeatable. That means that we should be able to extract the same features from two independent images of the same scene. 

![1567086171455](assets/1567086171455.png)

Third, features should be local. That means the features should not change if an image region far away from the immediate neighborhood changes. Forth, our features should be abundant in an image. This is because many applications such as calibration and localization require a minimum number of distinctive points to perform effectively. Finally, generating features should not require a large amount of computation, as it is usually used as a pre-processing step for the applications that we've described. 

---

### 3. Feature Extraction

Take a look at the following images. Can you think of pixels that abide by the above characteristics? Repetitive texture less patches are very hard to localize. So these are definitely not feature locations. You can see that the two red rectangles located on the road are almost identical. Patches with large contrast change, where there's a strong gradient, are much easier to localize, but the patches along a certain image edge might still be confusing. As an example, the two red rectangles on the edge of the same lane marking look very similar. So again, these are challenging locations to use as features. The easiest concept to localize in images is that of a corner. A corner occurs when the gradients in at least two significantly different directions are large. Examples of corners are shown in the red rectangles. 

![1567086247463](assets/1567086247463.png)

---

### 4. Feature Detection: Algorithms

The most famous corner detector is the **Harris Corner Detector**, which uses image gradient information to identify pixels that have a strong change in intensity in both x and y directions. Many implementations are available online in different programming languages. 

However, the corners detected by Harris corner detectors are not scale invariant, meaning that the corners can look different depending on the distance the camera is away from the object generating the corner. To remedy this problem, researchers proposed the Harris-Laplace corner detector. 

![1567086395976](assets/1567086395976.png)

Harris-Laplace detectors detect corners at different scales and choose the best scale based on the Laplacian of the image. Furthermore, researchers have also been able to machine learn corners. One prominent algorithm, the fast corner detector, is one of the most used feature detectors due to its very high computational efficiency and solid detection performance. Other scale invariant feature detectors are based on the concept of blobs such as the Laplacian of Gaussian or the difference of Gaussian feature detectors of which there are many variance. We will not be discussing these detectors in great depth here, as they represent a complex area of ongoing research, but we can readily use a variety of feature extractors. Thanks to robust open source implementations like OpenCV. 

---

### 5. Harris Corners && Harris Laplace

Now let's see some examples of these detectors in action. Here you can see corners detected by the Harris Corner Detector. 

![1567086467089](assets/1567086467089.png)

The features primarily capture corners as expected, where strong illumination changes are visible. Here you can see Harris-Laplace features on the same image. By using the Laplacian to determine scale, we can detect scale and variant corners that can be more easily matched as a vehicle moves relative to the scene. Scale is represented here by the size of the circle around each feature. The larger the circle, the larger the principal scale of that feature. 

![1567086505049](assets/1567086505049.png)

---

### 6. Summary

> - Good image features need to be salient, repeatable, local, efficient, and numerous
> - Plenty of methods exist to extract features
> - Empirical validation is required to choose the best extractor based on application

In this lesson, you learn what characteristics are required for good image features. You also learn the different methods that can be used to extract image features. Most of these methods are already implemented in many programming languages including Python and C plus plus, and are ready for you to use whenever needed. As a matter of fact, you will be using the OpenCV Python implementation of the Harris-Laplace corner detector for this week's programming assignment. In the next video, we will learn about the second step of our feature extraction framework, the feature descriptors.

---

## Lesson 2: Feature Descriptors

### Learning Objectives

> - Learn what characteristics make a good feature descriptor
> - Learn different algorithms used to extract feature descriptors from images

[MUSIC] In the last video, we described feature detection or the process of identifying feature points in an image in a variety ways. However, remember that our end goal is to use match features between two different images for localization, object detection, and other perception tasks that require depth estimation to points in the environment. To do so, we need to describe features in a way that it allows for feature comparison to determine the best match between frames. We therefore assign a descriptor to every feature point in an image. In this video, you will learn what makes a good feature descriptor for computer vision applications. You'll learn how to derive these descriptors from images so we can use them in autonomous driving. 

---

### 1. Feature Descriptors

Let's begin by defining what a feature descriptor is. Mathematically, we define a feature point by its coordinates u and v in the image frame. We describe a descriptor f as an n dimensional vector associated with each feature. The descriptor has the task of providing a summary of the image information in the vicinity of the feature itself, and can take on many forms. 

![1567336080172](assets/1567336080172.png)

Similar to the design of feature detectors we also have some favorable characteristics required for the design of descriptors to allow for robust feature matching. **As with feature detectors descriptors should be repeatable, that means that regardless of shifts in position, scale, and illumination, the same point of interest in two images should have approximately the same descriptor.** This invariance in transformations is one of the most researched topics when it comes to descriptor design. And a large amount of work has been done to provide descriptors that are invariant to scale, illumination, and other variables in image formation. 

![1567336142703](assets/1567336142703.png)

The second important characteristic of a feature descriptor is distinctiveness. Two nearby features should not have similar descriptors, as this will confuse our feature matching process later on. 

![1567336200699](assets/1567336200699.png)

Finally, descriptors should be compact and efficient to compute. This is because we will usually require matching to be performed in real time for autonomous driving applications. 

![1567336250775](assets/1567336250775.png)

---

### 2. Designing Invariant Descriptors: SIFT

A wide variety of effective descriptors have been developed for feature matching. So let's take a look at a specific case study on the design of a single feature descriptors to give you sense for descriptors work. We will describe how to compute the shift features descriptors specifically designed by David Lowe in 1999. The procedure for computing shift feature descriptors is as follows. Given a feature in the image, the shift descriptor takes a 16 by 16 window of pixels around it, we call this window the features local neighborhood. We then separate this window in to four, 4 by 4 cells such that each cell contains 16 pixels. Next we compute the edges and edge orientation of each pixel in each cell using the gradient filters we discussed in module one. 

![1567336427244](assets/1567336427244.png)

For stability of the descriptor, we suppress weak edges using a predefined threshold as they are likely to vary significantly in orientation with small amounts of noise between images. Finally, we compute a 32 dimensional histogram of orientations for each cell. And concatenate the histograms for all four cells to get a final 128 dimensional histogram for the feature at hand, we call this histogram or descriptor. Some additional post processing is done as well in that it helps the 128 dimensional vector retain stable values under variable contrast, game, and other fundametric variations. 

---

### 3. Scale Invariant Feature Transform

SIFT is an example of a very well human engineered feature descriptor, and is used in many state-of-the-art systems. It is usually computed over multiple scales and orientations for better scale and rotation invariants. Finally, when combined with a scale invariant feature detector, such as the difference of Gaussian's detector, it results in a highly robust feature detector and descriptor pair. 

![1567336476622](assets/1567336476622.png)

---

### 4. Other Descriptors

It is worth mentioning that there is huge literature out there for feature detectors and descriptors. The surf descriptive for example uses similar concepts to SIFT while being significantly faster to compute. Many other variants exist in the literature including the Gradient Location-Orientation Histogram or GLOH descriptor. The Binary Robust Independent Elementary Features descriptor or BRIEF, and the Oriented Fast and Rotated Brief descriptor or ORB. 

![1567336563977](assets/1567336563977.png)

This is a lot of acronyms to remember, but don't worry, we don't expect you to remember all of these. But you may see them in the implementations available for use in Open Source Computer Vision Libraries. We've now completed our discussion on feature detectors and descriptors. Although most of the discussed algorithms have open source implementations, some like SIFT and SURF are patented and should not be used commercially without approval of the authors. Fortunately, the feature detector and descriptor literature up there is vast and some really good algorithms such as ORB match the performance of SIFT and SURF and are free to use even commercially. 

---

### 5. Summary

In this lesson, you learned what comprises a feature descriptor, what characteristics are favorable when designing these descriptors. And different algorithms that are available in the open source libraries to extract feature descriptors as you need them. In combination with the feature extractors we talked about in the previous video, you're now ready to take on the challenging tasks of matching features between images using their computed descriptors. You'll learn more about this in the next video. See you then. [MUSIC]

---

## Lesson 3 Part 1: Feature Matching

### Learning Objectives

So far, we have learned how to extract feature positions in the image and how to extract descriptors from the local neighborhood of these features. This video, will teach you about the last step of using features for computer vision applications in autonomous driving feature matching. Specifically, we will cover how to match features based on distance functions, we will then describe brute force matching as simple but powerful feature matching algorithm. But first, let's remind ourselves of how we intend to use features for a variety of perception tasks. 

---

### 1. Image Features: A General Process

First, we identify image features, distinctive points in our images. Second, we associate a descriptor for each feature from its neighborhood. Finally, we use descriptors to match features across two or more images. Afterwards, we can use the matched features for a variety of applications including state estimation, visual odometry, and object detection. It is essential to identify matches correctly however, as these applications are susceptible to catastrophic failures if incorrect matches are provided too frequently. As a result, feature matching plays a critical role in robust perception methods for self-driving cars. 

![1567336817372](assets/1567336817372.png)

---

### 2. Brute Force Feature Matching

Here's an example of a feature matching problem. Given a feature and it's descriptor in image one, we want to try to find the best match for the feature in image two. So how can we solve this problem? The simplest solution to the matching problem is referred to as brute force feature matching, and is described as the following. 

![1567336895824](assets/1567336895824.png)

First, define a distance function d that compares the descriptors of two features fi and fj, and defines the distance between them. The more similar the two descriptors are to each other, the smaller the distance between them. Second, for every feature fi in image one, we apply the distance function d to compute the distance with every feature fj in image two. Finally, we will return the feature which we'll call fc from image two with the minimum distance to the feature fi in image one as our match. This feature is known as the nearest neighbor, and it is the closest feature to the original one in the descriptor space. 

![1567336980657](assets/1567336980657.png)

---

### 3. Distance Function

The most common distance function used to compare descriptors is the sum of squared distances or SSD. Which penalizes variations between two descriptors quadratically making it sensitive to large variations in the descriptor, but insensitive to smaller ones. Other distance functions such as the sum of absolute differences or the Hamming distance are also viable alternatives. The sum of absolute difference penalizes all variations equally while the Hamming distance is used for binary features, for which all descriptor elements are binary values. We will be using the SSD distance function for our examples to follow. Our matching technique and distance choices are really quite simple. But what do you think might go wrong with our proposed nearest neighbor matching technique? 

![1567337059641](assets/1567337059641.png)

Let's look at our first case and see how our brute force matcher works in practice. Consider the feature inside the yellow bounding box. 

![1567337079390](assets/1567337079390.png)

For simplicity, this feature has a four-dimensional descriptor, which we'll call f1. Let's compute the distance between f1 and the first feature in the image two, which we'll label f2. We get a sum of squared difference or SSD value of nine. We then compute the distance between f1 and the second feature in image two, which we'll label f3. Here, we get an SSD of 652. We can now repeat this process for every other feature in the second image and find out that all the other distances are similarly large relative to the first one. We therefore choose feature f2 to be our match as it has the lowest distance to f1. Visually, our brute force approach appears to be working. As humans, we can immediately see that feature f1 in the image is indeed the same point of interest as feature f2 in image two.

![1567337187020](assets/1567337187020.png)

Now, let us consider a second case where our feature detector tries to match a feature from image one, for which there is no corresponding feature in image two. Let's take a look at what the brute force approach will do when our feature detector encounters this situation. Following the same procedure as before, we compute the SSD between the descriptors of a feature f1 in image one, and all the features in image two. Assume that f2 and f3 are the nearest neighbors of f1 and with f2 having the lowest score. Although at 441, it is still rather dissimilar to the f1 feature descriptor from the original image. As a result, f2 will be returned as our best match. Clearly, this is not correct. Because feature f1 is not the same point of interest as feature f2 in the scene. So how can we solve this problem? We can solve this problem by setting a distance threshold Delta on the acceptance of matches. This means that any feature in image two with a distance greater than Delta to f1, is not considered a match even if it has the minimum distance to f1 among all the features in image two. 

---

### 4. Brute Force Feature Matching

Now, let's update our brute force matcher algorithm with our threshold. We usually define Delta empirically, as it depends on the application at hand and the descriptor we are using. Once again, we define our distance function to quantify the similarity of two feature descriptors. We also fix a maximum distance threshold Delta for acceptable matches. Then, for every feature in image one, we compute the distance to each feature in image two and store the shortest distance or nearest neighbor as the most likely match. 

![1567337371657](assets/1567337371657.png)

---

### 5. Feature Matching

Brute force matching is suitable when the number of features we want to match is reasonable, but has quadratic computational complexity making it ill-suited as the number of features increases. For large sets of features, special data structures such as k-d trees are used to enhance computation time. Both brute force and k-d tree-based matchers are implemented as part of OpenCV, making them easy for you to try out. Just follow the links shown at the bottom of this slide. As a reminder, you can download these lecture slides for your review. By now, you should have a much better understanding of feature detection, description, and matching. These three steps are required to use features for various self-driving applications, such as visual odometry and object detection. Our brute force matcher is pretty deep, but still far from perfect. We really need precise results to create safe and reliable self-driving car perception. 

![1567337396827](assets/1567337396827.png)

---

### 6. Summary

So in the next lesson, we will learn how to improve our brute force matcher to accommodate some of the troublesome and ambiguous matches that frequently lead to incorrect results. See you in the next video.

---

## Lesson 3 Part 2: Feature Matching: Handling Ambiguity in Matching

### Learning Objectives

> - Learn what consists an ambiguous match
> - Learn how to handle ambiguous matches through the distance ratio

So, far this week we've learned how to detect features, compute their descriptors, and perform brute force matching using distance functions. We're almost ready to start applying feature detection, description, and matching to self-driving car perception. In this video, we will explore the issue of ambiguous matches and how to make our matches more robust to matching errors caused by similar feature descriptors through the distance ratio formulation. But first, let's review the two feature matching cases we discussed in the last lesson. 

---

### 1. Brute Force Feature Matching Case

In the first case, we have a useful feature descriptor that clearly gives a small distance to the feature f2 and a large distance to other features in the second image.

![1567338559276](assets/1567338559276.png)

In this case we can successfully identify the correct match to the feature f1 and image one. Our brute force matching algorithm works well with this descriptor and as seamlessly capable of finding the right match in image two. In the second case, the feature f1 in image one does not have a match at all in image two. We modified our brute force matching algorithm with a threshold delta to eliminate incorrect matches in this case. Since both features and image two have a distance greater than the distance threshold Delta, the brute force matcher rejects both the features f2 and f3 as potential matches and no match is returned. 

![1567338572121](assets/1567338572121.png)

But, let us consider a third case, once again we are trying to match feature f1 in image one to a corresponding feature in image two. With the feature vectors presented here, feature f1 gets an SSD value of nine with feature two in image two. We test another feature f3, and we also get an SSD of nine. Both of these features have an SSD less than Delta which was 20 in this case, and as such are valid matches. So what should we do?

![1567338626568](assets/1567338626568.png)

---

### 2. Distance Ratio [Lowe 1999]

We refer to feature fi in case three as a feature with ambiguous matches. An elegant solution to this problem was proposed by David Lowe in 1999. The solution goes as follows. 

![1567338684251](assets/1567338684251.png)

First, we compute the distance between feature fi in image one and all the features fj in image two, similar to our previous algorithm, we choose the feature fc in image two with the minimum distance to feature fi in image of one as our closest match. We then proceed to get feature fs the feature in image two with the second closest distance to the feature fi. Finally, we find how much nearer our closest match fc is over our second closest match fs. This can be done through the distance ratio. The distance ratio can be defined as the distance computed between feature fi in image one and fc the closest match in image two. Over the distance computed between feature fi and fs, the second closest match in image two. If the distance ratio is close to one, it means that according to our descriptor and distance function, fi matches both fs and fc. In this case, we don't want to use this match in our processing later on, as it clearly is not known to our matcher which location in image two corresponds to the feature in image one. 

---

### 3. Brute Force Feature Matching: Updated

Let us update our brute force matcher algorithm with the distance ratio formulation. 

![1567338792006](assets/1567338792006.png)

The updates replace the distance with the ratio of distance as our metric to keep matches. We usually set the distance ratio threshold which we'll refer to as row somewhere around 0.5, which means that we require our best match to be at least twice as close as our second best match to our initial features descriptor. Revisiting case three, we can see that using the distance ratio and a corresponding threshold row set to 0.5, we discard our ambiguous matches and retain the good ones. 

![1567338826269](assets/1567338826269.png)

---

### 4. Summary

In this video, you've learned what ambiguous matches are, and how to handle these ambiguous matches through the distance ratio formulation. Unfortunately, even with the distance ratio formulation, as much as 50 percent of typical matches can still be wrong when using modern descriptors. This is because, repetitive patterns in images and small variations in pixel values, are often sufficient to confuse the matching process. We call these erroneous matches outliers. For our next lesson, I will describe a method to account for and eliminate outliers before using are matched features for further perception tasks.

---

## Lesson 4: Outlier Rejection

### Learning Objectives

> - Learn the definition of outliers, and how outliers interfere with model estimation that rely on image feature matchers
> - Learn how to handle outliers through the RANSAC algorithm

So far we have described the three steps we need to use image features for autonomous vehicle applications. We also mentioned that feature matchers are not very robust to outliers. In this lesson, we will describe what outliers are and how they might affect our usage of image features to solve real-world problems. We will also provide a powerful method to handle outliers called random sample consensus, or RANSAC for short. This method will help us account for and eliminate outliers, as they can have a strong negative impact on the use of features in other perception tasks. But first, let us introduce the use of the three-step feature extraction framework for the real-world problem of vehicle localization. 

---

### 1. Image Features: Localization

Our localization problem is defined as follows: given any two images of the same scene from different perspectives, find the translation T, between the coordinate system of the first image shown in red, and the coordinate system of the second image shown in green. In practice, we'd also want to solve for the scale and skew due to different viewpoints. But we'll keep this example simple to stay focused on the current topic. To solve this localization problem, we need to perform the following steps. First, we need to find the displacement of image one on the u image axis of image two. We call this displacement t sub u. Second, we need to find the displacement of image one on the v axis of image two, and we'll call this displacement t sub v. We will find t sub u and t sub v by matching features between the images, and then solving for the displacements that best align these matched features. 

![1567339128414](assets/1567339128414.png)

We begin by computing features and their descriptors in image one and image two. 

![1567339147469](assets/1567339147469.png)

We then match these features using the brute force matcher we developed in the previous lesson. Do you notice anything a little off in the results from our brute force match? Don't worry. We will come back to these results in a little bit. But first, let's define the solution of our problem mathematically in terms of our matched features. 

![1567339205158](assets/1567339205158.png)

We denote a feature pair from images one and two, as f1 sub i and f2 sub i. Where i ranges between zero and n, the total number of feature pairs returned by our matching algorithm. Each feature in the feature pair is represented by its pixel coordinates ui and vi. Note that every pixel in the image ones should coincide with its corresponding pixel in image two after application of the translation t sub q and t sub v. We can then use our feature pairs to model the translation as follows: the location of a feature in image one is translated to a corresponding location in image two through model parameters t sub u and t sub v. Here the translations on the u image axis t sub u, and the v image axis t sub v, are the same for all feature pairs. Since we assume a rigid body motion. 

![1567339289938](assets/1567339289938.png)Now we can solve for t sub u and t sub v using least squares estimation. The solution to the least squares problem will be the values for t sub u and t sub v that minimize the sum of squared errors between all pairs of pixels. Now that we have our localization problem defined, let's return to the results of our feature matching. By observing the feature locations visually, it can be seen that the feature pair in the purple circles is actually an incorrect match. This happens even though we use the distance ratio method, and is a common occurrence in feature matching. We call such feature pairs outliers. 

![1567600272536](assets/1567600272536.png)

Outliers can comprise a large portion of our feature set, and typically have an out-sized negative effect on our model solution, especially when using least squares estimation. 

---

### 2. Random Sample Consensus(RANSAC)

Let us see if we can identify these outliers and avoid using them in our least squares solution. Outliers can be handled using a model-based outlier rejection method called Random Sample Consensus, or RANSAC for short. RANSAC developed by Martin Fischler and Robert Bolles in 1981 is one of the most used model-based methods for outlier rejection in robotics. 

![1567600966334](assets/1567600966334.png)

The RANSAC algorithm proceeds as follows: first, given a model for identifying a problem solution from a set of data points, find the smallest number M of data points or samples needed to compute the parameters of this model. In our case, the problem localization and the model parameters, are the t sub u and t sub v offsets of the least square solution. Second, randomly select M samples from your data. Third, compute the model parameters using only the M samples selected from your data set. Forth, use the computed parameters and count how many of the remaining data points agree with this computed solution. The accepted points are retained and referred to as inliers. Fifth, if the number of inliers C is satisfactory, or if the algorithm has iterated a pre-set maximum number of iterations, terminate and return the computed solution and the inlier set. Else, go back to step two and repeat. Finally, recompute and return the model parameters from the best inlier set. The one with the largest number of features. Now we can revisit our localization problem and try to accommodate for the outliers from our feature matcher. 

---

### 3. Image Features: Localization

As a reminder, our model parameters t sub u and t sub v, shift each feature pair equally from the first image to the second. To estimate t sub u and t sub v, we need one pair of features. Now, let us go through the RANSAC algorithm for this problem. 

![1567601051181](assets/1567601051181.png)

First, we randomly select one feature pair from the matched samples. 

![1567601100933](assets/1567601100933.png)

Now, we need to estimate our model using the computed feature pair. Using the feature pair, we compute the displacement along the u image axis, t sub u, and the displacement along the v image axis, t sub v. 

![1567601128906](assets/1567601128906.png)

We now need to check if our model is valid by computing the number of inliers. Here, we use a tolerance to determine the inliers, since it is highly unlikely that we satisfy the model with a 100 percent precision. Unfortunately, our first iteration chose a poor feature match to compute the model parameters. When using this model to compute how many features in image one translate to their matched location in image two, we notice that none of them do. Since our number of inliers is zero, we go back and choose another feature pair at random, and restart the RANSAC process. 

![1567601166368](assets/1567601166368.png)

Once again, we compute t sub u and t sub v, using a new randomly sampled feature pair to get our new model parameters. 

![1567601187003](assets/1567601187003.png)

Using the model, we compute how many features and image one translate to their match in image two. This time we can see that most of the features actually fit this model. In fact 11 out of 12 features are considered in inliers. Since most of our features are inliers, we're satisfied with this model, and we can stop the RANSAC algorithm. 

![1567601225090](assets/1567601225090.png)

At this point you should now understand the proper use of image features for an autonomous vehicle applications. You've learned what outliers are within the scope of feature matching, and how to handle outliers through the RANSAC algorithm. Outlier removal is a key process in improving robustness when using feature matching, and greatly improves the quality of localization results. 

---

### 4. Summary

> - Outliers are wrong feature matching outputs, that can occur due to errors in any of the three stages of feature usage
> - RANSAC can be used to efficiently arrive to a good model even when outliers are among the matched features

In the next video, we will use what we learned so far to estimate the position of our autonomous vehicle using camera image features. This will help us track our own vehicles motion through the environment. Which is a process known as Visual Odometry, and is essential to navigating smoothly and safely

---

## Lesson 5: Visual Odometry

### Learnging Objectives

> - Learn why visual odometry is useful for self-driving cars
> - Learn how to perform visual odometry using image features in consecutive frames, along with their 3D position in the world coordinate frame

So far in this module, you've learned how to detect, describe and match features, as well as how to handle outliers in our feature matching results. We've also explored an example of how to use features to localize an object in an image, which could be used to estimate the depth to the object from a pair of images. In this lesson, you will learn how to perform visual odometry, a fundamental task for vision-based state estimation in autonomous vehicles. 

---

### 1. Visual Odometry

Visual odometry, or VO for short, can be defined as the process of incrementally estimating the pose of the vehicle by examining the changes that motion induces on the images of its onboard cameras. It is similar to the concept of wheel odometry you learned in the second course, but with cameras instead of encoders. What do you think using visual odometry might offer over regular wheel odometry for autonomous cars? Visual odometry does not suffer from wheel slip while turning or an uneven terrain and tends to be able to produce more accurate trajectory estimates when compared to wheel odometry. This is because of the larger quantity of information available from an image. However, we usually cannot estimate the absolute scale from a single camera. What this means is that estimation of motion produced from one camera can be stretched or compressed in the 3D world without affecting the pixel feature locations by adjusting the relative motion estimate between the two images. 

![1567601740793](assets/1567601740793.png)

As a result, we need at least one additional sensor, often a second camera or an inertial measurement unit, to be able to provide accurately scaled trajectories when using VO. Furthermore, cameras are sensitive to extreme illumination changes, making it difficult to perform VO at night and in the presence of headlights and streetlights. Finally, as seen with other odometry estimation mechanisms, pose estimates from VO will always drift over time as estimation errors accumulate. For this reason, we often quote VO performance as a percentage error per unit distance traveled. 

---

### 2. Problem Formulation

Let's define the visual odometry problem mathematically. Given two consecutive image frames, I_k minus one and I_k, we want to estimate a transformation matrix T_k defined by the translation T and a rotation R between the two frames. Concatenating the sequence of transformations estimated at each time step k from k naught to capital K will provide us with the full trajectory of the camera over the sequence of images. Since the camera is rigidly attached to the autonomous vehicle, this also represents an estimate of the vehicle's trajectory. 

![1567601806597](assets/1567601806597.png)

---

### 3. Visual Odometry

Now we'll describe the general process of visual odometry. We are given two consecutive image frames, I_k and I_k minus one, and we want to estimate the transformation T_k between these two frames. First, we perform feature detection and description. We end up with a set of features f_k minus one in image k minus one and F_k in image of k. We then proceed to match the features between the two frames to find the ones occurring in both of our target frames. After that, we use the matched features to estimate the motion between the two camera frames represented by the transformation T_k. 

![1567601895587](assets/1567601895587.png)

---

### 4. Motion Estimation

Motion estimation is the most important step in VO, and will be the main theme of this lesson. The way we perform the motion estimation step depends on what type of feature representation we have. In 2D-2D motion estimation, feature matches in both frames are described purely in image coordinates. This form of visual odometry is great for tracking objects in the image frame. This is extremely useful for visual tracking and image stabilization in videography, for example. In 3D-3D motion estimation, feature matches are described in the world 3D coordinate frame. This approach requires the ability to locate new image features in 3D space, and is therefore used with depth cameras, stereo cameras, and other multi-camera configurations that can provide depth information. These two cases are important and follow the same general visual odometry framework that we'll use for the rest of this lesson. 

![1567602003666](assets/1567602003666.png)

Let's take a closer look at 3D-2D motion estimation, where the features from frame k minus one are specified in the 3D world coordinates while their matches in frame k are specified in image coordinates. 

---

### 5. 3D-2D motion estimation

Here's how 3D-2D motion estimation is performed. We are given the set of features in frame k minus one and estimates of their 3D world coordinates. Furthermore, through feature matching, we also have the 2D image coordinates of the same features in the new frame k. Note that since we cannot recover the scale for a monocular visual odometry directly, we include a scaling parameter S when forming the homogeneous feature vector from the image coordinates. 

![1567602135876](assets/1567602135876.png)

We want to use this information to estimate the rotation matrix R and a translation vector t between the two camera frames. Does this figure remind you of something that we've learned about previously? If you're thinking of camera calibration, you're correct. In fact, we use the same projective geometry equations we used for calibration in visual odometry as well. A simplifying distinction to note between calibration and VO is that the camera intrinsic calibration matrix k is already known. So we don't have to solve for it again. Our problem now reduces to the estimation of the transformation components R and t from the system of equations constructed using all of our matched features. 

---

### 6. Perspective N Point(PNP)

One way we can solve for the rotation and translation t is by using the **Perspective-n-Point algorithm**. Given feature locations in 3D, their corresponding projection in 2D, and the camera intrinsic calibration matrix k, PnP solves for the extrinsic transformations as follows. First, PnP uses the Direct Linear Transform to solve for an initial guess for R and t. The DLT method for estimating R and t requires a linear model and constructs a set of linear equations to solve using standard methods such as SVD. However, the equations we have are nonlinear in the parameters of R and t. 

![1567602265741](assets/1567602265741.png)

In the next step, we'll refine the initial DLT solution with an iterative nonlinear optimization technique such as the Luvenburg Marquardt method. The PnP algorithm requires at least three features to solve for R and t. When only three features are used, four possible solutions results, and so a fourth feature point is employed to decide which solution is valid. Finally, RANSAC can be incorporated into PnP by assuming that the transformation generated by PnP on four points is our model. We then choose a subset of all feature matches to evaluate this model and check the percentage of inliers that result to confirm the validity of the point matches selected. 

The PnP method is an efficient approach to solving the visual odometry problem, but uses only a subset of the available matches to compute the solution. We can improve on PnP by applying the batch estimation techniques you studied in course two. By doing so, we can also incorporate additional measurements from other onboard sensors and incorporate vision into the state estimation pipeline. With vision included, we can better handle GPS-denied environments and improve both the accuracy and reliability of our pose estimates. 

![1567602294016](assets/1567602294016.png)

There are many more interesting details to consider when implementing VO algorithms. Fortunately, the PnP method has a robust implementation available in OpenCV. In fact, OpenCV even contains a version of PnP with RANSAC incorporated for outlier rejection. You can follow the link in the supplementary reading for a description on how to use PnP in OpenCV. In this lesson, you learned why visual odometry is an attractive solution to estimate the trajectory of a self-driving car and how to perform visual odometry for 3D-2D correspondences. 

---

### 7. Summary

> - Visual odometry can be used to provide accurate trajectory estimate for a self-driving car without suffering from slipping effects due to adverse weather conditions
> - Visual odometry can be performed using 2D-3D feature correspondences and the PnP algorithm

Next week, we'll delve into a fundamental approach to extracting information from images for self-driving car perception, deep neural networks. By this point, you've now finished the second week of visual perception for self-driving cars. Don't worry if you did not acquire a full grasp of all the material explained in this week. In this week's assignment, you'll be gaining hands-on experience on all of these topics. You'll use feature detection, matching, and the PnP algorithm to build your own autonomous vehicle visual odometry system in Python. See you in the next module.