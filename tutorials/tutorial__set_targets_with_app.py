import os, sys

from flowcontrol.crownetcontrol.setup.entrypoints import get_controller_from_args
from flowcontrol.crownetcontrol.setup.vadere import get_scenario_content
from flowcontrol.crownetcontrol.state.state_listener import VadereDefaultStateListener
from flowcontrol.strategy.controller.dummy_controller import Controller
from flowcontrol.crownetcontrol.traci import constants_vadere as tc
from flowcontrol.utils.misc import get_scenario_file

import json


class CorridorChoiceExample(Controller):
    def __init__(self):
        super().__init__()
        self.time_step = 0
        self.time_step_interval = 0.4

    def handle_sim_step(self, sim_time, sim_state):

        if sim_time <= 7.0:
            p1 = [0.0, 1.0]
            print("Use target [3]")
        else:
            p1 = [1.0, 0.0]
            print("Use target [2]")

        command = {"targetIds": [2, 3], "probability": p1}
        action = {
            "time": sim_time + 0.4,
            "space": {"x": 0.0, "y": 0.0, "radius": 100},
            "command": command,
        }
        action = json.dumps(action)

        print(f"CorridorChoiceExample: {sim_time} apply control action ")
        self.con_manager.domains.v_sim.send_control(message=action, model="RouteChoice")

        self.time_step += self.time_step_interval
        self.con_manager.next_call_at(self.time_step)

    def handle_init(self, sim_time, sim_state):
        print("CorridorChoiceExample: handle_init")
        self.con_manager.next_call_at(0.0)
        print(sim_state)


if __name__ == "__main__":

    if len(sys.argv) == 1:
        settings = [
            "--port",
            "9999",
            "--host-name",
            "localhost",
            "--client-mode",
            "--start-server",
            "--gui-mode",
            "--output-dir",
            os.path.splitext(os.path.basename(__file__))[0],
            "--download-jar-file",  # remove this if you prefer to build vadere locally
        ]
    else:
        settings = sys.argv[1:]

    # Tutorial 2:

    # Scenario: there are two targets.
    # Control action: change the agents' targets over time using a navigation app.
    # Communication channel: navigation app (no delay, information arrives immediately)
    # Reaction behavior: none (all agents react immediately)

    # Take-away from this tutorial
    # - learn how to disseminate information using a navigation app

    # Before you start:
    # Make sure that the system variable VADERE_PATH=/path/to/vadere-repo/ is defined (e.g. add it to your configuration).

    sub = VadereDefaultStateListener.with_vars(
        "persons",
        {"pos": tc.VAR_POSITION, "speed": tc.VAR_SPEED, "angle": tc.VAR_ANGLE},
        init_sub=True,
    )

    controller = CorridorChoiceExample()

    controller = get_controller_from_args(
        working_dir=os.getcwd(), args=settings, controller=controller
    )

    kwargs = {"file_name": get_scenario_file("scenarios/test001.scenario")}
    controller.register_state_listener("default", sub, set_default=True)
    controller.start_controller(**kwargs)
