"""
Created on 2026-03-14

@author: wf
"""
import sys

import uvicorn
from basemkit.base_cmd import BaseCmd

import govservice.version as version
from govservice.govservice import GovService


class GovServiceCmd(BaseCmd):
    """
    GOV-Service command line interface
    """

    def __init__(self):
        """
        constructor
        """
        super().__init__(version.Version())

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("--host", default="0.0.0.0", help="host to run the server on")
        parser.add_argument("--port", type=int, default=8000, help="port to run the server on")
        parser.add_argument("-s", "--serve", action="store_true", help="start webserver")

    def handle_args(self, args) -> bool:
        """
        Handle arguments
        """
        if super().handle_args(args):
            return True

        if args.serve:
            if args.debug:
                print("Running in debug mode...")

            service = GovService(debug=args.debug)

            # Extract host/port if specified, else use defaults
            host = getattr(args, "host", "0.0.0.0")
            port = getattr(args, "port", 8000)
            uvicorn.run(service.app, host=host, port=port)
            return True
            
        return False


def main(argv: list | None = None):
    cmd = GovServiceCmd()
    exit_code = cmd.run(argv)
    return exit_code


DEBUG = 0
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-d")
    sys.exit(main())
