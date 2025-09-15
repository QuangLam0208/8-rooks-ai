def placement_cost_goal(state, row, col, goal):
    '''
    Tính chi phí đặt quân ở (row, col) so với trạng thái đích goal.
    state: danh sách các cột đã đặt
    row: hàng hiện tại
    col: cột hiện tại
    goal: trạng thái đích dạng list
    '''

    if goal is None:
        return 1
    
    target_col = goal[row]
    if col == target_col:
        return 1
    else:
        return abs(col - target_col) + 1