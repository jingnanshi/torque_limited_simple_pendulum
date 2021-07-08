# Other imports
from stable_baselines import SAC
import numpy as np
import yaml
import os
from pathlib import Path

# Set path for local imports
import site
site.addsitedir('../..')

# Local imports
from controllers.abstract_controller import AbstractClosedLoopController

# default parameters, can be changed
model_path = os.path.join(Path(__file__).parents[4], 'data/models/sac_model.zip')
params_path = os.path.join(Path(__file__).parents[4],
                           'data/parameters/sp_parameters_sac.yaml')


class SacController(AbstractClosedLoopController):
    def __init__(self, model_path=model_path):

        self.model = SAC.load(model_path)
        self.params = None

    def get_params(self, params_path=params_path):
        with open(params_path, 'r') as fle:
            params = yaml.safe_load(fle)
            self.params = params
        return params

    def get_control_output(self, meas_pos, meas_vel, meas_tau, meas_time=0):

        observation = np.squeeze(np.array([meas_pos, meas_vel]))
        des_tau, _states = self.model.predict(observation)
        des_tau *= float(self.params['torque_limit'])
        
        # since this is a pure torque controller, set pos_des and vel_des to None
        des_pos = None
        des_vel = None
        
        return des_pos, des_vel, des_tau

#    def return_all(self):
#        return SacController()
