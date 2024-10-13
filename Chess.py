'''
    **** CHESS GAME ****

       ** Code By
                AKRAM SHAIK **
'''
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
# import random as rd


def color_change(c1, c2):
    global color1, color2
    color1 = c1
    color2 = c2
    for i in b_dict:
        button_colour(i)


def button_colour(bt):
    global color1, color2
    r, c, cp = get_r_c_p(bt)
    bg_color1 = color1 if (r % 2 == 0 and c % 2 == 0) or (r % 2 != 0 and c % 2 != 0) else color2
    b_dict[bt].config(bg=bg_color1)


def move_info(moves, same_color):
    for i in moves:
        b_dict[i]['bg'] = 'orange'
        if i not in same_color and i not in empty:
            b_dict[i]['bg'] = 'orange red'


def piece_change(dr):
    global path, Main_Path, photo1, k_dict
    path = Main_Path + dr
    photo1 = PhotoImage(file=path + 'blank' + '.png')
    for i in range(1, 9):
        for j in range(1, 9):
            b = 'b' + str(i) + str(j)
            photo = 'p' + str(i) + str(j)
            if i == 1 or i == 8:
                img = path + str(i) + str(j) + '.png'
            elif i == 2 or i == 7:
                img = path + 'pawn' + str(i) + '.png'
            else:
                img = path + 'blank' + '.png'
            p_dict[photo] = PhotoImage(file=img)
            b_dict[b]['image'] = p_dict[photo]
    for i in empty:
        kill(i)
    for i in k_dict.values():
        i[1]['image'] = p_dict[i[0]]


def get_r_c_p(bt):
    d = b_dict[bt].grid_info()
    r, c = d['row'], d['column']
    cp = (r * 8 - 8) + c
    return r, c, cp


def kill(piece):
    global x1, y1, x2, y2, b_dict, k_dict
    if (piece not in empty and count == 2) or ((piece[1] == '1' or piece[1] == '2' or piece[1] == '7' or piece[1] == '8') and piece in empty and pg == 'pg'):
        if piece in b_pieces or (piece[1] == '1' or piece[1] == '2'):
            if x1 > 240:
                x1 = 7
                y1 += 64
            k_dict['k'+str(x1)+str(y1)] = Button(l_frame, width=55, height=55, bg='gold', image=b_dict[piece]['image'])
            k_dict['k'+str(x1)+str(y1)].place(x=x1, y=y1)
            k_dict['k' + str(x1) + str(y1)] = ('p' + piece[1:3], k_dict['k'+str(x1)+str(y1)])
            x1 += 62
        elif piece in w_pieces or (piece[1] == '7' or piece[1] == '8'):
            if x2 > 240:
                x2 = 2
                y2 += 64
            k_dict['k'+str(x2)+str(y2)] = Button(r_frame, width=55, height=55, bg='gold', image=b_dict[piece]['image'])
            k_dict['k' + str(x2) + str(y2)].place(x=x2, y=y2)
            k_dict['k' + str(x2) + str(y2)] = ('p' + piece[1:3], k_dict['k' + str(x2) + str(y2)])
            x2 += 62

    b_dict[piece]['image'] = photo1
    b_div_list[5].remove(piece) if piece in b_div_list[5] else None
    w_pieces.remove(piece) if piece in w_pieces else None
    b_pieces.remove(piece) if piece in b_pieces else None


