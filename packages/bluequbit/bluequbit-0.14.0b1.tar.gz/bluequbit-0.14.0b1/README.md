<!-- EXCLUDE -->
![lint and tests](https://github.com/BlueQubitDev/bluequbit-python-sdk/actions/workflows/lint_and_tests.yml/badge.svg) ![PyPI release status](https://github.com/BlueQubitDev/bluequbit-python-sdk/actions/workflows/release.yml/badge.svg) ![Deploy docs](https://github.com/BlueQubitDev/bluequbit-python-sdk/actions/workflows/deploy_docs.yml/badge.svg)

# Development

To install dev environment run:

```
./scripts/install_dev_env.sh
```

Source created virtual environment:

```
source .venv/bin/activate
```

Run integration tests:

```
export BLUEQUBIT_API_TOKEN=<your_api_token>
export BLUEQUBIT_MAIN_ENDPOINT=https://dev.api.bluequbit.io/v1

tox
```

Run linting and formatting checks:

```
tox -e linters
```



<!-- /EXCLUDE -->
# BlueQubit Python SDK

## Quick Start

1. Register on https://app.bluequbit.io and copy the API token.

2. Install Python SDK from PyPI:
```
    pip install bluequbit
```
3. An example of how to run a Qiskit circuit using the SDK:

```
    import qiskit

    import bluequbit

    bq_client = bluequbit.init("<token>")

    qc_qiskit = qiskit.QuantumCircuit(2)
    qc_qiskit.h(0)
    qc_qiskit.x(1)

    job_result = bq_client.run(qc_qiskit, job_name="testing_1")

    state_vector = job_result.get_statevector() 
    # returns a NumPy array of [0. +0.j 0. +0.j 0.70710677+0.j 0.70710677+0.j]
```

4. An example of how to run a Pennylane circuit:

```
    import pennylane as qml
    from pennylane import numpy as np
    
    dev = qml.device('bluequbit.cpu', wires=1, token="<token>")
    
    @qml.qnode(dev)
    def circuit(angle):
        qml.RY(angle, wires=0)
        return qml.probs(wires=0)
    
    
    probabilities = circuit(np.pi / 4)
    # returns a NumPy array of [0.85355339 0.14644661]
```
To use the Pennylane plugin, you must have `pennylane` version 0.39 or above installed. 

5. This SDK requires Python versions 3.9 or above. But we recommend using Python 3.10 or above.
The package is tested extensively on Python 3.10.

## Full reference

Please find detailed reference at https://app.bluequbit.io/sdk-docs.

## Questions and Issues

Please submit questions and issues to info@bluequbit.io.
