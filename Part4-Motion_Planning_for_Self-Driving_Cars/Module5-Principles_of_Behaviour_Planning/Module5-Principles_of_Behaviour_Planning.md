# Module 5: Principles of Behaviour Planning

This module develops a basic rule-based behaviour planning system, which performs high level decision making of driving behaviours such as lane changes, passing of parked cars and progress through intersections. The module defines a consistent set of rules that are evaluated to select preferred vehicle behaviours that restrict the set of possible paths and speed profiles to be explored in lower level planning.

## Learning Objectives

- Recall the role of the Behaviour Planner, as well as its inputs and outputs.
- Use state machines to perform behaviour planning, and recognize their advantages and disadvantages.
- Recognize which behaviours are required to handle certain scenarios.
- Understand the advantages and disadvantages of rule engines in behaviour planning.
- Understand the advantages and disadvantages of reinforcement learning in behaviour planning.

---

## Lesson 1: Behaviour Planning

### Learning Objectives

> - Define a behaviour planning system
> - Understand the standard input and output of a behaviour planner
> - Understand state machines as they relate to behavior planning

Welcome to the fifth week of the motion planning course. In this module, we will be discussing a very important part of our motion planning architecture, behavior planning. We will start this module off by introducing the concept of behavior planning, and how to construct the behavior plan or using a state machine. Then, throughout the rest of the module, we will go through the process of creating a state machine-based behavior planner, able to handle multiple scenarios. Finally, we will finish off this module by looking at alternative approaches to the behavior planning problem, to understand their relative strengths and weaknesses. 

In this lesson, we will, define the requirements for a behavior planning system, explore the typical inputs and outputs to a behavior planning module, and finally, introduce the concept of finite state machines, and how they can be used to create a behavior planning system. Let's begin. 

---

### 1. Behavior Planning

**A behavior planning system, plans the set of high level driving actions, or maneuvers to safely achieve the driving mission under various driving situations.** The set of maneuvers which are planned should take into account, the rules of the road, and the interactions with all static and dynamic objects in the environment. The set of high level decisions made by the planner must ensure vehicle safety and efficient motion through the environment. We discussed many of these concepts already in course one of this specialization, and it is the behavior planner that needs to make the right decisions to keep us moving safely towards our goal. 

![1565265630083](assets/1565265630083.png)

As an example of the role of the behavior planner, let's suppose the autonomous vehicle arrives at a busy intersection. The behavior planner must plan when and where to stop, how long to stay stopped for, and when to proceed through the intersection. The behavior planner has to perform this type of decision-making in a computationally efficient manner, so that it can react quickly to changes in the environment, and be deployed on an autonomous vehicle hardware. The behavior planners should also be able to deal with inputs that are both inaccurate, corrupted by measurement noise, and incorrect, affected by perception errors such as false positive detections and false negative detections. Now that we have the definition for the role of the behavior planner, let's build a list of basic behaviors that we'll work with for the rest of this module. We've described most of these in an earlier video in this course, and we'll use this list as a representation of the set of likely maneuvers or driving behaviors encountered throughout regular driving that an autonomous vehicle may need to execute. 

---

### 2. Driving maneuvers

In all, we'll consider five behaviors. The first is track speed. This behavior amounts to unconstrained driving on open road, meaning that the only restriction on forward progress is that the speed limit should be respected. Next, is follow lead vehicle. The speed of the vehicle in front of the ego vehicle should be matched and a safe following distance should be maintained. The third is decelerate to stop. A stop point exists in the ego vehicle's lane within the planning horizon, and the vehicle should decelerate to a standstill at that stop point. Every regulatory element that requires a complete stop triggers this behavior. Next, we have stay stopped. The vehicle should continue to stay stationary for a fixed amount of time. As an example, when the vehicle stops at a stop sign, it should stay stopped for at least three seconds. Finally, we have the merge behavior. The vehicle should either merge into the left or right lane at this time. 

![1565265937595](assets/1565265937595.png)

This basic list of maneuvers will serve us well in developing the principles of behavior planning. However, many more behaviors should be considered in practice, and the overall complexity of the behavior planner will grow as a result. 

---

### 3. Output of Behavior Planner

The primary output of the behavior planner is a **driving maneuver** to be performed in the current environment. **Along with the driving maneuver, the behavior planner also outputs a set of constraints, which constrain the local planning problem**. The constraints which we will use and populate throughout this module include, the default path from the current location of the vehicle to the goal destination, for many behaviors, this is the center line of the ego vehicle's current lane. 

![1565266196151](assets/1565266196151.png)

The speed limit along the default path. The lane boundaries of the current lane that should be maintained under nominal driving conditions. Any future stop locations which the vehicle needs to arrive at, and this constraint is only populated if the relevant maneuver is selected. Finally, the set of dynamic objects of high interest which the local planner should attend to. These dynamic objects may be important due to proximity or estimated future path. 

---

### 4. Input Requirements

In order for the behavior planner to be able to produce the required output, it needs a large amount of information from many other software systems in our autonomy stack. First, the behavior planner relies on full knowledge of the road network near the vehicle. This knowledge comes from the high definition road map. Next, the behavior planner must know which roadways to follow to get to a goal location. This comes in the form of a mission path over the road network graph. Further, the location of the vehicle is also vital to be able to correctly position HD roadmap elements in the local environment around the vehicle. Accurate localization information is also needed from the localization system as a result. Finally, the behavior planner requires all relevant perception information, in order to fully understand the actions that need to be taken, to safely activate the mission. This information includes, all observed dynamic objects in the environment, such as cars, pedestrians, or bicycles. 

