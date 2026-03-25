Terminal 1:
    cd ~/ros2_ws
    colcon build
    source install/setup.bash
    ros2 launch my_robot_pkg spawn_my_robot.launch.py # this executes tje file and opens gazebot with the robot spawned

to run the plot python code: enter
    cd ros2_ws/src/my_robot_pkg
    cd my_robot_pkg
    python3 plot_trajectories.py

