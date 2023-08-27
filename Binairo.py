import copy
import State


def check_Adjacency_Limit(state: State):
    # check rows
    for i in range(0, state.size):
        for j in range(0, state.size - 2):
            # print("checking ", state.board[i][j].value, state.board[i][j+1].value, state.board[i][j+2].value)
            if (state.board[i][j].value.upper() == state.board[i][j + 1].value.upper() and
                    state.board[i][j + 1].value.upper() == state.board[i][j + 2].value.upper() and
                    state.board[i][j].value != '_'):
                # print("adjacency failed")
                return False
    # check cols
    for j in range(0, state.size):  # cols
        for i in range(0, state.size - 2):  # rows
            # print("checking ", state.board[i][j].value, state.board[i+1][j].value, state.board[i+2][j].value)
            if (state.board[i][j].value.upper() == state.board[i + 1][j].value.upper()
                    and state.board[i + 1][j].value.upper() == state.board[i + 2][j].value.upper()
                    and state.board[i][j].value != '_'):
                # print("adjacency failed")
                return False

    return True


def check_circles_limit(state: State):  # returns false if number of white or black circles exceeds board_size/2
    # check in rows
    for i in range(0, state.size):  # rows
        no_white_row = 0
        no_black_row = 0
        for j in range(0, state.size):  # each col
            # if cell is black or white and it is not empty (!= '__')
            if state.board[i][j].value.upper() == 'W':
                no_white_row += 1
            if state.board[i][j].value.upper() == 'B':
                no_black_row += 1
        if no_white_row > state.size / 2 or no_black_row > state.size / 2:
            # print("whites: ", no_white_row, " blacks: ", no_black_row, "limit: ", state.size / 2)
            # print("circle limit failed")
            return False

    # check in cols
    for j in range(0, state.size):  # cols
        no_white_col = 0
        no_black_col = 0
        for i in range(0, state.size):  # each row
            # if cell is black or white and it is not empty (!= '__')
            if state.board[i][j].value.upper() == 'W':
                no_white_col += 1
            if state.board[i][j].value.upper() == 'B':
                no_black_col += 1
        if no_white_col > state.size / 2 or no_black_col > state.size / 2:
            # print("whites: ", no_white_col, " blacks: ", no_black_col, "limit: ", state.size / 2)
            # print("circle limit failed")
            return False

    return True


def is_unique(state: State):  # checks if all rows are unique && checks if all cols are unique
    # check rows
    for i in range(0, state.size - 1):
        for j in range(i + 1, state.size):
            count = 0
            for k in range(0, state.size):
                if (state.board[i][k].value.upper() == state.board[j][k].value.upper()
                        and state.board[i][k].value != '_'):
                    count += 1
            if count == state.size:
                # print("unique failed")
                return False

    # check cols
    for j in range(0, state.size - 1):
        for k in range(j + 1, state.size):
            count_col = 0
            for i in range(0, state.size):
                if (state.board[i][j].value.upper() == state.board[i][k].value.upper()
                        and state.board[i][j].value != '_'):
                    count_col += 1
            if count_col == state.size:
                # print("unique failed")
                return False

    return True


def is_assignment_complete(state: State):  # check if all variables are assigned or not
    for i in range(0, state.size):
        for j in range(0, state.size):
            if state.board[i][j].value == '_':  # exists a variable which is not assigned (empty '_')
                return False

    return True


def is_consistent(state: State):
    return check_Adjacency_Limit(state) and check_circles_limit(state) and is_unique(state)


def check_termination(state: State):
    return is_assignment_complete(state) and is_consistent(state)


def backTrack(state: State):
    pop_was_successful = True
    finished = False
    queue = []
    state_queue = []

    for i in range(0, state.size):
        for j in range(0, state.size):
            forward_check(state, i, j)

    while not finished:
        [row, col, domain_size] = MRV(state)

        if pop_was_successful:
            old_state = copy.deepcopy(state)

            if domain_size == 1:
                queue.append([row, col, state.board[row][col].domain[0]])
                state_queue.append(old_state)
            else:
                whiteFirst = LCV(state, row, col)

                if whiteFirst:
                    queue.append([row, col, 'w'])
                    queue.append([row, col, 'b'])
                else:
                    queue.append([row, col, 'b'])
                    queue.append([row, col, 'w'])
                state_queue.append(old_state)
                state_queue.append(old_state)

            pop_was_successful = False

        while len(queue) > 0 and not pop_was_successful:
            popped = queue.pop(len(queue) - 1)
            state = copy.deepcopy(state_queue.pop(len(state_queue) - 1))

            state.board[popped[0]][popped[1]].value = popped[2]

            check_lines(state)

            for i in range(0, state.size):
                for j in range(0, state.size):
                    forward_check(state, i, j)

            if is_consistent(state) and arc_consistency(state) and check_failure(state):
                pop_was_successful = True

            else:
                pop_was_successful = False

        if check_termination(state):
            finished = True
            state.print_board()


