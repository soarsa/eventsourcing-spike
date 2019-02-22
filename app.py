from commands import Commands
from processes import ExecutionService
from eventsourcing.application.system import System, SingleThreadedRunner
from eventsourcing.application.popo import PopoApplication

if __name__ == '__main__':

    commands_pipeline = Commands | ExecutionService | Commands
    system = System(commands_pipeline)

    with SingleThreadedRunner(system, infrastructure_class=PopoApplication):

        with system:
            # Create "create trade" command.
            cmd_id = system.commands.create_trade

            # Check the command has a trade ID
            cmd = system.executionservice.repository[cmd_id]

            trade = system.orders.repository[cmd.trade_id]
            print(trade.status)
