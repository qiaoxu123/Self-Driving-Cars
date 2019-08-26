import numpy as np
import data.utils as u

PI = 3.14159265359



class Data():
    """
    Data storage class specific to ground truth received from CARLA.
    If it can be initialized
    """

    def __init__(self, t=np.array([None]), p=np.array([None]), r=np.array([None]), v=np.array([None]),
                 w=np.array([None]), a=np.array([None]), alpha=np.array([None]), do_diff = False):
        """
        :param t: Timestamps [s]
        :param p: Position [m]
        :param r: Orientation [rad]
        :param v: Velocity [m/s]
        :param w: Ang. Velocity [rad/s]
        :param a: Acceleration [m/s^2]
        :param alpha: Ang. Acceleration [rad/s^2]
        :param diff: Indicates whether to generate velocities and acc. by differentiating
        """
        self.do_diff = do_diff
        self._p_init = p
        self._r_init = r
        self._v_init = v
        self._w_init = w
        self._a_init = a
        self._alpha_init = alpha

        self._t = t
        self._p = p
        self._r = r
        self._v = v
        self._w = w
        self._a = a
        self._alpha = alpha

    def reset(self):
        """
        Resets all data back to ground truth positions and orientations.
        """
        self._p = self._p_init
        self._r = self._r_init
        self._v = self._v_init
        self._w = self._w_init
        self._a = self._a_init
        self._alpha = self._alpha_init

    @property
    def p(self):
        if self._p.any():
            return self._p
        raise ValueError('No position data available.')

    @p.setter
    def p(self, value):
        self._p = value

    @property
    def r(self):
        if self._r.any():
            return self._r
        raise ValueError('No orientation data available.')

    @r.setter
    def r(self, value):
        self._r = value

    @property
    def v(self):
        if self._v.any():
            return self._v
        elif self.do_diff:
            self._v = np.array(u.diff(self.p, self._t))
            return self._v
        raise ValueError('No velocity data available')


    @v.setter
    def v(self, value):
        self._v = value

    @property
    def a(self):
        if self._a.any():
            return self._a
        elif self.do_diff:
            self._a = np.array(u.diff(self.v, self._t))
            return self._a
        raise ValueError('No acceleration data available')

    @a.setter
    def a(self, value):
        self._a = value

    @property
    def w(self):
        if self._w.any():
            return self._w
        elif self.do_diff:
            self._w = np.array(u.diff(self.r, self._t))
            return self._w
        raise ValueError('No ang. velocity data available')

    @w.setter
    def w(self, value):
        self._w = value

    @property
    def alpha(self):
        if self._alpha.any():
            return self._alpha
        elif self.do_diff:
            self._alpha = np.array(u.diff(self.w, self._t))
            return self._alpha
        raise ValueError('No ang. acceleration data available')

    @alpha.setter
    def alpha(self, value):
        self._alpha = value

    def transform(self,T = np.array([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]]),side = "right"):
        if side == "right":
            p, r = u.transform_data(self.p, self.r, T)
        else:
            p, r = u.transform_data_left(self.p, self.r, T)
        return Data(self._t,p,r,do_diff = True)

    def slice(self, s=0, e=0):
        """" Slice all data from s to e """
        self.p = self.p[s:e]
        self.r = self.r[s:e]
        self.alpha = self.alpha[s:e]
        self.v = self.v[s:e]
        self.w = self.w[s:e]
        self.a = self.a[s:e]