![Screenshot from 2019-08-08 20-17-07](assets/Screenshot from 2019-08-08 20-17-07.png)



For each dynamic object, its current state, predicted paths, collision points, and time to collision, are all required. It also includes, all observed static objects in their respective states, such as parked vehicles, construction cones, and traffic lights, with an indication of their state. Finally, it includes a local occupancy grid map defining the safe areas to execute maneuvers. With all the necessary information available to it, the behavior planner must select the appropriate behavior, and define the necessary accompanying constraints to keep the vehicle safe and moving efficiently. To do so, we will construct a set of rules either explicitly or implicitly that consider all of the rules of the road and all of the interactions with other dynamic objects. 

---

### 5. Finite State Machines

One approach traditionally used to represent the set of rules required to solve behavior selection is a finite state machine. Throughout this module, we will go through a step-by-step process of constructing a finite state machine-based behavior planner. We'll discuss some of the limitations of this approach. To better understand the finite state machine approach, let's walk through a simple example of a finite-state machine for a single scenario, handling a stop sign intersection with no traffic. 

The first set of components of a finite state machine, is the set of states. **For behavior planning system, the states will represent each of the possible driving maneuvers, which can be encountered.** In our example, we will only need two possible maneuvers or states, track speed and decelerate to stop. The maneuver decision defined by the behavior planner is set by the state of the finite state machine. Each state has associated with it an entry action, which is the action that is to be taken when a state is first entered. For our behavior planner, these entry actions involve setting the necessary constraint outputs to accompany the behavior decision. For instance, as soon as we enter the decelerate to stop state, we must also define the stopping point along the path. Similarly, the entry condition for the track speed state, sets the speed limit to track. 

![1565268521658](assets/1565268521658.png)

**The second set of components of the finite state machine, are the transitions, which define the movement from one state to another.** In our two-state example, we can transition from track speed to decelerate to stop, and from decelerate to stop back to track speed. Note that there can also be transitions which return us to the current state, triggering the entry action to repeat for that state. Each transition is accompanied with a set of transition conditions that need to be met before changing to the next state. These transition conditions are monitored while in a state to determine when a transition should occur. For our simple example, the transition conditions going from track speed to decelerate to stop involved checking if a stop point is within a threshold distance in our current lane. Similarly, if we have reached zero velocity at the stop point, we can transition from decelerate to stop back to track speed. 

These two-state example highlights the most important aspects of the finite state machine-based behavior planner. As the number of scenarios and behaviors increases, the finite state machine that is needed becomes significantly more complex, with many more states and conditions for transition. 

---

### 6. Advantages of Finite State Machines in Behaviour Planning

Finite state machines can be a very simple and effective tool for behavior planning. We can think of them as a direct implementation of the definition of behavior planning, which requires us to define maneuvers or states, and local planning constraints or entry actions that satisfy the rules of the road and check safe interaction with other dynamic and static objects in the environment or transition conditions. **By keeping track of the current maneuver and state of the driving environment, only relevant transitions out of the current state need to be considered, greatly reducing the number of conditions to check at each iteration.**

![1565269086097](assets/1565269086097.png)

As a result of the decomposition of behavior planning into a set of states with transitions between them, the individual rules required remain relatively simple. This leads to straightforward implementations with clear divisions between separate behaviors. However, as the number of states increases, the complexity of defining all possible transitions and their conditions explodes. There is also no explicit way to handle uncertainty and errors in the input data. These challenges mean that the finite-state machine approach tends to run into difficulties, as we approach full level five autonomy. But it is an excellent starting point for systems with restricted operational design domains, permitting a manageable number of states. We'll look into these limitations and alternative approaches to behavior planning in the final video in this module. This concludes our introduction to behavior planning. 

---

### 7. Summary

> - Defined the role of a behaviour planning system
> - Standard input and output of a behaviour planner
> - Deploying State Machines as a Behavior Planning
>   - Advantages of using a state machine for behavior planning

In this video, we formulated a clear definition of the behavior planning problem and its role within the overall motion planning system. We discussed the standard inputs and outputs of the behavior planning module. We introduced the finite state machine and its components, and applied it to a two-state behavior planning problem. From here, we'll start to add more capabilities to our finite-state machine behavior planner. In the next lesson, we will learn how to handle all the rules associated with an intersection scenario without any dynamic objects. Well, see you there.

---

## Lesson 2: Handling an Intersection Scenario Without Dynamic Objects

### Learning Objectives

> - Identify the intersection scenario that will be handled
> - Discuss the discretization of the environment that will be used
> - Review the states required to complete the scenario
> - Create the state transitions and state outputs required to safely and effectively complete the scenario
> - Highlighting testing procedures to confirm a correct and accurate system

In the last video, we introduced the concept of a behavior planner, and described the basics of the finite state machine to implement behavior planning. In this video, we will see how to build out our system to handle a more complete intersection scenario. We will start by defining the specifics of the scenario that will be handled. We will then look at how we can discretize the intersection map into sections to establish clear transitions between states. Then we will define the states and transitions which are required to complete the given scenario safely and efficiently. To finish this video, we will highlight the testing procedure required to confirm the correctness and accuracy of our behavior planning system. Let's begin. 

