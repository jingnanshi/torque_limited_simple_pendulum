import unittest
import numpy as np

from simple_pendulum.model.pendulum_plant import PendulumPlant
from simple_pendulum.simulation.simulation import Simulator
from simple_pendulum.controllers.energy_shaping.energy_shaping_controller import EnergyShapingController


class Test(unittest.TestCase):

    epsilon = 0.2

    def test_0_energy_shaping_swingup(self):
        mass = 0.57288
        length = 0.5
        damping = 0.05
        gravity = 9.81
        coulomb_fric = 0.0
        torque_limit = 1.0
        inertia = mass*length*length

        pendulum = PendulumPlant(mass=mass,
                                 length=length,
                                 damping=damping,
                                 gravity=gravity,
                                 coulomb_fric=coulomb_fric,
                                 inertia=inertia,
                                 torque_limit=torque_limit)

        controller = EnergyShapingController(mass, length, damping, gravity)
        controller.set_goal([np.pi, 0])

        sim = Simulator(plant=pendulum)

        dt = 0.01
        t_final = 5.0

        T, X, U = sim.simulate(t0=0.0,
                               x0=[0.01, 0.0],
                               tf=t_final,
                               dt=dt,
                               controller=controller,
                               integrator="runge_kutta")

        self.assertIsInstance(T, list)
        self.assertIsInstance(X, list)
        self.assertIsInstance(U, list)

        swingup_success = True
        if np.abs((X[-1][0] % (2*np.pi)) - np.pi) > self.epsilon:
            if np.abs(X[-1][1]) > self.epsilon:
                swingup_success = False
                print("Energy Shaping Controller did not swing up",
                      "final state: ", X[-1])

        self.assertTrue(swingup_success)
