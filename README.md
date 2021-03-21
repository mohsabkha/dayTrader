# dayTrader

## STRAT 1 - ichimoku cloud inidcator strat 1
    closing price ends above the cloud (a combination of two rolling averages)
    cloud must be green 26 periods (the extended average is higher than the destended average)
    conversion line crossed above the base line (these two are also ratio/averages)
    lagging span must be above the cloud
  ### Data Needed:
	  5 minute open
	  5 minute close
	  5 minute high
	  5 minute low
	  5 minute volume weighted average price
		  polygon provides this in one api call

## STRAT 2 - Reversal VWAP + Bollinger Strat
    RSI is above 90 or below 10 at the time of the 5th bar (below the standard deviation)
    At least 5 candlesticks moving in the same direction
    Use open, close, high and low factors to find trend reversal indicators
    When price is above vwap, buyers are in control.
    Look for a crossing point and buy 1-2 periods after that point. 
    Put a take loss at the current VWAP point
   ### Data Needed:
	  5 minute open
	  5 minute close
	  5 minute high
	  5 minute low
	  5 minute volume weighted average price
		polygon provides this in one api call


## Phases

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



### (MAYBE?) Phase 3: (based on volume)
    get correct historic data
    implement FA strat
    make sure websockets work
    make sure you can pull data from websockets
    make sure FA works
