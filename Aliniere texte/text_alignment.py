t1 = ["A", "G", "G", "G", "C", "T"]
t2 = ["A", "G", "G", "C", "A"]
pgap = -2
pxy = -3


def build_table(text1, text2, gap_penalty, mismatch_penalty):
    m = len(text1)
    n = len(text2)

    table = []
    for i in range(n + m + 1):
        row = []
        for j in range(n + m + 1):
            row.append(0)
        table.append(row)

    for i in range(n + m + 1):
        table[i][0] = i * pgap
    for j in range(n + m + 1):
        table[0][j] = j * pgap

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j - 1] + pxy,
                                  table[i - 1][j] + pgap,
                                  table[i][j - 1] + pgap)

    # reconstructie
    max_length = n + m
    i = m
    j = n
    xpos = max_length
    ypos = max_length
    xans = [-1 for x in range(max_length + 1)]
    yans = [-1 for x in range(max_length + 1)]

    while not (i == 0 or j == 0):
        if text1[i - 1] == text2[j - 1]:
            xans[xpos] = text1[i - 1]
            yans[ypos] = text2[j - 1]
            xpos = xpos - 1
            ypos = ypos - 1
            i = i - 1
            j = j - 1
        elif table[i - 1][j - 1] + pxy == table[i][j]:
            xans[xpos] = text1[i - 1]
            yans[ypos] = text2[j - 1]
            xpos = xpos - 1
            ypos = ypos - 1
            i = i - 1
            j = i - 1
        elif table[i - 1][j] + pgap == table[i][j]:
            xans[xpos] = text1[i - 1]
            yans[ypos] = '_'
            xpos = xpos - 1
            ypos = ypos - 1
            i = i - 1
        elif table[i][j - 1] + pgap == table[i][j]:
            xans[xpos] = '_'
            yans[ypos] = text2[j - 1]
            xpos = xpos - 1
            ypos = ypos - 1
            j = j - 1

    while xpos > 0:
        if i > 0:
            i = i - 1
            xans[xpos] = text1[i]
            xpos = xpos - 1
        else:
            xans[xpos] = '_'
            xpos = xpos - 1

    while ypos > 0:
        if j > 0:
            j = j - 1
            yans[ypos] = text2[j]
            ypos = ypos - 1
        else:
            yans[ypos] = '_'
            ypos = ypos - 1

    id = 1
    for i in range(max_length, 0, -1):
        if yans[i] == '_' and xans[i] == '_':
            id = i + 1
            break

    print(xans[id:])
    print(yans[id:])


build_table(t1, t2, pgap, pxy)

