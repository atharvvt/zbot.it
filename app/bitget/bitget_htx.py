import os
import time
import ccxt
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
bitget_fee = 0.0005         # 0.05%
htx_fee = 0.0005            # 0.05%
network_fee = 0.0001        # BTC network fee
tax_rate = 0.0              # Change if needed
slippage_percentage = 0.001  # 0.1%

# Initialize Bitget
bitget = ccxt.bitget({
    'apiKey': os.getenv('bitget_API_KEY'),
    'secret': os.getenv('bitget_SECRET'),
    'enableRateLimit': True
})

# Initialize HTX (Huobi)
htx = ccxt.huobi({
    'apiKey': os.getenv('htx_API_KEY'),
    'secret': os.getenv('htx_SECRET'),
    'enableRateLimit': True
})


def get_bitget_price(symbol):
    try:
        order_book = bitget.fetch_order_book(symbol)
        return order_book['bids'][0][0], order_book['asks'][0][0]
    except Exception as e:
        print(f"⚠️ Bitget error: {e}")
        return None, None


def get_htx_price(symbol):
    try:
        order_book = htx.fetch_order_book(symbol)
        return order_book['bids'][0][0], order_book['asks'][0][0]
    except Exception as e:
        print(f"⚠️ HTX error: {e}")
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
        "currency_bought": round(btc_bought, 2),
        "currency_after_network_fee": round(btc_to_sell, 2),
        "usd_gained": round(usd_gained, 2),
        "buy_fee_usd": round(buy_fee_usd, 2),
        "sell_fee_usd": round(sell_fee_usd, 2),
        "tax": round(tax, 2),
        "profit": round(profit, 2)
    }

    # print(f"\n🧮 {from_exchange} → {to_exchange}")
    # print(f"Buy @ ${buy_price:.2f}, Sell @ ${sell_price:.2f}")
    # print(f"currency Bought: {btc_bought:.2f}, After Network Fee: {btc_to_sell:.2f}")
    # print(f"USD Gained: ${usd_gained:.2f}")
    # print(f"Fees: Buy=${buy_fee_usd:.2f}, Sell=${sell_fee_usd:.2f}, Tax=${tax:.2f}")
    # print(f"💰 Profit: ${profit:.2f}")

    return data


def check_arbitrage_opportunity(symbol, trade_amount_usd):
    bitget_bid, bitget_ask = get_bitget_price(symbol)
    htx_bid, htx_ask = get_htx_price(symbol)

    # print(f"\n🔍 Prices:")
    # print(f"Bitget        - Bid: {bitget_bid}, Ask: {bitget_ask}")
    # print(f"HTX (Huobi)   - Bid: {htx_bid}, Ask: {htx_ask}")
    result = []
    if bitget_ask and htx_bid:
        result.append(simulate_arbitrage(
            buy_price=bitget_ask,
            sell_price=htx_bid,
            buy_fee=bitget_fee,
            sell_fee=htx_fee,
            trade_amount_usd=trade_amount_usd,
            from_exchange="Bitget",
            to_exchange="HTX (Huobi)"
        ))

    if htx_ask and bitget_bid:
        result.append(simulate_arbitrage(
            buy_price=htx_ask,
            sell_price=bitget_bid,
            buy_fee=htx_fee,
            sell_fee=bitget_fee,
            trade_amount_usd=trade_amount_usd,
            from_exchange="HTX (Huobi)",
            to_exchange="Bitget"
        ))
    return result


def run_arbitrage(symbol='BTC/USDT', trade_amount_usd=50000):
    try:
        return check_arbitrage_opportunity(symbol, trade_amount_usd)
    except Exception as e:
        return {"error": str(e)}


# Optional CLI running