def move(a, b_prev, m):
    global count, start, movable_p, del_img
    r, c, cp1 = get_r_c_p(a)
    r1, c1, cp2 = get_r_c_p(b_prev)
    if (a not in empty or (a in empty and (a[1] == '1' or a[1] == '2' or a[1] == '7' or a[1] == '8'))) and m == 'm':
        del_pieces[a] = b_dict[a]
        del_img = b_dict[a]['image']
        kill(a)
        empty.append(a)
    elif a in empty and (a[1] == '1' or a[1] == '2' or a[1] == '7' or a[1] == '8') and (m == 'u' or m == 'un') and a in del_pieces:
        kill(a)
        empty.remove(a)
        b_dict[a] = del_pieces[a]
        del del_pieces[a]
        if a not in empty:
            b_dict[a]['image'] = del_img
            del_img = None
            b_pieces.append(a) if a[1] == '1' or a[1] == '2' else None
            w_pieces.append(a) if a[1] == '7' or a[1] == '8' else None
            b_div_list[5].append(a) if a[1] == '2' or a[1] == '7' else None

    b_dict[b_prev].grid(row=r, column=c)
    b_dict[a].grid(row=r1, column=c1)
    button_colour(b_prev)
    button_colour(a)
    b_position[cp1], b_position[cp2] = b_prev, a

    if m == 'un':
        count = 0
        start = start + 2 if start == 0 else start - 2
        if movable_p:
            if (movable_p[0] in b_pieces and b_prev in b_pieces) or (movable_p[0] in w_pieces and b_prev in w_pieces):
                pass
            else:
                movable_p = []

    rk = -1 if (m == 'u' or m == 'un') else 1
    if b_prev in cas_dict:
        cas_dict[b_prev] += rk


def king(a, p_color):
    global n1, movable_p, start, count, n
    selected1 = []
    r, c, cp1 = get_r_c_p(a)
    for r2 in range(r - 1, r + 2):
        for c2 in range(c - 1, c + 2):
            cp = (r2 * 8 - 8) + c2
            if r2 not in range(1, 9) or c2 not in range(1, 9) or b_position[cp] in p_color:
                continue
            selected1.append(b_position[cp])
    if cp1 == 5 or cp1 == 61:
        for i in range(2):
            if (b_position[cp1] in b_div_list[4] and cas_dict[b_position[cp1]] == 0 and ((cp1 == 5 and bk2 == 0) or (cp1 == 61 and wk2 == 0))) and \
                b_position[cp1 + 1 * ((-1) ** i)] in empty and b_position[cp1 + 2 * ((-1) ** i)] in empty and \
                ((b_position[cp1 + 3 * ((-1) ** i)] in b_div_list[0] and cas_dict[b_position[cp1 + 3 * ((-1) ** i)]] == 0) or
                (b_position[cp1 - 3] in empty and b_position[cp1 - 4] in b_div_list[0] and cas_dict[b_position[cp1 - 4]] == 0)):
                selected1.append(b_position[cp1 + 2 * ((-1) ** i)])

    n1 += 1
    if n1 == 1:
        n1 = 2
        movable_p1 = movable_p
        movable_p = []
        st, cnt, n2 = start, count, n + 1
        select2, k3, p3, p_s3 = search_check(a, p_color)
        start, count, n = st, cnt, n2 - 1
        movable_p = movable_p1
        for j in selected1.copy():
            movable_p = []
            st, cnt, n2, a1 = start, count, n + 1, a
            del_pieces1 = {}
            j1 = ' '
            if j in del_pieces and j in empty:
                del_pieces1[j] = del_pieces[j]
                j1 = j
                empty.remove(j)
                del del_pieces[j]
            move(j, a1, 'm')
            # print('m4')
            select1, k1, p1, p_s1 = search_check('b15', b_pieces)
            if k1 != 'b15':
                movable_p = []
                select1, k1, p1, p_s1 = search_check('b85', w_pieces)
            move(j, a1, 'u')
            # print('u4')
            if j1 == j and j in del_pieces1:
                del_pieces[j] = del_pieces1[j]
                empty.append(j1)
                kill(j1)
            start, count, n, a = st, cnt, n2 - 1, a1
            movable_p = movable_p1
            selected1.remove(j) if j in select2 or k1 == a else None
        n1 = 0
    if (cp1 == 5 or cp1 == 61) and (b_position[cp1 + 2] or b_position[cp1 - 2] in selected1):
        if b_position[cp1 + 2] in selected1 and b_position[cp1 + 1] not in selected1:
            selected1.remove(b_position[cp1 + 2])
        if b_position[cp1 - 2] in selected1 and b_position[cp1 - 1] not in selected1:
            selected1.remove(b_position[cp1 - 2])

    return selected1


