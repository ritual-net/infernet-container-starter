# `GM! 🤠`

In this tutorial we'll make a very simple consumer contract called `SaysGm`.
All this contract does is request compute from our `hello-world` container and
upon receiving a response, it prints everything to the console.

> [!NOTE]
> Run this tutorial in a new directory, the end result of this tutorial will
> be pretty much the same as the [contracts](.) project, so refer to that if
> you get stuck.

## Prerequisites

### Installing foundry

You'll need [foundry](https://book.getfoundry.sh/getting-started/installation) installed.

### Scaffolding a new project

Create a new directory, and run `forge init` in it. This will create a new
project with a `foundry.yaml` file in it.

```bash
mkdir says-gm
cd says-gm
forge init
```

### Installing Infernet sdk

Install our Infernet SDK via forge.

```bash
forge install ritual-net/infernet-sdk
```

### Specifying remappings

Create a new file called `remappings.txt` in the root of your project.

```
forge-std/=lib/forge-std/src
infernet-sdk/=lib/infernet-sdk/src
```

This'll make it easier to import our dependencies. More explanation on
remappings [here](https://book.getfoundry.sh/projects/dependencies?highlight=remappings#remapping-dependencies).

### `SaysGm` contract

Under the `src/` directory, create a new file called `SaysGm.sol` with the following content:

```solidity
// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.13;

import {console2} from "forge-std/console2.sol";
import {CallbackConsumer} from "infernet-sdk/consumer/Callback.sol";

contract SaysGM is CallbackConsumer {
    constructor(address coordinator) CallbackConsumer(coordinator) {}

    function sayGM() public {
        _requestCompute(
            "hello-world",
            bytes("Good morning!"),
            20 gwei,
            1_000_000,
            1
        );
    }

    function _receiveCompute(
        uint32 subscriptionId,
        uint32 interval,
        uint16 redundancy,
        address node,
        bytes calldata input,
        bytes calldata output,
        bytes calldata proof
    ) internal override {
        console2.log("\n\n"
        "_____  _____ _______ _    _         _\n"
        "|  __ \\|_   _|__   __| |  | |  /\\   | |\n"
        "| |__) | | |    | |  | |  | | /  \\  | |\n"
        "|  _  /  | |    | |  | |  | |/ /\\ \\ | |\n"
        "| | \\ \\ _| |_   | |  | |__| / ____ \\| |____\n"
        "|_|  \\_\\_____|  |_|   \\____/_/    \\_\\______|\n\n");


        console2.log("subscription Id", subscriptionId);
        console2.log("interval", interval);
        console2.log("redundancy", redundancy);
        console2.log("node", node);
        console2.log("input:");
        console2.logBytes(input);
        console2.log("output:");
        console2.logBytes(output);
        console2.log("proof:");
        console2.logBytes(proof);
    }
}
```

All this contract does is request compute from our `hello-world` container via the `_requestCompute` function.
An Infernet node will pick up this subscription, execute the compute, and deliver the result to our contract via
the `_receiveCompute` function.

### Adding a Deploy Script

In the `scripts` directory, add a new file called `Deploy.s.sol`:

```solidity

// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.13;

import {Script, console2} from "forge-std/Script.sol";
import {SaysGM} from "../src/SaysGM.sol";

contract Deploy is Script {
    function run() public {
        // Setup wallet
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        // Log address
        address deployerAddress = vm.addr(deployerPrivateKey);
        console2.log("Loaded deployer: ", deployerAddress);

        address coordinator = 0x5FbDB2315678afecb367f032d93F642f64180aa3;
        // Create consumer
        SaysGM saysGm = new SaysGM(coordinator);
        console2.log("Deployed SaysHello: ", address(saysGm));

        // Execute
        vm.stopBroadcast();
        vm.broadcast();
    }
}
```

The coordinator address is the address of the Infernet coordinator. Our
Infernet Anvil Node already has `Coordinator` pre-deployed to that address.

### Adding a Call Script

Create another file under the `script` directory called `CallContract.s.sol`

```solidity
// SPDX-License-Identifier: BSD-3-Clause-Clear
pragma solidity ^0.8.0;

import {Script, console2} from "forge-std/Script.sol";
import {SaysGM} from "../src/SaysGM.sol";

contract CallContract is Script {
    function run() public {
        // Setup wallet
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        SaysGM saysGm = SaysGM(0x663F3ad617193148711d28f5334eE4Ed07016602);

        saysGm.sayGM();

        vm.stopBroadcast();
    }
}

```

### Building the Project

Before building our project, we'll need to add this line to the `foundry.toml` file:

```
via_ir = true
```

So your `foundry.toml` file should look like [this](./foundry.toml). Otherwise the compiler will complain
about stack too deep errors.

Now, let's build our project.

```bash
forge build
```

The project should build successfully.

### Deploying the Contracts

**Deploy Infernet**

To deploy our contracts, and later be able to call and test them, we'll need to deploy infernet, as well as
our `hello-world` container! Refer to [the readme at the root of this project](../../README.md) for instructions on how
to do that.

After deploying an Infernet Node locally, we'll need to run the `Deploy` script.

```bash
PRIVATE_KEY=0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a \
  forge script script/Deploy.s.sol:Deploy --broadcast \
  --rpc-url http://localhost:8545
```

The private key here is anvil's anvil's third default address which contains 10000 ETH.

### Calling the Contract

Similarly, to run our `CallContract.s.sol` script, we'll invoke it with `forge script`:

```bash
PRIVATE_KEY=0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a \
  forge script script/CallContract.s.sol:Deploy --broadcast \
  --rpc-url http://localhost:8545
```

### Using a `Makefile`
To make running these commands easier, we can add them to a `Makefile`. This allows 
us to run `make deploy` and `make call` instead of typing out the full command every time.

Refer to [this project's Makefile](./Makefile) for an example.

### 🎉 Done!

Congratulations! You've successfully created a contract that requests compute from
our `hello-world` container. 
