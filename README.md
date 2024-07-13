# infernet-container-starter
![image](https://github.com/user-attachments/assets/a80164e5-b928-42d8-ac70-7cec0456bbad)

Ritual is a response to these aforementioned problems. Fundamentally, it is envisioned as an open, modular, sovereign execution layer for AI. Ritual brings together a distributed network of nodes with access to compute and model creators, and enables said creators to host their models on these nodes. Users are then able to access any model on this network — whether its an LLM or a classical ML model — with one common API, and the network has additional cryptographic infrastructure that allows for guarantees around computational integrity and privacy.

## Node Prerequisites
![image](https://github.com/user-attachments/assets/152029ec-5891-496b-9872-5f6ff9ab695d)
> - Ubuntu : 24.04
>
> - Wallet with ~$20 Base ETH
>

## Install dependecies
```console
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git jq lz4 build-essential screen

sudo apt update && sudo apt install apt-transport-https ca-certificates curl software-properties-common -y && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" && sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin && sudo apt-get install docker-compose-plugin 
 
 
sudo apt install git-all 
 
 
sudo apt-get remove docker docker-engine docker.io containerd runc 
 
 
sudo apt-get update 
 
sudo apt-get install ca-certificates curl gnupg lsb-release 
 
 
sudo mkdir -m 0755 -p /etc/apt/keyrings 
 
 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg 
 
echo  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null 
 
 
sudo apt-get update 
 
 
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin 
 
sudo docker run hello-world
```
## Source
```console
git clone https://github.com/ritual-net/infernet-container-starter

cd infernet-container-starter
```
![image](https://github.com/user-attachments/assets/8339f3d1-8b3d-44f5-95b4-b3dcbfa633b4)
```console
screen -S ritual
# start
project=hello-world make deploy-container
```
![image](https://github.com/user-attachments/assets/23ba1e99-1684-4ec2-8446-19971edec30d)

Ctrl + A + D

## Activate and register node
Go to https://basescan.org/address/0x8d871ef2826ac9001fb2e33fdd6379b6aabf449c#writeContract

![image](https://github.com/user-attachments/assets/dbbfc781-895c-45be-88b4-01c72c84f1f2)

![image](https://github.com/user-attachments/assets/5f30fcc8-92df-40b5-8fb3-6be39bea328a)

Wait an hour, and activate your node: in the same basescan page, go to ```activateNode``` and click ```Write``` . Ensure that the tx succeeds, and that your node is activated.

## Reconfigure the files
```console
nano ~/infernet-container-starter/deploy/config.json
```
> - change registry_address to 0x3B1554f346DFe5c482Bb4BA31b880c1C18412170
>   
> - change rpc_url to https://base-rpc.publicnode.com (paid RPC from [Alchemy](https://alchemy.com/?r=01848891d474d9fd) is recommended to handle rate limits)
>   
> - change private_key to your wallet's private key (add 0x in front of private key)
```console
nano ~/infernet-container-starter/projects/hello-world/contracts/Makefile
```
> - change sender's address to your wallet's private key (remember to add 0x in front)
> - change RPC_URL to https://base-rpc.publicnode.com (or paid RPC from [Alchemy](https://alchemy.com/?r=01848891d474d9fd))
```console
nano ~/infernet-container-starter/projects/hello-world/contracts/script/Deploy.s.sol
```
> - change registry_address to 0x3B1554f346DFe5c482Bb4BA31b880c1C18412170

## Update Version
```console
cd deploy 

nano docker-compose.yaml
```
Change version from 3 to 1.0.0

![image](https://github.com/user-attachments/assets/8a80e33a-89d8-420c-90ba-84eceff5e38d)

```console
# Be sure to check that you are in the deploy folder

docker compose down
docker compose up -d
```
## Update containers
```console
docker restart anvil-node
docker restart hello-world
docker restart deploy-node-1
docker restart deploy-fluentbit-1
docker restart deploy-redis-1
```

![image](https://github.com/user-attachments/assets/004b84eb-ce4d-4534-b7a4-a61394606cea)

## Install foundry
```console
cd
mkdir foundry
cd foundry
curl -L https://foundry.paradigm.xyz | bash
source ~/.bashrc
foundryup

cd ~/infernet-container-starter/projects/hello-world/contracts
forge install --no-commit foundry-rs/forge-std
forge install --no-commit ritual-net/infernet-sdk
cd ../../../
```
## Deploy contracts
```console
cd infernet-container-starter/
project=hello-world make deploy-contracts
```

![image](https://github.com/user-attachments/assets/12a194e8-7ae1-4a03-b547-e4bc10cdbb89)

Then go to ```CallContract.s.sol``` and change the ```SaysGM``` address to the one you got above:
```console
nano ~/infernet-container-starter/projects/hello-world/contracts/script/CallContract.s.sol
```
call the contract
```console
make call-contract project=hello-world
```
![image](https://github.com/user-attachments/assets/42b40fa4-4e6b-4410-9436-e9b508741ce0)

## Logs
```console
docker ps
```
```console
docker logs <CONTAINER ID>
```
```console
curl localhost:4000/health
```
result
```
status: {healthy}
```
