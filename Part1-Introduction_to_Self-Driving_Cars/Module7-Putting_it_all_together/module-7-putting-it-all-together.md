# Module 7：Putting it all together

For the last week of the course, now you will get hands on with a simulation of an autonomous vehicle that requires longitudinal and lateral vehicle control design to track a predefined path along a racetrack with a given speed profile. You are encouraged to modify the speed profile and/or path to improve their lap time, without any requirement to do so. Work and play!

### 学习目标

* Integrate vehicle modeling and controller design into a complete vehicle control system
* Develop a working simulation with a python-based vehicle autonomy agent
* Tune a control system for tracking performance on a complex path

## Lesson 1: Carla Overview - Self-Driving Car Simulation

Welcome to the final module of the first course in our self-driving cars specialization. In this module, you'll get the chance to bring together and apply the concepts we've discussed throughout this course and test them in simulation. We'll start by discussing various self-driving car simulation environments. Then I'll show you the simulator that you'll use in this course and throughout this specialization.

A realistic simulation environment is an essential tool for developing a self-driving car, because it allows us to ensure that our vehicle will operate safely before we even step foot in it. Using a simulator, we can test all of the different modules that make up our system including perception, planning, and control, either together or independently. We can run sophisticated scenarios involving many AI controlled vehicles and pedestrians, and we can run variations on these scenarios, hundreds or even thousands of times to ensure our car consistently makes the correct decision. Most importantly, we can test our car in situations that would be too dangerous for us to test on actual roads.

There are a wide range of simulators available, developed by teams from industry and academia alike. For this course, we'll be using the simulator called Carla. Carla is a simulator developed by a team with members from the Computer Vision Center at the Autonomous University of Barcelona, Intel and the Toyota Research Institute and built using the Unreal game engine. It features highly detailed virtual worlds with roadways, buildings, weather, and vehicle and pedestrian agents. Images of these environments can be captured in various formats including depth maps and segmented images which you'll learn more about in the third course of this specialization.

The entire simulation can be controlled with an external client which can be used to send commands to the vehicle, record data and automatically execute scenarios for evaluating the performance of your car. Best of all, Carla is open source. So, anyone is free to modify any aspect of the code in order to meet their particular simulation requirements.

For this specialization, we've developed a customized version of Carla with some extra tools to help you implement and test your code and simulation. Let's take a look at how you might interact with and use the simulator. Don't worry about the following along. There's a detailed guide about how to set up Carla and run the Python clients in the assessment instructions. We've already downloaded and installed everything. So, let's jump right into the simulator itself.

The easiest way to start Carla is to use the launch script provided. The script itself is used to load the Carla session with a map or scenario of our choosing. Here, I choose the town environment provided in Carla for our demonstration. We can also change various configurations for our simulator session, such as the simulation window size and setting a fixed time step to be either small or large. A Carla session can also be loaded in server mode. This allows a programmable client to connect to the server, and send commands to control the car or receive information about the simulation environment. Being able to program our client opens up a diverse range of possibilities.

From the simulator feedback, we can know where every car is on the map, develop a controller and planner to smoothly navigate our car around or even use depth and segmented images to learn to detect cars and pedestrians. Simulation results from the client can also be post-processed to evaluate the performance of our current software algorithms and methods. This provides insight on improvements and limitations to both the simulator and algorithms.

For our upcoming course project, we use these results as a way to evaluate your algorithm's performance and to encourage exploration of the strengths, as well as the weaknesses of the algorithms you are developing. We've talked about why simulation is useful and what you can use it for, and we've met Carla, the simulator that we'll use throughout this specialization. We've also seen some of the capabilities of Carla which you'll use in the upcoming course project.

Now, before we move on to the details of the project, it's time for you to take a closer look at the simulator itself and to set it up on your own computer. Now's the time to follow those detailed instructions that will take you through the full process. I also encourage you to consult the discussion forums if you run into any problems, chances are someone's had the same issue as you before. Once you have the simulator up and running and you're comfortable launching and running a client, you'll be ready to start using it for the course project. In the next video, we'll go over the final project requirements and get you ready to start designing controllers for your simulated self-driving vehicle. See you there.