---

### 1. Scenario Evaluation & Discretizing the Intersection

The scenario which we will be attempting to handle is a four-way intersection, with two lanes and stop signs for every direction. A diagram of such an intersection can be seen here, where the red lines represent the stop lines which the car is required to stop behind. 

![1565270228719](assets/1565270228719.png)

By the end of the video, this vehicle should be able to travel left, right, or straight through this intersection. We'll leave dynamic objects out of the scenario for now, and we'll address them in the next video. We've now defined a very restricted operational design domain for our behavior planner to handle. It's now time to implement the behavior planner. Let's start by looking at how to discretize an intersection so that we can more simply make decisions in the environment. 

![1565270333461](assets/1565270333461.png)

The area of the intersection where a vehicle should begin safely braking is defined as the approaching zone of the intersection, highlighted in red. The zone of the intersection in which the vehicle must stop and wait until the appropriate time to proceed will be known as the at zone, highlighted in green. Finally, the zone in which the vehicle is crossing the actual intersection is defined as on the intersection, and is highlighted in orange. The size of each of the above zones are dynamically changed based on two primary factors: the ego vehicle speed, at higher speed, we will require more distance to safely and comfortably stop, and the size of the intersection. The bigger the intersection, the bigger each zone has to be. 

---

### 2. State Machine States

To handle this scenario, we will require three high-level driving maneuvers. Track speed, this maneuver state is only bounded by the current speed limit of the road. Traditionally, this is the maneuver given before entering any region of the intersection, or after entering the on the intersection zone safely. The state entry action sets the speed limit. Decelerate to stop, this maneuver state forces the future trajectory of the object to stop before reaching the stop point. The entry action defines the stop point location. Stop, this maneuver tells the vehicle to stay stopped in its current location. 

![1565270717992](assets/1565270717992.png)

The entry action is to start a timer to wait for a fixed amount of time before proceeding through the intersection. We will now look at the different situations the ego vehicle will encounter in this scenario, and figure out the finite state machine elements needed to encode the correct behavior planning solution. 

---

### 3. State Machine Transitions

Let's start by looking at the ego vehicle before it enters the intersection region, where it has a single constraint to follow the speed limit of the road. This constraint is set based on the entry action of the track speed state. When the ego vehicle enters the approaching zone, the red zone, it must begin decelerating to the stop sign, thus will transition to the decelerate to stop state. The transition condition on moving from track speed to decelerate to stop is therefore entry into the approaching zone. 

![1565270829438](assets/1565270829438.png)

Then, once decelerating, the next maneuver which the autonomous vehicle must execute is to come to a full stop before the stop line, or in the at zone of the intersection. To make sure this happens, the vehicle stays in the decelerate to stop state until it has both a zero velocity and a position within the at zone. 

![1565270905167](assets/1565270905167.png)

The entry action in the decelerate to stop state is the establishment of a safe stop location. 

![1565270949008](assets/1565270949008.png)

Due to the simplicity of this scenario, this is a single stop location, the stop line as given to the planner by the high-definition roadmap. This, however, we will see in the next lesson, will become harder to do once other dynamic objects interact with the ego vehicle. 

![1565271144409](assets/1565271144409.png)

Once fully stopped, the car enters the stop state.  As the entry action, a timer is started to make sure that the vehicle stays in the stopped state for three seconds before proceeding in accordance with typical driving rules. Once the timer is complete, the planner automatically transitions to the track speed state and follows the route provided to it by the mission planner through the intersection, be at left, right, or straight through. This is all the required computation to handle the simple four-way intersection with the finite state machine. Throughout this process, it is vitally important that we understand how we the human expert analyze the scenario, and what the specific capabilities of the resulting behavior planner are. These need to be captured in the operational design domain definition, and we need to ensure that we create a complete state machine able to handle every possible case that can arise for the given scenarios. 

---

### 4. Dealing With Environmental Noise

One particular issue that has a big impact on the performance of our state machine is the issue of noise in the inputs. The state transition conditions defined above are exact, and rely on the vehicle reaching the stop point and achieving a zero velocity exactly. Even with no other dynamic objects to detect, the localization estimates of the vehicle state may contain noise and not satisfy these conditions exactly. 

![1565271481754](assets/1565271481754.png)

To handle this type of input noise, we can introduce noise threshold **hyperparameters**. This is a small threshold value allowing speeds close to zero to be accepted as stopped. We will continue to see these **hyperparameters** more and more in the next lesson, when handling more complex scenarios with dynamic objects. 

---

### 5. Behavior Planning Testing

Now that we've finished creating the finite state machine, how do we test if it works? Well, traditionally, there are **four stages of testing required to confirm functionality of a behavior planning system**, which follow from our discussion of safety assessment for the full vehicle in course 1. First, we perform code-based tests, which are done to confirm that the logic of the code is correct. For example, code-based tests can tell the programmer if the speed limits set in the roadmap will be the speed limit produced by the finite state machine. However, these checks are incapable of confirming if the state transitions are correct, or if the states are capable of handling all of the situations in a given scenario. 

![1565271535000](assets/1565271535000.png)

