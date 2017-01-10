#!/usr/bin/python3
import subprocess

# network puis router puis topology
network_stacks = [
    "databases_network",
    "services_network"
]

router_stacks = [
    "databases_router",
    "services_router"
]

topology_stacks = [
    "databases_topology",
    "objects_topology",
    "services_topology"
]

def main():

    # Check if we can deploy
    # TODO

    # For each stack, deploy
    for i in xrange(0, len(network_stacks)):
        result = subprocess.run(["heat", ["stack-create", "--template-file", "./heat/"+network_stacks[i]]], stdout=subprocess.PIPE)
        if result.return_code != 0:
            print("There was a problem while deploying "+network_stacks[i]+".yaml stack\n")
            print("Command output : "+result.stdout)

    # For each stack, deploy
    for i in xrange(0, len(router_stacks)):
        result = subprocess.run(["heat", ["stack-create", "--template-file", "./heat/"+router_stacks[i]]], stdout=subprocess.PIPE)
        if result.return_code != 0:
            print("There was a problem while deploying "+router_stacks[i]+".yaml stack\n")
            print("Command output : "+result.stdout)

    # For each stack, deploy
    for i in xrange(0, len(topology_stacks)):
        result = subprocess.run(["heat", ["stack-create", "--template-file", "./heat/"+topology_stacks[i]]], stdout=subprocess.PIPE)
        if result.return_code != 0:
            print("There was a problem while deploying "+network_stacks[i]+".yaml stack\n")
            print("Command output : "+result.stdout)
        else:
            # Récupérer les IPs des machines dans les outputs

if __name__ == "__main__":
    # execute only if run as a script
    main()
