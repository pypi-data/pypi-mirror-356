## framepack

enter the user menu by (if no py command; use python/python3 instead)
```
py -m framepack
```

### packpack (aka framepack) - inside the code pack (option 2)

all-in-one approach
```
py index.py
```

### portablepack - extra tools inside the full pack (option 1)
- cuda128(+torch270) installer for 50 series gpu/card(s)
- installer.bat (online) and run.bat (offline)
- 1st time launch: installer.bat (pull the model to local storage)
- then run it entirely offline by: run.bat

### run it straight with gguf-connector (optional)

activate backend and frontend by (need ggc command; pip install gguf-connector)
```
ggc f2
```

### reference: [lllyasviel](https://github.com/lllyasviel/FramePack)
![screenshot](https://raw.githubusercontent.com/calcuis/gguf-pack/master/framepack.png)