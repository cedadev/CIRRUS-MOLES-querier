# On start

copy `src/etc/config.yml.example` to `src/etc/config.yml` then change this file depending on how you will run the interface (more information below)


# Terminal conversation version

## JASMIN

If running on JASMIN, the config should be fine as is.

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

When running locally, ollama needs to be running and you need to set the model that you want ollama to use in src/etc/config.yml
(LOCAL_LLM), you will also need to change the host to be "local".

On ollama, make sure the model context in settings is set to at least 32K, this is to avoid the LLM running irrelevant tool calls if it runs out of context length

### mac
```shell
source setup-env.sh
```

### windows
```shell
. .\setup-env.ps1
```



Then you can run the LLM interface
```shell
cd src
python main.py
```







# UI version

When you get access to the UI page, login with the below credentials (it doesn't matter what you use, as long as it is consistent)
username = test
password = test

## JASMIN

The config should again be fine as is.

start GPU node and wait until you get resources
```shell
srun --gres=gpu:2 --mem=192000 --partition=orchid --account=orchid --qos=orchid --time=03:00:00 --pty /bin/bash
```

start ollama. This takes a while which is why the sleep is here.
```shell
./run-ollama.sh > ollama.log 2>&1 &
sleep 60
```

```shell
module load jaspy
source start-ui.sh
```

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
