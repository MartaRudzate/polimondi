a = [0, 0, 2, 2, 0, 0, 8, 14, 0, 0,
     70, 124, 0, 0, 722, 1314, 0, 0, 8220, 15272,
     0, 0, 99820, 187692, 0, 0, 1265204, 2399784, 0, 0,
     16547220, 31592878, 0, 0, 221653776, 425363952, 0, 0, 3025553180, 5830034720,
     0, 0, 41931984034, 81072032060, 0, 0, 588491482334, 1140994231458, 0, 0,
     8346638665718, 16221323177468, 0, 0, 119447839104366, 232615054822964, 0, 0, 1722663727780132, 3360682669655028,
     0, 0, 25011714460877474, 48870013251334676, 0, 0, 365301750223042066, 714733339229024336, 0, 0,
     5363288299585278800, 10506331021814142340, 0, 0, 79110709437891746598, 155141342711178904962, 0, 0, 1171806326862876802144, 2300241216389780443900,
     0, 0, 17422684839627191647442, 34230838910489146400266, 0, 0, 259932234752908992679732, 511107966282059114105424, 0, 0,
     3890080539905554395312172, 7654746470466776636508150, 0, 0, 58384150201994432824279356, 114963593898159699687805154, 0, 0, 878552973096352358805720000, 1731024005948725016633786324,
     0, 0, 13252206944539668255309614628, 26125970093681074272987123356, 0, 0, 200344082330934061448858342232, 395176777042702357415290092836, 0, 0,
     3035025396219304581284232093788, 5989512457056967650450623499824, 0, 0, 46066215008858751557816176406474, 90951775865823502958277459296556, 0, 0, 700455326458500626656995680137090, 1383551526481468522114814635209546,
     0, 0, 10668539554202332379619189925771954, 21081141524801870066635938612604420, 0, 0, 162745841781501946583283452966558748, 321708432168504823746978787081152850, 0, 0,
     2486298602895927539733035014325425334, 4916537322600925137571911735575827186, 0, 0, 38036184499332584883112732636805913070, 75239777218996797031991486200168278750, 0, 0, 582647682985759867621761102255969613208, 1152903190854960041235527050090876623798,
     0, 0, 8936112261960296110680784882322562246638, 17687405847971827734977690201095477579260, 0, 0, 137213058131141481166525085403700327851590, 271664401832243607401300675435573100509970, 0, 0,
     2109208797862395639896265274928706274715148, 4177074608416566875966558602856582408096820, 0, 0, 32456088315748815781817819951506287174721934, 64292201692737997009032406470855594647870722, 0, 0, 499922068200004204308534991680177008126993576, 990531819608799738604071137206517551558617466
     ]

def main():
    b = [x % 4 for x in a]
    for i in range(len(b)):
        print(b[i], end=' ')
        if i % 16 == 15:
            print()

if __name__ == '__main__':
    main()