For this, we have to see if the program code correctly handles all situations as intended. Next, we move to simulation testing, which is performed in a simulated environment like Carla, in which the state machine performs the scenarios which it was designed to handle. This type of testing is able to confirm if the state machine transitions and state coverage are correct. The number of tests performed in the simulation should be representative of all possible situations which can be seen when driving the scenario to catch any edge cases which programmers might have missed. Many times selecting a representative set of tests is not trivial, especially as the complexity of the scenarios increases. 

We then move into **closed track testing**, once confident that the state machine performs as intended in simulation. This type of testing tests specific scenarios which are hard to confirm exactly in simulation, such as parameter tuning and noise, and errors in the perception output in a real environment. Finally, we proceed to **on-road validation testing**. Whereas all previous tests were performed in a highly controlled environment, road tests can be highly unpredictable, and often break the system in a manner otherwise not imagined by engineers. New variations on scenarios can then be incorporated into earlier stages of the testing process. 

---

### 6. Summary

> - The intersection scenario that was handled by the behavior planner state machine
> - Identified the discretization of the environment that will be used 
> - Review the states required to complete the listed scenario
> - Create the state transitions and state outputs required to safely and effectively complete the scenario
> - Highlighting testing procedures to confirm a correct and accurate system

Let's review what we've learned in this video. We first defined the scenario and the operational design domain to be handled, a single intersection scenario with a stop sign in all directions. We then saw how the intersection can be discretized so that each zone can be used when making the transitions of the state diagram. We then built up the states in transitions at the system to correctly define the required behaviors throughout the intersection. Finally, we reviewed four stages of testing that can be used to confirm proper behaviors in the scenario. In the next video, we will show you how to handle the same intersection scenario while interacting with other dynamic objects. As we will see, this makes the state machines significantly more complex and interesting. We'll see you then.

---

## Lesson 3: Handling an Intersection Scenario with Dynamic Objects

### Learning Objectives

> - Review interactions with dynamic object
> - Build upon the previous lesson to include dynamic objects as part of the state machine
> - Develop an understanding of the complexities and edge cases when dealing with dynamic objects

Welcome to the third video this week on behavior planning. In the last video, we developed a basic behavior planner using a finite state machine for a four-way intersection without traffic. We now focus on incorporating traffic interactions in the same four-way intersection. In today's lesson, we will begin by reviewing some of the interactions with the dynamic object covered in previous modules, which we use throughout this lesson to safely interact with the other objects in the environment. We will then extend the state machine that we had built in the previous lesson to include these interactions with other vehicles. Finally, we will briefly discuss the many edge cases and various complexities that occur when dealing with dynamic objects. Let's dive in. 

---

### 1. Review - Scenario Evaluation & Discretizing the Intersection

Once again, the scenario we study in this video is a single lane four-way stop intersection. We would like to be able to travel in any possible direction through this intersection, while now handling interaction with other vehicles. 

![1565351398895](assets/1565351398895.png)

Recall that in the previous lesson, we broke up the intersection into three areas or zones. The approaching zone highlighted in red, represents when a vehicle should decelerate to stop at the intersection. 

![1565351463281](assets/1565351463281.png)

The ad zone highlighted in green, is where the vehicle should stop prior to entering the intersection. The on zone in orange, which represents the intersection itself. The zone's size can be shifted based on the ego and dynamic velocities, as well as the size of the intersection. 

---

### 2. Review - Interaction With Dynamic Objects

Throughout this lesson, we will be focusing on the interactions with other dynamic objects, specifically other vehicles. In order to be able to safely deal with these vehicles, one important aspect is a measurement of the distance to various interaction points with the other objects. 

![1565351558452](assets/1565351558452.png)

The first distance measure to consider, is the distance to dynamic objects. This is defined as the Euclidean distance between the current ego position to the center of any dynamic object in the environment. The second is the distance to collision point, which is the distance to a potential collision point with another dynamic object. Finally, the time to collision is the time it would take to reach the given collision point. Our approach to calculating this was discussed in the previous video. 

---

### 3. State Machine States

Now let's expand a finite state machine to accommodate the added complexity of the dynamic objects. We will need to increase the required maneuvers to four in order to correctly handle all interactions with vehicles in this scenario. 

First, let's review the maneuvers we included in our first version of the finite state machine. These were: track speed, who's only constraint is the speed of the given road, decelerate to stop, which requires the ego vehicle to decelerate to a stop point at a specific location in the environment, and stop, where we remained in the stop position. The new maneuver we need to add is follow leader. This maneuver state requires the ego vehicle to follow the speed of and maintain a safe distance to a lead vehicle, which is any vehicle directly in front of it in its lane. The safe distance is speed dependent and both safe speed and safe distance are updated as entry actions on every iteration of the behavior planner. 

![1565351746845](assets/1565351746845.png)

Now that we have all of the states defined for our expanded finite state machine, we turn to populating the transitions. We will do this in a similar fashion to the previous lesson, starting at a given state and then identifying all of the transitions out of that state before proceeding to the next. We'll display progress through the intersection as we define transitions in a pictorial representation of the scenario seen here on the left, and we'll build up the finite state machine on the right. 

#### Track Speed

In each pictorial representation, the autonomous ego vehicle will be denoted by a red arrow. We will then start as we did in the previous lesson with the ego vehicle being located outside the intersection in the track speeds state. Much as we've seen in the previous lesson, the ego vehicle will only move to the decelerate to stop state once in the approaching zone. However, there is an additional concern, the situation in which another vehicle appears or enters the lane in front of the ego vehicle. In this case, we will move to attempt to follow the vehicle by performing a follow check. 

