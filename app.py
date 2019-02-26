from commands import Commands
from processes import ExecutionService
from eventsourcing.application.system import System


if __name__ == '__main__':

    commands_pipeline = Commands | ExecutionService | Commands
    system = System(commands_pipeline)

    with system:
        # Create "create trade" command.
        trade_id = system.commands.create_trade(1234)
        cmd = system.commands.repository[trade_id]
        trade = system.executionservice.repository[cmd.trade_id]
