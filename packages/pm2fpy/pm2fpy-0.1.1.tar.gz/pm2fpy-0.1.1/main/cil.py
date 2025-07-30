import shlex
from main.manager import SimpleDaemonManager, parse_start_args, print_table


def handle_command(cmd, manager):
    parts = shlex.split(cmd.strip())
    if len(parts) < 2 or parts[0] != 'pypm':
        return None

    action = parts[1]

    if action == 'list':
        return manager.list()

    elif action == 'start':
        if len(parts) < 3:
            return None
        parsed = parse_start_args(parts[2:])
        if not parsed:
            return None
        name, script, interpreter = parsed
        success = manager.start(name, script, interpreter)
        return success

    elif action == 'stop':
        if len(parts) != 3:
            return None
        name = parts[2]
        success = manager.stop(name)
        return success

    else:
        return None


def main():
    manager = SimpleDaemonManager()

    print("health daemon manager started. Commands:")
    print("  health list")
    print("  health start <file> [--name <name>] [--interpreter <interpreter>]")
    print("  health stop <name>")
    print("Ctrl+C to exit")

    while True:
        try:
            cmd = input('> ')
            res = handle_command(cmd, manager)

            if res is None:
                print('Invalid command or format')
            elif isinstance(res, list):
                print_table(res)
            elif isinstance(res, bool):
                print('Success' if res else 'Failed')

        except KeyboardInterrupt:
            print("\nStopping all processes and exiting...")
            for pi in manager.processes.values():
                pi.stop()
            break


if __name__ == '__main__':
    main()