![1565351891851](assets/1565351891851.png)

The follow check can be decomposed into two elements. A distance check and a same lane check. The distance check confirms that the vehicle is close enough such that it should be followed. In the same lane check confirms that the vehicle is actually in the same lane as the ego vehicle. In this case, we can use distance to dynamic object, which is the Euclidean distance to the object and compare that to a threshold. There are several methods which can be employed to check if the vehicle is in the same lane as the ego vehicle. However for simplicity, we will check if the lead vehicle is within the lane limits and if the heading of the dynamic object is within a given threshold to that of the ego vehicle indicating it is moving in the same direction. 

#### Follow Leader

In the follow leaders state, we define only two transitions. First, the lead vehicle might exit the lean before the ego vehicle is approaching or at the intersection, resulting in a switch to the track speed state. Or the lead vehicle drives out of the current lane, usually, onto the intersection when the ego vehicle is already in the at or approaching zones, resulting in a direct transition to the decelerate to stop state. 

![1565352009046](assets/1565352009046.png)

We add the transition condition, that the distance to collision is greater than the distance to the stop point when the ego vehicle is either in the approach or add zones. In this situation, the ego vehicles should transition to decelerate to stop and set the stop point to the correct location at the stop line of the intersection. 

![1565352056140](assets/1565352056140.png)

#### Decelerate to Stop

As before, in the decelerate to stop state, the ego vehicle continues decelerating until the time when it comes to a stop at the stop line. Which will result in a switch to the stop state as seen in our previous lesson. 

![1565414989998](assets/1565414989998.png)

However, we once again have to take into account that a vehicle is able to pull in front of the autonomous car at an intersection, either from a driveway or an overtaking maneuver. Much as before, we perform the follow check throughout the decelerate to stop state when the ego vehicle is in the approaching or add zones, and transition to follow leader if the check returns true. In this case however, the distance check considers whether the lead vehicle distance to collision is less than the stop point distance, so that the leader following modes should take precedence. 

![1565415061448](assets/1565415061448.png)

#### Stop

Finally, to complete our expansion of the finite state machine, let's look at the situations we can face once stopped. To keep things simple, we'll assume a very conservative driving style, where our autonomous car waits until all vehicles have cleared the approaching, at, or on intersections zones before proceeding through it. We leave the implementation of precedents at the stop sign for you to explore on your own. 

![1565415160190](assets/1565415160190.png)

Further, we'll define simple checks for a rectilinear intersections, that identify all vehicles direction of travel with four easy labels and only consider other vehicles moving straight through the intersection. Relative to the ego vehicles body frame, a vehicle object with a relative heading of between minus 45 and 45 degrees, will be labeled as going in the same direction as the ego vehicle. 

![1565415271973](assets/1565415271973.png)

A vehicle between minus 45 and 135 degrees relative heading, will be labeled as heading to the right. Between minus 135 and 135 as heading towards the ego vehicle and finally, between 45-135 degrees relative heading, will be labeled as going to the left. This simplification can be improved using predicted paths for the dynamic objects, especially if additional perception information is available to improve prediction of the direction of travel through the intersection. We can now define the transitions out of the stop state. Will have two sets of transitions. Either follow leader or track speed, depending on whether a vehicle is present within the lane through the intersection that satisfies the follow check. 

![1565415303194](assets/1565415303194.png)

In each case, the transition conditions change based on the path through the intersection required by our mission plan. When the ego vehicle needs to turn left, any vehicle approaching from the left, right, or any oncoming vehicle, must clear the on intersection zone before the ego vehicle can proceed. When the ego vehicle needs to go straight, only vehicles approaching from the left or right, need to clear the intersection. 

![1565415363019](assets/1565415363019.png)

Finally, when the ego vehicle needs to turn right, only vehicles approaching from the left need to clear the intersection. From this simple definition of the transitions out of the stop state, we hope you can visualize the additional checks needed to handle the precedence due to arrival order at an intersection and the possibility that the other vehicles might also turn left or right. 

---

### 4. State Machine Transitions

The resulting full state machine includes the following states and transitions. 

![1565415496491](assets/1565415496491.png)

While this state machine is unable to be used on a real autonomous vehicle due to the oversimplifications we relied on, it serves as a good demonstration of the process of converting a given operational design domain into a functional finite state machine. You're now ready to start tackling more complex scenarios with more complete dynamic object models. 

---

### 5. Dynamic Object Edge Cases Not Handled

So far throughout the creation of a state machine, we have made one particularly **strong assumption** about how dynamic objects behave. Namely, that all dynamic objects obey the rules of the road. However, this is not always the case, and this difficulty leads to many edge cases that also need to be considered. 

![1565415572068](assets/1565415572068.png)

Let's quickly discuss a few examples of what can go wrong with this strong assumption. The first example would be when a driver unintentionally swerves into oncoming traffic, entering the lane of the ego vehicle. This actually happened to a Waymo van in 2018, when a driver careened over a median into oncoming traffic. Another example, is of an aggressive driver racing through an intersection even as the ego vehicle has begun driving through it. Another common example, is when a vehicle fails to stop at the intersection. 

