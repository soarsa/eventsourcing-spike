from decimal import Decimal
from enum import Enum
from datetime import datetime
from eventsourcing.domain.model.aggregate import AggregateRoot
from eventsourcing.domain.model.decorators import attribute


class Direction(Enum):
    Buy: int = 0
    Sell: int = 1


class TradeStatus(Enum):
    PENDING: int = 0
    DONE: int = 1
    REJECTED: int = 2


class Trade(AggregateRoot):

    def __init__(self, trade_id: int, trader_name: str, currency_pair: str, spot_rate: Decimal, trade_date: datetime,
                 value_date: datetime, direction: Direction, notional: Decimal, dealt_currency: str, **kwargs):
        super(Trade, self).__init__(**kwargs)

        self._trade_id = trade_id
        self._trader_name = trader_name
        self._currency_pair = currency_pair
        self._spot_rate = spot_rate
        self._trade_date = trade_date
        self._value_date = value_date
        self._direction = direction
        self._notional = notional
        self._dealt_currency = dealt_currency
        self._status = TradeStatus.PENDING
        self.reason = ""

    class Event(AggregateRoot.Event):
        pass

    @classmethod
    def create(cls, trade_id):
        return cls.__create__(trade_id=trade_id)

    class Created(Event, AggregateRoot.Event):
        pass

    @attribute
    def trade_id(self) -> int:
        return self._trade_id

    @attribute
    def trader_name(self) -> str:
        return self._trader_name

    @attribute
    def currency_pair(self) -> str:
        return self._currency_pair

    @attribute
    def spot_rate(self) -> Decimal:
        return self._spot_rate

    @attribute
    def trade_date(self) -> datetime:
        return self._trade_date

    @attribute
    def notional(self) -> Decimal:
        return self._notional

    @attribute
    def dealt_currency(self) -> str:
        return self._dealt_currency

    @attribute
    def status(self) -> TradeStatus:
        return self._status

    @attribute
    def reason(self) -> str:
        return self._reason

    @attribute
    def direction(self) -> Direction:
        return self._direction
