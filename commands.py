from eventsourcing.application.decorators import applicationpolicy
from eventsourcing.domain.model.command import Command
import eventsourcing.domain.model.decorators
from eventsourcing.application.command import CommandProcess
from eventsourcing.domain.model.decorators import retry as model_retry
from eventsourcing.exceptions import OperationalError, RecordConflictError
from aggregates import TradeStatus


class Event(Command.Event):
    pass


class CreateTrade(Command):

    @classmethod
    def create(cls):
        return cls.__create__()

    class Created(Event, Command.Created):
        pass

    @eventsourcing.domain.model.decorators.attribute
    def trade_id(self):
        pass


class DoneTrade(Command):
    @classmethod
    def create(cls):
        return cls.__create__()

    class Done(Event, Command.Created):
        pass

    @eventsourcing.domain.model.decorators.attribute
    def trade_id(self):
        pass


class Commands(CommandProcess):
    persist_event_type = CreateTrade.Event

    @applicationpolicy
    def policy(self, repository, event):
        pass

    @policy.register(CreateTrade.Created)
    def _(self, repository, event):
        cmd = repository[event.command_id]
        cmd.trade_id = event.trade_id

    @policy.register(DoneTrade.Done)
    def _(self, repository, event):
        cmd = repository[event.command_id]
        cmd.status = TradeStatus.DONE

    @staticmethod
    @model_retry((OperationalError, RecordConflictError), max_attempts=10, wait=0.01)
    def create_trade():
        cmd = CreateTrade.create()
        cmd.__save__()
        return cmd.id