Finally, I will end with the case of a vehicle which is parked in close proximity to the intersection. If this vehicle is not tagged as parked, so that it might be treated as a static instead of dynamic object, our behavior planner may get stuck in a deadlock state waiting for this parked vehicle to move. This is by no means a complete set of all possibilities, and one of the primary objectives of behaviors safety assessment and testing, is to uncover as many variations of unexpected behaviors as possible, so that they also can be detected, categorized, and incorporated into the behavior planning design process. 

Just simply uncovering edge cases is not enough, however. Rather we must define how the autonomous vehicles should react to every one of these cases. For this emergency maneuvers such as a swerve or a hard break are required, with many more transitions and conditions to define. This is an active area of research and development and we've included some additional resources in the supplemental materials, if you'd like to find out more. 

---

### 6. Summary

> - Build upon the previous lesson to include dynamic objects as part of the state machine
> - Developing an understanding of the complexities and edge cases when dealing with dynamic objects

In summary, in today's video, we learned how we can create a finite state machine, able to interact with dynamic objects which follow the rules of the road. We saw why dealing with dynamic objects is so challenging by looking at just a few of the many possible edge cases which they can create. In our next lesson, we will see how we can continue building our behavior planner to be able to handle multiple scenarios simultaneously. We'll see you next time.

---

## Lesson 4: Handling Multiple Scenarios

### Learning Objectives

> - Develop a larger overarching state machine which includes multiple scenarios
> - Develop a method to switch between driving scenarios

Welcome to the fourth video in the behavior planning module. In the last video, we introduced dynamic objects into our finite state machine behavior planner. In this video, we will develop a larger behavior planner which is able to manage the decision process for multiple scenarios simultaneously. We will do this by introducing the notion of a hierarchical finite state machine. We will also develop a method to switch between each of the driving scenarios as they occur. Let's begin. 

---

### 1. Scenario Done So Far & Multiple Scenarios

So far in this module, we have developed a finite state machine behavior planner that can handle a single four-way stop intersection scenario with dynamic objects. 

![1565416476135](assets/1565416476135.png)

However, in driving, there are many such scenarios which will be encountered. For example, there are three-way stop intersections, traffic light controlled intersections, and straight road scenarios, just to name a few. 

![1565416497150](assets/1565416497150.png)

While many of these scenarios share some similarities largely due to the logic required to handle them, each of the scenarios can be considered to require fundamentally different driving behaviors. 

---

### 2. Single State Machine

One method of handling these multiple scenarios is by adding additional states, transitions and conditions to a single state machine in an ever-expanding network of behaviors. However, there are several problems with this approach. The first problem is that we would need to develop additional logic to differentiate the current scenario, as well as the rules needed to handle each scenario individually. 

![1565416763449](assets/1565416763449.png)

This quickly runs into a problem known as rule explosion, in which the number of rules required to add additional scenarios becomes unimaginably large. The second problem with a single state machine is that due to the number of extra rules and transitions that need to be evaluated at each step, the computational time required significantly increases, and lastly, such a system is complicated to create and maintain as a number of cases which one must worry about increases quickly. Essentially, as the complexity increases, we lose all the advantages of using a finite state machine that were highlighted back in lesson one. 

---

### 3. Multiple State Machine

There is however, another approach we can use. We can represent each high level scenario as a single state. This would allow us to create much simpler transitions in between the high level scenario states. In this example, we can see that the states represent a straight road scenario and the four-way intersection scenario we worked with previously. 

![1565416875131](assets/1565416875131.png)

With each one of these high level scenario states, we will store a low-level state machine with which we can handle the scenario independently. For example, for the intersection scenario, the low-level state machine will be the one constructed over the last two lessons. This method of representation is known as a hierarchical state machine, with the super-states representing each scenario, and the sub-states representing the maneuvers to be handled in each scenario. 

---

### 4. Hierarchical State Machine

The transitions between the high level scenario state machine would be a rule that defines when a new scenario has been entered, based on the HD roadmap and dynamic vehicle information. Let's say we have this simple hierarchical state machine with two scenarios, one for straight road with a pedestrian crossing, and another for a stop sign-based intersection. 

![1565416986746](assets/1565416986746.png)

To move from the straight road to the stop sign intersection, the autonomous vehicle has to be close to an encounter with this intersection. This is done with a distance check to the next intersection along the mission plan. All the movements which we have talked about here is at the super-state level. The next question we have to answer is, how do we switch between scenarios when processing the sub-state maneuvers? 

---

### 5. Entry and Exit Transitions - Intersection

One method is to introduce transitions to key maneuver sub-states out of the current scenario super-state. Let us continue to use the intersection scenario as an example. First, let's establish which state will be the key exit state out of the scenario. The only way we're able to exit an intersection is while in the track speed or follow leader states after having passed the intersection. So let's put the exit transitions there. 

![1565417200533](assets/1565417200533.png)

The condition on the transitions would be to confirm that this scenario has indeed been completed. In this example, we can use the distance to the next stop sign intersection. If this is larger than a given threshold, we can exit the intersection scenario. With this method of transition, we were able to also maintain maneuvers between scenario switches. In this case, track speed in the intersection super-state will connect to the track speed of the next scenario that we enter. 

---

### 6. Hierarchical State Machine & Advantages and Disadvantages

Adding an additional multi-lane scenario to this hierarchical state machine is done by creating a new super-state scenario node, with a sub-state state machine capable of handling that scenario. 

