from aggregates import Trade, TradeStatus
from commands import CreateTrade
from eventsourcing.application.process import ProcessApplication
from eventsourcing.application.decorators import applicationpolicy


class ExecutionService(ProcessApplication):

    @applicationpolicy
    def policy(self, repository, event):
        pass

    @policy.register(CreateTrade)
    def _(self, repository, event):
        self.create_trade(trade_id=event.trade_id)

    @staticmethod
    def create_trade(trade_id):
        return Trade.create(trade_id)

    @staticmethod
    def reject_trade(self, repository, event):
        trade: Trade = repository[event.trade_id]
        trade.status = TradeStatus.REJECTED
        trade.reason = event.reason

    @staticmethod
    def _set_trade_is_done(self, repository, event):
        trade: Trade = repository[event.trade_id]
        assert not trade.status == TradeStatus.DONE
        trade.status = TradeStatus.DONE