def rook_bishop(a, p_color, selc):
    selected = []
    r, c, cp = get_r_c_p(a)
    for r3, c3 in selc:
        r2, c2 = r + r3, c + c3
        while 0 < r2 < 9 and 0 < c2 < 9:
            cp = (r2 * 8 - 8) + c2
            if b_position[cp] in p_color:
                break
            selected.append(b_position[cp])
            if b_position[cp] not in empty:
                break
            r2, c2 = r2 + r3, c2 + c3

    return selected


def knight(a, p_color):
    selected = []
    r, c, cp2 = get_r_c_p(a)
    for r3, c3 in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
        r2, c2 = r + r3, c + c3
        cp = (r2 * 8 - 8) + c2
        if r2 not in range(1, 9) or c2 not in range(1, 9) or b_position[cp] in p_color:
            continue
        selected.append(b_position[cp])

    return selected


def queen(a, p_color):
    selected = rook_bishop(a, p_color, rook_selc)
    select1 = rook_bishop(a, p_color, bishop_selc)
    selected.extend(select1)
    return selected


def pawn(a):
    selected = []
    r, c, cp1 = get_r_c_p(a)
    r3 = [r + 1, r + 2] if a[1] == '2' else [r - 1, r - 2]
    for r2 in r3:
        for c2 in range(c - 1, c + 2):
            cp1 = (r2 * 8 - 8) + c2
            if 0 < r2 < 9 and 0 < c2 < 9 and ((((b_position[cp1] in b_pieces and a[1] == '7') or
               (b_position[cp1] in w_pieces and a[1] == '2')) and c2 != c and
               r2 == r3[0]) or (b_position[cp1] in empty and c2 == c and (r2 == r3[0] or (r2 == r3[1] and
               ((r == 2 and b_position[cp1 - 8] in empty) or (r == 7 and b_position[cp1 + 8] in empty)))))):
                selected.append(b_position[cp1])
    return selected


def search_check(king, k_color):
    select = []
    global selected, count, start, n
    k, p, p_s = ' ', ' ', []
    s1 = [i for i in queen(king, k_color) if i not in empty and i not in b_div_list[1]]
    s2 = [j for j in knight(king, k_color) if j in b_div_list[1]]
    s1.extend(s2)
    for m in s1:
        count, selected, n = 0, [], 1
        start = 2 if m[1] == '1' or m[1] == '2' else 0
        click(m)
        n = 0
        select.extend(selected)
        if king in selected:
            k = king
            p = m
            p_s = selected

    return select, k, p, p_s


