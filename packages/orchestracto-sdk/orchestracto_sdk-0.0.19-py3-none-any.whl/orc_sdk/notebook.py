import argparse
import shlex
import tempfile
import uuid
from collections import OrderedDict, defaultdict

from IPython.core.magic import magics_class, cell_magic, Magics, line_magic

from orc_sdk.processor import process_python_file


@magics_class
class WorkflowMagics(Magics):
    def __init__(self, shell):
        super().__init__(shell)
        self.workflows = defaultdict(OrderedDict)

    @line_magic
    def clear_workflow(self, line):
        parser = argparse.ArgumentParser()
        parser.add_argument("wf_id", nargs="?", default=None)
        args = parser.parse_args(shlex.split(line))

        wf_id = args.wf_id if args.wf_id else "default"
        if wf_id in self.workflows:
            del self.workflows[wf_id]
            print(f"Workflow '{wf_id}' cleared.")
        else:
            print(f"Workflow '{wf_id}' does not exist.")


    @cell_magic
    def register_tasks(self, line, cell):
        parser = argparse.ArgumentParser()
        parser.add_argument("cell_id", nargs="?", default=None)
        parser.add_argument("wf_id", nargs="?", default=None)
        args = parser.parse_args(shlex.split(line))

        cell_id = args.cell_id if args.cell_id else uuid.uuid4().hex
        wf_id = args.wf_id if args.wf_id else "default"

        self.workflows[wf_id][cell_id] = cell

    @cell_magic
    def register_workflow(self, line, cell):
        parser = argparse.ArgumentParser()
        parser.add_argument("cell_id", nargs="?", default=None)
        parser.add_argument("wf_id", nargs="?", default=None)
        parser.add_argument("--debug-docker-build", action="store_true")
        args = parser.parse_args(shlex.split(line))

        cell_id = args.cell_id if args.cell_id else uuid.uuid4().hex
        wf_id = args.wf_id if args.wf_id else "default"

        self.workflows[wf_id][cell_id] = cell

        with tempfile.TemporaryDirectory() as tmp_dir:
            with open(f"{tmp_dir}/workflow.py", "w") as tmp_f:
                for cell in self.workflows[wf_id].values():
                    tmp_f.write(cell)

            process_python_file(
                f"{tmp_dir}/workflow.py",
                docker_builder="wizard",
                debug_docker_build=args.debug_docker_build,
            )


def load_ipython_extension(ipython):
    ipython.register_magics(WorkflowMagics)
