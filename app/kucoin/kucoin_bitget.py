import os
import time
import ccxt
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
kucoin_fee = 0.001
bitget_fee = 0.001
network_fee = 0.0001
tax_rate = 0.0
slippage_percentage = 0.001

# Initialize KuCoin
kucoin = ccxt.kucoin({
    'apiKey': os.getenv('kucoin_API_KEY'),
    'secret': os.getenv('kucoin_SECRET'),
    'password': os.getenv('kucoin_PASSWORD'),
    'enableRateLimit': True
})

# Initialize Bitget
bitget = ccxt.bitget({
    'apiKey': os.getenv('bitget_API_KEY'),
    'secret': os.getenv('bitget_SECRET'),
    'password': os.getenv('bitget_PASSWORD'),
    'enableRateLimit': True
})


def get_kucoin_price(symbol):
    try:
        order_book = kucoin.fetch_order_book(symbol)
        return order_book['bids'][0][0], order_book['asks'][0][0]
    except Exception as e:
        print(f"⚠️ KuCoin error: {e}")
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

    # print(f"\n🧮 {from_exchange} → {to_exchange}")
    # print(f"Buy @ ${buy_price:.2f}, Sell @ ${sell_price:.2f}")
    # print(f"currency Bought: {btc_bought:.6f}, After Network Fee: {btc_to_sell:.6f}")
    # print(f"USD Gained: ${usd_gained:.2f}")
    # print(f"Fees: Buy=${buy_fee_usd:.2f}, Sell=${sell_fee_usd:.2f}, Tax=${tax:.2f}")
    # print(f"💰 Profit: ${profit:.2f}")

    return data


def check_arbitrage_opportunity(symbol, trade_amount_usd):
    kucoin_bid, kucoin_ask = get_kucoin_price(symbol)
    bitget_bid, bitget_ask = get_bitget_price(symbol)

    # print(f"\n🔍 Prices:")
    # print(f"KuCoin - Bid: {kucoin_bid}, Ask: {kucoin_ask}")
    # print(f"Bitget - Bid: {bitget_bid}, Ask: {bitget_ask}")
    result = []
    if kucoin_ask and bitget_bid:
        result.append(simulate_arbitrage(
            buy_price=kucoin_ask,
            sell_price=bitget_bid,
            buy_fee=kucoin_fee,
            sell_fee=bitget_fee,
            trade_amount_usd=trade_amount_usd,
            from_exchange="KuCoin",
            to_exchange="Bitget"
        ))

    if bitget_ask and kucoin_bid:
        result.append(simulate_arbitrage(
            buy_price=bitget_ask,
            sell_price=kucoin_bid,
            buy_fee=bitget_fee,
            sell_fee=kucoin_fee,
            trade_amount_usd=trade_amount_usd,
            from_exchange="Bitget",
            to_exchange="KuCoin"
        ))
    return result


def run_arbitrage(symbol='BTC/USDT', trade_amount_usd=50000):
    try:
        return check_arbitrage_opportunity(symbol, trade_amount_usd)
    except Exception as e:
        return {"error": str(e)}


# Optional CLI running

