# Overview

This simple project integrates OpenAI's GPT-4 language model with ROS 2 to create an interactive, natural language interface for robot navigation. Users can input commands in plain English, and the assistant will interpret them to navigate the robot to the desired location.

# How it works

The assistant operates by integrating GPT-4's natural language processing capabilities with ROS 2's navigation functionalities. Here's a step-by-step breakdown:

**1. User Input** 

The user provides a command in natural language via the command-line interface.

**2. Language Processing**

* The assistant sends the user input to the ```OpenAI GPT-4``` model.
* ```GPT-4``` interprets the input and determines whether a navigation action is required.
* If a navigation command is identified, ```GPT-4``` generates a ```function_call``` to ```navigate_robot``` with the appropriate parameters.

**3. Parameter Extraction**

* The assistant parses the ```function_call``` arguments to extract navigation parameters: ```x```, ```y```, and ```z_rotation```.
* Uses ```Pydantic```'s ```NavigationCommand``` model for data validation.

**4. Robot Navigation**

* Initializes the ```ROS 2``` client library (```rclpy```) and creates a ```BasicNavigator``` instance.
* Sets the robot's initial pose.
* Constructs a ```PoseStamped``` message with the goal position and orientation.
* Commands the robot to navigate to the goal pose using ```nav.goToPose(goal_pose)```.

**5. Feedback Loop**

* While the navigation task is not complete, the assistant retrieves feedback using ```nav.getFeedback()``` and provides updates to the user.
* Once the task is complete, it confirms completion to the user.

**6. Error Handling**

* If ```GPT-4``` does not produce a ```function_call```, the assistant outputs the assistant's message content.
* If there's an error parsing the arguments, it informs the user.

# Executing
1. **Nav2 installation**

First of all, make sure to have [ROS 2 installed](https://docs.ros.org/en/foxy/Installation.html#). 
Next, we will install three necessary packages to interact with Nav2 and specifically with the Turtlebot3 Burger robot:

```bash
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-turtlebot3*
```

2. **Initiate the virtual environment**

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt
```

3. **Run the Robot or Simulator Bringup**
First, you need to start your robot's bringup sequence or launch your simulation environment. This initializes all the necessary nodes and configurations for your robot.

* For a physical robot

```bash
ros2 launch turtlebot3_bringup robot.launch.py
```

* For a physical robot

For a Simulation (e.g., Gazebo (Webots is better!)):

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```
_Ensure that the simulation environment is properly configured to work with your robot model._

4. **Run Cartographer to Load the Map**

```bash
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=<path/to/the/map>.yaml
```

Note: If you already have a saved map, make sure Cartographer is configured to load it. Otherwise, it will start building a new map.

5. **Run the Navigation Assistant**
With the robot/simulator and Cartographer running, you can now start the navigation assistant script.
```bash
python main.py
```

6. **Execute a Navigation Command**
When prompted by the assistant, enter your navigation command in natural language.

Example command
```bash
Enter your command: move the robot to x in 1.1 and y in -0.45
```

# Project Structure

``` bash
ros2-gpt/
├── main.py   # Main script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not committed)
└── README.md                 # Project documentation
```

# 
By following these steps, you should be able to successfully run the navigation assistant and command your robot using natural language inputs!

