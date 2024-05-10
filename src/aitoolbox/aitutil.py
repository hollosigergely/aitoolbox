import argparse
import sys
import logging
import json
import more_itertools
import yaml
import os
import shutil
import pkg_resources

def generate_source(ipynb_file, target_dir):
    if ipynb_file is None or target_dir is None:
        logging.error("Provide target directory or notebook file!")
        sys.exit(-1)

    logging.info(f"Generate source for {ipynb_file} into {target_dir}")

    with open(ipynb_file,"r") as f:
        nb = json.load(f)
        
    cells = nb["cells"]
    preamble,rem = more_itertools.before_and_after(lambda cell: cell["cell_type"] != "markdown" or len(cell["source"]) == 0 or cell["source"][0] != "# Setup", cells)
    list(preamble) # consume
    setup_cells,service_cells = more_itertools.before_and_after(lambda cell: cell["cell_type"] != "markdown" or len(cell["source"]) == 0 or cell["source"][0] != "# Service", rem)

    source_mapper = lambda cell: cell["source"]
    source_filter = lambda cell: cell["cell_type"] == "code" and len(cell["source"]) > 0 and not cell["source"][0].startswith("#!skip")

    setup_src = ("".join(lines) for lines in map(source_mapper,filter(source_filter, setup_cells)))
    service_src = ("".join(lines) for lines in map(source_mapper,filter(source_filter, service_cells)))
    
    with open(f"{target_dir}/setup.py", "w") as f:
        for block in setup_src:
            f.write(block)
            f.write("\n\n")

    with open(f"{target_dir}/service.py", "w") as f:
        for block in service_src:
            f.write(block)
            f.write("\n\n")


def deploy_tool_rest(tool_dir, target_dir):
    if tool_dir is None or target_dir is None:
        logging.error("Provide tool directory and target directory!")
        sys.exit(-1)

    if not os.path.exists(os.path.join(tool_dir,'config.ai')):
        logging.error("Tool has no 'config.ai' file!")
        sys.exit(-1)

    with open(os.path.join(tool_dir,'config.ai'), 'r') as file:
        tool_config = yaml.safe_load(file)

    logging.info(f"Generate deploy scripts for tool {tool_config['tool']['name']} (version {tool_config['tool']['version']}) into {target_dir}")

    if tool_config['deploy']['mode'] != "rest_builtin":
        logging.error(f"Unknown deploy mode {tool_config['deploy']['mode']}")
        sys.exit(-1)

    nb_path = tool_config['deploy']['nb_path']
    deploy_dir = tool_config['deploy']['deploy_dir']
    logging.debug(f"np_path: {nb_path}, deploy_dir: {deploy_dir}")

    shutil.rmtree(target_dir,ignore_errors=True)
    os.makedirs(target_dir, mode = 0o777, exist_ok = False)

    shutil.copytree(os.path.join(tool_dir,deploy_dir), target_dir, dirs_exist_ok = True)

    if nb_path is not None:
        service_main_file_path = pkg_resources.resource_filename('aitoolbox', 'artifacts/main.py')
        logging.debug(f"Service main file: {service_main_file_path}")

        os.makedirs(os.path.join(target_dir,'service','src'), mode = 0o777, exist_ok = False)

        generate_source(os.path.join(tool_dir,nb_path),os.path.join(target_dir,'service','src'))
        shutil.copy(service_main_file_path, os.path.join(target_dir,'service','src'))


def run_cmd():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(
                    prog='aitutil.py',
                    description='AI Toolbox Support Library CMD Utils',
                    epilog='')
    
    parser.add_argument('command', help="The command to use. One of ['gensrc','deploy']")           # positional argument
    parser.add_argument('etc', metavar='args', nargs='+', help="Arguments to command, see 'command'")
    parser.add_argument('-o', '--output',type=str,help='Output directory')  # on/off flag
    
    args = parser.parse_args()

    if args.command == "gensrc":
        generate_source(args.etc[0], args.output)
    elif args.command == "deploy":
        deploy_tool_rest(args.etc[0], args.output)
    else:
        logging.error(f'Unknown command: {args.command}')



if __name__ == "__main__":
   run_cmd()