def click(a):
    print(a)
    global count, start, b_prev, selected, n, piece_info, piece_info2, piece_info1, temp
    global bk2, wk2, movable_p, p2, p_s2, rem_moves, k_selected, ak, au, b_prevu
    count += 1
    start += 1
    if movable_p != [] and a not in movable_p and count == 1 and n == 0:
        selected = []
        count = 0
        start -= 1
        print('Not Movable')
        messagebox.showerror('INFO', 'KING In CHECK')
    else:
        print('Movable')
        if a in b_pieces:
            piece_info = b_pieces
            ak = 'b15'
        elif a in w_pieces:
            piece_info = w_pieces
            ak = 'b85'
        if b_prev in b_pieces:
            piece_info1 = b_pieces
        elif b_prev in w_pieces:
            piece_info1 = w_pieces

        for i in selected:
            button_colour(i)
        b_prev1, a1 = b_prev, a
        if count == 2 and (a != 'b15' or a != 'b85'):
            temp = start
            s = selected
            if a in selected and (b_prev != 'b15' and b_prev != 'b85'):
                r, c, cp = get_r_c_p(a)
                move(a, b_prev, 'm')
                # print('m1')
                if b_prev in b_div_list[5] and (r == 1 or r == 8):
                    selc = StringVar()
                    piece_slec = ttk.Combobox(chess, width=10, textvariable=selc, state='readonly')
                    piece_slec['values'] = ('Queen', 'Rook', 'Bishop', 'Knight')
                    piece_slec.grid(row=r, column=c)

                    def selc_piece(arg):
                        g = selc.get()
                        sel = {'Queen': 3, 'Rook': 0, 'Bishop': 2, 'Knight': 1}
                        b_div_list[sel[g]].append(b_prev1)
                        b_div_list[5].remove(b_prev1)
                        r1 = 1 if r == 8 else 8
                        b_dict[b_prev1]['image'] = p_dict['p'+str(r1)+str(sel[g]+1)]
                        # b_dict[b_prev1].config(image=p_dict['p'+str(r1)+str(sel[g]+1)])
                        piece_slec.grid_forget()
                    piece_slec.bind('<<ComboboxSelected>>', selc_piece)
                start = 0 if start == 4 else start
            elif a in selected and (b_prev == 'b15' or b_prev == 'b85'):
                r, c, cp1 = get_r_c_p(a)
                r1, c1, cp2 = get_r_c_p(b_prev)
                if (cp2 - cp1) == 2 or (cp1 - cp2) == 2:
                    move(a, b_prev, 'm')
                    if cp1 < cp2:
                        move(b_position[cp1 + 1], b_position[cp1 - 2], 'castling')
                    elif cp1 > cp2:
                        move(b_position[cp1 - 1], b_position[cp1 + 1], 'castling')
                else:
                    move(a, b_prev, 'm')
                start = 0 if start == 4 else start
                # movable_p = []
            else:
                start -= 2
                if a != b_prev1:
                    messagebox.showerror('INFO', 'Invalid Move')
            count, selected = 0, []

            n += 1
            if n == 1:
                bk2, wk2 = 0, 0
                movable_p = []
                rem_moves = []
                temp = start
                p_i = piece_info1
                b_prev1, a1 = b_prev, a
                select, k, p2, p_s2 = search_check('b15', b_pieces)
                if k != 'b15':
                    select, k, p2, p_s2 = search_check('b85', w_pieces)
                selected = [' ']
                piece_info2 = []
                if k in select:
                    selected = []
                    if k == 'b15':
                        v = 'Black King CHECK'
                        piece_info2 = b_pieces
                        bk2 = 1
                    else:
                        v = 'White King CHECK'
                        piece_info2 = w_pieces
                        wk2 = 1
                    print(v)
                    # b_dict[k]['bg'] = 'red'
                    # messagebox.showinfo('INFO', v)
                    k_selected = king(k, piece_info2)
                    selected = k_selected

                check = 'no checkmate'
                if k in select:
                    check = ' '
                    movable_p.append(k) if k_selected != [] else None
                    movable_p1 = movable_p
                    for m in piece_info2:
                        count, selected = 0, []
                        movable_p = []
                        start = 2 if m[1] == '1' or m[1] == '2' else 0
                        st, cnt, ak1, pi, n2 = start, count, ak, piece_info, n+1
                        click(m)
                        start, count, ak, piece_info, n = st, cnt, ak1, pi, n2-1
                        common = list(set(p_s2).intersection(set(selected)))
                        common.append(p2) if p2 in selected else None
                        if common:
                            for i in common:
                                movable_p = []
                                st, cnt, ak1, pi, n2 = start, count, ak, piece_info, n+1
                                move(i, m, 'm')
                                # print('m2')
                                select1, k1, p1, p_s1 = search_check('b15', b_pieces)
                                if k1 != 'b15':
                                    movable_p = []
                                    select1, k1, p1, p_s1 = search_check('b85', w_pieces)
                                move(i, m, 'u')
                                # print('u2')
                                start, count, ak, piece_info, n = st, cnt, ak1, pi, n2-1
                                if k1 == k and k_selected == []:
                                    check = ' '
                                elif k1 != k:
                                    check = 'no checkmate'
                                    if m not in movable_p1 or i == p2:
                                        movable_p1.append(m)
                                elif k1 == k:
                                    rem_moves.append(i)
                    movable_p = movable_p1
                if k in p_i and check == 'no checkmate' and b_prev1 not in b_div_list[4] and a1 in s:
                    move(a1, b_prev1, 'u')
                    # print('u1')
                    messagebox.showerror('INFO', 'Invalid Move')
                    temp = temp + 2 if temp == 0 else temp - 2
                if check == ' ' and not k_selected:
                    if k[1] == 1:
                        win = "WHITE\'s Won the GAME "
                    else:
                        win = "BLACK\'s Won the GAME "
                    messagebox.showinfo('INFO', 'CheckMate \n \n GAME OVER \n \n' + win)
                    exit()
                elif bk2 == 1 or wk2 == 1:
                    messagebox.showinfo('INFO', v)
                n = 0
            au, b_prevu = a1, b_prev1
            start, count, selected = temp, 0, []
            k_selected = []
        elif (start == 1 and a in w_pieces) or (start == 3 and a in b_pieces):
            if a in b_div_list[0]:
                selected = rook_bishop(a, piece_info, rook_selc)
            elif a in b_div_list[1]:
                selected = knight(a, piece_info)
            elif a in b_div_list[2]:
                selected = rook_bishop(a, piece_info, bishop_selc)
            elif a in b_div_list[3]:
                selected = queen(a, piece_info)
            elif a in b_div_list[4]:
                if count == 2:
                    count, selected = 0, []
                    messagebox.showerror('INFO', 'Invalid Move')
                else:
                    st, cnt, n2, pi = start, count, n+1, piece_info
                    a2 = 'b15' if a == 'b85' else 'b85'
                    a2piece = w_pieces if a2 == 'b85' else b_pieces
                    selected2 = king(a, piece_info)
                    selected3 = king(a2, a2piece)
                    for i in selected3:
                        selected2.remove(i) if i in selected2 else None
                    selected = selected2
                    start, count, n, piece_info = st, cnt, n2-1, pi
            elif a in b_div_list[5]:
                selected = pawn(a)
            else:
                print('Blank')
        elif start == 1 or start == 3:
            start -= 1
            count -= 1
            # messagebox.showerror('INFO', 'Invalid Move')
        b_prev = a1
        if count == 1 and n == 0:
            movable_p.append(ak) if k_selected else None
            s = selected
            movable_p1 = movable_p
            movable_p = []
            for i in s.copy():
                # print(i,a1,ak)
                st, cnt, ak1, pi, n2 = start, count, ak, piece_info, n+1
                movable_p = []
                move(i, a1, 'm')
                # print('m3')
                select1, k1, p1, p_s1 = search_check(ak, piece_info)
                move(i, a1, 'u')
                # print('u3')
                start, count, ak, piece_info, n = st, cnt, ak1, pi, n2-1
                if k1 == ak1:
                    s.remove(i)
            selected = s
            movable_p = movable_p1
            if movable_p:
                for j in selected.copy():
                    if (j not in p_s2 and j != p2 and a not in b_div_list[4]) or (j in rem_moves):
                        selected.remove(j)
            if selected == []:
                count -= 1
                start -= 1
            for i in b_dict.keys():
                button_colour(i)
            move_info(selected, piece_info)
        print(selected)
        b_prev = a1
        # if start == 2:
        #     r = rd.choice(selected)
        #     print('random',r)
        #     click(r)



