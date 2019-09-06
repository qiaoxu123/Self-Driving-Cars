import os

import math
import numpy as np
import cv2 as cv

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D


class DatasetHandler:

    def __init__(self):
        # Define number of frames
        self.num_frames = 52

        # Set up paths
        root_dir_path = os.path.dirname(os.path.realpath(__file__))
        self.image_dir = os.path.join(root_dir_path, 'data/rgb')
        self.depth_dir = os.path.join(root_dir_path, 'data/depth')

        # Set up data holders
        self.images = []
        self.images_rgb = []
        self.depth_maps = []

        self.k = np.array([[640, 0, 640],
                           [0, 480, 480],
                           [0,   0,   1]], dtype=np.float32)
        

        # Read first frame
        self.read_frame()
        print("\r" + ' '*20 + "\r", end='')
        
    def read_frame(self):
        self._read_depth()
        self._read_image()
              
    def _read_image(self):
        for i in range(1, self.num_frames + 1):
            zeroes = "0" * (5 - len(str(i)))
            im_name = "{0}/frame_{1}{2}.png".format(self.image_dir, zeroes, str(i))
            self.images.append(cv.imread(im_name, flags=0))
            self.images_rgb.append(cv.imread(im_name)[:, :, ::-1])
            print ("Data loading: {0}%".format(int((i + self.num_frames) / (self.num_frames * 2 - 1) * 100)), end="\r")
            
       
    def _read_depth(self):
        for i in range(1, self.num_frames + 1):
            zeroes = "0" * (5 - len(str(i)))
            depth_name = "{0}/frame_{1}{2}.dat".format(self.depth_dir, zeroes, str(i))
            depth = np.loadtxt(
                depth_name,
                delimiter=',',
                dtype=np.float64) * 1000.0
            self.depth_maps.append(depth)
            print ("Data loading: {0}%".format(int(i / (self.num_frames * 2 - 1) * 100)), end="\r")
            
        
def visualize_camera_movement(image1, image1_points, image2, image2_points, is_show_img_after_move=False):
    image1 = image1.copy()
    image2 = image2.copy()
    
    for i in range(0, len(image1_points)):
        # Coordinates of a point on t frame
        p1 = (int(image1_points[i][0]), int(image1_points[i][1]))
        # Coordinates of the same point on t+1 frame
        p2 = (int(image2_points[i][0]), int(image2_points[i][1]))

        cv.circle(image1, p1, 5, (0, 255, 0), 1)
        cv.arrowedLine(image1, p1, p2, (0, 255, 0), 1)
        cv.circle(image1, p2, 5, (255, 0, 0), 1)

        if is_show_img_after_move:
            cv.circle(image2, p2, 5, (255, 0, 0), 1)
    
    if is_show_img_after_move: 
        return image2
    else:
        return image1