![1565417252343](assets/1565417252343.png)

This type of finite state machine has some inherent strengths and weaknesses. The strengths of this approach are due to it's subdivided nature. By creating individual state machines within each super-state, this method is able to limit the computational time required at any one time step by restructuring our sub-space. This subdivided nature also makes both testing and programming of a hierarchical state machine significantly easier. However, the hierarchical state machine is not without its problems, while limiting the number of rules required, this approach is still unable to handle rule explosion completely. 

![1565417307242](assets/1565417307242.png)

One reason for the large number of rules is that all scenarios have fully separated state machines, and thus many of the rules are duplicates of one another in order to handle similar behaviors in different scenarios. Ultimately, the hierarchical approach allows the system designer to handle a greater amount of complexity than a flat single layered finite state machine. The idea can be extended to multiple layers as long as key states can be defined at each level. In reality, the perspective enforced by finite state machines, that a single behavior is active at any given time, and that all transitions to other behaviors can be explicitly defined, has a limit on how large a set of scenarios it can handle. Nonetheless, it provides a useful tool for typical behavior planning in a self-driving car. 

---

### 7. Summary

> - Developing a larger overarching state machine which includes multiple scenarios
> - Develop a method to switch between driving scenarios

Let's summarize what we've discussed in this video. We first introduced the hierarchical finite state machine, which is able to handle multiple scenarios simultaneously. We also discussed how to transition between the different driving scenarios at the super and sub-state levels, and we discussed the capabilities and limits of behavior planning with hierarchical finite state machines. Join us in our next video where we will discuss a range of advanced research approaches that are able to solve some of the issues we've faced so far with behavior planning. See you there.

---

## Lesson 5: Advanced Methods for Behaviour Planning

### Learning Objectives

> - Identify issues with the state machine based behaviour planner
> - Identify the open areas of research in behaviour planning

Welcome to the fifth and final video of the behavior planning module. In this video we will discuss the limitations of state machine based approaches to behavior planning. And we will then take a tour through some alternative behavior planning systems that aim to address some of these limitations. By the end of this video you should have a good overall picture of the main methods used in behavior planning. 

---

### 1. State Machine Behaviour Planning Issues

> - Rule-explosion when Dealing with Complex Scenarios
> - Dealing with a Noisy Environment
> - Hyperparameter Tuning
> - Incapable of Dealing with Unencountered Scenarios

Let's begin by identifying the issues with our state machine model. The first issue we identified throughout the development of this module is the issue of rule-explosion. This means that as we develop a more complete set of scenarios and maneuvers to handle the number of rules required grows very quickly. This limitation means that while it is possible to develop a finite state machine behavior planner to handle a limited operational design domain. 

Developing a full level four or five capable vehicle is almost impossible with finite state machines. Dealing with a noisy environment is the next issue. While we saw in lesson two and three how the addition of **hyperparameters** can be used to deal with some noise. This type of noise handling is only able to deal with some every limited situations. To deal with all types of input uncertainty different methods will be required. On that note, the next issue I would like to point out is the actual tuning of the hyperparameters. As the behaviors required get more complex, the number of hyperparameters to both discretize the environment and handle some of the low level noise grow rapidly. All these hyperparameters have to be tuned very carefully and this can be a lengthy process. 

Finally, the last issue we'll discuss is handling of unencountered situations. Due to the program nature of this approach it is very likely that there will arise a situation in which the programmed logic of the system will react in an incorrect or unintended manner. State machine based approaches are classified as experts systems, systems which have been designed and develop by human experts. However, state machines are not the only such expert systems devised. There are also approaches that rely on a database of rules which are applied to the input data at every time step. 

---

### 2. Rule-Based Behaviour Planner

The rules are formed into a hierarchy where safety critical rules take precedence, override comfort rules, or defensive driving rules, for example. Each rule is engaged only when the appropriate conditions arise for it to affect the selection of the output maneuver. 

![1565421509022](assets/1565421509022.png)

Such rule databases do not suffer from the problem of needing to duplicate the rules that we encountered with hierarchical state machines. As the rules can apply throughout the ODD or over significant portions of it. However, rule based systems have to very carefully develop rules in such a way that they do not negatively impact each other. Or lead to unintended outcomes when multiple rules are activated at the same time. Due to the common reliance on expert users to design for all possible scenarios, both types of expert systems suffer from the same issues described above. 

---

### 3. Fuzzy Logic

One possible solution to some of the problems we've identified above is to extend the human expert type plan or to incorporate Fuzzy logic. Fuzzy logic is a system by which a set of crisp, well-defined values are used to create a more continuous set of fuzzy states. For a simple example of how a Fuzzy based system works, let's take a look at the example of the vehicle following behavior. 

![1565418151697](assets/1565418151697.png)

While previously we set a parametrized distance which divided the space into follow the vehicle or do not follow the vehicle. With a Fuzzy system we're able to have a continuous space over which different rules can be applied. For example, a Fuzzy system might react strongly to a lead vehicle when very close to it. But be less concerned with the speed matching or distance following requirements when it's further away. While Fuzzy based rule systems are able to deal with the environmental noise of a system to a greater degree than traditional discreet systems. Both rule-explosion and hyperparameter tuning remain issues with Fuzzy systems. In fact, Fuzzy systems can result in rule-explosion to an even greater degree, as even more logic is required to handle the fuzzy set of inputs. Accompanying the rule-explosion is a large challenge in hyperparameter tuning as well. 

