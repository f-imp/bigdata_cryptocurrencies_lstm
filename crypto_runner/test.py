#da cancellare prima di consegnare

from decimal import Decimal


def formatNumber(number):
    if number<=0.0001:
        return (f"{Decimal(number):.2E}")
    else:
        return number


dec1=0.000800000
dec2=0.0000800000


asd=[1,2]

table=f"""\\begin{{frame}}{{Results - Wilcoxon}}
\\begin{{block}}{{Wilcoxon signed-rank test}}
\\begin{{table}}[]
    \centering
    \\begin{{tabular}}{{c?c|c|c|c}}
          & ST & ST-i & MT & MT-i \\\\
         \specialrule{{.1em}}{{.05em}}{{.05em}}
         ST &  & {formatNumber(asd[0])} & {formatNumber(asd[1])} & {2:.4f}\\\\
         ST-i & {0:.4f} & & {3:.4f} & {4:.4f}\\\\
         MT & {1:.4f} & {3:.4f} & & {5:.4f}\\\\
         MT-i & {2:.4f} & {4:.4f} & {5:.4f} &
    \end{{tabular}}
\end{{table}}
\end{{block}}
\end{{frame}}"""



print(table)



