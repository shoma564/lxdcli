#!/usr/bin/env python3

#pip install paramiko
#pip install scp

import re, subprocess, sys, time, pylxd, paramiko, os, sys, subprocess, glob, scp



def workerfunc(masterip, masteruser, masterpass, workerhost, workerip, workeruser, workerpass):
    print(">>>>> workerfunc")
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(masterip, username=masteruser, password=masterpass, timeout=5.0)
    command = "lxc cluster add " + str(workerhost)
    stdin, stdout, stderr = client.exec_command(command, timeout=5)
    for com in stdout:
        print(com, end='')
    com = com.replace("\n", "")


    with paramiko.SSHClient() as sshc:
        sshc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshc.connect(hostname=workerip, port=22, username=workeruser, password=workerpass)
        with scp.SCPClient(sshc.get_transport()) as scpc:
            scpc.put("lxdconfig-worker", "/root/")
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(workerip, username=workeruser, password=workerpass, timeout=5.0)
    command = "sed -e \"s#token_here#" + str(com) + "#g\" -i /root/lxdconfig-worker"
    print(command)
    stdin, stdout, stderr = client.exec_command(command, timeout=5)
    for com in stdout:
        print(com, end='')

    command = "cat /root/lxdconfig-worker | lxd init"
    print(command)
    stdin, stdout, stderr = client.exec_command(command, timeout=5)
    for com in stdout:
        print(com, end='')


    



def masterfunc(masterip, masteruser, masterpass):
    print(">>>>> masterfunc")
    with paramiko.SSHClient() as sshc:
        sshc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshc.connect(hostname=masterip, port=22, username=masteruser, password=masterpass)

        # SCPによるput処理
        with scp.SCPClient(sshc.get_transport()) as scpc:
            scpc.put("lxdconfig-master", "/root/")
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        client.connect(masterip, username=masteruser, password=masterpass, timeout=5.0)
        command = "cat /root/lxdconfig-master | lxd init"
        stdin, stdout, stderr = client.exec_command(command, timeout=5)
        for com in stdout:
            print(com, end='')
    





def splitline():
    mastercount = 0

    with open('lxdclusterfile') as f:
        for line in f:
            linesplit = line.split()
            print(linesplit[0])
            print(linesplit[1])
            print(linesplit[2])
            print(linesplit[3])
            
            if mastercount > 0:
                workerfunc(master_ip, master_user, master_pass, linesplit[0], linesplit[1], linesplit[2], linesplit[3])

            elif mastercount == 0:
                
                master_host = linesplit[0]
                master_ip = linesplit[1]
                master_user = linesplit[2]
                master_pass = linesplit[3]

                masterfunc(master_ip, master_user, master_pass)
                mastercount = mastercount + 1







args = sys.argv

p = 0
number = 0

if len(args) < 2:
    print("\nUsage: lxdcli COMMAND\n\n")
    print("Common Commands:")
    print("  build    build a lxdfile")
    print("  copy     copy containers")
    print("  delete   delete containers")
    print("  reset    delete all containers")
    print("  cluster  create a cluster")
    print("\n\n\n")
    sys.exit()

if args[1] == "cluster":
    splitline()




if args[1] == "reset":
    command = "lxc delete --force $(lxc list --format csv -c \"n\")" 
    print(">>>>>>>> " + str(command) + "\n\n")
    process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
    print(process)
    command = "lxc image delete $(lxc image list --format csv -c \"l\")"
    print(">>>>>>>> " + str(command) + "\n\n")
    process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
    print(process)


if args[1] == "delete":
    if len(args) < 3:
        print("\n削除するコンテナ名を指定してください")
        sys.exit()

        containername = "your_container_name_here"  # Replace with the actual container name
    elif len(args) < 4:
        print("\n削除するコンテナ数を指定してください")
        sys.exit()
    
    containername = args[2]

    number = args[3]
    number = int(number)
    if number > 0:
        for k in range(number):
            command = "lxc delete " + str(containername) + "-" + str(k) + " --force"
            print(">>>>>>>> " + str(command) + "\n\n")
            process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
            print(process)

            time.sleep(3)

        command = "lxc list"
        process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
        print(process)


if args[1] == "copy":
    if len(args) < 3:
        print("\nコピーするコンテナ名を指定してください")
        sys.exit()

        containername = "your_container_name_here"  # Replace with the actual container name
    elif len(args) < 4:
        print("\nコピーするコンテナ数を指定してください")
        sys.exit()
    
    containername = args[2]

    number = args[3]
    number = int(number)
    if number > 0:
        for k in range(number):
            command = "lxc stop " + str(containername)
            print(">>>>>>>> " + str(command) + "\n\n")
            process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
            print(process)
            command = "lxc copy " + str(containername) + " " + str(containername) + "-" + str(k)
            print(">>>>>>>> " + str(command) + "\n\n")
            process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
            print(process)
            command = "lxc start " + str(containername) + "-" + str(k)
            print(">>>>>>>> " + str(command) + "\n\n")
            process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
            print(process)

            time.sleep(2)

        command = "lxc start " + str(containername)
        print(">>>>>>>> " + str(command) + "\n\n")
        process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
        print(process)
        command = "lxc list"
        process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
        print(process)



