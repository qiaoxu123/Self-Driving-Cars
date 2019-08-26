#!/usr/bin/env python3

# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

# Author: Ryan De Iaco
# Additional Comments: Carlos Wang
# Date: November 21, 2018

import numpy as np
import math

# State machine states
FOLLOW_LANE = 0
DECELERATE_TO_STOP = 1
STAY_STOPPED = 2
# Stop speed threshold
STOP_THRESHOLD = 0.02
# Number of cycles before moving from stop sign.
STOP_COUNTS = 10

class BehaviouralPlanner:
    def __init__(self, lookahead, stopsign_fences, lead_vehicle_lookahead):
        self._lookahead                     = lookahead
        self._stopsign_fences               = stopsign_fences
        self._follow_lead_vehicle_lookahead = lead_vehicle_lookahead
        self._state                         = FOLLOW_LANE
        self._follow_lead_vehicle           = False
        self._goal_state                    = [0.0, 0.0, 0.0]
        self._goal_index                    = 0
        self._stop_count                    = 0

    def set_lookahead(self, lookahead):
        self._lookahead = lookahead

    ######################################################
    ######################################################
    # MODULE 7: TRANSITION STATE FUNCTION
    #   Read over the function comments to familiarize yourself with the
    #   arguments and necessary internal variables to set. Then follow the TODOs
    #   and use the surrounding comments as a guide.
    ######################################################
    ######################################################
    # Handles state transitions and computes the goal state.
    def transition_state(self, waypoints, ego_state, closed_loop_speed):
        """Handles state transitions and computes the goal state.  
        
        args:
            waypoints: current waypoints to track (global frame). 
                length and speed in m and m/s.
                (includes speed to track at each x,y location.)
                format: [[x0, y0, v0],
                         [x1, y1, v1],
                         ...
                         [xn, yn, vn]]
                example:
                    waypoints[2][1]: 
                    returns the 3rd waypoint's y position

                    waypoints[5]:
                    returns [x5, y5, v5] (6th waypoint)
            ego_state: ego state vector for the vehicle. (global frame)
                format: [ego_x, ego_y, ego_yaw, ego_open_loop_speed]
                    ego_x and ego_y     : position (m)
                    ego_yaw             : top-down orientation [-pi to pi]
                    ego_open_loop_speed : open loop speed (m/s)
            closed_loop_speed: current (closed-loop) speed for vehicle (m/s)
        variables to set:
            self._goal_index: Goal index for the vehicle to reach
                i.e. waypoints[self._goal_index] gives the goal waypoint
            self._goal_state: Goal state for the vehicle to reach (global frame)
                format: [x_goal, y_goal, v_goal]
            self._state: The current state of the vehicle.
                available states: 
                    FOLLOW_LANE         : Follow the global waypoints (lane).
                    DECELERATE_TO_STOP  : Decelerate to stop.
                    STAY_STOPPED        : Stay stopped.
            self._stop_count: Counter used to count the number of cycles which
                the vehicle was in the STAY_STOPPED state so far.
        useful_constants:
            STOP_THRESHOLD  : Stop speed threshold (m). The vehicle should fully
                              stop when its speed falls within this threshold.
            STOP_COUNTS     : Number of cycles (simulation iterations) 
                              before moving from stop sign.
        """
        # In this state, continue tracking the lane by finding the
        # goal index in the waypoint list that is within the lookahead
        # distance. Then, check to see if the waypoint path intersects
        # with any stop lines. If it does, then ensure that the goal
        # state enforces the car to be stopped before the stop line.
        # You should use the get_closest_index(), get_goal_index(), and
        # check_for_stop_signs() helper functions.
        # Make sure that get_closest_index() and get_goal_index() functions are
        # complete, and examine the check_for_stop_signs() function to
        # understand it.
        if self._state == FOLLOW_LANE:
            print("I am following the lane")
            # First, find the closest index to the ego vehicle.
            # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
            # ------------------------------------------------------------------
            closest_len, closest_index = get_closest_index(waypoints, ego_state)
            # ------------------------------------------------------------------
            # Next, find the goal index that lies within the lookahead distance
            # along the waypoints.
            # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
            # ------------------------------------------------------------------
            goal_index = self.get_goal_index(waypoints, ego_state, closest_len, closest_index)
            # ------------------------------------------------------------------
            # Finally, check the index set between closest_index and goal_index
            # for stop signs, and compute the goal state accordingly.
            # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
            # ------------------------------------------------------------------
            goal_index, stop_sign_found = self.check_for_stop_signs(waypoints, closest_index, goal_index)
            self._goal_index = goal_index
            self._goal_state = waypoints[self._goal_index]
            # ------------------------------------------------------------------

            # If stop sign found, set the goal to zero speed, then transition to 
            # the deceleration state.
            # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
            # ------------------------------------------------------------------
            if stop_sign_found:
                self._goal_state[2] = 0
                self._state = DECELERATE_TO_STOP
            # ------------------------------------------------------------------
            print("stop_sign_found = %d" % stop_sign_found)
            pass

        # In this state, check if we have reached a complete stop. Use the
        # closed loop speed to do so, to ensure we are actually at a complete
        # stop, and compare to STOP_THRESHOLD.  If so, transition to the next
        # state.
        elif self._state == DECELERATE_TO_STOP:
            print("Decelerating to stop")
            # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
            # ------------------------------------------------------------------
            if closed_loop_speed > STOP_THRESHOLD:
                self._state = DECELERATE_TO_STOP
                print("closed_loop_speed = %f" % closed_loop_speed)
                print("The state of car: ")
                print(ego_state)
            else:
                self._state = STAY_STOPPED
                print("Begin to stop ======================================================================================")
            # ------------------------------------------------------------------
            pass

        # In this state, check to see if we have stayed stopped for at
        # least STOP_COUNTS number of cycles. If so, we can now leave
        # the stop sign and transition to the next state.
        elif self._state == STAY_STOPPED:
            print("Staying stopped")
            # We have stayed stopped for the required number of cycles.
            # Allow the ego vehicle to leave the stop sign. Once it has
            # passed the stop sign, return to lane following.
            # You should use the get_closest_index(), get_goal_index(), and 
            # check_for_stop_signs() helper functions.
            if self._stop_count == STOP_COUNTS:
                print("Try to follow the lane")
                # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
                # --------------------------------------------------------------
                closest_len, closest_index = get_closest_index(waypoints, ego_state)
                goal_index = self.get_goal_index(waypoints, ego_state, closest_len, closest_index)
                # --------------------------------------------------------------

                # We've stopped for the required amount of time, so the new goal 
                # index for the stop line is not relevant. Use the goal index
                # that is the lookahead distance away.
                # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
                # --------------------------------------------------------------
                stop_sign_found = self.check_for_stop_signs(waypoints, closest_index, goal_index)[1]
                self._goal_index = goal_index
                self._goal_state = waypoints[self._goal_index]
                # --------------------------------------------------------------

                # If the stop sign is no longer along our path, we can now
                # transition back to our lane following state.
                # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
                # --------------------------------------------------------------
                if not stop_sign_found:
                    self._state = FOLLOW_LANE
                # --------------------------------------------------------------

                pass

            # Otherwise, continue counting.
            else:
                # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
                # --------------------------------------------------------------
                self._stop_count += 1
                # --------------------------------------------------------------

                pass
        else:
            raise ValueError('Invalid state value.')

    ######################################################
    ######################################################
    # MODULE 7: GET GOAL INDEX FOR VEHICLE
    #   Read over the function comments to familiarize yourself with the
    #   arguments and necessary variables to return. Then follow the TODOs
    #   and use the surrounding comments as a guide.
    ######################################################
    ######################################################
    # Gets the goal index in the list of waypoints, based on the lookahead and
    # the current ego state. In particular, find the earliest waypoint that has accumulated
    # arc length (including closest_len) that is greater than or equal to self._lookahead.
    def get_goal_index(self, waypoints, ego_state, closest_len, closest_index):
        """Gets the goal index for the vehicle. 
        
        Set to be the earliest waypoint that has accumulated arc length
        accumulated arc length (including closest_len) that is greater than or
        equal to self._lookahead.

        args:
            waypoints: current waypoints to track. (global frame)
                length and speed in m and m/s.
                (includes speed to track at each x,y location.)
                format: [[x0, y0, v0],
                         [x1, y1, v1],
                         ...
                         [xn, yn, vn]]
                example:
                    waypoints[2][1]: 
                    returns the 3rd waypoint's y position

                    waypoints[5]:
                    returns [x5, y5, v5] (6th waypoint)
            ego_state: ego state vector for the vehicle. (global frame)
                format: [ego_x, ego_y, ego_yaw, ego_open_loop_speed]
                    ego_x and ego_y     : position (m)
                    ego_yaw             : top-down orientation [-pi to pi]
                    ego_open_loop_speed : open loop speed (m/s)
            closest_len: length (m) to the closest waypoint from the vehicle.
            closest_index: index of the waypoint which is closest to the vehicle.
                i.e. waypoints[closest_index] gives the waypoint closest to the vehicle.
        returns:
            wp_index: Goal index for the vehicle to reach
                i.e. waypoints[wp_index] gives the goal waypoint
        """
        # Find the farthest point along the path that is within the
        # lookahead distance of the ego vehicle.
        # Take the distance from the ego vehicle to the closest waypoint into
        # consideration.
        arc_length = closest_len
        wp_index = closest_index
        
        # In this case, reaching the closest waypoint is already far enough for
        # the planner.  No need to check additional waypoints.
        if arc_length > self._lookahead:
            return wp_index

        # We are already at the end of the path.
        if wp_index == len(waypoints) - 1:
            return wp_index

        # Otherwise, find our next waypoint.
        # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
        # ------------------------------------------------------------------
        while wp_index < len(waypoints) - 1:
            # arc_length += math.sqrt(1 + ((waypoints[wp_index+1][1] - waypoints[wp_index][1]) 
            #                     / (waypoints[wp_index+1][0] - waypoints[wp_index][0])) ** 2)
            arc_length += math.sqrt((waypoints[wp_index+1][0] - waypoints[wp_index][0]) ** 2 + (waypoints[wp_index+1][1] - waypoints[wp_index][1]) ** 2)
            if arc_length >= self._lookahead:
                wp_index += 1
                break
            else:
                wp_index += 1
        # ------------------------------------------------------------------
        return wp_index

    # Checks the given segment of the waypoint list to see if it
    # intersects with a stop line. If any index does, return the
    # new goal state accordingly.
    def check_for_stop_signs(self, waypoints, closest_index, goal_index):
        """Checks for a stop sign that is intervening the goal path.

        Checks for a stop sign that is intervening the goal path. Returns a new
        goal index (the current goal index is obstructed by a stop line), and a
        boolean flag indicating if a stop sign obstruction was found.
        
        args:
            waypoints: current waypoints to track. (global frame)
                length and speed in m and m/s.
                (includes speed to track at each x,y location.)
                format: [[x0, y0, v0],
                         [x1, y1, v1],
                         ...
                         [xn, yn, vn]]
                example:
                    waypoints[2][1]: 
                    returns the 3rd waypoint's y position

                    waypoints[5]:
                    returns [x5, y5, v5] (6th waypoint)
                closest_index: index of the waypoint which is closest to the vehicle.
                    i.e. waypoints[closest_index] gives the waypoint closest to the vehicle.
                goal_index (current): Current goal index for the vehicle to reach
                    i.e. waypoints[goal_index] gives the goal waypoint
        variables to set:
            [goal_index (updated), stop_sign_found]: 
                goal_index (updated): Updated goal index for the vehicle to reach
                    i.e. waypoints[goal_index] gives the goal waypoint
                stop_sign_found: Boolean flag for whether a stop sign was found or not
        """
        for i in range(closest_index, goal_index):
            # Check to see if path segment crosses any of the stop lines.
            intersect_flag = False
            for stopsign_fence in self._stopsign_fences:
                wp_1   = np.array(waypoints[i][0:2])
                wp_2   = np.array(waypoints[i+1][0:2])
                s_1    = np.array(stopsign_fence[0:2])
                s_2    = np.array(stopsign_fence[2:4])

                v1     = np.subtract(wp_2, wp_1)
                v2     = np.subtract(s_1, wp_2)
                sign_1 = np.sign(np.cross(v1, v2))
                v2     = np.subtract(s_2, wp_2)
                sign_2 = np.sign(np.cross(v1, v2))

                v1     = np.subtract(s_2, s_1)
                v2     = np.subtract(wp_1, s_2)
                sign_3 = np.sign(np.cross(v1, v2))
                v2     = np.subtract(wp_2, s_2)
                sign_4 = np.sign(np.cross(v1, v2))

                # Check if the line segments intersect.
                if (sign_1 != sign_2) and (sign_3 != sign_4):
                    intersect_flag = True

                # Check if the collinearity cases hold.
                if (sign_1 == 0) and pointOnSegment(wp_1, s_1, wp_2):
                    intersect_flag = True
                if (sign_2 == 0) and pointOnSegment(wp_1, s_2, wp_2):
                    intersect_flag = True
                if (sign_3 == 0) and pointOnSegment(s_1, wp_1, s_2):
                    intersect_flag = True
                if (sign_3 == 0) and pointOnSegment(s_1, wp_2, s_2):
                    intersect_flag = True

                # If there is an intersection with a stop line, update
                # the goal state to stop before the goal line.
                if intersect_flag:
                    goal_index = i
                    return goal_index, True

        return goal_index, False
                
    # Checks to see if we need to modify our velocity profile to accomodate the
    # lead vehicle.
    def check_for_lead_vehicle(self, ego_state, lead_car_position):
        """Checks for lead vehicle within the proximity of the ego car, such
        that the ego car should begin to follow the lead vehicle.

        args:
            ego_state: ego state vector for the vehicle. (global frame)
                format: [ego_x, ego_y, ego_yaw, ego_open_loop_speed]
                    ego_x and ego_y     : position (m)
                    ego_yaw             : top-down orientation [-pi to pi]
                    ego_open_loop_speed : open loop speed (m/s)
            lead_car_position: The [x, y] position of the lead vehicle.
                Lengths are in meters, and it is in the global frame.
        sets:
            self._follow_lead_vehicle: Boolean flag on whether the ego vehicle
                should follow (true) the lead car or not (false).
        """
        # Check lead car position delta vector relative to heading, as well as
        # distance, to determine if car should be followed.
        # Check to see if lead vehicle is within range, and is ahead of us.
        if not self._follow_lead_vehicle:
            # Compute the angle between the normalized vector between the lead vehicle
            # and ego vehicle position with the ego vehicle's heading vector.
            lead_car_delta_vector = [lead_car_position[0] - ego_state[0], 
                                     lead_car_position[1] - ego_state[1]]
            lead_car_distance = np.linalg.norm(lead_car_delta_vector)
            # In this case, the car is too far away.   
            if lead_car_distance > self._follow_lead_vehicle_lookahead:
                return

            lead_car_delta_vector = np.divide(lead_car_delta_vector, 
                                              lead_car_distance)
            ego_heading_vector = [math.cos(ego_state[2]), 
                                  math.sin(ego_state[2])]
            # Check to see if the relative angle between the lead vehicle and the ego
            # vehicle lies within +/- 45 degrees of the ego vehicle's heading.
            if np.dot(lead_car_delta_vector, 
                      ego_heading_vector) < (1 / math.sqrt(2)):
                return

            self._follow_lead_vehicle = True

        else:
            lead_car_delta_vector = [lead_car_position[0] - ego_state[0], 
                                     lead_car_position[1] - ego_state[1]]
            lead_car_distance = np.linalg.norm(lead_car_delta_vector)

            # Add a 15m buffer to prevent oscillations for the distance check.
            if lead_car_distance < self._follow_lead_vehicle_lookahead + 15:
                return
            # Check to see if the lead vehicle is still within the ego vehicle's
            # frame of view.
            lead_car_delta_vector = np.divide(lead_car_delta_vector, lead_car_distance)
            ego_heading_vector = [math.cos(ego_state[2]), math.sin(ego_state[2])]
            if np.dot(lead_car_delta_vector, ego_heading_vector) > (1 / math.sqrt(2)):
                return

            self._follow_lead_vehicle = False


