# `Hello-World` Consumer Contracts

This is a [foundry](https://book.getfoundry.sh/) project that implements a simple Consumer
contract, [`SaysGm`](./src/SaysGM.sol). 

This readme explains how to compile and deploy the contract to the Infernet Anvil Testnet network. 
For a detailed tutorial on how to write a consumer contract, refer to the [tutorial doc](./Tutorial.md).


> [!IMPORTANT]  
> Ensure that you are running the following scripts with the Infernet Anvil Testnet network. 
> The [tutorial](./../../../README.md) at the root of this repository explains how to
> bring up an infernet node.

### Installing the libraries

```bash
forge install
```

### Compiling the contracts

```bash
forge compile
```

### Deploying the contracts
The deploy script at `script/Deploy.s.sol` deploys the `SaysGM` contract to the Infernet Anvil Testnet network.

We have the [following make target](./Makefile#L9) to deploy the contract. Refer to the Makefile 
for more understanding around the deploy scripts.
```bash
make deploy
```

### Requesting a job
We also have a script called `CallContract.s.sol` that requests a job to the `SaysGM` contract.
Refer to the [script](./script/CallContract.s.sol) for more details. Similar to deployment, 
you can run that script using the following convenience make target.
```bash
make call-contract
```
Refer to the [Makefile](./Makefile#L14) for more details.