def visualize_trajectory(trajectory):
    # Unpack X Y Z each trajectory point
    locX = []
    locY = []
    locZ = []
    # This values are required for keeping equal scale on each plot.
    # matplotlib equal axis may be somewhat confusing in some situations because of its various scale on
    # different axis on multiple plots
    max = -math.inf
    min = math.inf

    # Needed for better visualisation
    maxY = -math.inf
    minY = math.inf

    for i in range(0, trajectory.shape[1]):
        current_pos = trajectory[:, i]
        
        locX.append(current_pos.item(0))
        locY.append(current_pos.item(1))
        locZ.append(current_pos.item(2))
        if np.amax(current_pos) > max:
            max = np.amax(current_pos)
        if np.amin(current_pos) < min:
            min = np.amin(current_pos)

        if current_pos.item(1) > maxY:
            maxY = current_pos.item(1)
        if current_pos.item(1) < minY:
            minY = current_pos.item(1)

    auxY_line = locY[0] + locY[-1]
    if max > 0 and min > 0:
        minY = auxY_line - (max - min) / 2
        maxY = auxY_line + (max - min) / 2
    elif max < 0 and min < 0:
        minY = auxY_line + (min - max) / 2
        maxY = auxY_line - (min - max) / 2
    else:
        minY = auxY_line - (max - min) / 2
        maxY = auxY_line + (max - min) / 2

    # Set styles
    mpl.rc("figure", facecolor="white")
    plt.style.use("seaborn-whitegrid")

    # Plot the figure
    fig = plt.figure(figsize=(8, 6), dpi=100)
    gspec = gridspec.GridSpec(3, 3)
    ZY_plt = plt.subplot(gspec[0, 1:])
    YX_plt = plt.subplot(gspec[1:, 0])
    traj_main_plt = plt.subplot(gspec[1:, 1:])
    D3_plt = plt.subplot(gspec[0, 0], projection='3d')

    # Actual trajectory plotting ZX
    toffset = 1.06
    traj_main_plt.set_title("Autonomous vehicle trajectory (Z, X)", y=toffset)
    traj_main_plt.set_title("Trajectory (Z, X)", y=1)
    traj_main_plt.plot(locZ, locX, ".-", label="Trajectory", zorder=1, linewidth=1, markersize=4)
    traj_main_plt.set_xlabel("Z")
    # traj_main_plt.axes.yaxis.set_ticklabels([])
    # Plot reference lines
    traj_main_plt.plot([locZ[0], locZ[-1]], [locX[0], locX[-1]], "--", label="Auxiliary line", zorder=0, linewidth=1)
    # Plot camera initial location
    traj_main_plt.scatter([0], [0], s=8, c="red", label="Start location", zorder=2)
    traj_main_plt.set_xlim([min, max])
    traj_main_plt.set_ylim([min, max])
    traj_main_plt.legend(loc=1, title="Legend", borderaxespad=0., fontsize="medium", frameon=True)

    # Plot ZY
    # ZY_plt.set_title("Z Y", y=toffset)
    ZY_plt.set_ylabel("Y", labelpad=-4)
    ZY_plt.axes.xaxis.set_ticklabels([])
    ZY_plt.plot(locZ, locY, ".-", linewidth=1, markersize=4, zorder=0)
    ZY_plt.plot([locZ[0], locZ[-1]], [(locY[0] + locY[-1]) / 2, (locY[0] + locY[-1]) / 2], "--", linewidth=1, zorder=1)
    ZY_plt.scatter([0], [0], s=8, c="red", label="Start location", zorder=2)
    ZY_plt.set_xlim([min, max])
    ZY_plt.set_ylim([minY, maxY])

    # Plot YX
    # YX_plt.set_title("Y X", y=toffset)
    YX_plt.set_ylabel("X")
    YX_plt.set_xlabel("Y")
    YX_plt.plot(locY, locX, ".-", linewidth=1, markersize=4, zorder=0)
    YX_plt.plot([(locY[0] + locY[-1]) / 2, (locY[0] + locY[-1]) / 2], [locX[0], locX[-1]], "--", linewidth=1, zorder=1)
    YX_plt.scatter([0], [0], s=8, c="red", label="Start location", zorder=2)
    YX_plt.set_xlim([minY, maxY])
    YX_plt.set_ylim([min, max])

    # Plot 3D
    D3_plt.set_title("3D trajectory", y=toffset)
    D3_plt.plot3D(locX, locZ, locY, zorder=0)
    D3_plt.scatter(0, 0, 0, s=8, c="red", zorder=1)
    D3_plt.set_xlim3d(min, max)
    D3_plt.set_ylim3d(min, max)
    D3_plt.set_zlim3d(min, max)
    D3_plt.tick_params(direction='out', pad=-2)
    D3_plt.set_xlabel("X", labelpad=0)
    D3_plt.set_ylabel("Z", labelpad=0)
    D3_plt.set_zlabel("Y", labelpad=-2)
    
    # plt.axis('equal')
    D3_plt.view_init(45, azim=30)
    plt.tight_layout()
    plt.show()