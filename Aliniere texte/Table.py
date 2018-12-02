# t1=["G","A","T","T","A","C","A"]
# t2=["G","C","A","T","G","C","U"]
# pgap=-1
# pxy=-1

def Build_Table(text1, text2, gap_penalty, mismatch_penalty):
    n=len(text1)
    m=len(text2)
    table=[]
    for i in range (m+1):
        row=[]
        for j in range(n+1):
            row.append(0)
        table.append(row)
    for i in range(n+1):
        table[i][0]=i*gap_penalty
    for j in range(m+1):
        table[0][j]=j*gap_penalty
    for i in range(1,n+1):
        for j in range(1,m+1):
            if text1[i-1]==text2[j-1]:
                table[i][j]=table[i-1][j-1]+1
            else:
                table[i][j] = max(table[i - 1][j - 1] + mismatch_penalty, table[i - 1][j] + gap_penalty, table[i][j-1] + gap_penalty)
    return table


# t=Build_Table(t1,t2,pgap,pxy)
# for row in t:
#     print(row,"\n")


