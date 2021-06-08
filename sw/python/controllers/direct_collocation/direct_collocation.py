import numpy as np
import matplotlib.pyplot as plt


from pydrake.solvers.mathematicalprogram import Solve
from pydrake.systems.trajectory_optimization import DirectCollocation
from pydrake.trajectories import PiecewisePolynomial

from pydrake.examples.pendulum import PendulumPlant, PendulumState


class DirectCollocationCalculator():
    def __init__(self):
        self.pendulum_plant = PendulumPlant()
        self.pendulum_context = self.pendulum_plant.CreateDefaultContext()

    def init_pendulum(self, mass=0.57288, length=0.5, damping=0.15,
                      gravity=9.81, torque_limit=2.0):
        self.pendulum_params = self.pendulum_plant.get_mutable_parameters(
                                                        self.pendulum_context)
        self.pendulum_params[0] = mass
        self.pendulum_params[1] = length
        self.pendulum_params[2] = damping
        self.pendulum_params[3] = gravity
        self.torque_limit = torque_limit

    def compute_trajectory(self, N=21, max_dt=0.5, start_state=[0.0, 0.0],
                           goal_state=[np.pi, 0.0], initial_x_trajectory=None):
        dircol = DirectCollocation(self.pendulum_plant,
                                   self.pendulum_context,
                                   num_time_samples=N,
                                   minimum_timestep=0.05,
                                   maximum_timestep=max_dt)

        dircol.AddEqualTimeIntervalsConstraints()

        u = dircol.input()
        dircol.AddConstraintToAllKnotPoints(-self.torque_limit <= u[0])
        dircol.AddConstraintToAllKnotPoints(u[0] <= self.torque_limit)

        initial_state = PendulumState()
        initial_state.set_theta(start_state[0])
        initial_state.set_thetadot(start_state[1])
        dircol.AddBoundingBoxConstraint(initial_state.get_value(),
                                        initial_state.get_value(),
                                        dircol.initial_state())

        final_state = PendulumState()
        final_state.set_theta(goal_state[0])
        final_state.set_thetadot(goal_state[1])
        dircol.AddBoundingBoxConstraint(final_state.get_value(),
                                        final_state.get_value(),
                                        dircol.final_state())

        R = 10.0  # Cost on input "effort".
        dircol.AddRunningCost(R * u[0]**2)

        if initial_x_trajectory is not None:
            dircol.SetInitialTrajectory(PiecewisePolynomial(),
                                        initial_x_trajectory)

        result = Solve(dircol)
        assert result.is_success()

        x_trajectory = dircol.ReconstructStateTrajectory(result)
        return x_trajectory, dircol, result

    def plot_phase_space_trajectory(self, x_trajectory, save_to=None):
        fig, ax = plt.subplots()

        time = np.linspace(x_trajectory.start_time(),
                           x_trajectory.end_time(),
                           100)

        x_knots = np.hstack([x_trajectory.value(t) for t in time])

        ax.plot(x_knots[0, :], x_knots[1, :])
        if save_to is None:
            plt.show()
        else:
            plt.xlim(-np.pi, np.pi)
            plt.ylim(-10, 10)
            plt.savefig(save_to)
        plt.close()

    def extract_trajectory(self, x_trajectory, dircol, result, N=801):
        # Extract Time
        time = np.linspace(x_trajectory.start_time(),
                           x_trajectory.end_time(),
                           N)
        time_traj = time.reshape(N, 1).T[0]

        # Extract State
        theta_theta_dot = np.hstack([x_trajectory.value(t) for t in time])

        theta = theta_theta_dot[0, :].reshape(N, 1).T[0]
        theta_dot = theta_theta_dot[1, :].reshape(N, 1).T[0]

        # Extract Control Inputs
        u_trajectory = dircol.ReconstructInputTrajectory(result)
        torque_traj = np.hstack([u_trajectory.value(t) for t in time])[0]

        return time_traj, theta, theta_dot, torque_traj
