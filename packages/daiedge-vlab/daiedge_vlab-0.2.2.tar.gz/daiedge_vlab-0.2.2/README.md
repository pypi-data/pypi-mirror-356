# dAIEdge VLab 
The [dAIEdge VLab](https://vlab.daiedge.eu/) is a benchmarking platform for edge AI devices. It allows users to run benchmarks on various edge devices and retrieve the results.

## Prerequisites
- An account on the dAIEdge VLab platform. You can create an account [here](https://vlab.daiedge.eu/register).
- Python 3.9 or higher 

## Setup 

Create a file `.yaml` in the root directory of the project and add the following content to it : 

```yaml
api:
    url: "vlab.daiedge.eu"
    port: "443"

user : 
    email: "your-email"
    password: "your-password"
    
```

## Use dAIEdgeVlabAPI

Give the `.yaml` file path to the `dAIEdgeVlabAPI` constructor.  The `dAIEdgeVlabAPI` object will try to log in to the API using the credentials provided in the `.yaml` file immediately after the object is created. 

```python
from daiedge_vlab import dAIEdgeVlabAPI

SETUP_FILE = "setup.yaml"

TARGET = 'rpi5'
RUNTIME = 'tflite'
MODEL = 'models/small_model.tflite'

if __name__ == '__main__':

    api = dAIEdgeVlabAPI(SETUP_FILE)
    r = api.startBenchmark(TARGET, RUNTIME, MODEL)

    result = api.waitBenchmarkResult(r['id'])
    
    print(result)
```
