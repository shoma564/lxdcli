#!/usr/bin/env python3
import re, subprocess, sys, time, pylxd

args = sys.argv

p = 0
number = 0

if len(args) < 2:
    print("\nUsage: lxdcli COMMAND\n\n")
    print("Common Commands:")
    print("  build    build a lxdfile")
    print("  copy     copy containers")
    print("  delete   delete containers")
    print("\n\n\n")
    sys.exit()

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
            command = "lxc copy " + str(containername) + " " + str(containername) + "-" + str(k)
            print(">>>>>>>> " + str(command) + "\n\n")
            process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
            print(process)
            command = "lxc start " + str(containername) + "-" + str(k)
            print(">>>>>>>> " + str(command) + "\n\n")
            process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
            print(process)

            time.sleep(3)

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
                    command = "lxc exec " + str(containername) + " -- " + str(remaining_words)
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

    time.sleep(3)






    command = "lxc list"
    process = (subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
    print(process)
