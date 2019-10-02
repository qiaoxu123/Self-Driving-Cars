import os

import numpy as np
import cv2

from matplotlib import pyplot as plt


class DatasetHandler:

    def __init__(self):
        # Define number of frames
        self.num_frames = 3

        # Set up paths
        root_dir_path = os.path.dirname(os.path.realpath(__file__))
        self.image_dir = os.path.join(root_dir_path, 'data/rgb')
        self.depth_dir = os.path.join(root_dir_path, 'data/depth')
        self.segmentation_dir = os.path.join(
            root_dir_path, 'data/segmentation')

        # Set up initial iterator value
        self.current_frame = 0

        # Set up data holders
        self.image = None
        self.depth = None
        self.segmentation = None
        self.object_detection = None
        self.lane_midpoint = None

        self.k = np.array([[640, 0, 640],
                           [0, 640, 480],
                           [0, 0, 1]])

        # Define segmentation Colormap
        self.colour_mappings = {
            'None': (0, 0, 0),  # Black
            'Buildings': (255, 0, 0),  # Red
            'Fences': (0, 0, 0),  # Black
            'Other': (0, 0, 0),  # Black
            'Pedestrians': (0, 255, 255),  # Green
            'Poles': (255, 255, 255),  # White
            'RoadLines': (255, 0, 255),  # Purple
            'Roads': (0, 0, 255),  # Blue
            'Sidewalks': (255, 255, 0),  # Yellow
            'Vegetation': (0, 0, 0),  # Black
            'Vehicles': (0, 255, 0),  # Teal
            'Walls': (0, 0, 0)  # black
        }

        # Read first frame
        self.read_frame()

    def _read_image(self):
        im_name = self.image_dir + '/' + str(self.current_frame) + '.png'
        self.image = cv2.imread(im_name)[:, :, ::-1]

    def _read_depth(self):
        depth_name = self.depth_dir + '/' + str(self.current_frame) + '.dat'
        depth = np.loadtxt(
            depth_name,
            delimiter=',',
            dtype=np.float64) * 1000.0
        self.depth = depth

    def _read_segmentation(self):
        seg_name = self.segmentation_dir + '/' + \
            str(self.current_frame) + '.dat'
        self.segmentation = np.loadtxt(seg_name, delimiter=',')

    def _read_object_detection(self):
        object_dicts = {0: np.array([['Car', 20.0, 406.0, 260 + 20.0, 193 + 406.0, 0.99],
                                     ['Car', 150.0, 406.0, 260 + 150.0, 193 + 406.0, 0.95],
                                     ['Car', 800.0, 400.0, 800 + 260.0, 400 + 200.0, 0.76]]),
                        1: np.array([['Pedestrian', 900.0, 350.0, 900.0 + 100, 350.0 + 250, 0.74],
                                     ['Car', 180.0, 390.0, 180.0 + 290, 390.0 + 210, 0.68],
                                     ['Car', 620.0, 438.0, 620.0 + 140, 438.0 + 120, 0.98],
                                     ['Car', 650.0, 476.0, 655.0 + 140, 476.0 + 120, 0.98]]),
                        2: np.array([['Cyclist', 140.0, 450.0, 130.0 + 180.0, 450.0 + 250.0, 0.89],
                                     ['Car', 615.0, 471.0, 615.0 + 63.0, 471.0 + 41.0, 0.56]])}

        self.object_detection = object_dicts[self.current_frame]

    def _read_lane_midpoint(self):
        midpoint_dict = {0: np.array([800, 900]),
                         1: np.array([800, 900]),
                         2: np.array([700, 900])}

        self.lane_midpoint = midpoint_dict[self.current_frame]

    def read_frame(self):
        self._read_image()
        self._read_depth()
        self._read_segmentation()
        self._read_object_detection()
        self._read_lane_midpoint()

    def get_next(self):
        self.current_frame += 1

        if self.current_frame > self.num_frames - 1:
            self.current_frame = self.num_frames - 1
            return False
        else:
            self.read_frame()
            return True

    def get_previous(self):
        self.current_frame -= 1

        if self.current_frame < 0:
            self.current_frame = 0
            return False
        else:
            self.read_frame()
            return True

    def set_frame(self, frame_number):
        self.current_frame = frame_number
        if self.current_frame > 2:
            self.current_frame = 2
            self.read_frame()
        elif self.current_frame < 0:
            self.current_frame = 0
            self.read_frame()
        else:
            self.read_frame()

    def vis_segmentation(self, segmented_image):
        colored_segmentation = np.zeros(self.image.shape)

        colored_segmentation[segmented_image ==
                             1] = self.colour_mappings['Buildings']
        colored_segmentation[segmented_image ==
                             4] = self.colour_mappings['Pedestrians']
        colored_segmentation[segmented_image ==
                             5] = self.colour_mappings['Poles']
        colored_segmentation[segmented_image ==
                             6] = self.colour_mappings['RoadLines']
        colored_segmentation[segmented_image ==
                             7] = self.colour_mappings['Roads']
        colored_segmentation[segmented_image ==
                             8] = self.colour_mappings['Sidewalks']
        colored_segmentation[segmented_image ==
                             10] = self.colour_mappings['Vehicles']

        return colored_segmentation.astype(np.uint8)

    def vis_object_detection(self, objects):

        colour_scheme = {'Car': (255, 255, 102),
                         'Cyclist': (102, 255, 255),
                         'Pedestrian': (255, 102, 255),
                         'Background': (0, 0, 255)}

        image_out = self.image[:]

        for obj in objects:
            category = obj[0]
            bounding_box = np.asfarray(obj[1:5]).astype(int)

            image_out = cv2.rectangle(image_out.astype(np.uint8),
                                      (bounding_box[0], bounding_box[1]),
                                      (bounding_box[2], bounding_box[3]),
                                      colour_scheme[category],
                                      4)
        return image_out

    def vis_lanes(self, lane_lines):
        image_out = self.image
        for line in lane_lines:
            x1, y1, x2, y2 = line.astype(int)

            image_out = cv2.line(
                image_out.astype(
                    np.uint8), (x1, y1), (x2, y2), (255, 0, 255), 7)

        return image_out

    def plot_free_space(self, segmentation):
        depth = self.depth

        sz = depth.shape
        f = self.k[0, 0]
        c_u = self.k[0, 2]

        # Generate a grid of coordinates corresponding to the shape of the depth
        # map
        u, v = np.meshgrid(np.arange(1, sz[1] + 1, 1),
                           np.arange(1, sz[0] + 1, 1))

        # Compute x and y coordinates
        xx = ((u - c_u) * depth) / f

        xx = xx * 10 + 200
        xx = np.maximum(0, np.minimum(xx, 399))

        depth = depth * 10
        depth[depth > 300] = np.nan

        occ_grid = np.full([301, 401], 0.5)

        for x, z, seg in zip(xx.flatten('C'), depth.flatten('C'),
                             segmentation.flatten('C')):
            if not(seg == 1):
                if not np.isnan(x) and not np.isnan(z):
                    x = int(x)
                    z = int(z)
                    occ_grid[z, x] = 1

        for x, z, seg in zip(xx.flatten('C'), depth.flatten('C'),
                             segmentation.flatten('C')):
            if seg == 1:
                if not np.isnan(x) and not np.isnan(z):
                    x = int(x)
                    z = int(z)
                    if not occ_grid[z, x] == 1:
                        occ_grid[z, x] = 0

        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.imshow(occ_grid, cmap='Greys')

        labels = ax.get_xticks()
        labels = [str((label - 200) / 10.0) for label in labels]
        ax.set_xticklabels(labels)

        labels = ax.get_yticks()
        labels = [str(label / 10.0) for label in labels]
        ax.set_yticklabels(labels)

        ax.invert_yaxis()
        plt.show()