elif args[1] == "build":
    if len(args) < 3:
        print("\nlxdfileを指定してください\n\n")
        sys.exit()

    i = 0
    with open(args[2], 'r') as file:
        for line in file:
            match = re.match(r'(\S+)\s+(.*)', line)
            if match:
                first_word = match.group(1)
                if first_word == "CONTAINERNAME":
                    i = i + 1
                else:
                    pass
    if i == 0:
        print("ERROR: please define containername\n\n")
        sys.exit()

    u = 0
    with open(args[2], 'r') as file:
        for line in file:
            match = re.match(r'(\S+)\s+(.*)', line)
            if match:
                first_word = match.group(1)
                if first_word == "NUMBER":
                    u = u + 1
                else:
                    pass
    if u == 0:
        number = 0



    containername = ""  # Initialize containername
    with open(args[2], 'r') as file:
        for line in file:
            time.sleep(1)
            match = re.match(r'(\S+)\s+(.*)', line)
            if match:
                first_word = match.group(1)
                remaining_words = match.group(2)
                if first_word == "CONTAINERNAME":
                    containername = remaining_words
                elif first_word == "NUMBER":
                    number = remaining_words

                elif first_word == "FROM":
                    command = "lxc launch images:" + str(remaining_words) + " " + str(containername)
                    command2 = "lxc start " + str(containername)
                    print(">>>>>>>> " + str(command) + "\n\n")
                    process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
                    print(process)

                    print(">>>>>>>> " + str(command2) + "\n\n")
                    process = (subprocess.Popen(command2, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
                    print(process)

                    time.sleep(1)

                elif first_word == "RUN":
                    remaining_words = remaining_words.replace('"', '\\"')

                    command = "lxc exec " + str(containername) + " -- bash -c \"" + str(remaining_words) + " && echo \"done\"\""
                    print(">>>>>>>> " + str(command) + "\n\n")
                    process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
                    print(process)

                elif first_word == "ADD":
                    words = line.split()
                    if words:
                        command = "lxc file push " + words[1] + " " + str(containername) + "/" + words[2]
                        print(">>>>>>>> " + str(command) + "\n\n")
                        process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
                        print(process)
                
                elif first_word == "ADDR":
                    words = line.split()
                    if words:
                        command = "lxc file pull " + str(containername) + "/" + words[2] + " " + words[1]
                        print(">>>>>>>> " + str(command) + "\n\n")
                        process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
                        print(process)

                
                elif first_word == "PORT":
                    client = pylxd.Client()
                    container_name = containername
                    container = client.containers.get(container_name)
                    eth0_ip = container.state().network['eth0']['addresses'][0]['address']

                    words = line.split()
                    print(words)
                    if len(words) == 5:
                        hostip = words[1]
                        hostport = words[2]
                        conport = words[3]
                        proxyname = words[4]
                        conip = eth0_ip

                        command = "lxc config device add " + " " + str(containername) + " " + str(proxyname) + " proxy listen=tcp:" + str(hostip) + ":" + str(hostport) + " connect=tcp:" + str(conip) + ":" + str(conport)+ " bind=host"
                        print(">>>>>>>> " + str(command) + "\n\n")
                        process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
                        print(process)
                        if number == 0:
                            p = 0
                        else:
                            p = 1


    number = int(number)
    if number > 0:
        for k in range(number):
            j = k + 1
            containername2 = str(containername) + "-" + str(k)

            command = "lxc stop " + str(containername)
            print(">>>>>>>> " + str(command) + "\n\n")
            process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
            print(process)

            command = "lxc copy " + str(containername) + " " + str(containername2)
            print(">>>>>>>> " + str(command) + "\n\n")
            process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
            print(process)

            command = "lxc start " + str(containername2)
            print(">>>>>>>> " + str(command) + "\n\n")
            process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
            print(process)

            if p == 1:
                hostport = int(hostport)
                hostport = hostport + j
                print(hostport)
                command = "lxc config device remove " + str(containername2) + " " +str(proxyname)
                print(">>>>>>>> " + str(command) + "\n\n")
                process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
                print(process)
                
                command = "lxc config device add " + " " + str(containername2) + " " + str(proxyname) + "-" + str(k) + " proxy listen=tcp:" + str(hostip) + ":" + str(hostport) + " connect=tcp:" + str(conip) + ":" + str(conport)+ " bind=host"
                print(">>>>>>>> " + str(command) + "\n\n")
                process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
                print(process)

                command = "lxc start " + str(containername2)
                print(">>>>>>>> " + str(command) + "\n\n")
                process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
                print(process)

            time.sleep(2)

        command = "lxc start " + str(containername)
        print(">>>>>>>> " + str(command) + "\n\n")
        process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
        print(process)


    command = "lxc list"
    process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
    print(process)
