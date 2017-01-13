#!/usr/bin/python2
# coding: utf-8

from subprocess import Popen,PIPE
import json

# The different kinds of stack we have to deploy
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

serveur_dns = None
clients_dns = ""

def interpret_json_for_inventory_file(json_string):

    hosts_file_content = ""
    json_object = json.loads(json_string)
    services = {}
    common_services = ""

    for key, value in json_object.iteritems():
        if "private_ip" in key:
            service_name = key[:key.index("private_ip") - 1]
            ip = json.loads(value)["output_value"]
            services[service_name] = ip
            if "service" in service_name or "web_app" in service_name:
                common_services += ip +"\n"
            
            if "web_app" in service_name:
                global serveur_dns
                serveur_dns = ip

            if "service" in service_name or "database" in service_name:
                global clients_dns
                clients_dns += "\n" + ip

    for service, ip in services.iteritems():
        hosts_file_content += "\n["+service+"]\n"
        hosts_file_content += ""+ip+"\n"

    return common_services, hosts_file_content


def interpret_json_for_etc_hosts_file(json_string):

    hosts_file_content = ""
    json_object = json.loads(json_string)
    services = {}

    for key, value in json_object.iteritems():
        if "private_ip" in key:
            services[key[:key.index("private_ip") - 1]] = json.loads(value)["output_value"]

    for service, ip in services.iteritems():
        hosts_file_content += "\n"+ip+" "+service

    return hosts_file_content


def main():

    # Initializing host file content
    hosts_file = open("./default_ubuntu_hosts_file", 'r').read()
    inventory_file = ""
    common_services = "[common_services]\n"

    # For each network stack, deploy
    for i in xrange(0, len(network_stacks)):
        print "Applying ./heat/"+network_stacks[i]+".yaml template"
        out = Popen(". ./project5-openrc.sh; openstack stack create -t ./heat/"+network_stacks[i]+".yaml --wait "+network_stacks[i], shell=True)
        return_code = out.wait()
        if return_code != 0:
            print("There was a problem while deploying "+network_stacks[i]+".yaml stack\n")
            print("Command output : "+str(return_code))
            exit(-1)

    # For each router stack, deploy
    for i in xrange(0, len(router_stacks)):
        print "Applying ./heat/" + router_stacks[i] + ".yaml template"
        out = Popen(". ./project5-openrc.sh; openstack stack create -t ./heat/" +router_stacks[i] + ".yaml --wait "+router_stacks[i], shell=True)
        return_code = out.wait()
        if return_code != 0:
            print("There was a problem while deploying "+router_stacks[i]+".yaml stack\n")
            print("Command output : "+str(return_code))
            exit(-1)

    # For each topology stack, deploy
    for i in xrange(0, len(topology_stacks)):
        print "Applying ./heat/" + topology_stacks[i] + ".yaml template"
        out = Popen(". ./project5-openrc.sh; openstack stack create -t ./heat/" + topology_stacks[i] + ".yaml --wait "+topology_stacks[i], shell=True)
        return_code = out.wait()
        if return_code != 0:
            print("There was a problem while deploying "+topology_stacks[i]+".yaml stack\n")
            print("Command output : "+str(return_code))
            exit(-1)
        else:
            # Récupérer les IPs des machines dans les outputs de heat
            out = Popen(". ./project5-openrc.sh; openstack stack output show -f json --all "+topology_stacks[i], stdout=PIPE, shell=True)
            return_code = out.wait()
            output = out.communicate()[0]
            hosts_file += interpret_json_for_etc_hosts_file(output)
            common_services_tmp,inventory_file_tmp = interpret_json_for_inventory_file(output)
            common_services += common_services_tmp
            inventory_file += inventory_file_tmp


    # Add commons_services into ansible inventory file
    inventory_file += "\n"+common_services
    inventory_file += "\n[serveur_dns]\n"+serveur_dns
    inventory_file += "\n[client_dns]\n"+clients_dns

    # Write /etc/hosts file
    print "Creating /etc/hosts file"
    f1 = open("./ansible/roles/common/files/hosts", "w+")
    f1.write(hosts_file)
    f1.close()

    # Write ansible playbook
    print "Creating ansible hosts file"
    f2 = open("./ansible/hosts", "w+")
    f2.write(inventory_file)
    f2.close()

    # Remove known_host
    print "Removing previous known_hosts file"
    Popen("rm ~/.ssh/known_hosts", shell=True)

    # Inject the machines into known host
    print "Injecting machine identities into known_hosts file"
    hosts_file_lines = hosts_file.split("\n")

    for line in hosts_file_lines:
        if " " in line and line.count(".") == 3:
            Popen("ssh-keyscan -t rsa " + line + " >> ~/.ssh/known_hosts", shell=True)

    # Launch ansible deployment
    #out = Popen("ansible-playbook -i ./ansible/hosts --private-key ~/.ssh/bastion -u ubuntu  ./ansible/site.yml", shell=True)
    #return_code = out.wait()

    print("Site deployment has been successful !")


if __name__ == "__main__":
    # execute only if run as a script
    main()