def Save_Game():
    f = open("prev_game.txt", "w")
    f.write(str(b_position) + '\n')
    f.write(str(w_pieces) + '\n')
    f.write(str(b_pieces) + '\n')
    f.write(str(b_div_list) + '\n')
    f.write(str(empty) + '\n')
    f.write(str(list(del_pieces.keys())) + '\n')
    f.write(str(selected) + '\n')
    f.write(str(movable_p) + '\n')
    f.write(str(p_s2) + '\n')
    f.write(p2 + '\n')
    values = str(start-count) + ',' + str(n) + ',' + str(bk2) + ',' + str(wk2)
    f.write(values + '\n')
    f.write(au + ',' + b_prevu + '\n')
    f.close()


def Previous_Game():
    def prev_g(op):
        global w_pieces, b_pieces, b_div_list, b_position, empty, del_pieces, selected, movable_p, p_s2, p2
        global count, start, n, a, b_prev, b_dict, pg, l_frame, r_frame, x1, y1, x2, y2, bk2, wk2, au, b_prevu
        prev_game = op
        pg = 'pg'
        au, b_prevu = ' ', ' '
        if prev_game == 'y' or prev_game == 'Y':
            x1, y1, x2, y2 = 7, 217, 2, 217
            l_frame = Frame(chess2, width=255, height=675, bg='gold')
            l_frame.place(x=0, y=0)
            r_frame = Frame(chess2, width=255, height=675, bg='gold')
            r_frame.place(x=1025, y=0)
            f = open("prev_game.txt", "r")
            b_position = eval(f.readline())
            w_pieces = eval(f.readline())
            b_pieces = eval(f.readline())
            b_div_list = eval(f.readline())
            empty = eval(f.readline())
            del_keys = eval(f.readline())
            for i in del_keys:
                del_pieces[i] = b_dict[i]
            selected = eval(f.readline())
            movable_p = eval(f.readline())
            p_s2 = eval(f.readline())
            p2 = f.readline()
            start, n, bk2, wk2 = tuple(int(i) for i in f.readline().split(','))
            a, b_prev = tuple(f.readline().split(','))
            count = 0
            f.close()
            for i in range(1, 9):
                for j in range(1, 9):
                    cp = (i * 8 - 8) + j
                    b_dict[b_position[cp]].grid(row=i, column=j)
                    button_colour(b_position[cp])
            for i in empty:
                kill(i)
            pg = ' '

    new_g = messagebox.askyesno('New Game', 'Do You Want To Continue Last Saved Game ?',)
    prev_g('y') if new_g else None