def forward_check(state: State, i, j):
    if state.board[i][j].value == 'w':
        state.board[i][j].domain = ['w']
    elif state.board[i][j].value == 'b':
        state.board[i][j].domain = ['b']

    if 1 <= i <= state.size - 2:
        if state.board[i][j].value.upper() == state.board[i - 1][j].value.upper() \
                and state.board[i + 1][j].value == '_':

            if state.board[i][j].value.upper() == 'B' and 'b' in state.board[i + 1][j].domain:
                state.board[i + 1][j].domain.remove('b')
            elif state.board[i][j].value.upper() == 'W' and 'w' in state.board[i + 1][j].domain:
                state.board[i + 1][j].domain.remove('w')

    if 1 <= i <= state.size - 2:
        if state.board[i][j].value.upper() == state.board[i + 1][j].value.upper() \
                and state.board[i - 1][j].value == '_':

            if state.board[i][j].value.upper() == 'B' and 'b' in state.board[i - 1][j].domain:
                state.board[i - 1][j].domain.remove('b')
            elif state.board[i][j].value.upper() == 'W' and 'w' in state.board[i - 1][j].domain:
                state.board[i - 1][j].domain.remove('w')

    if i <= state.size - 3:
        if state.board[i][j].value.upper() == state.board[i + 2][j].value.upper() \
                and state.board[i + 1][j].value == '_':

            if state.board[i][j].value.upper() == 'B' and 'b' in state.board[i + 1][j].domain:
                state.board[i + 1][j].domain.remove('b')
            elif state.board[i][j].value.upper() == 'W' and 'w' in state.board[i + 1][j].domain:
                state.board[i + 1][j].domain.remove('w')

    if 1 <= j <= state.size - 2:
        if state.board[i][j].value.upper() == state.board[i][j - 1].value.upper() \
                and state.board[i][j + 1].value == '_':

            if state.board[i][j].value.upper() == 'B' and 'b' in state.board[i][j + 1].domain:
                state.board[i][j + 1].domain.remove('b')
            elif state.board[i][j].value.upper() == 'W' and 'w' in state.board[i][j + 1].domain:
                state.board[i][j + 1].domain.remove('w')

    if 1 <= j <= state.size - 2:
        if state.board[i][j].value.upper() == state.board[i][j + 1].value.upper() \
                and state.board[i][j - 1].value == '_':

            if state.board[i][j].value.upper() == 'B' and 'b' in state.board[i][j - 1].domain:
                state.board[i][j - 1].domain.remove('b')
            elif state.board[i][j].value.upper() == 'W' and 'w' in state.board[i][j - 1].domain:
                state.board[i][j - 1].domain.remove('w')

    if j <= state.size - 3:
        if state.board[i][j].value.upper() == state.board[i][j + 2].value.upper() \
                and state.board[i][j + 1].value == '_':

            if state.board[i][j].value.upper() == 'B' and 'b' in state.board[i][j + 1].domain:
                state.board[i][j + 1].domain.remove('b')
            elif state.board[i][j].value.upper() == 'W' and 'w' in state.board[i][j + 1].domain:
                state.board[i][j + 1].domain.remove('w')

    black_count = 0
    white_count = 0
    for new_i in range(0, state.size):
        if state.board[new_i][j].value.upper() == 'B':
            black_count += 1
        elif state.board[new_i][j].value.upper() == 'W':
            white_count += 1

    if black_count == state.size / 2:
        for new_i in range(0, state.size):
            if state.board[new_i][j].value == '_' and 'b' in state.board[new_i][j].domain:
                state.board[new_i][j].domain.remove('b')
    elif white_count == state.size / 2:
        for new_i in range(0, state.size):
            if state.board[new_i][j].value == '_' and 'w' in state.board[new_i][j].domain:
                state.board[new_i][j].domain.remove('w')

    black_count = 0
    white_count = 0
    for new_j in range(0, state.size):
        if state.board[i][new_j].value.upper() == 'B':
            black_count += 1
        elif state.board[i][new_j].value.upper() == 'W':
            white_count += 1

    if black_count == state.size / 2:
        for new_j in range(0, state.size):
            if state.board[i][new_j].value == '_' and 'b' in state.board[i][new_j].domain:
                state.board[i][new_j].domain.remove('b')
    elif white_count == state.size / 2:
        for new_j in range(0, state.size):
            if state.board[i][new_j].value == '_' and 'w' in state.board[i][new_j].domain:
                state.board[i][new_j].domain.remove('w')

    return


def MRV(state: State):
    domain_size = 2
    row = 0
    col = 0
    for i in range(0, state.size):
        for j in range(0, state.size):
            if state.board[i][j].value == '_' and domain_size >= len(state.board[i][j].domain) > 0:
                domain_size = len(state.board[i][j].domain)
                row = i
                col = j
                if domain_size == 1:
                    return [row, col, domain_size]

    return [row, col, domain_size]


