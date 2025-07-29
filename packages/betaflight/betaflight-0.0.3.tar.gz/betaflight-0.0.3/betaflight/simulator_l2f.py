import websockets
import l2f
from betaflight import Simulator
import asyncio
import numpy as np
import json
import time
from scipy.spatial.transform import Rotation as R


crazyflie_from_betaflight_motors = [0, 3, 1, 2]

class L2F(Simulator):
    def __init__(self, UI_SERVER="ws://localhost:13337/backend", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UI_SERVER = UI_SERVER
        self.device = l2f.Device()
        self.rng = l2f.Rng()
        self.env = l2f.Environment()
        self.ui = l2f.UI()
        self.params = l2f.Parameters()
        self.state = l2f.State()
        self.next_state = l2f.State()
        l2f.initialize_rng(self.device, self.rng, 0)
        l2f.initialize_environment(self.device, self.env)
        l2f.sample_initial_parameters(self.device, self.env, self.params, self.rng)
        l2f.initial_state(self.device, self.env, self.params, self.state)
        self.previous_time = None
        self.simulation_dts = []
    async def step(self, rpms):
        simulation_dt = time.time() - self.previous_time
        self.previous_time = time.time()
        self.simulation_dts.append(simulation_dt)
        self.simulation_dts = self.simulation_dts[-100:]

        parameters_string = l2f.parameters_to_json(self.device, self.env, self.params)
        parameters = json.loads(parameters_string)
        parameters["integration"]["dt"] = simulation_dt
        l2f.parameters_from_json(self.device, self.env, json.dumps(parameters), self.params)
        
        action = np.array(rpms)[crazyflie_from_betaflight_motors] * 2 - 1
        dts = l2f.step(self.device, self.env, self.params, self.state, action, self.next_state, self.rng)
        acceleration = (self.next_state.linear_velocity - self.state.linear_velocity) / simulation_dt
        r = R.from_quat([*self.state.orientation[1:], self.state.orientation[0]])
        R_wb = r.as_matrix()
        accelerometer = R_wb.T @ (acceleration - np.array([0, 0, -9.81], dtype=np.float64))
        self.state.assign(self.next_state)
        if self.state.position[2] <= -0.05:
            self.state.position[2] = 0
            self.state.linear_velocity[:] = 0
            self.state.orientation = [1, 0, 0, 0]
            self.state.angular_velocity[:] = 0
        state_action_message = l2f.set_state_action_message(self.device, self.env, self.params, self.ui, self.state, action)
        await self.websocket.send(state_action_message)
        print(f"RPMs: {rpms} dt: {np.mean(self.simulation_dts):.4f} s, action: {action[0].tolist()}")
        return self.state.position, self.state.orientation, self.state.linear_velocity, self.state.angular_velocity, accelerometer, 101325

    async def run(self):
        self.websocket = await websockets.connect(self.UI_SERVER)
        handshake = json.loads(await self.websocket.recv(self.UI_SERVER))
        assert(handshake["channel"] == "handshake")
        namespace = handshake["data"]["namespace"]
        self.ui.ns = namespace
        ui_message = l2f.set_ui_message(self.device, self.env, self.ui)
        parameters_message = l2f.set_parameters_message(self.device, self.env, self.params, self.ui)
        await self.websocket.send(ui_message)
        await self.websocket.send(parameters_message)
        self.previous_time = time.time()
        await super().run()