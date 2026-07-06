# On start

copy `src/etc/config.yml.example` to `src/etc/config.yml` then change this file depending on how you will run the interface (more information below)


# Terminal conversation version

## JASMIN

If running on JASMIN, the config should be fine as is.\
You must be in a sci-ph server to run this\
Simply run the following commands in the same terminal window

```shell
module load jaspy
source setup-env.sh
```

start GPU node and wait until you get resources
```shell
srun --gres=gpu:2 --mem=192000 --partition=orchid --account=orchid --qos=orchid --time=03:00:00 --pty /bin/bash
```

start ollama. This takes a while which is why the sleep is here.
```shell
./run-ollama.sh > ollama.log 2>&1 &
sleep 60
```


Then you can run the LLM interface
```shell
cd src
python main.py
```



---
## Local

When running locally, ollama needs to be running and you need to set the model that you want ollama to use in src/etc/config.yml\
(LOCAL_LLM), you will also need to change the host in Host-type to be "local".

On ollama, make sure the model context in settings is set to at least 32K, this is to avoid the LLM running irrelevant tool calls if it runs out of context length

### mac
```shell
source setup-env.sh
```

### windows
You must have a python version of either 3.12 or 3.13 (it will tell you if you don't)
```shell
. .\setup-env.ps1
```



Then you can run the LLM interface
```shell
cd src
python main.py
```







# UI version

When you get access to the UI page, login with the below credentials (it doesn't matter what username or password you use, as long as it is consistent)\
username = test\
password = test

## JASMIN

**Unfortunately running the UI on JASMIN currently does not work due to a port forwarding issue**

The config should again be fine as is.

start GPU node and wait until you get resources\
then start ollama. This takes a while which is why the sleep is here.
```shell
srun --gres=gpu:2 --mem=192000 --partition=orchid --account=orchid --qos=orchid --time=03:00:00 --pty /bin/bash
sleep 5

./run-ollama.sh > ollama.log 2>&1 &
sleep 60
```
Take note of the GPU host you were sent to (for example the terminal will say)\
`[{username}@gpuhost004 CIRRUS-MOLES-querier]$`

Then you must open a new terminal and SSH into the gpuhost\
`ssh {username}@gpuhost{host_number}`\
then `cd` into the project directory
```shell
module load jaspy
source start-ui.sh --JASMIN
```

After running that, open a third terminal and run this
```shell
ssh -L 8000:localhost:8000 {username}@gpuhost{host_number}
```

Once the three terminals are open and everything has been run, first, try control (or command) clicking the link chainlit gives you (`INFO - chainlit - Your app is available at http://0.0.0.0:8000`)\
If that doesn't work, try go into the PORTS tab in the vs code terminal and press the "open in browser" button in Forwarded Address for port 8000.\
I have personally found this to be very tricky to run.\

---

## local

When running locally, ollama needs to be running and you need to set the model that you want ollama to use in src/etc/config.yml
(LOCAL_LLM), you will also need to change the host to be "local".

On ollama, make sure the model context in settings is set to at least 32K, this is to avoid the LLM running irrelevant tool calls if it runs out of context length

### mac
```shell
source start-ui.sh
```

### Windows
```shell
. .\start-ui.ps1
```

Then visit the UI\
link to UI:
http://127.0.0.1:8000/login
