#!/usr/bin/env python3

# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

# Author: Ryan De Iaco
# Additional Comments: Carlos Wang
# Date: October 29, 2018

import numpy as np
import copy
import path_optimizer
import collision_checker
import velocity_planner
from math import sin, cos, pi, sqrt


class LocalPlanner:
    def __init__(self, num_paths, path_offset, circle_offsets, circle_radii,
                 path_select_weight, time_gap, a_max, slow_speed,
                 stop_line_buffer, prev_best_path):
        self._num_paths = num_paths
        self._path_offset = path_offset
        self._path_optimizer = path_optimizer.PathOptimizer()
        self._collision_checker = \
            collision_checker.CollisionChecker(circle_offsets,
                                               circle_radii,
                                               path_select_weight)
        self._velocity_planner = \
            velocity_planner.VelocityPlanner(time_gap, a_max, slow_speed,
                                             stop_line_buffer)
        self.prev_best_path = []

    ######################################################
    ######################################################
    # MODULE 7: GOAL STATE COMPUTATION
    #   Read over the function comments to familiarize yourself with the
    #   arguments and necessary variables to return. Then follow the TODOs
    #   (top-down) and use the surrounding comments as a guide.
    ######################################################
    ######################################################
    # Computes the goal state set from a given goal position. This is done by
    # laterally sampling offsets from the goal location along the direction
    # perpendicular to the goal yaw of the ego vehicle.
    def get_goal_state_set(self, goal_index, goal_state, waypoints, ego_state):
        """Gets the goal states given a goal position.
        
        Gets the goal states given a goal position. The states 

        args:
            goal_index: Goal index for the vehicle to reach
                i.e. waypoints[goal_index] gives the goal waypoint
            goal_state: Goal state for the vehicle to reach (global frame)
                format: [x_goal, y_goal, v_goal], in units [m, m, m/s]
            waypoints: current waypoints to track. length and speed in m and m/s.
                (includes speed to track at each x,y location.) (global frame)
                format: [[x0, y0, v0],
                         [x1, y1, v1],
                         ...
                         [xn, yn, vn]]
                example:
                    waypoints[2][1]: 
                    returns the 3rd waypoint's y position

                    waypoints[5]:
                    returns [x5, y5, v5] (6th waypoint)
            ego_state: ego state vector for the vehicle, in the global frame.
                format: [ego_x, ego_y, ego_yaw, ego_open_loop_speed]
                    ego_x and ego_y     : position (m)
                    ego_yaw             : top-down orientation [-pi to pi]
                    ego_open_loop_speed : open loop speed (m/s)
        returns:
            goal_state_set: Set of goal states (offsetted laterally from one
                another) to be used by the local planner to plan multiple
                proposal paths. This goal state set is in the vehicle frame.
                format: [[x0, y0, t0, v0],
                         [x1, y1, t1, v1],
                         ...
                         [xm, ym, tm, vm]]
                , where m is the total number of goal states
                  [x, y, t] are the position and yaw values at each goal
                  v is the goal speed at the goal point.
                  all units are in m, m/s and radians
        """
        # Compute the final heading based on the next index.
        # If the goal index is the last in the set of waypoints, use
        # the previous index instead.
        # To do this, compute the delta_x and delta_y values between
        # consecutive waypoints, then use the np.arctan2() function.
        # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
        # ------------------------------------------------------------------
        if goal_index != len(waypoints) - 1:
            delta_x = waypoints[goal_index+1][0] - waypoints[goal_index][0]
            delta_y = waypoints[goal_index+1][1] - waypoints[goal_index][1]
            heading = np.arctan2(delta_y, delta_x)
        else: 
            delta_x = waypoints[goal_index][0] - waypoints[goal_index-1][0]
            delta_y = waypoints[goal_index][1] - waypoints[goal_index-1][1]
            heading = np.arctan2(delta_y, delta_x)
        # ------------------------------------------------------------------
        # Compute the center goal state in the local frame using 
        # the ego state. The following code will transform the input
        # goal state to the ego vehicle's local frame.
        # The goal state will be of the form (x, y, t, v).
        goal_state_local = copy.copy(goal_state)

        # Translate so the ego state is at the origin in the new frame.
        # This is done by subtracting the ego_state from the goal_state_local.
        # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
        # ------------------------------------------------------------------
        goal_state_local[0] -= ego_state[0]
        goal_state_local[1] -= ego_state[1]
        # ------------------------------------------------------------------

        # Rotate such that the ego state has zero heading in the new frame.
        # Recall that the general rotation matrix is [cos(theta) -sin(theta)
        #                                             sin(theta)  cos(theta)]
        # and that we are rotating by -ego_state[2] to ensure the ego vehicle's
        # current yaw corresponds to theta = 0 in the new local frame.
        # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
        # ------------------------------------------------------------------
        goal_x = goal_state_local[0] * np.cos(ego_state[2]) + goal_state_local[1] * np.sin(ego_state[2])
        goal_y = goal_state_local[0] * -np.sin(ego_state[2]) + goal_state_local[1] * np.cos(ego_state[2])
        # ------------------------------------------------------------------

        # Compute the goal yaw in the local frame by subtracting off the 
        # current ego yaw from the heading variable.
        # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
        # ------------------------------------------------------------------
        goal_t = heading - ego_state[2]
        # ------------------------------------------------------------------

        # Velocity is preserved after the transformation.
        goal_v = goal_state[2]

        # Keep the goal heading within [-pi, pi] so the optimizer behaves well.
        if goal_t > pi:
            goal_t -= 2*pi
        elif goal_t < -pi:
            goal_t += 2*pi

        # Compute and apply the offset for each path such that
        # all of the paths have the same heading of the goal state, 
        # but are laterally offset with respect to the goal heading.
        goal_state_set = []
        for i in range(self._num_paths):
            # Compute offsets that span the number of paths set for the local
            # planner. Each offset goal will be used to generate a potential
            # path to be considered by the local planner.
            offset = (i - self._num_paths // 2) * self._path_offset

            # Compute the projection of the lateral offset along the x
            # and y axis. To do this, multiply the offset by cos(goal_theta + pi/2)
            # and sin(goal_theta + pi/2), respectively.
            # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
            # ------------------------------------------------------------------
            x_offset = offset * np.cos(goal_t + pi/2)
            y_offset = offset * np.sin(goal_t + pi/2)
            # ------------------------------------------------------------------

            goal_state_set.append([goal_x + x_offset, 
                                   goal_y + y_offset, 
                                   goal_t, 
                                   goal_v])
           
        return goal_state_set  
              
    # Plans the path set using polynomial spiral optimization to
    # each of the goal states.
    def plan_paths(self, goal_state_set):
        """Plans the path set using the polynomial spiral optimization.

        Plans the path set using polynomial spiral optimization to each of the
        goal states.

        args:
            goal_state_set: Set of goal states (offsetted laterally from one
                another) to be used by the local planner to plan multiple
                proposal paths. These goals are with respect to the vehicle
                frame.
                format: [[x0, y0, t0, v0],
                         [x1, y1, t1, v1],
                         ...
                         [xm, ym, tm, vm]]
                , where m is the total number of goal states
                  [x, y, t] are the position and yaw values at each goal
                  v is the goal speed at the goal point.
                  all units are in m, m/s and radians
        returns:
            paths: A list of optimized spiral paths which satisfies the set of 
                goal states. A path is a list of points of the following format:
                    [x_points, y_points, t_points]:
                        x_points: List of x values (m) along the spiral
                        y_points: List of y values (m) along the spiral
                        t_points: List of yaw values (rad) along the spiral
                    Example of accessing the ith path, jth point's t value:
                        paths[i][2][j]
                Note that this path is in the vehicle frame, since the
                optimize_spiral function assumes this to be the case.
            path_validity: List of booleans classifying whether a path is valid
                (true) or not (false) for the local planner to traverse. Each ith
                path_validity corresponds to the ith path in the path list.
        """
        paths         = []
        path_validity = []
        for goal_state in goal_state_set:
            path = self._path_optimizer.optimize_spiral(goal_state[0], 
                                                        goal_state[1], 
                                                        goal_state[2])
            if np.linalg.norm([path[0][-1] - goal_state[0], 
                               path[1][-1] - goal_state[1], 
                               path[2][-1] - goal_state[2]]) > 0.1:
                path_validity.append(False)
            else:
                paths.append(path)
                path_validity.append(True)
        return paths, path_validity

def transform_paths(paths, ego_state):
    """ Converts the to the global coordinate frame.

    Converts the paths from the local (vehicle) coordinate frame to the
    global coordinate frame.

    args:
        paths: A list of paths in the local (vehicle) frame.  
            A path is a list of points of the following format:
                [x_points, y_points, t_points]:
                    , x_points: List of x values (m)
                    , y_points: List of y values (m)
                    , t_points: List of yaw values (rad)
                Example of accessing the ith path, jth point's t value:
                    paths[i][2][j]
        ego_state: ego state vector for the vehicle, in the global frame.
            format: [ego_x, ego_y, ego_yaw, ego_open_loop_speed]
                ego_x and ego_y     : position (m)
                ego_yaw             : top-down orientation [-pi to pi]
                ego_open_loop_speed : open loop speed (m/s)
    returns:
        transformed_paths: A list of transformed paths in the global frame.  
            A path is a list of points of the following format:
                [x_points, y_points, t_points]:
                    , x_points: List of x values (m)
                    , y_points: List of y values (m)
                    , t_points: List of yaw values (rad)
                Example of accessing the ith transformed path, jth point's 
                y value:
                    paths[i][1][j]
    """
    transformed_paths = []
    for path in paths:
        x_transformed = []
        y_transformed = []
        t_transformed = []

        for i in range(len(path[0])):
            x_transformed.append(ego_state[0] + path[0][i]*cos(ego_state[2]) - \
                                                path[1][i]*sin(ego_state[2]))
            y_transformed.append(ego_state[1] + path[0][i]*sin(ego_state[2]) + \
                                                path[1][i]*cos(ego_state[2]))
            t_transformed.append(path[2][i] + ego_state[2])

        transformed_paths.append([x_transformed, y_transformed, t_transformed])

    return transformed_paths