def LCV(state: State, row, col):
    blacks = 0
    whites = 0
    for j in range(0, state.size):
        if state.board[row][j].value.upper() == 'W':
            whites += 1
        elif state.board[row][j].value.upper() == 'B':
            blacks += 1

    for i in range(0, state.size):
        if state.board[i][col].value.upper() == 'W':
            whites += 1
        elif state.board[i][col].value.upper() == 'B':
            blacks += 1

    if whites >= blacks:
        return True

    return False


def check_failure(state: State):
    for i in range(0, state.size):
        for j in range(0, state.size):
            if len(state.board[i][j].domain) == 0:
                return False

    return True


def check_lines(state: State):
    line_filled = False

    for i in range(0, state.size):
        black_count = 0
        white_count = 0
        for j in range(0, state.size):
            if state.board[i][j].value.upper() == 'B':
                black_count += 1
            elif state.board[i][j].value.upper() == 'W':
                white_count += 1

        if black_count == state.size / 2:
            if not line_filled:
                line_filled = fill_line(state, True, False, i, True, False)
            else:
                fill_line(state, True, False, i, True, False)
        elif white_count == state.size / 2:
            if not line_filled:
                line_filled = fill_line(state, True, False, i, False, True)
            else:
                fill_line(state, True, False, i, False, True)

    for j in range(0, state.size):
        black_count = 0
        white_count = 0
        for i in range(0, state.size):
            if state.board[i][j].value.upper() == 'B':
                black_count += 1
            elif state.board[i][j].value.upper() == 'W':
                white_count += 1

        if black_count == state.size / 2:
            if not line_filled:
                line_filled = fill_line(state, False, True, j, True, False)
            else:
                fill_line(state, False, True, j, True, False)
        elif white_count == state.size / 2:
            if not line_filled:
                line_filled = fill_line(state, False, True, j, False, True)
            else:
                fill_line(state, False, True, j, False, True)

    return line_filled


def fill_line(state: State, row, col, number, black, white):
    line_filled = False

    if row:
        if black:
            for j in range(0, state.size):
                if state.board[number][j].value == '_':
                    line_filled = True
                    state.board[number][j].value = 'w'
        elif white:
            for j in range(0, state.size):
                if state.board[number][j].value == '_':
                    line_filled = True
                    state.board[number][j].value = 'b'
    elif col:
        if black:
            for i in range(0, state.size):
                if state.board[i][number].value == '_':
                    line_filled = True
                    state.board[i][number].value = 'w'
        elif white:
            for i in range(0, state.size):
                if state.board[i][number].value == '_':
                    line_filled = True
                    state.board[i][number].value = 'b'

    return line_filled


def arc_consistency(state: State):
    found_inconsistency = True
    while found_inconsistency:
        found_inconsistency = False
        for i in range(0, state.size):
            for j in range(0, state.size - 1):
                if state.board[i][j].value == '_' and state.board[i][j + 1] == '_':
                    for domain1 in state.board[i][j].domain:
                        arc_consistent = False
                        for domain2 in state.board[i][j + 1].domain:
                            temp_state = copy.deepcopy(state)
                            temp_state.board[i][j].value = domain1
                            temp_state.board[i][j + 1].value = domain2
                            if is_consistent(temp_state):
                                arc_consistent = True

                        if not arc_consistent:
                            found_inconsistency = True
                            state.board[i][j].domain.remove(domain1)

                    for domain1 in state.board[i][j + 1].domain:
                        arc_consistent = False
                        for domain2 in state.board[i][j].domain:
                            temp_state = copy.deepcopy(state)
                            temp_state.board[i][j + 1].value = domain1
                            temp_state.board[i][j].value = domain2
                            if is_consistent(temp_state):
                                arc_consistent = True

                        if not arc_consistent:
                            found_inconsistency = True
                            state.board[i][j + 1].domain.remove(domain1)

        for j in range(0, state.size):
            for i in range(0, state.size - 1):
                if state.board[i][j].value == '_' and state.board[i + 1][j] == '_':
                    for domain1 in state.board[i][j].domain:
                        arc_consistent = False
                        for domain2 in state.board[i + 1][j].domain:
                            temp_state = copy.deepcopy(state)
                            temp_state.board[i][j].value = domain1
                            temp_state.board[i + 1][j].value = domain2
                            if is_consistent(temp_state):
                                arc_consistent = True

                        if not arc_consistent:
                            found_inconsistency = True
                            state.board[i][j].domain.remove(domain1)

                    for domain1 in state.board[i + 1][j].domain:
                        arc_consistent = False
                        for domain2 in state.board[i][j].domain:
                            temp_state = copy.deepcopy(state)
                            temp_state.board[i + 1][j].value = domain1
                            temp_state.board[i][j].value = domain2
                            if is_consistent(temp_state):
                                arc_consistent = True

                        if not arc_consistent:
                            found_inconsistency = True
                            state.board[i + 1][j].domain.remove(domain1)

    return True
