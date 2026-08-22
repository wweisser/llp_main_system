fio2 = 30
flow = 200

def calc_fracts(fio2):
    ox = ((fio2-21)/0.79)/100
    if ox:
        frac_air = (1-(ox))

        frac_air = round(frac_air, 2)
        frac_ox = round(ox, 2)

    return frac_ox, frac_air


for i in range(22, 100):
    frac_ox, frac_air = calc_fracts(i)
    print(f'fio2: {i}, frac_air: {frac_air}, frac_ox: {frac_ox}')