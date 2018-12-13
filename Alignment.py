import numpy as np
import sys

s1 = input("Enter Sequence 1:")
s2 = input("Enter Sequence 2:")

match=int(input("Enter Match Score: "))
mmatch=int(input("Enter Mismatch Score: "))
indel = int(input("Enter Gap Score: "))
alignment=int(input("Enter Alignment (1 for Global Alignment and 2 for Local Alignment): "))
subst_matrix = {
'A': {'A': match,'C':mmatch,'G':mmatch,'T':mmatch}, 
'C': {'A':mmatch,'C': match,'G':mmatch,'T':mmatch}, 
'G': {'A':mmatch,'C':mmatch,'G': match,'T':mmatch},
'T': {'A':mmatch,'C':mmatch,'G':mmatch,'T': match},
}

s_matrix = np.ndarray(shape=(len(s1)+1,len(s2)+1), dtype=int)
s_matrix.fill(0)
bt_matrix = np.ndarray(shape=(len(s1)+1,len(s2)+1), dtype=int)
bt_matrix.fill(3)
if alignment == 1:
    for i in range(len(s1)+1):
        for j in range(len(s2)+1):
            if i==0 and j==0:
                continue
            bs1 = s1[i-1] 
            bs2 = s2[j-1] 
            scores = [-999,-999,-999]
            if i==0 and j > 0:
                scores[0]=j*indel
            if j==0 and i > 0:
                scores[2]=i*indel
            if j > 0 and i > 0:
                if bs1==bs2:
                    scores[1]=max(s_matrix[i-1,j-1]+match,s_matrix[i-1,j]+indel,s_matrix[i,j-1]+indel)
                if bs1 != bs2 and (s_matrix[i-1,j-1]+mmatch) >= (s_matrix[i-1,j]+indel) and (s_matrix[i-1,j-1]+mmatch) >= (s_matrix[i,j-1]+indel):
                    scores[1]=s_matrix[i-1,j-1]+mmatch
                if bs1 != bs2 and (s_matrix[i-1,j]+indel) >= (s_matrix[i-1,j-1]+mmatch) and (s_matrix[i-1,j]+indel) >= (s_matrix[i,j-1]+indel):
                    scores[2]=s_matrix[i-1,j]+indel
                if bs1 != bs2 and (s_matrix[i,j-1]+indel) >= (s_matrix[i-1,j-1]+mmatch) and (s_matrix[i,j-1]+indel) >= (s_matrix[i-1,j]+indel):
                    scores[0]=s_matrix[i,j-1]+indel
            best = max(scores)
            s_matrix[i,j]=best
            for k in range(3):
                if scores[k] == best:
                    bt_matrix[i,j] = k
                    
    print("Dynamic programming matrix:")
    print(s_matrix)
    print("\nBack pointers:")
    print(bt_matrix)
    align1 = ""
    align2 = ""
    i=len(s1)
    j=len(s2)
    while i>0 or j>0:
        if bt_matrix[i,j] == 0: 
            align1 += "-"
            align2 += s2[j-1]
            j -= 1
        if bt_matrix[i,j] == 1:
            align1 += s1[i-1]
            align2 += s2[j-1]
            i -= 1
            j -= 1
        if bt_matrix[i,j] == 2:
            align1 += s1[i-1]
            align2 += "-"
            i -= 1
    align1 = align1[::-1]
    align2 = align2[::-1]
    print("\nOptimal Alignment:")
    print(align1)
    print(align2)
    print("Best Score: ",s_matrix[len(s1)][len(s2)])
