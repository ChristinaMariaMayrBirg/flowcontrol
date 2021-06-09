import argparse

from flowcontrol.crownetcontrol.setup.vadere import VadereServer
from flowcontrol.crownetcontrol.traci.connection_manager import (
    ServerModeConnection,
    ClientModeConnection,
)

from flowcontrol.strategy.controller.dummy_controller import Controller


def get_controller_from_args(working_dir, args=None, controller=None):

    ns = parse_args_as_dict(args)

    if controller is None:
        print("No controller found.")
        controller = Controller.get(ns["controller_type"])


    if ns["port"] == 9999 and ns["is_in_client_mode"]:

        vadere = VadereServer(is_start_server=ns["start_server"], is_gui_mode=ns["gui_mode"], output_dir = ns["output_dir"])

        traci_manager = ClientModeConnection(
            control_handler=controller, port=ns["port"], host=ns["host_name"], server_thread = vadere.get_server_thread()
        )
    elif ns["port"] == 9997 and not ns["is_in_client_mode"]:  # TODO check port number
        traci_manager = ServerModeConnection(
            control_handler=controller, port=ns["port"], host=ns["host_name"]
        )
    else:
        raise NotImplementedError("Port and host configuration not found.")

    controller.initialize_connection(traci_manager)

    return controller


def parse_args_as_dict(args=None):
    # parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-n",
        "--host-name",
        dest="host_name",
        default="localhost",  # TODO: discuss -> defaults
        required=True,
        help="If vadere is set, the controller is started in client-mode",
    )

    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        default=9999,
        required=True,
        help="Client: 9999, server: 9997?",
        type=int,
    )

    parser.add_argument(
        "--client-mode",
        dest="is_in_client_mode",
        action="store_true",
        default=False,
        required=False,
        help="Additional information.",  # TODO: redundant?
    )

    parser.add_argument(
        "--gui-mode",
        dest="gui_mode",
        action="store_true",
        default=False,
        required=False,
        help="Only available when server is started automatically.",
    )

    parser.add_argument(
        "--start-server",
        dest="start_server",
        action="store_true",
        default=False,
        required=False,
        help="Only available when server is started automatically.",
    )
    parser.add_argument(
        "-c",
        "--controller-type",
        dest="controller_type",
        default="",
        required=False,
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        default="vadere-server-output",
        required=False,
    )

    if args is None:
        ns = vars(parser.parse_args())
    else:
        ns = vars(parser.parse_args(args))

    if ns["start_server"] is True and ns["is_in_client_mode"] is False:
        raise ValueError(
            "Start server option is only available in client-mode. Set --client-mode option."
        )

    if ns["start_server"] is False and ns["gui_mode"] is True:
        raise ValueError(
            "Gui mode is only available if the server is started automatically. Set --start-server option."
        )

    return ns
