import os, sys

from flowcontrol.crownetcontrol.setup.entrypoints import get_controller_from_args
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
        self.controlModelName = "RouteChoice1"
        self.controlModelType = "RouteChoice"


    def handle_sim_step(self, sim_time, sim_state):

        if sim_time == 4.0:
            p1 = [0.0, 1.0]
            print("Use target [2]")

            command = {"targetIds": [2, 3], "probability": p1}
            action = {
                "space": {"x": 0.0, "y": 0.0, "radius": 100},
                "commandId": self.commandID,
                "stimulusId": -400,
                "command": command,
            }
            action = json.dumps(action)

            print(f"TikTokController: {sim_time} apply control action ")
            self.con_manager.domains.v_sim.send_control(
                message=action, model=self.controlModelName
            )

            self.commandID += 1

    def handle_init(self, sim_time, sim_state):
        super().handle_init(sim_time, sim_state)
        #TODO remove reaction model from python code and vadere code!
        self.con_manager.domains.v_sim.init_control(
            self.controlModelName, self.controlModelType, json.dumps({})
        )


if __name__ == "__main__":

    if len(sys.argv) == 1:
        settings = [
            "--port",
            "9999",
            "--host-name",
            "localhost",
            "--client-mode",
            #"--start-server",
            #"--gui-mode",
            #"--output-dir",
            #os.path.splitext(os.path.basename(__file__))[0],
            #"--download-jar-file",  # remove this if you prefer to build vadere locally
        ]
    else:
        settings = sys.argv[1:]

    settings.extend(["--scenario-file", get_scenario_file("scenarios/test001.scenario")])

    # Tutorial 3:

    # Scenario: there are two targets.
    # Control action: change the agents' targets over time using a navigation app.
    # Communication channel: navigation app (no delay, information arrives immediately)
    # Reaction behavior: agents react with a probability 50%-100%

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

    controller.register_state_listener("default", sub, set_default=True)
    controller.start_controller()
