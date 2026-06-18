# JASMIN

If running on JASMIN, the config should be fine as is.

run the chmod once
```shell
chmod +x setup-env.sh
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
# Local

When running locally, ollama needs to be running and you need to set the model that you want ollama to use in src/etc/config.yml
(LOCAL_LLM), you will also need to change the host to be "local".

### mac
run the chmod once
```shell
chmod +x setup-env.sh
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