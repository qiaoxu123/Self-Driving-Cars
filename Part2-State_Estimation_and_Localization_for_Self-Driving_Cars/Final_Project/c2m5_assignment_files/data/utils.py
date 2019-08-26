import numpy as np
from numpy import sin, cos, arctan2, sqrt

def to_rot(r):
    Rx = np.mat([[ 1,         0,           0],
                 [ 0, cos(r[0]), -sin(r[0]) ],
                 [ 0, sin(r[0]),  cos(r[0]) ]])

    Ry = np.mat([[ cos(r[1]), 0,  sin(r[1]) ],
                 [ 0,         1,          0 ],
                 [-sin(r[1]), 0,  cos(r[1]) ]])

    Rz = np.mat([[ cos(r[2]), -sin(r[2]), 0 ],
                 [ sin(r[2]),  cos(r[2]), 0 ],
                 [         0,          0, 1 ]])

    return Rz*Ry*Rx

def to_mat(p, r):
    "Given a position [m] and orientation in RPY [rad], create homogenous transformation matrix"
    R = to_rot(r)

    return np.mat(np.r_[np.c_[R, p], [np.array([0, 0, 0, 1])]])

def from_mat(T):
    "Get position [m] and orientation in RPY [rad] from homogenous transformation matrix"

    p = [T[0,3], T[1,3], T[2,3]]

    r = [arctan2(T[2,1],T[2,2]) , arctan2(-T[2,0],sqrt(T[2,1] ** 2 + T[2,2] ** 2)), arctan2(T[1,0],T[0,0]) ]

    return p, r

def transform_data(p, r, T_frame):
    "Transform gt data to different frame"
    p_new = [0]*len(p)
    r_new = [0]*len(p)

    for i in (range(len(p))):
        T_i = to_mat(p[i, :], r[i, :])
        T_new = T_i.dot(T_frame)
        p_new[i], r_new[i] = from_mat(T_new)

    return np.array(p_new), np.array(r_new)

def transform_data_left(p, r, T_frame):
    "Transform gt data to different frame"
    p_new = [0]*len(p)
    r_new = [0]*len(p)

    for i in (range(len(p))):
        T_i = to_mat(p[i, :], r[i, :])
        T_new = T_frame.dot(T_i)
        p_new[i], r_new[i] = from_mat(T_new)

    return np.array(p_new), np.array(r_new)

def to_own_frame(r,x):
    x_new = np.zeros(x.shape)

    for i in (range(len(x))):
        x_new[i] = x[i].dot(to_rot(r[i]))

    return x_new

def intg(x,t):
    out = [None] * (len(x) + 1)
    for i in range(len(out)):
        dt = t[i + 1] - t[i]
        out[i+1,:] = out[i,:] + x[i,:]*dt

    return out

def diff(x, t):
    out = [None] * (len(x) - 1)
    for i in (range(len(out))):
        dt = t[i + 1] - t[i]
        dx = x[i + 1, :] - x[i, :]
        out[i] = dx / dt

    return out