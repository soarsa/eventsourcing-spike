from commands import Commands
from processes import ExecutionService
from eventsourcing.application.system import System


if __name__ == '__main__':

    commands_pipeline = Commands | ExecutionService | Commands
    system = System(commands_pipeline)

    with system:
        # Create "create trade" command.
        cmd_id = system.commands.create_trade()

        # Check the command has a trade ID
        cmd = system.executionservice.repository[str(cmd_id)]

        trade = system.orders.repository[cmd.trade_id]
        print(trade.status)