def New_Game():
    global Main_Path, path, b_dict, p_dict, del_pieces, w_pieces, b_pieces, empty, b_div_list, photo1, l_frame, r_frame
    global count, start, n, n1, bk2, wk2, x1, y1, x2, y2, b_position, selected, movable_p, rem_moves
    global p_s2, k_selected, b_prev, au, b_prevu, p2, cas_dict
    b_dict, p_dict, del_pieces, b_position = {}, {}, {}, {}
    w_pieces, b_pieces, empty = [], [], []
    b_div_list = [[], [], [], [], [], []]
    count, start, n, n1 = 0, 0, 0, 0
    bk2, wk2, x1, y1, x2, y2 = 0, 0, 7, 217, 2, 217
    cas_dict = {'b11': 0, 'b18': 0, 'b81': 0, 'b88': 0, 'b15': 0, 'b85': 0}
    selected, movable_p, rem_moves, p_s2, k_selected = [], [], [], [], []
    b_prev, au, b_prevu, p2 = ' ', ' ', ' ', ' '
    l_frame = Frame(chess2, width=255, height=675, bg='gold')
    l_frame.place(x=0, y=0)
    r_frame = Frame(chess2, width=255, height=675, bg='gold')
    r_frame.place(x=1025, y=0)
    for i in range(1, 9):
        for j in range(1, 9):
            b = 'b' + str(i) + str(j)
            photo = 'p' + str(i) + str(j)
            cp = (i * 8 - 8) + j
            bg_color = color1 if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0) else color2
            if i == 1 or i == 8:
                img = path + str(i) + str(j) + '.png'
                if j <= 5:
                    b_div_list[j - 1].append(b)
                elif j > 5:
                    b_div_list[8 - j].append(b)
            elif i == 2 or i == 7:
                img = path + 'pawn' + str(i) + '.png'
                b_div_list[5].append(b)
            else:
                img = path + 'blank' + '.png'
                empty.append(b)
            b_pieces.append(b) if i == 1 or i == 2 else None
            w_pieces.append(b) if i == 7 or i == 8 else None
            p_dict[photo] = PhotoImage(file=img)
            b_dict[b] = Button(chess, width=90, height=78, bg=bg_color, activebackground='sky blue', image=p_dict[photo],
                               command=lambda arg=b: click(arg))
            b_dict[b].grid(row=i, column=j)
            b_position[cp] = b