def compute_plane(xyz):
    """
    Computes plane coefficients a,b,c,d of the plane in the form ax+by+cz+d = 0

    Arguments:
    xyz -- tensor of dimension (3, N), contains points needed to fit plane.
    k -- tensor of dimension (3x3), the intrinsic camera matrix

    Returns:
    p -- tensor of dimension (1, 4) containing the plane parameters a,b,c,d
    """
    ctr = xyz.mean(axis=1)
    normalized = xyz - ctr[:, np.newaxis]
    M = np.dot(normalized, normalized.T)

    p = np.linalg.svd(M)[0][:, -1]
    d = np.matmul(p, ctr)

    p = np.append(p, -d)

    # Correct plane
    # p = [0.0, 1.0, 0.0, -1.5]
    return p


def dist_to_plane(plane, x, y, z):
    """
    Computes distance between points provided by their x, and y, z coordinates
    and a plane in the form ax+by+cz+d = 0

    Arguments:
    plane -- tensor of dimension (4,1), containing the plane parameters [a,b,c,d]
    x -- tensor of dimension (Nx1), containing the x coordinates of the points
    y -- tensor of dimension (Nx1), containing the y coordinates of the points
    z -- tensor of dimension (Nx1), containing the z coordinates of the points

    Returns:
    distance -- tensor of dimension (N, 1) containing the distance between points and the plane
    """
    a, b, c, d = plane

    return (a * x + b * y + c * z + d) / np.sqrt(a**2 + b**2 + c**2)


def get_slope_intecept(lines):
    slopes = (lines[:, 3] - lines[:, 1]) / (lines[:, 2] - lines[:, 0] + 0.001)
    intercepts = ((lines[:, 3] + lines[:, 1]) - slopes * (
        lines[:, 2] + lines[:, 0])) / 2
    return slopes, intercepts


def extrapolate_lines(lines, y_min, y_max):
    slopes, intercepts = get_slope_intecept(lines)

    new_lines = []

    for slope, intercept, in zip(slopes, intercepts):
        x1 = (y_min - intercept) / slope
        x2 = (y_max - intercept) / slope
        new_lines.append([x1, y_min, x2, y_max])

    return np.array(new_lines)


def find_closest_lines(lines, point):
    x0, y0 = point
    distances = []
    for line in lines:
        x1, y1, x2, y2 = line
        distances.append(((x2 - x1) * (y1 - y0) - (x1 - x0) *
                          (y2 - y1)) / (np.sqrt((y2 - y1)**2 + (x2 - x1)**2)))

    distances = np.abs(np.array(distances))
    sorted = distances.argsort()

    return lines[sorted[0:2], :]
