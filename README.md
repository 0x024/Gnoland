# Gnoland
## 本脚本不保留任何数据
## 本脚本主要通过python的方式批量生成Gno链的钱包
### step0:

需要先搭建Gen的环境，

推荐使用Ubuntu 22.04 x64

sudo apt-get update -y && sudo apt-get upgrade -y

sudo apt-get install curl build-essential jq git -y

cd

sudo rm -rf /usr/local/go

curl https://dl.google.com/go/go1.19.2.linux-amd64.tar.gz | sudo tar -C/usr/local -zxvf -

cat <<'EOF' >>$HOME/.profile

export GOROOT=/usr/local/go

export GOPATH=$HOME/go

export GO111MODULE=on

export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin

EOF

source $HOME/.profile

git clone https://github.com/gnolang/gno/

cd gno

make install

最后输入gnokey来确定环境是否搭建完成

### step1:

数据库采用sqllite 通过手动创建的，只有一个Gnoland表，表结构如下

（"bjtime" varchar(256)----北京时间
"name" varchar(256)----钱包名称
"addr" varchar(256)----钱包地址
"pub" varchar(256)----私钥
"key" varchar(256)----助记词
"balance" varchar(256)----余额）
### step2：

`python3 1`进行钱包的创建

`python3 2`进行钱包余额查询
### step3:

1:如需修改创建钱包数量，需修改get_Gnoland()中的count值即可

2: