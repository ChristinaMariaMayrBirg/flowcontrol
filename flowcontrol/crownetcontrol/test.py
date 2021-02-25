from flowcontrol.crownetcontrol.traci.connection import Client, Controller, ClientModeConnection
from flowcontrol.crownetcontrol.traci.VadereMiscAPI import VadereMiscAPI
from flowcontrol.crownetcontrol.traci.VaderePersonAPI import VaderePersonAPI
from flowcontrol.crownetcontrol.traci import VadereConstants as tc
import logging


def server_test():
    controller = Controller.build_client_mode()
    s: ClientModeConnection = controller.connection
    s.domains.v_person.subscribe(objectID="-1", varIDs=[tc.VAR_ID_LIST, ])
    sub_result = s._simulation_step(2.0)
    controller.start_controller()


if __name__ == "__main__":
    # main()
    logging.getLogger().setLevel(logging.INFO)
    server_test()
