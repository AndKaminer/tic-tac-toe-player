def load_agent_value_function(load_file: str) -> dict[tuple, float]:
    output: dict[tuple, float] = {}
    with open(load_file, 'r') as lf:
        lines: list[str] = lf.readlines()
        statestr: str = None
        valuestr: str = None
        for line in lines:
            statestr, valuestr = line.split(':')
            state: tuple = tuple([ str_to_bool(el) for el in statestr.split(',') ])
            value: float = float(valuestr)

            output[state] = value

    return output

def str_to_bool(num: str) -> bool:
    if num == '1':
        return True
    elif num == '-1':
        return False
    elif num == '0':
        return None
    else:
        raise Exception("Invalid string")

def gen_all_states() -> list[tuple]:
    output: list[tuple] = []

    def rec_helper(i, l):
        if i >= 9:
            output.append(tuple(l))
            return

        l.append(True)
        rec_helper(i+1, l)
        l.pop()

        l.append(False)
        rec_helper(i+1, l)
        l.pop()

        l.append(None)
        rec_helper(i+1, l)
        l.pop()

    rec_helper(0, [])

    return output

