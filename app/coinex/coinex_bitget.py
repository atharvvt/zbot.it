import os
import time
import ccxt
import random
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fees & Configs
coinex_fee = 0.001  # 0.1%
bitget_fee = 0.0005  # 0.05%
network_fee = 0.0001  # BTC withdrawal fee
tax_rate = 0.0
slippage_percentage = 0.001  # 0.1%

# Initialize CoinEx
coinex = ccxt.coinex({
    'apiKey': os.getenv('coinex_API_KEY'),
    'secret': os.getenv('coinex_SECRET'),
    'enableRateLimit': True
})

# Initialize Bitget
bitget = ccxt.bitget({
    'apiKey': os.getenv('bitget_API_KEY'),
    'secret': os.getenv('bitget_SECRET'),
    'password': os.getenv('bitget_PASSWORD'),
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'}
})

def get_coinex_price(symbol):
    try:
        order_book = coinex.fetch_order_book(symbol)
        return order_book['bids'][0][0], order_book['asks'][0][0]
    except Exception as e:
        print(f"⚠️ CoinEx error: {e}")
        return None, None

def get_bitget_price(symbol):
    try:
        order_book = bitget.fetch_order_book(symbol)
        return order_book['bids'][0][0], order_book['asks'][0][0]
    except Exception as e:
        print(f"⚠️ Bitget error: {e}")
        return None, None

def apply_slippage(price, slippage_pct):
    return price * (1 + random.uniform(-slippage_pct, slippage_pct))

def simulate_arbitrage(buy_price, sell_price, buy_fee, sell_fee, trade_amount_usd, from_exchange, to_exchange):
    buy_price = apply_slippage(buy_price, slippage_percentage)
    sell_price = apply_slippage(sell_price, slippage_percentage)

    btc_bought = trade_amount_usd / buy_price
    btc_to_sell = btc_bought - network_fee
    usd_gained = btc_to_sell * sell_price

    buy_fee_usd = trade_amount_usd * buy_fee
    sell_fee_usd = usd_gained * sell_fee
    tax = tax_rate * (usd_gained - trade_amount_usd)

    profit = usd_gained - trade_amount_usd - buy_fee_usd - sell_fee_usd - tax

    data = {
        "from_exchange": from_exchange,
        "to_exchange": to_exchange,
        "buy_price": round(buy_price, 2),
        "sell_price": round(sell_price, 2),
        "currency_bought": round(btc_bought, 6),
        "currency_after_network_fee": round(btc_to_sell, 6),
        "usd_gained": round(usd_gained, 2),
        "buy_fee_usd": round(buy_fee_usd, 2),
        "sell_fee_usd": round(sell_fee_usd, 2),
        "tax": round(tax, 2),
        "profit": round(profit, 2)
    }

    print(f"\n🧮 {from_exchange} → {to_exchange}")
    print(f"Buy @ ${buy_price:.2f}, Sell @ ${sell_price:.2f}")
    print(f"currency Bought: {btc_bought:.6f}, After Network Fee: {btc_to_sell:.6f}")
    print(f"USD Gained: ${usd_gained:.2f}")
    print(f"Fees: Buy=${buy_fee_usd:.2f}, Sell=${sell_fee_usd:.2f}, Tax=${tax:.2f}")
    print(f"💰 Profit: ${profit:.2f}")

    return data

def check_arbitrage_opportunity(symbol, trade_amount_usd):
    coinex_bid, coinex_ask = get_coinex_price(symbol)
    bitget_bid, bitget_ask = get_bitget_price(symbol)

    print(f"\n🔍 Prices:")
    print(f"CoinEx  - Bid: {coinex_bid}, Ask: {coinex_ask}")
    print(f"Bitget  - Bid: {bitget_bid}, Ask: {bitget_ask}")
    result = []
    if coinex_ask and bitget_bid:
        result.append(simulate_arbitrage(
            buy_price=coinex_ask,
            sell_price=bitget_bid,
            buy_fee=coinex_fee,
            sell_fee=bitget_fee,
            trade_amount_usd=trade_amount_usd,
            from_exchange="CoinEx",
            to_exchange="Bitget"
        ))

    if bitget_ask and coinex_bid:
        result.append(simulate_arbitrage(
            buy_price=bitget_ask,
            sell_price=coinex_bid,
            buy_fee=bitget_fee,
            sell_fee=coinex_fee,
            trade_amount_usd=trade_amount_usd,
            from_exchange="Bitget",
            to_exchange="CoinEx"
        ))
    return result

def run_arbitrage(symbol='BTC/USDT', trade_amount_usd=50000):
    try:
        return check_arbitrage_opportunity(symbol, trade_amount_usd)
    except Exception as e:
        return {"error": str(e)}


# Optional CLI running
if __name__ == "__main__":
    while True:
        check_arbitrage_opportunity("BTC/USDT")
        time.sleep(10)
