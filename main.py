import openai
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from math import pi
from nav2_simple_commander.robot_navigator import BasicNavigator
from tf_transformations import quaternion_from_euler
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json

load_dotenv()

openai.api_key = os.getenv("API_KEY")

def navigate_robot(x: float, y: float, z_rotation: float):
    rclpy.init()
    nav = BasicNavigator()

    q_x, q_y, q_z, q_w = quaternion_from_euler(0.0, 0.0, z_rotation)

    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = nav.get_clock().now().to_msg()
    initial_pose.pose.position.x = 0.0
    initial_pose.pose.position.y = 0.0
    initial_pose.pose.position.z = 0.0
    initial_pose.pose.orientation.x = q_x
    initial_pose.pose.orientation.y = q_y
    initial_pose.pose.orientation.z = q_z
    initial_pose.pose.orientation.w = q_w

    nav.setInitialPose(initial_pose)
    nav.waitUntilNav2Active()

    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = nav.get_clock().now().to_msg()
    goal_pose.pose.position.x = x
    goal_pose.pose.position.y = y
    goal_pose.pose.position.z = 0.0
    goal_pose.pose.orientation.x = q_x
    goal_pose.pose.orientation.y = q_y
    goal_pose.pose.orientation.z = q_z
    goal_pose.pose.orientation.w = q_w

    nav.goToPose(goal_pose)

    while not nav.isTaskComplete():
        feedback = nav.getFeedback()
        print("Feedback:", feedback)

    print("Navigation task completed.")
    rclpy.shutdown()
    return "Navigation task completed!"

class NavigationCommand(BaseModel):
    x: float
    y: float
    z_rotation: float

tools = [
    {
        "name": "navigate_robot",
        "description": "Move the robot to a specific location with a given rotation.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "number", "description": "X coordinate of the goal position."},
                "y": {"type": "number", "description": "Y coordinate of the goal position."},
                "z_rotation": {
                    "type": "number",
                    "description": "Rotation around the Z-axis in radians."
                },
            },
            "required": ["x", "y", "z_rotation"],
        },
    }
]

def main():
    print("Welcome to the ROS2 Navigation System! Type 'exit' to quit.")
    while True:
        user_input = input("Enter your command: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a robot control assistant. Interpret user input and decide "
                        "when to trigger the 'navigate_robot' function."
                    ),
                },
                {"role": "user", "content": user_input},
            ],
            functions=tools,
        )

        if "function_call" in response["choices"][0]["message"]:
            function_call = response["choices"][0]["message"]["function_call"]
            if function_call["name"] == "navigate_robot":
                try:
                    args = json.loads(function_call["arguments"])
                    x = args["x"]
                    y = args["y"]
                    z_rotation = args["z_rotation"]

                    result = navigate_robot(x, y, z_rotation)
                    print(result)
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error parsing arguments: {e}")
        else:
            print(response["choices"][0]["message"]["content"])

if __name__ == "__main__":
    main()
