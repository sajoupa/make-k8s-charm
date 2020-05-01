#!/usr/bin/env python3

import argparse
import jinja2
import os
import sys
import yaml


def make_skeleton(application):
    print("Creating skeleton tree ...")
    rootdir = '../{}-k8s-charm'.format(application)
    try:
        print(rootdir)
        os.mkdir(rootdir)
    except FileExistsError:
        print("Target directory already exists, exiting.")
        sys.exit()
    for subdir in 'hooks', 'lib', 'mod', 'src':
        print('{}/{}'.format(rootdir,subdir))
        os.mkdir('{}/{}'.format(rootdir,subdir))

    print("Adding submodules ...")
    os.system("git -C {} init".format(rootdir))
    os.system("git -C {} submodule add https://github.com/johnsca/resource-oci-image mod/resource-oci-image".format(rootdir))
    os.system("git -C {} submodule add https://github.com/canonical/operator mod/operator".format(rootdir))
    print("Generating symlinks ...")
    os.system("ln -s ../src/charm.py {}/hooks/start".format(rootdir))
    os.system("ln -s ../mod/operator/ops {}/lib/ops".format(rootdir))
    os.system("ln -s ../mod/resource-oci-image/oci_image.py {}/lib/oci_image.py".format(rootdir))
    print("Making initial commit.")
    os.system("git -C {} commit -a -m 'initial commit'".format(rootdir))
    print("Done creating skeleton structure for {}".format(rootdir))

def render_templates(config, templates_path):
    templateLoader = jinja2.FileSystemLoader(searchpath=templates_path)
    templateEnv = jinja2.Environment(loader=templateLoader)
    rootdir = '../{}-k8s-charm'.format(config['application'])

    for target in ['charm.py', 'config.yaml', 'metadata.yaml', 'README.md']:
        if target == 'charm.py':
            target_dir = "{}/src".format(rootdir)
        else:
            target_dir = rootdir

        print("Rendering {}/{} ...".format(rootdir, target))
        template = templateEnv.get_template("{}.template".format(target))
        target_file = open("{}/{}".format(target_dir, target), 'x')
        content = template.render(config=config)
        target_file.write(content)
        target_file.close()
        if target == 'charm.py':
            os.system("chmod 755 {}/src/charm.py".format(rootdir))

    print("Committing generated charm ...")
    os.system("cd {} ; git add . ; git commit -a -m 'Automatically generated charm files.'".format(rootdir))


def main():

    parser = argparse.ArgumentParser(
        description="Create a basic k8s charm using the operator framework, from a template.")
    parser.add_argument("-c", "--config-path", help="Config file location.", required=True)
    parser.add_argument("-t", "--templates-path", help="Templates location, e.g. ./templates .", required=True)
    args = parser.parse_args()

    with open(args.config_path, 'rt') as f:
        config = yaml.safe_load(f.read())

    make_skeleton(config['application'])
    render_templates(config, args.templates_path)


if __name__ == "__main__":
    sys.exit(main())