---

### 4. Reinforcement Learning

The next exciting research approach I'd like to discuss is the use of reinforcement learning for behavior planning. Reinforcement learning is a form of machine learning in which an agent learns how to interact with a given environment by taking action and receiving a continuous reward. The agent begins by engaging in play with a simulated environment. Which means that at the start the agent will not be good at the particular task, however, over time as the agent maximizes its reward, they eventually learn to master the task. By learning in a simulated environment, no real world repercussions occurred during the many failures experienced during learning. 

![1565418298243](assets/1565418298243.png)

More specifically, we can say the agent is attempting to learn a policy, denoted by p, which maps a given environment, denoted by s, to a given actions, denoted by a. To connect the concept of reinforcement learning to behavior planning let's say we're attempting to teach the autonomous vehicle how to follow a lead vehicle. In this case our policy p will be attempting to do vehicle following. Our actions may be explicitly defined as behaviors to execute or can define behaviors implicitly through selection of desired accelerations and turn rates. The environment can be represented by a continuous set of variables telling us relevant information, such as distance to all objects and our mission path. And, finally, the reward function could be based on an optimal following distance. And give the highest reward at the preferred distance, penalizing getting too close more heavily than being too far away. 

![1565418316216](assets/1565418316216.png)

Because of the extremely large variety of scenarios and inputs that an autonomous vehicle can encounter, direct reinforcement learning for behavior planning is unlikely to succeed. Instead some further adaptations are usually applied. **One such adaptation is known as hierarchical reinforcement learning.** Where we divide the problem into low level policies in the maneuver space and high level policies the scenarios. This is similar to the hierarchical finite state machine. Then each low level policy is learned independently and only once successfully learned a high level policy can be learned to complete a scenario. **The second technique often applied is called model-based reinforcement learning.** In model-based reinforcement learning not only is the agent attempting to learn a policy, p, but also a model of the current environment around the agent. An example of how this approach might apply to behavior planning for self driving cars would be to include a model of the movement of dynamic objects. If the agent understands the movement patterns of the dynamic object it can create more effective plans through the environment. 

---

### 5. Reinforcement Learning Issues

While reinforcement learning is a very exciting and highly promising area of research it too is not without its own limitations. Many simulation environments used to learn the policies required for autonomous driving are overly simplified. And due to their simplicity the policies learned may not be transferable to real world environments. Overly realistic simulators lead to the issue of severe computational requirements. Especially when running thousands of repetitions of widely varying scenarios for self driving learning. 

![1565418558805](assets/1565418558805.png)

The second is an issue concerning safety. While there are techniques within reinforcement learning that attempt to ensure safety constraints along the trajectories created by the reinforcement learner. There is still no way to perform rigorous safety assessment of a learned system, as they are mostly black boxes in terms of the way in which decisions are made. 

---

### 6. Machine Learning

Many other interesting ideas are also being explored right now in the research community and many of them try to learn from human driving actions. For example, in inverse reinforcement learning rather than trying to obtain a policy given a reward function, the approach is to use human driving data as the policy. An attempt to learn the reward function used by humans. Once the reward function is learned the algorithm can then execute driving maneuvers similarly to a human driver. 

![1565418604011](assets/1565418604011.png)

Finally, end-to-end approaches take as an input raw sensor data and attempt to output throttle, break, and steering commands. By learning, once again, from human driving commands in an imitation learning approach. This approach was pioneered by researchers at Nvidia with their paper, End to End Learning for Self-Driving Cars. While this is not explicitly classified as behavior planning, the end-to-end approach still implicitly performs the task of behavior selection as part of its output selection process. These brief explanations only scratched the surface of a huge and rapidly evolving research area. Behavior planning remains one of the hotbeds of activity in autonomous driving research. And one of the toughest bottlenecks in achieving real world level five autonomy. We've included a reading list of some of the recent work in this area in the supplemental materials for those interested in learning more.

- J. Wei, J. M. Snider, T. Gu, J. M. Dolan, and B. Litkouhi, “[A behavioral planning framework for autonomous driving](https://ieeexplore.ieee.org/abstract/document/6856582),” 2014 IEEE Intelligent Vehicles Symposium Proceedings, 2014. This gives a nice overview of an example framework that can be used in behaviour planning.
- R. S. Sutton and A. G. Barto, [Reinforcement learning an introduction](http://incompleteideas.net/book/the-book-2nd.html). Cambridge: A Bradford Book, 1998. Gives a great introduction to reinforcement learning concepts.

---

### 7. Summary

> - Identify issues with the state machine based behaviour planner
> - Identify the open areas of research in behaviour planning

Let's summarize what we've discussed in this video. We presented some of the issues with finite state machine based planning. And presented multiple advanced approaches to the problem of behavior planning which seek to address the full complexity of the behavior planning problem. And with that we have come to the end of our behavior planning module. In this module we've defined the requirements needed to make a behavior planning system capable of autonomous driving. Then we walked through the creation of such a system for a specific scenario, a four way intersection. We then added dynamic vehicle interactions and expanded to incorporate multiple scenarios. We ended with a brief review of a few exciting methods emerging from the behavior planning research community. Join us for the next module where we will build a full local planning solution using parameterized curves and nonlinear optimization, until then. 