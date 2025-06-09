from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import OrderNotFound
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise

class blockchaincom(Exchange):

    def describe(self):
        return self.deep_extend(super(blockchaincom, self).describe(), {'id': 'blockchaincom', 'secret': None, 'name': 'Blockchain.com', 'countries': ['LX'], 'rateLimit': 500, 'version': 'v3', 'has': {'CORS': False, 'spot': True, 'margin': None, 'swap': False, 'future': False, 'option': False, 'cancelAllOrders': True, 'cancelOrder': True, 'createOrder': True, 'createStopLimitOrder': True, 'createStopMarketOrder': True, 'createStopOrder': True, 'fetchBalance': True, 'fetchCanceledOrders': True, 'fetchClosedOrders': True, 'fetchDeposit': True, 'fetchDepositAddress': True, 'fetchDeposits': True, 'fetchFundingHistory': False, 'fetchFundingRate': False, 'fetchFundingRateHistory': False, 'fetchFundingRates': False, 'fetchIndexOHLCV': False, 'fetchL2OrderBook': True, 'fetchL3OrderBook': True, 'fetchLedger': False, 'fetchMarginMode': False, 'fetchMarkets': True, 'fetchMarkOHLCV': False, 'fetchMyTrades': True, 'fetchOHLCV': False, 'fetchOpenInterestHistory': False, 'fetchOpenOrders': True, 'fetchOrder': True, 'fetchOrderBook': True, 'fetchPositionMode': False, 'fetchPremiumIndexOHLCV': False, 'fetchTicker': True, 'fetchTickers': True, 'fetchTrades': False, 'fetchTradingFee': False, 'fetchTradingFees': True, 'fetchTransfer': False, 'fetchTransfers': False, 'fetchWithdrawal': True, 'fetchWithdrawals': True, 'fetchWithdrawalWhitelist': True, 'transfer': False, 'withdraw': True}, 'timeframes': None, 'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/147515585-1296e91b-7398-45e5-9d32-f6121538533f.jpeg', 'test': {'public': 'https://testnet-api.delta.exchange', 'private': 'https://testnet-api.delta.exchange'}, 'api': {'public': 'https://api.blockchain.com/v3/exchange', 'private': 'https://api.blockchain.com/v3/exchange'}, 'www': 'https://blockchain.com', 'doc': ['https://api.blockchain.com/v3'], 'fees': 'https://exchange.blockchain.com/fees'}, 'api': {'public': {'get': {'tickers': 1, 'tickers/{symbol}': 1, 'symbols': 1, 'symbols/{symbol}': 1, 'l2/{symbol}': 1, 'l3/{symbol}': 1}}, 'private': {'get': {'fees': 1, 'orders': 1, 'orders/{orderId}': 1, 'trades': 1, 'fills': 1, 'deposits': 1, 'deposits/{depositId}': 1, 'accounts': 1, 'accounts/{account}/{currency}': 1, 'whitelist': 1, 'whitelist/{currency}': 1, 'withdrawals': 1, 'withdrawals/{withdrawalId}': 1}, 'post': {'orders': 1, 'deposits/{currency}': 1, 'withdrawals': 1}, 'delete': {'orders': 1, 'orders/{orderId}': 1}}}, 'fees': {'trading': {'feeSide': 'get', 'tierBased': True, 'percentage': True, 'tiers': {'taker': [[self.parse_number('0'), self.parse_number('0.004')], [self.parse_number('10000'), self.parse_number('0.0022')], [self.parse_number('50000'), self.parse_number('0.002')], [self.parse_number('100000'), self.parse_number('0.0018')], [self.parse_number('500000'), self.parse_number('0.0018')], [self.parse_number('1000000'), self.parse_number('0.0018')], [self.parse_number('2500000'), self.parse_number('0.0018')], [self.parse_number('5000000'), self.parse_number('0.0016')], [self.parse_number('25000000'), self.parse_number('0.0014')], [self.parse_number('100000000'), self.parse_number('0.0011')], [self.parse_number('500000000'), self.parse_number('0.0008')], [self.parse_number('1000000000'), self.parse_number('0.0006')]], 'maker': [[self.parse_number('0'), self.parse_number('0.002')], [self.parse_number('10000'), self.parse_number('0.0012')], [self.parse_number('50000'), self.parse_number('0.001')], [self.parse_number('100000'), self.parse_number('0.0008')], [self.parse_number('500000'), self.parse_number('0.0007000000000000001')], [self.parse_number('1000000'), self.parse_number('0.0006')], [self.parse_number('2500000'), self.parse_number('0.0005')], [self.parse_number('5000000'), self.parse_number('0.0004')], [self.parse_number('25000000'), self.parse_number('0.0003')], [self.parse_number('100000000'), self.parse_number('0.0002')], [self.parse_number('500000000'), self.parse_number('0.0001')], [self.parse_number('1000000000'), self.parse_number('0')]]}}}, 'requiredCredentials': {'apiKey': False, 'secret': True}, 'precisionMode': TICK_SIZE, 'exceptions': {'exact': {'401': AuthenticationError, '404': OrderNotFound}, 'broad': {}}})

    def fetch_markets(self, params={}):
        """
        retrieves data on all markets for blockchaincom
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        markets = self.publicGetSymbols(params)
        marketIds = list(markets.keys())
        result = []
        for i in range(0, len(marketIds)):
            marketId = marketIds[i]
            market = self.safe_value(markets, marketId)
            baseId = self.safe_string(market, 'base_currency')
            quoteId = self.safe_string(market, 'counter_currency')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            numericId = self.safe_number(market, 'id')
            active = None
            marketState = self.safe_string(market, 'status')
            if marketState == 'open':
                active = True
            else:
                active = False
            minPriceIncrementString = self.safe_string(market, 'min_price_increment')
            minPriceIncrementScaleString = self.safe_string(market, 'min_price_increment_scale')
            minPriceScalePrecisionString = self.parse_precision(minPriceIncrementScaleString)
            pricePrecisionString = Precise.string_mul(minPriceIncrementString, minPriceScalePrecisionString)
            lotSizeString = self.safe_string(market, 'lot_size')
            lotSizeScaleString = self.safe_string(market, 'lot_size_scale')
            lotSizeScalePrecisionString = self.parse_precision(lotSizeScaleString)
            amountPrecisionString = Precise.string_mul(lotSizeString, lotSizeScalePrecisionString)
            minOrderSizeString = self.safe_string(market, 'min_order_size')
            minOrderSizeScaleString = self.safe_string(market, 'min_order_size_scale')
            minOrderSizeScalePrecisionString = self.parse_precision(minOrderSizeScaleString)
            minOrderSizePreciseString = Precise.string_mul(minOrderSizeString, minOrderSizeScalePrecisionString)
            minOrderSize = self.parse_number(minOrderSizePreciseString)
            maxOrderSize = None
            maxOrderSize = self.safe_string(market, 'max_order_size')
            if maxOrderSize != '0':
                maxOrderSizeScaleString = self.safe_string(market, 'max_order_size_scale')
                maxOrderSizeScalePrecisionString = self.parse_precision(maxOrderSizeScaleString)
                maxOrderSizeString = Precise.string_mul(maxOrderSize, maxOrderSizeScalePrecisionString)
                maxOrderSize = self.parse_number(maxOrderSizeString)
            else:
                maxOrderSize = None
            result.append({'info': market, 'id': marketId, 'numericId': numericId, 'symbol': base + '/' + quote, 'base': base, 'quote': quote, 'settle': None, 'baseId': baseId, 'quoteId': quoteId, 'settleId': None, 'type': 'spot', 'spot': True, 'margin': False, 'swap': False, 'future': False, 'option': False, 'active': active, 'contract': False, 'linear': None, 'inverse': None, 'contractSize': None, 'expiry': None, 'expiryDatetime': None, 'strike': None, 'optionType': None, 'precision': {'amount': self.parse_number(amountPrecisionString), 'price': self.parse_number(pricePrecisionString)}, 'limits': {'leverage': {'min': None, 'max': None}, 'amount': {'min': minOrderSize, 'max': maxOrderSize}, 'price': {'min': None, 'max': None}, 'cost': {'min': None, 'max': None}}})
        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        return self.fetch_l3_order_book(symbol, limit, params)

    def fetch_l3_order_book(self, symbol, limit=None, params={}):
        """
        fetches level 3 information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified market symbol
        :param int|None limit: max number of orders to return, default is None
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: an `order book structure <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'symbol': market['id']}
        if limit is not None:
            request['depth'] = limit
        response = self.publicGetL3Symbol(self.extend(request, params))
        return self.parse_order_book(response, market['symbol'], None, 'bids', 'asks', 'px', 'qty')

    def fetch_l2_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {'symbol': market['id']}
        if limit is not None:
            request['depth'] = limit
        response = self.publicGetL2Symbol(self.extend(request, params))
        return self.parse_order_book(response, market['symbol'], None, 'bids', 'asks', 'px', 'qty')

    def parse_ticker(self, ticker, market=None):
        marketId = self.safe_string(ticker, 'symbol')
        symbol = self.safe_symbol(marketId, market, '-')
        last = self.safe_string(ticker, 'last_trade_price')
        baseVolume = self.safe_string(ticker, 'volume_24h')
        open = self.safe_string(ticker, 'price_24h')
        return self.safe_ticker({'symbol': symbol, 'timestamp': None, 'datetime': None, 'high': None, 'low': None, 'bid': None, 'bidVolume': None, 'ask': None, 'askVolume': None, 'vwap': None, 'open': open, 'close': None, 'last': last, 'previousClose': None, 'change': None, 'percentage': None, 'average': None, 'baseVolume': baseVolume, 'quoteVolume': None, 'info': ticker}, market)

    def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'symbol': market['id']}
        response = self.publicGetTickersSymbol(self.extend(request, params))
        return self.parse_ticker(response, market)

    def fetch_tickers(self, symbols=None, params={}):
        """
        fetches price tickers for multiple markets, statistical calculations with the information calculated over the past 24 hours each market
        :param [str]|None symbols: unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: an array of `ticker structures <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        tickers = self.publicGetTickers(params)
        return self.parse_tickers(tickers, symbols)

    def parse_order_state(self, state):
        states = {'OPEN': 'open', 'REJECTED': 'rejected', 'FILLED': 'closed', 'CANCELED': 'canceled', 'PART_FILLED': 'open', 'EXPIRED': 'expired'}
        return self.safe_string(states, state, state)

    def parse_order(self, order, market=None):
        clientOrderId = self.safe_string(order, 'clOrdId')
        type = self.safe_string_lower(order, 'ordType')
        statusId = self.safe_string(order, 'ordStatus')
        state = self.parse_order_state(statusId)
        side = self.safe_string_lower(order, 'side')
        marketId = self.safe_string(order, 'symbol')
        symbol = self.safe_symbol(marketId, market, '-')
        exchangeOrderId = self.safe_string(order, 'exOrdId')
        price = self.safe_string(order, 'price') if type != 'market' else None
        average = self.safe_number(order, 'avgPx')
        timestamp = self.safe_integer(order, 'timestamp')
        datetime = self.iso8601(timestamp)
        filled = self.safe_string(order, 'cumQty')
        remaining = self.safe_string(order, 'leavesQty')
        result = self.safe_order({'id': exchangeOrderId, 'clientOrderId': clientOrderId, 'datetime': datetime, 'timestamp': timestamp, 'lastTradeTimestamp': None, 'status': state, 'symbol': symbol, 'type': type, 'timeInForce': None, 'side': side, 'price': price, 'average': average, 'amount': None, 'filled': filled, 'remaining': remaining, 'cost': None, 'trades': [], 'fees': {}, 'info': order})
        return result

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        orderType = self.safe_string(params, 'ordType', type)
        uppercaseOrderType = orderType.upper()
        clientOrderId = self.safe_string_2(params, 'clientOrderId', 'clOrdId', self.uuid16())
        params = self.omit(params, ['ordType', 'clientOrderId', 'clOrdId'])
        request = {'ordType': uppercaseOrderType, 'symbol': market['id'], 'side': side.upper(), 'orderQty': self.amount_to_precision(symbol, amount), 'clOrdId': clientOrderId}
        stopPrice = self.safe_value_2(params, 'stopPx', 'stopPrice')
        params = self.omit(params, ['stopPx', 'stopPrice'])
        if uppercaseOrderType == 'STOP' or uppercaseOrderType == 'STOPLIMIT':
            if stopPrice is None:
                raise ArgumentsRequired(self.id + ' createOrder() requires a stopPx or stopPrice param for a ' + uppercaseOrderType + ' order')
        if stopPrice is not None:
            if uppercaseOrderType == 'MARKET':
                request['ordType'] = 'STOP'
            elif uppercaseOrderType == 'LIMIT':
                request['ordType'] = 'STOPLIMIT'
        priceRequired = False
        stopPriceRequired = False
        if request['ordType'] == 'LIMIT' or request['ordType'] == 'STOPLIMIT':
            priceRequired = True
        if request['ordType'] == 'STOP' or request['ordType'] == 'STOPLIMIT':
            stopPriceRequired = True
        if priceRequired:
            request['price'] = self.price_to_precision(symbol, price)
        if stopPriceRequired:
            request['stopPx'] = self.price_to_precision(symbol, stopPrice)
        response = self.privatePostOrders(self.extend(request, params))
        return self.parse_order(response, market)

    def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str|None symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        request = {'orderId': id}
        response = self.privateDeleteOrdersOrderId(self.extend(request, params))
        return {'id': id, 'info': response}

    def cancel_all_orders(self, symbol=None, params={}):
        """
        cancel all open orders
        :param str|None symbol: unified market symbol of the market to cancel orders in, all markets are used if None, default is None
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: an list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {}
        if symbol is not None:
            marketId = self.market_id(symbol)
            request['symbol'] = marketId
        response = self.privateDeleteOrders(self.extend(request, params))
        return {'symbol': symbol, 'info': response}

    def fetch_trading_fees(self, params={}):
        """
        fetch the trading fees for multiple markets
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: a dictionary of `fee structures <https://docs.ccxt.com/en/latest/manual.html#fee-structure>` indexed by market symbols
        """
        self.load_markets()
        response = self.privateGetFees(params)
        makerFee = self.safe_number(response, 'makerRate')
        takerFee = self.safe_number(response, 'takerRate')
        result = {}
        for i in range(0, len(self.symbols)):
            symbol = self.symbols[i]
            result[symbol] = {'info': response, 'symbol': symbol, 'maker': makerFee, 'taker': takerFee}
        return result

    def fetch_canceled_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches information on multiple canceled orders made by the user
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: timestamp in ms of the earliest order, default is None
        :param int|None limit: max number of orders to return, default is None
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        state = 'CANCELED'
        return self.fetch_orders_by_state(state, symbol, since, limit, params)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches information on multiple closed orders made by the user
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        state = 'FILLED'
        return self.fetch_orders_by_state(state, symbol, since, limit, params)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all unfilled currently open orders
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch open orders for
        :param int|None limit: the maximum number of  open orders structures to retrieve
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        state = 'OPEN'
        return self.fetch_orders_by_state(state, symbol, since, limit, params)

    def fetch_orders_by_state(self, state, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {'status': state, 'limit': 100}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        response = self.privateGetOrders(self.extend(request, params))
        return self.parse_orders(response, market, since, limit)

    def parse_trade(self, trade, market=None):
        orderId = self.safe_string(trade, 'exOrdId')
        tradeId = self.safe_string(trade, 'tradeId')
        side = self.safe_string(trade, 'side').lower()
        marketId = self.safe_string(trade, 'symbol')
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'qty')
        timestamp = self.safe_integer(trade, 'timestamp')
        datetime = self.iso8601(timestamp)
        market = self.safe_market(marketId, market, '-')
        symbol = market['symbol']
        fee = None
        feeCostString = self.safe_string(trade, 'fee')
        if feeCostString is not None:
            feeCurrency = market['quote']
            fee = {'cost': feeCostString, 'currency': feeCurrency}
        return self.safe_trade({'id': tradeId, 'timestamp': timestamp, 'datetime': datetime, 'symbol': symbol, 'order': orderId, 'type': None, 'side': side, 'takerOrMaker': None, 'price': priceString, 'amount': amountString, 'cost': None, 'fee': fee, 'info': trade}, market)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all trades made by the user
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch trades for
        :param int|None limit: the maximum number of trades structures to retrieve
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html#trade-structure>`
        """
        self.load_markets()
        request = {}
        if limit is not None:
            request['limit'] = limit
        market = None
        if symbol is not None:
            request['symbol'] = self.market_id(symbol)
            market = self.market(symbol)
        trades = self.privateGetFills(self.extend(request, params))
        return self.parse_trades(trades, market, since, limit, params)

    def fetch_deposit_address(self, code, params={}):
        """
        fetch the deposit address for a currency associated with self account
        :param str code: unified currency code
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: an `address structure <https://docs.ccxt.com/en/latest/manual.html#address-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        request = {'currency': currency['id']}
        response = self.privatePostDepositsCurrency(self.extend(request, params))
        rawAddress = self.safe_string(response, 'address')
        tag = None
        address = None
        if rawAddress is not None:
            (address, tag) = rawAddress.split(':')
        result = {'info': response}
        result['currency'] = currency['code']
        result['address'] = address
        if tag is not None:
            result['tag'] = tag
        return result

    def parse_transaction_state(self, state):
        states = {'COMPLETED': 'ok', 'REJECTED': 'failed', 'PENDING': 'pending', 'FAILED': 'failed', 'REFUNDED': 'refunded'}
        return self.safe_string(states, state, state)

    def parse_transaction(self, transaction, currency=None):
        type = None
        id = None
        amount = self.safe_number(transaction, 'amount')
        timestamp = self.safe_integer(transaction, 'timestamp')
        currencyId = self.safe_string(transaction, 'currency')
        code = self.safe_currency_code(currencyId, currency)
        state = self.safe_string(transaction, 'state')
        if 'depositId' in transaction:
            type = 'deposit'
            id = self.safe_string(transaction, 'depositId')
        elif 'withdrawalId' in transaction:
            type = 'withdrawal'
            id = self.safe_string(transaction, 'withdrawalId')
        feeCost = self.safe_number(transaction, 'fee') if type == 'withdrawal' else None
        fee = None
        if feeCost is not None:
            fee = {'currency': code, 'cost': feeCost}
        address = self.safe_string(transaction, 'address')
        txid = self.safe_string(transaction, 'txhash')
        result = {'info': transaction, 'id': id, 'txid': txid, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'network': None, 'addressFrom': None, 'address': address, 'addressTo': address, 'tagFrom': None, 'tag': None, 'tagTo': None, 'type': type, 'amount': amount, 'currency': code, 'status': self.parse_transaction_state(state), 'updated': None, 'comment': None, 'fee': fee}
        return result

    def fetch_withdrawal_whitelist(self, params={}):
        """
        fetch the list of withdrawal addresses on the whitelist
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: dictionary with keys beneficiaryId, name, currency
        """
        self.load_markets()
        response = self.privateGetWhitelist()
        result = []
        for i in range(0, len(response)):
            entry = response[i]
            result.append({'beneficiaryId': self.safe_string(entry, 'whitelistId'), 'name': self.safe_string(entry, 'name'), 'currency': self.safe_string(entry, 'currency'), 'info': entry})
        return result

    def fetch_withdrawal_whitelist_by_currency(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {'currency': currency['id']}
        response = self.privateGetWhitelistCurrency(self.extend(request, params))
        result = []
        for i in range(0, len(response)):
            entry = response[i]
            result.append({'beneficiaryId': self.safe_string(entry, 'whitelistId'), 'name': self.safe_string(entry, 'name'), 'currency': self.safe_string(entry, 'currency'), 'info': entry})
        return result

    def withdraw(self, code, amount, address, tag=None, params={}):
        """
        make a withdrawal
        :param str code: unified currency code
        :param float amount: the amount to withdraw
        :param str address: the address to withdraw to
        :param str|None tag:
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        request = {'amount': amount, 'currency': currency['id'], 'beneficiary': address, 'sendMax': False}
        response = self.privatePostWithdrawals(self.extend(request, params))
        return self.parse_transaction(response, currency)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        """
        fetch all withdrawals made from an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch withdrawals for
        :param int|None limit: the maximum number of withdrawals structures to retrieve
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {}
        if since is not None:
            request['from'] = since
        response = self.privateGetWithdrawals(self.extend(request, params))
        return self.parse_transactions(response, code, since, limit)

    def fetch_withdrawal(self, id, code=None, params={}):
        """
        fetch data on a currency withdrawal via the withdrawal id
        :param str id: withdrawal id
        :param str|None code: not used by blockchaincom.fetchWithdrawal
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {'withdrawalId': id}
        response = self.privateGetWithdrawalsWithdrawalId(self.extend(request, params))
        return self.parse_transaction(response)

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        """
        fetch all deposits made to an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch deposits for
        :param int|None limit: the maximum number of deposits structures to retrieve
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {}
        if since is not None:
            request['from'] = since
        response = self.privateGetDeposits(self.extend(request, params))
        return self.parse_transactions(response, code, since, limit)

    def fetch_deposit(self, id, code=None, params={}):
        """
        fetch information on a deposit
        :param str id: deposit id
        :param str|None code: not used by blockchaincom fetchDeposit()
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        depositId = self.safe_string(params, 'depositId', id)
        request = {'depositId': depositId}
        deposit = self.privateGetDepositsDepositId(self.extend(request, params))
        return self.parse_transaction(deposit)

    def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        self.load_markets()
        accountName = self.safe_string(params, 'account', 'primary')
        params = self.omit(params, 'account')
        request = {'account': accountName}
        response = self.privateGetAccounts(self.extend(request, params))
        balances = self.safe_value(response, accountName)
        if balances is None:
            raise ExchangeError(self.id + ' fetchBalance() could not find the "' + accountName + '" account')
        result = {'info': response}
        for i in range(0, len(balances)):
            entry = balances[i]
            currencyId = self.safe_string(entry, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(entry, 'available')
            account['total'] = self.safe_string(entry, 'balance')
            result[code] = account
        return self.safe_balance(result)

    def fetch_order(self, id, symbol=None, params={}):
        """
        fetches information on an order made by the user
        :param str|None symbol: not used by blockchaincom fetchOrder
        :param dict params: extra parameters specific to the blockchaincom api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {'orderId': id}
        response = self.privateGetOrdersOrderId(self.extend(request, params))
        return self.parse_order(response)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        requestPath = '/' + self.implode_params(path, params)
        url = self.urls['api'][api] + requestPath
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        elif api == 'private':
            self.check_required_credentials()
            headers = {'X-API-Token': self.secret}
            if method == 'GET':
                if query:
                    url += '?' + self.urlencode(query)
            else:
                body = self.json(query)
                headers['Content-Type'] = 'application/json'
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        text = self.safe_string(response, 'text')
        if text is not None:
            if text == 'Insufficient Balance':
                raise InsufficientFunds(self.id + ' ' + body)
        errorCode = self.safe_string(response, 'status')
        errorMessage = self.safe_string(response, 'error')
        if code is not None:
            feedback = self.id + ' ' + self.json(response)
            self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, feedback)
            self.throw_broadly_matched_exception(self.exceptions['broad'], errorMessage, feedback)