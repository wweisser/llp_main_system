# "<gbm>m:state|" + set_fio2 + "|" + set_total_flow + "|" + set_oxygen_flow + "|" + set_air_flow + "|" + fio2 + "|" + oxygen_flow + "|" + air_flow;

def parse_gbm(input: str) -> list:
    arr = []
    l = len(input)
    i = 0
    while i < l:
        if input[i] == '|' and i < l:
            i += 1
            numb = 0
            while i < l and input[i].isdigit():
                numb = numb * 10 + int(input[i])
                i += 1
            arr.append(numb)
        else:
            i += 1
    return arr
            

if __name__ == "__main__":
    input = "<gbm>m:state|" + '21' + "|" + '400' + "|" + '84' + "|" + '316' + "|" + '23' + "|" + '91' + "|" + '306'
    print(input)
    parse_gbm(input)