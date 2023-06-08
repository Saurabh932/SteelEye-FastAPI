import uuid
from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel, Field
import datetime as dt

app = FastAPI()


# Pydantic model representing a single Trade
class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    assetClass: Optional[str] = Field(alias="assetClass", default=None,
                                      description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: Optional[str] = Field(default=None,
                                        description="The counterparty the trade was executed with. May not always be available")
    instrumentId: str = Field(alias="instrumentId",
                              description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrumentName: str = Field(alias="instrumentName", description="The name of the instrument traded.")
    tradeDateTime: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")
    tradeDetails: TradeDetails = Field(alias="tradeDetails",
                                       description="The details of the trade, i.e. price, quantity")
    tradeId: Optional[str] = Field(alias="tradeId", default=None, description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")


# Dummy data to be used in place of a database
trades_db = [
    {
        "id": 1,
        "assetClass": "Equity",
        "counterparty": "Goldman Sachs",
        "instrumentId": "AAPL",
        "instrumentName": "Apple Inc.",
        "tradeDateTime": "2022-04-14T10:00:00",
        "tradeDetails": {
            "buySellIndicator": "BUY",
            "price": 155.0,
            "quantity": 100
        },
        "trader": "John Doe"
    },
    {
        "id": 2,
        "assetClass": "Equity",
        "counterparty": "Bank of America",
        "instrumentId": "AMZN",
        "instrumentName": "Amazon.com Inc.",
        "tradeDateTime": "2022-04-16T13:15:00",
        "tradeDetails": {
            "buySellIndicator": "BUY",
            "price": 3200.0,
            "quantity": 10
        },
        "trader": "David Wilson"
    },

    {
        "id": 3,
        "assetClass": "Equity",
        "counterparty": "Morgan Stanley",
        "instrumentId": "MSFT",
        "instrumentName": "Microsoft Corporation",
        "tradeDateTime": "2022-04-15T09:30:00",
        "tradeDetails": {
            "buySellIndicator": "BUY",
            "price": 250.0,
            "quantity": 200
        },
        "trader": "Alice Smith"
    },
    {
        "id": 4,
        "assetClass": "FX",
        "counterparty": "Citigroup",
        "instrumentId": "EURUSD",
        "instrumentName": "Euro/US Dollar",
        "tradeDateTime": "2022-04-15T14:45:00",
        "tradeDetails": {
            "buySellIndicator": "SELL",
            "price": 1.22,
            "quantity": 5000
        },
        "trader": "Bob Johnson"
    },
    {
        "id": 5,
        "assetClass": "Equity",
        "counterparty": "Bank of America",
        "instrumentId": "AMZN",
        "instrumentName": "Amazon.com Inc.",
        "tradeDateTime": "2022-04-16T13:15:00",
        "tradeDetails": {
            "buySellIndicator": "BUY",
            "price": 3200.0,
            "quantity": 10
        },
        "trader": "David Wilson"
    }
]


@app.get("/")
async def root():
    return {"message": "Welcome to the Trade API"}


@app.get("/pagination")
async def get_trades(
        page_num: int = Query(1, gt=0), # gt --> it ensures that the provided value must be greater than 0.
        page_size: int = Query(2, gt=0),
        sort_by: Optional[str] = Query(None, description="Field to sort the trades by")
):
    # Calculate the start and end indices based on the pagination parameters
    start = (page_num - 1) * page_size
    end = start + page_size

    # Create a copy of the trades database
    sorted_trades = trades_db.copy()

    # Sort the trades if a sort field is provided
    if sort_by:
        try:
            sorted_trades.sort(key=lambda trade: trade[sort_by])
        except KeyError:
            # Raise an HTTPException if the sort field is invalid
            raise HTTPException(status_code=400, detail="Invalid sort field")

    # Return the sorted and paginated trades
    return sorted_trades[start:end]


@app.get("/trades/{trade_id}", response_model=Trade)
async def get_trade_by_id(trade_id: str):
    for trade in trades_db:
        if trade["id"] == int(trade_id):
            return trade
    raise HTTPException(status_code=404, detail="Trade not found")


@app.get("/trades", response_model=List[Trade])
async def filter_trades(
        search_by_keyword: Optional[str] = None,
        asset_class: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        starting_date: Optional[dt.datetime] = None,
        ending_date: Optional[dt.datetime] = None,
        trade_type_BUY_OR_SELL: Optional[str] = None
) -> List[Trade]:
    filtered_trades = trades_db.copy()

    if search_by_keyword:
        filtered_trades = [trade for trade in filtered_trades if search_by_keyword.lower() in str(trade).lower()]

    if asset_class:
        filtered_trades = [trade for trade in filtered_trades if trade.assetClass == asset_class]

    if starting_date:
        filtered_trades = [trade for trade in filtered_trades if trade.tradeDateTime >= starting_date]
    if ending_date:
        filtered_trades = [trade for trade in filtered_trades if trade.tradeDateTime <= ending_date]

    if min_price:
        filtered_trades = [trade for trade in filtered_trades if trade.tradeDetails.price >= min_price]
    if max_price:
        filtered_trades = [trade for trade in filtered_trades if trade.tradeDetails.price <= max_price]

    if trade_type_BUY_OR_SELL:
        filtered_trades = [trade for trade in filtered_trades if
                           trade.tradeDetails.buySellIndicator == trade_type_BUY_OR_SELL]

    return filtered_trades


@app.put("/trades/{trade_id}", response_model=Trade)
async def update_trade(trade_id: str, trade: Trade):
    for t in trades_db:
        if t["id"] == int(trade_id):
            trades_db.remove(t)
            trades_db.append(trade.dict())
            return trade
    raise HTTPException(status_code=404, detail="Trade not found")


@app.post("/trades", response_model=Trade)
async def create_trade(trade: Trade):
    trade_dict = trade.dict()
    trade_dict["tradeId"] = str(uuid.uuid4())
    trades_db.append(trade_dict)
    return trade_dict


@app.delete("/trades/{trade_id}, response_model=Trade")
async def delete_trade(trade_id: str):
    for t in trades_db:
        if t["id"] == int(trade_id):
            trades_db.remove(t)
            return {"message": "Trade deleted successfully"}
    raise HTTPException(status_code=404, detail="Trade not found")