######################################################
######################################################
# MODULE 7: CLOSEST WAYPOINT INDEX TO VEHICLE
#   Read over the function comments to familiarize yourself with the
#   arguments and necessary variables to return. Then follow the TODOs
#   and use the surrounding comments as a guide.
######################################################
######################################################
# Compute the waypoint index that is closest to the ego vehicle, and return
# it as well as the distance from the ego vehicle to that waypoint.
def get_closest_index(waypoints, ego_state):
    """Gets closest index a given list of waypoints to the vehicle position.

    args:
        waypoints: current waypoints to track. (global frame)
            length and speed in m and m/s.
            (includes speed to track at each x,y location.)
            format: [[x0, y0, v0],
                     [x1, y1, v1],
                     ...
                     [xn, yn, vn]]
            example:
                waypoints[2][1]: 
                returns the 3rd waypoint's y position

                waypoints[5]:
                returns [x5, y5, v5] (6th waypoint)
        ego_state: ego state vector for the vehicle. (global frame)
            format: [ego_x, ego_y, ego_yaw, ego_open_loop_speed]
                ego_x and ego_y     : position (m)
                ego_yaw             : top-down orientation [-pi to pi]
                ego_open_loop_speed : open loop speed (m/s)

    returns:
        [closest_len, closest_index]:
            closest_len: length (m) to the closest waypoint from the vehicle.
            closest_index: index of the waypoint which is closest to the vehicle.
                i.e. waypoints[closest_index] gives the waypoint closest to the vehicle.
    """
    closest_len = float('Inf')
    closest_index = 0
    # TODO: INSERT YOUR CODE BETWEEN THE DASHED LINES
    # ------------------------------------------------------------------
    for i in range(len(waypoints)):
      distence = math.sqrt((ego_state[0] - waypoints[i][0]) ** 2 + (ego_state[1] - waypoints[i][1]) ** 2)
      if distence <= closest_len:
          closest_len = distence
          closest_index = i
    # ------------------------------------------------------------------

    return closest_len, closest_index

# Checks if p2 lies on segment p1-p3, if p1, p2, p3 are collinear.        
def pointOnSegment(p1, p2, p3):
    if (p2[0] <= max(p1[0], p3[0]) and (p2[0] >= min(p1[0], p3[0])) and \
       (p2[1] <= max(p1[1], p3[1])) and (p2[1] >= min(p1[1], p3[1]))):
        return True
    else:
        return False
