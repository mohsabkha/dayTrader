# day-Trader

# To Run:

Get into the project folder in your terminal
You should see the src folder, the README, and the LICENSE
When you are in this directory in the ternimal, run this commad:

```shell
cd dayTrader/src
export PYTHONPATH="$PWD"
```

set the end date to the previous day. So if you wanna buy at market open on 4/20, then set the end date to 4/19 so it gets the previous days data

This will set your absolute path to be the src folder, and any import statements will be able to use this path to properly import
After this, you will have to install all of the packages that are used.

```
# to install all the packages below run
pip install -r requirements.txt
```

Once the packages are installed, you can run the program from the src directory by running the command in the terminal:

# To deploy to heroku

1. Will need access to the heroku account (gonzalos)
1. run `git push heroku nameOfBranch:master` to deploy a local branch to heroku
   - Heroku only lets you deploy main or master by default. Run `git push heroku master` if it's not in a local branch

##### python main.py

### Phase 1: (based on volume, price, and averages of each)

    get correct historic data
    implement vwap strat
    make sure websockets work
    make sure you can pull data from websockets
    make sure vwap works

### Phase 2: (based on many moving averages and ratios)

    get correct historic data
    implement IC strat
    make sure websockets work
    make sure you can pull data from websockets
    make sure IC works