chess2 = Tk()
chess2.title('CHESS')
chess2.geometry('1490x700')

count, start, n, n1 = 0, 0, 0, 0
bk2, wk2, x1, y1, x2, y2 = 0, 0, 7, 217, 2, 217
rook_selc = [(-1, 0), (0, -1), (0, 1), (1, 0)]
bishop_selc = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
knight_selec = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
cas_dict = {'b11': 0, 'b18': 0, 'b81': 0, 'b88': 0, 'b15': 0, 'b85': 0}
selected, movable_p, rem_moves, p_s2, k_selected = [], [], [], [], []
b_dict, p_dict, del_pieces, b_position, k_dict = {}, {}, {}, {}, {}
w_pieces, b_pieces, empty = [], [], []
b_div_list = [[], [], [], [], [], []]
b_prev, au, b_prevu, p2, pg = ' ', ' ', ' ', ' ', ' '
color1 = 'light green'
color2 = 'white'
Main_Path = str("D:\\Programming\\Python Programming\\PyCharm\\Chess\\ChessPieces1\\")
path = Main_Path + '60x60\\'
photo1 = PhotoImage(file=path + 'blank' + '.png')
del_img = None

l_frame = Frame(chess2, width=255, height=675, bg='gold')
l_frame.place(x=0, y=0)
chess = Frame(chess2, width=675, height=675, bg='gold')
chess.place(x=256, y=0)
r_frame = Frame(chess2, width=255, height=675, bg='gold')
r_frame.place(x=1025, y=0)

Menu_bar = Menu(chess2)

File = Menu(Menu_bar)
Menu_bar.add_cascade(label='File', menu=File)
File.add_command(label='New Game', command=lambda: New_Game())
File.add_command(label='Previous Game', command=lambda: Previous_Game())
File.add_command(label='Save Game', command=lambda: Save_Game())

Edit = Menu(Menu_bar)
Menu_bar.add_cascade(label='Edit', menu=Edit)
Edit.add_command(label='Undo', command=lambda: move(au, b_prevu, 'un'))
Change_Board = Menu(Edit)
Edit.add_cascade(label='Change Board', menu=Change_Board)
Change_Board.add_command(label='Light Green and White', command=lambda: color_change('light green', 'white'))
Change_Board.add_command(label='Sky Blue and White', command=lambda: color_change('sky blue', 'white'))
Change_Board.add_command(label='Green and Yellow', command=lambda: color_change('green', 'yellow'))
Change_Board.add_command(label='Sky Blue and light Green', command=lambda: color_change('sky blue', 'light green'))
Change_Pieces = Menu(Edit)
Edit.add_cascade(label='Change Pieces', menu=Change_Pieces)
Change_Pieces.add_command(label='50x50', command=lambda: piece_change('50x50\\'))
Change_Pieces.add_command(label='60x60', command=lambda: piece_change('60x60\\'))
Change_Pieces.add_command(label='100x100', command=lambda: piece_change('100x100\\'))
Change_Pieces.add_command(label='style1 70', command=lambda: piece_change('style1 70\\'))
Change_Pieces.add_command(label='style1 80', command=lambda: piece_change('style1 80\\'))
Change_Pieces.add_command(label='style2', command=lambda: piece_change('style2\\'))
chess2.config(menu=Menu_bar)

New_Game()

chess2.mainloop()
