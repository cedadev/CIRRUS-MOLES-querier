# On start

copy `src/etc/config.yml.example` to `src/etc/config.yml` then change this file depending on how you will run the interface (more information below)



# JASMIN

If running on JASMIN, the config should be fine as is.

run the chmod once
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
# Local

When running locally, ollama needs to be running and you need to set the model that you want ollama to use in src/etc/config.yml
(LOCAL_LLM), you will also need to change the host to be "local".

### mac
run the chmod once
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







# UI

on first creation:
```bash
chainlit create-secret
```
copy the key into a .env file that you will create in `src` (`src/.env`)
it should look something like this
CHAINLIT_AUTH_SECRET="{YOUR_SECRET_KEY}"


```bash
python graphical_interface/init_sqlite_db.py
```




commands to run each time
``` bash
cd src
export PYTHONPATH=$PWD
chainlit run graphical_interface/chainlit_chatbot.py -w
```

link to UI:
http://127.0.0.1:8000/login
