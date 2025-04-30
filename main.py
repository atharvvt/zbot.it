from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
# Import your modules
from app.binance import (
    binance_bitget, binance_bitmex, binance_bybit, binance_coinbase,
    binance_coinex, binance_crypto, binance_htx, binance_kucoin
)
from app.bitget import bitget_bitmex, bitget_crypto, bitget_htx
from app.bybit import bybit_bitget, bybit_coinbase, bybit_coinex, bybit_crypto, bybit_htx, bybit_kucoin
from app.coinbase import coinbase_bitget, coinbase_bitmex, coinbase_coinex, coinbase_crypto, coinbase_htx, coinbase_kucoin
from app.coinex import coinex_bitget, coinex_bitmex, coinex_crypto, coinex_htx, coinex_kucoin
from app.kucoin import kucoin_bitget, kucoin_crypto, kucoin_htx
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class ArbitrageRequest(BaseModel):
    symbol: str
    trade_amount_usd: float = 50000

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# BINANCE routes
@app.post("/run/binance-bitget")
def run_binance_bitget(req: ArbitrageRequest):
    return {"result": binance_bitget.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/binance-bitmex")
def run_binance_bitmex(req: ArbitrageRequest):
    return {"result": binance_bitmex.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/binance-bybit")
def run_binance_bybit(req: ArbitrageRequest):
    return {"result": binance_bybit.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/binance-coinbase")
def run_binance_coinbase(req: ArbitrageRequest):
    return {"result": binance_coinbase.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/binance-coinex")
def run_binance_coinex(req: ArbitrageRequest):
    return {"result": binance_coinex.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/binance-crypto")
def run_binance_crypto(req: ArbitrageRequest):
    return {"result": binance_crypto.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/binance-htx")
def run_binance_htx(req: ArbitrageRequest):
    return {"result": binance_htx.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/binance-kucoin")
def run_binance_kucoin(req: ArbitrageRequest):
    return {"result": binance_kucoin.run_arbitrage(req.symbol, req.trade_amount_usd)}

# BITGET routes
@app.post("/run/bitget-bitmex")
def run_bitget_bitmex(req: ArbitrageRequest):
    return {"result": bitget_bitmex.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/bitget-crypto")
def run_bitget_crypto(req: ArbitrageRequest):
    return {"result": bitget_crypto.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/bitget-htx")
def run_bitget_htx(req: ArbitrageRequest):
    return {"result": bitget_htx.run_arbitrage(req.symbol, req.trade_amount_usd)}

# BYBIT routes
@app.post("/run/bybit-bitget")
def run_bybit_bitget(req: ArbitrageRequest):
    return {"result": bybit_bitget.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/bybit-coinbase")
def run_bybit_coinbase(req: ArbitrageRequest):
    return {"result": bybit_coinbase.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/bybit-coinex")
def run_bybit_coinex(req: ArbitrageRequest):
    return {"result": bybit_coinex.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/bybit-crypto")
def run_bybit_crypto(req: ArbitrageRequest):
    return {"result": bybit_crypto.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/bybit-htx")
def run_bybit_htx(req: ArbitrageRequest):
    return {"result": bybit_htx.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/bybit-kucoin")
def run_bybit_kucoin(req: ArbitrageRequest):
    return {"result": bybit_kucoin.run_arbitrage(req.symbol, req.trade_amount_usd)}

# COINBASE routes
@app.post("/run/coinbase-bitget")
def run_coinbase_bitget(req: ArbitrageRequest):
    return {"result": coinbase_bitget.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/coinbase-bitmex")
def run_coinbase_bitmex(req: ArbitrageRequest):
    return {"result": coinbase_bitmex.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/coinbase-coinex")
def run_coinbase_coinex(req: ArbitrageRequest):
    return {"result": coinbase_coinex.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/coinbase-crypto")
def run_coinbase_crypto(req: ArbitrageRequest):
    return {"result": coinbase_crypto.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/coinbase-htx")
def run_coinbase_htx(req: ArbitrageRequest):
    return {"result": coinbase_htx.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/coinbase-kucoin")
def run_coinbase_kucoin(req: ArbitrageRequest):
    return {"result": coinbase_kucoin.run_arbitrage(req.symbol, req.trade_amount_usd)}

# COINEX routes
@app.post("/run/coinex-bitget")
def run_coinex_bitget(req: ArbitrageRequest):
    return {"result": coinex_bitget.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/coinex-bitmex")
def run_coinex_bitmex(req: ArbitrageRequest):
    return {"result": coinex_bitmex.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/coinex-crypto")
def run_coinex_crypto(req: ArbitrageRequest):
    return {"result": coinex_crypto.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/coinex-htx")
def run_coinex_htx(req: ArbitrageRequest):
    return {"result": coinex_htx.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/coinex-kucoin")
def run_coinex_kucoin(req: ArbitrageRequest):
    return {"result": coinex_kucoin.run_arbitrage(req.symbol, req.trade_amount_usd)}

# KUCOIN routes
@app.post("/run/kucoin-bitget")
def run_kucoin_bitget(req: ArbitrageRequest):
    return {"result": kucoin_bitget.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/kucoin-crypto")
def run_kucoin_crypto(req: ArbitrageRequest):
    return {"result": kucoin_crypto.run_arbitrage(req.symbol, req.trade_amount_usd)}

@app.post("/run/kucoin-htx")
def run_kucoin_htx(req: ArbitrageRequest):
    return {"result": kucoin_htx.run_arbitrage(req.symbol, req.trade_amount_usd)}
