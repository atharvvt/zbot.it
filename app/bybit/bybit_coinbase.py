import os
import time
import ccxt
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants for fees and tax
bybit_fee = 0.00075  # 0.075%
coinbase_fee = 0.001  # 0.1%
network_fee = 0.0001  # BTC withdrawal fee
tax_rate = 0.0        # Set tax if applicable
slippage_percentage = 0.001  # 0.1%

# Initialize exchanges
bybit = ccxt.bybit({
    'apiKey': os.getenv('bybit_API_KEY'),
    'secret': os.getenv('bybit_SECRET'),
    'enableRateLimit': True
})

coinbase = ccxt.coinbase({
    'apiKey': os.getenv('coinbase_API_KEY'),
    'secret': os.getenv('coinbase_SECRET'),
    'password': os.getenv('coinbase_PASSWORD'),
    'enableRateLimit': True
})

def get_bybit_price(symbol):
    try:
        order_book = bybit.fetch_order_book(symbol)
        return order_book['bids'][0][0], order_book['asks'][0][0]
    except Exception as e:
        print(f"⚠️ Bybit error: {e}")
        return None, None

def get_coinbase_price(symbol):
    try:
        order_book = coinbase.fetch_order_book(symbol)
        return order_book['bids'][0][0], order_book['asks'][0][0]
    except Exception as e:
        print(f"⚠️ Coinbase error: {e}")
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
    bybit_bid, bybit_ask = get_bybit_price(symbol)
    coinbase_bid, coinbase_ask = get_coinbase_price(symbol)

    print(f"\n🔍 Prices:")
    print(f"Bybit   - Bid: {bybit_bid}, Ask: {bybit_ask}")
    print(f"Coinbase - Bid: {coinbase_bid}, Ask: {coinbase_ask}")
    result = []
    # Arbitrage: Bybit → Coinbase
    if bybit_ask and coinbase_bid:
        result.append(simulate_arbitrage(
            buy_price=bybit_ask,
            sell_price=coinbase_bid,
            buy_fee=bybit_fee,
            sell_fee=coinbase_fee,
            trade_amount_usd=trade_amount_usd,
            from_exchange="Bybit",
            to_exchange="Coinbase"
        ))

    # Arbitrage: Coinbase → Bybit
    if coinbase_ask and bybit_bid:
        result.append(simulate_arbitrage(
            buy_price=coinbase_ask,
            sell_price=bybit_bid,
            buy_fee=coinbase_fee,
            sell_fee=bybit_fee,
            trade_amount_usd=trade_amount_usd,
            from_exchange="Coinbase",
            to_exchange="Bybit"
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
