import argparse
import sys
import logging
import json
import more_itertools
import yaml
import os
import shutil

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
    source_filter = lambda cell: cell["cell_type"] == "code"

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

    with open(f"{tool_dir}/config.ai", 'r') as file:
        tool_config = yaml.safe_load(file)

    logging.info(f"Generate deploy scripts for tool {tool_config['tool']['name']} (version {tool_config['tool']['version']}) into {target_dir}")

    toolbox_support_lib_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..')
    logging.debug(f"Toolbox support library dir: {toolbox_support_lib_dir}")

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
        os.makedirs(os.path.join(target_dir,'service','src'), mode = 0o777, exist_ok = False)

        generate_source(os.path.join(tool_dir,nb_path),os.path.join(target_dir,'service','src'))
        shutil.copy(os.path.join(toolbox_support_lib_dir,'artifacts','main.py'), os.path.join(target_dir,'service','src'))

    #await fs.copyFile(path.resolve(aitoolbox_dir,"artifacts","main.py"), path.resolve(target_dir,'service','src','main.py'))



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(
                    prog='aitutil.py',
                    description='AI Toolbox Support Library CMD Utils',
                    epilog='')
    
    parser.add_argument('command', help="The command to use. One of ['gensrc','deploy']")           # positional argument
    parser.add_argument('etc', metavar='args', nargs='+', help="Arguments to command, see 'command'")
    parser.add_argument('-o', '--output',type=str,help='Output directory')  # on/off flag
    
    args = parser.parse_args()

    match args.command:
        case "gensrc":
            generate_source(args.etc[0], args.output)
        case "deploy":
            deploy_tool_rest(args.etc[0], args.output)