# Other imports
import numpy as np

# Set path for local imports
import site
site.addsitedir('../..')

# Local imports
from controllers.lqr.lqr import lqr
from controllers.abstract_controller import AbstractClosedLoopController


class LQRController(AbstractClosedLoopController):
    def __init__(self, params):
        self.params = params
        self.m = params["mass"]
        self.len = params["length"]
        self.b = params["damping"]
        self.g = params["gravity"]
        self.torque_limit = params["torque_limit"]

        self.A = np.array([[0, 1],
                           [self.g/self.len, -self.b/self.m/self.len**2.0]])
        self.B = np.array([[0, 0], [0, self.m/self.len**2.0]])
        self.Q = np.diag((10, 1))
        self.R = np.array([[100, 0], [0, 1]])

        self.K, self.S, _ = lqr(self.A, self.B, self.Q, self.R)

    def set_goal(self, x):
        pass

    def get_control_output(self, meas_pos, meas_vel,
                           meas_tau=0, meas_time=0):

        if isinstance(meas_pos, (list, tuple, np.ndarray)):
            pos = meas_pos[0]
        else:
            pos = meas_pos

        if isinstance(meas_vel, (list, tuple, np.ndarray)):
            vel = meas_vel[0]
        else:
            vel = meas_vel

        th = pos + np.pi
        th = (th + np.pi) % (2*np.pi) - np.pi

        y = np.asarray([th, vel])

        u = np.asarray(-self.K.dot(y))[0][1]

        if np.abs(u) > self.torque_limit:
            u = None

        # since this is a pure torque controller,
        # set des_pos and des_pos to None
        des_pos = None
        des_vel = None

        return des_pos, des_vel, u
