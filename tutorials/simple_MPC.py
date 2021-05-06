import os, sys

from flowcontrol.crownetcontrol.setup.entrypoints import get_controller_from_args
from flowcontrol.crownetcontrol.setup.vadere import get_scenario_content
from flowcontrol.crownetcontrol.state.state_listener import VadereDefaultStateListener
from flowcontrol.crownetcontrol.controller.dummy_controller import Controller
from flowcontrol.crownetcontrol.traci import constants_vadere as tc
from flowcontrol.utils.opp.scenario import get_scenario_file

class PingPong(Controller):

    def __init__(self):
        super().__init__()
        self.control = [
            (0, ["2"]),
            (5.0, ["3"]),
            (10, ["2"]),
            (15, ["3"]),
            (20, ["2"]),
            (25, ["3"]),
            (30, ["2"]),
        ]
        self.count = 0

    def initialize_connection(self, con_manager):
        self.con_manager = con_manager

    def handle_sim_step(self, sim_time, sim_state):
        if self.count >= len(self.control):
            return
        print(f"TikTokController: {sim_time} handle_sim_step evaluate control...")

        with open("scenarios/CorridorChoiceData.json", "r") as myfile:
            json_command = myfile.read()
        print(json_command)

        self.con_manager.domains.v_sim.send_control(message=json_command)


        print(f"TikTokController: {sim_time} apply control action ")
        for ped_id in ["1", "2", "3", "4"]:
            self.con_manager.domains.v_person.set_target_list(
                str(ped_id), self.control[self.count][1]
            )
        # read if listeners are used


        self.con_manager.next_call_at(self.control[self.count][0])
        self.count += 1

    def handle_init(self, sim_time, sim_state):
        print("TikTokController: handle_init")
        self.con_manager.next_call_at(0.0)
        print(sim_state)


if __name__ == "__main__":

    sub = VadereDefaultStateListener.with_vars(
        "persons",
        {"pos": tc.VAR_POSITION, "speed": tc.VAR_SPEED, "angle": tc.VAR_ANGLE},
        init_sub=True,
    )

    controller = PingPong()
    scenario_file = get_scenario_file("scenarios/test001.scenario")

    settings = [
        "--port",
        "9999",
        "--host-name",
        "localhost",
        "--client-mode"
    ]


    traci_manager = get_controller_from_args(working_dir=os.getcwd(), args=settings, controller=controller)

    controller.initialize_connection(traci_manager)
    kwargs = {"file_name": scenario_file, "file_content": get_scenario_content(scenario_file)}
    controller.register_state_listener("default", sub, set_default=True) #? new
    controller.start_controller(**kwargs)
