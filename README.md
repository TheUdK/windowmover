# windowmover

## Config

The CSV is used for configuring the windows that should be moved.

```csv
TeamSpeak,-2537,-147,1020,768
Friends List,-342,-149,334,1401
```

The CVS is constructed as follows
Windowname,xpos,ypos,width,height

The config file is expected to be in the same directory as the exe or script and should be named `config.csv`.

To find the names and positions of windows use the GUIPropView.exe developed by nirsoft <https://www.nirsoft.net/utils/gui_prop_view.html>

The GUIPropView.exe hash can be viewed at <https://www.nirsoft.net/hash_check/?software=guipropview> or redownloaded from nirsoft directly.


## Run

The script can be run directly with python after installing the requirements

`pip install -r requirements.txt`

## Build

The script is written to be built out as an .exe. This can be done using `pyinstaller` with the provided `windowmover.spec`

`pyinstaller --clean windowmover.spec`
