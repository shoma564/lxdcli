## 目的
コンテナにおけるメリットの一つは可搬性である。LXDはVMよりは軽量ではあるがDockerコンテナ程軽量ではない。そのため、可搬性が失われつつある。
そこで、Dokcerの様にどこでも同じ様にビルドが出来れば可搬性が上がるのではないかと考えた。

## 配置場所
本コードはgithubにも配置している

https://github.com/shoma564/lxdcli

## インストール方法
```
git clone https://github.com/shoma564/lxdcli.git
cd lxdcli
cp lxdcli /usr/local/sbin/
```


## 使い方
lxdcliには3つの命令文がある。
```bash
$ lxdcli

Usage: lxdcli COMMAND


Common Commands:
  build    build a lxdfile
  copy     copy containers
  delete   delete containers
```

### build
buildはlxdfileに基づいて、lxdコンテナを作成する。また、引数にlxdfileを指定しなければならない。

```bash
root@shoma:/home/shoma/lxdcli/sample # lxdcli build

lxdfileを指定してください


root@shoma:/home/shoma/lxdcli/sample # lxdcli build ./lxdfile
>>>>>>>> lxc launch images:ubuntu/23.10 ubuntu-lamp


Error: Failed instance creation: Failed creating instance record: Add instance info to the database: This "instances" entry already exists
Creating ubuntu-lamp

>>>>>>>> lxc start ubuntu-lamp


Error: The instance is already running
```

### copy
copyは既に存在するLXDコンテナを複数個コピーする。引数には、コンテナ名と、コンテナの数を指定する必要がある。

```bash
root@shoma:/home/shoma/lxdcli/sample # lxdcli copy

コピーするコンテナ名を指定してください
root@shoma:/home/shoma/lxdcli/sample # lxdcli copy ubuntu-lamp

コピーするコンテナ数を指定してください
root@shoma:/home/shoma/lxdcli/sample # lxdcli copy ubuntu-lamp 2
>>>>>>>> lxc copy ubuntu-lamp ubuntu-lamp-0
```

```bash
root@shoma:/home/shoma/lxdcli/sample # lxc list
+---------------+---------+------------------------------+-----------------------------------------------+-----------+-----------+
|     NAME      |  STATE  |             IPV4             |                     IPV6                      |   TYPE    | SNAPSHOTS |
+---------------+---------+------------------------------+-----------------------------------------------+-----------+-----------+
| alma-lamp     | RUNNING | 10.107.73.31 (eth0)          | fd42:d70a:2761:a81b:216:3eff:fee3:7476 (eth0) | CONTAINER | 2         |
+---------------+---------+------------------------------+-----------------------------------------------+-----------+-----------+
| ubuntu-lamp   | RUNNING | 172.19.0.1 (br-1b82b9c5b955) | fd42:d70a:2761:a81b:216:3eff:fe9d:ab36 (eth0) | CONTAINER | 0         |
|               |         | 172.17.0.1 (docker0)         |                                               |           |           |
|               |         | 10.107.73.158 (eth0)         |                                               |           |           |
+---------------+---------+------------------------------+-----------------------------------------------+-----------+-----------+
| ubuntu-lamp-0 | RUNNING | 172.19.0.1 (br-1b82b9c5b955) | fd42:d70a:2761:a81b:216:3eff:fe6e:a670 (eth0) | CONTAINER | 0         |
|               |         | 172.17.0.1 (docker0)         |                                               |           |           |
|               |         | 10.107.73.112 (eth0)         |                                               |           |           |
+---------------+---------+------------------------------+-----------------------------------------------+-----------+-----------+
| ubuntu-lamp-1 | RUNNING | 172.19.0.1 (br-1b82b9c5b955) | fd42:d70a:2761:a81b:216:3eff:fe28:393a (eth0) | CONTAINER | 0         |
|               |         | 172.17.0.1 (docker0)         |                                               |           |           |
|               |         | 10.107.73.79 (eth0)          |                                               |           |           |
+---------------+---------+------------------------------+-----------------------------------------------+-----------+-----------+
```

### delete
deleteは主にcopyで生成されたコンテナを削除するのに使用する。引数にコンテナ名とコンテナの数を指定する必要がある。
```bash
root@shoma:/home/shoma/lxdcli/sample # lxdcli delete

削除するコンテナ名を指定してください
root@shoma:/home/shoma/lxdcli/sample # lxdcli delete ubuntu-lamp

削除するコンテナ数を指定してください
root@shoma:/home/shoma/lxdcli/sample # lxdcli delete ubuntu-lamp 3
>>>>>>>> lxc delete ubuntu-lamp-0 --force
```
```bash
+-------------+---------+------------------------------+-----------------------------------------------+-----------+-----------+
|    NAME     |  STATE  |             IPV4             |                     IPV6                      |   TYPE    | SNAPSHOTS |
+-------------+---------+------------------------------+-----------------------------------------------+-----------+-----------+
| alma-lamp   | RUNNING | 10.107.73.31 (eth0)          | fd42:d70a:2761:a81b:216:3eff:fee3:7476 (eth0) | CONTAINER | 2         |
+-------------+---------+------------------------------+-----------------------------------------------+-----------+-----------+
| ubuntu-lamp | RUNNING | 172.19.0.1 (br-1b82b9c5b955) | fd42:d70a:2761:a81b:216:3eff:fe9d:ab36 (eth0) | CONTAINER | 0         |
|             |         | 172.17.0.1 (docker0)         |                                               |           |           |
|             |         | 10.107.73.158 (eth0)         |                                               |           |           |
+-------------+---------+------------------------------+-----------------------------------------------+-----------+-----------+
```


## LXDfileの書き方
命令文は以下の通り

1. CONTAINERNAME：コンテナ名(必須)
1. FROM : コンテナイメージ名(必須)
1. RUN : コンテナ内で実行するコマンド
1. ADD : コンテナにファイルを追加する
1. NUMBER : コンテナ数
1. PORT : コンテナのポートを外部に公開する(ホスト側のIP ホスト側のポート　コンテナポート　proxy名) 




LXDfileには```CONTAINERNAME```が必須の命令文である。また、```CONTAINERNAME```は```FROM```の前に記述をしなければならない。また、```NUMBER```は必須項目ではないが、書く場合は```PORT```の前に配置する必要がある。


例
```bash
CONTAINERNAME ubuntu-lamp
FROM ubuntu/23.10

RUN apt -y update
RUN apt -y install docker.io docker-compose
ADD ./docker-compose.yml /etc/
RUN docker-compose -f /etc/docker-compose.yml up -d
RUN docker ps

NUMBER 2
PORT PORT 192.168.219.40 80 80 proxy-lamp
```
