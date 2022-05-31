EXIT_COMMANDS = ('good bye', 'close', 'exit')
CONTACTS = {}


# This decorator handles correctness of the phone number: can start with '+'
# and then must contain only digits. But doesn't check if the number is real
def input_error(func):
    def wrapper(*args):
        if len(args) != 2:
            return func(*args)

        name, phone = args
        try:
            phone_check = phone[1:] if phone[0] == '+' else phone
            # check at once if the phone number doesn't start with '-' sign
            # and if it contains only digits by int()
            if int(phone_check) < 0:
                raise ValueError
                return 1
        except ValueError:
            return "ERROR: Phone can or couldn't start with '+' and then must contain only digits!\n \
                    Example: +380..., 380..."

        result = func(name, phone)
        return result

    return wrapper


# This decorator handles the correct number of arguments that are passed into the function
def func_arg_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
            return result
        except TypeError:
            f_name = func.__name__
            if f_name in ('exit_program', 'hello', 'show_all_phones'):
                return "ERROR: This command has to be written without arguments!"
            if f_name in ('add_phone', 'change_phone'):
                return "ERROR: This command needs 2 arguments: 'name' and 'phone' separated by 1 space!"
            if f_name == 'show_phone':
                return "ERROR: This command needs 1 arguments: 'name' separated by 1 space!"

    return wrapper


@func_arg_error
def hello() -> str:
    return "Hello! How can I help you?"


@input_error
@func_arg_error
def add_phone(name: str, phone: str) -> str:
    if name in CONTACTS.keys():
        return f"Name '{name}' is already in contacts!\n \
                Try another name or change existing contact"

    CONTACTS.update({name: phone})
    return f"Contact was added successfully!"


@input_error
@func_arg_error
def change_phone(name: str, phone: str) -> str:
    if name not in CONTACTS.keys():
        return f"There is no contact with name '{name}'"

    CONTACTS.update({name: phone})
    return f"Contact was updated successfully!"


@func_arg_error
def show_phone(name: str) -> str:
    if name not in CONTACTS.keys():
        return f"There is no contact with name '{name}'"

    return CONTACTS.get(name)


@func_arg_error
def show_all_phones() -> str:
    if not CONTACTS:
        return "There are no contacts to show yet..."

    return '\n'.join(["{:<10}: {:<10}".format(name, phone) for name, phone in CONTACTS.items()])


@func_arg_error
def exit_program():
    return "Good bye!"


def choose_command(cmd: str):
    # cmd = cmd.strip().split(' ')  # apply strip() as well to exclude spaces at the ends
    cmd_check = cmd[0].lower()

    if cmd_check in EXIT_COMMANDS:
        return exit_program
    if cmd_check == 'hello':
        return hello
    if cmd_check == 'add':
        return add_phone
    if cmd_check == 'change':
        return change_phone
    if cmd_check == 'phone':
        return show_phone
    if cmd_check == 'show':
        # take into account that this command consists 2 words
        cmd[:2] = [' '.join(cmd[:2])]
        cmd_check = cmd[0].lower()
        if cmd_check == 'show all':
            return show_all_phones


def parse_command(cmd: str) -> list:
    return cmd.strip().split(' ')  # apply strip() as well to exclude spaces at the ends


def handle_cmd(cmd: str):
    cmd = parse_command(cmd)
    func, result = choose_command(cmd), "Unknown command!"  # default result

    if func:
        result = func(*cmd[1:]) if len(cmd) > 1 else func()  # else part to take into account hello() and show()

    # to prevent exit script if exit function finishes with error
    # also was thinking about how to handle this with exceptions... but decided to leave it as is
    if 'ERROR' in result:
        func = None
    return func, result


def main():
    while True:
        command = None

        # Check if command is not empty
        while not command:
            command = input('Enter command: ')

        # if command in EXIT_COMMANDS:
        #     print("Good bye!")
        #     break

        func, result = handle_cmd(command)

        print(result)

        if func == exit_program:
            break
        print()


if __name__ == '__main__':
    main()
