import asyncio
import serial_asyncio

def test_po2_align():
    current_fio2 = 54

    current_po2 = 120
    set_po2 = 110

    factor_fio2 = (set_po2-current_po2)/(current_po2*3)
    print(round(factor_fio2, 4))

    if abs(factor_fio2) > 0.03:
        new_fio2 = ((factor_fio2) * current_fio2) + current_fio2
        print(round(new_fio2, 3))

def test_pco2_align():
    current_flow = 200

    current_pco2 = 44
    set_pco2 = 40

    factor_flow = (current_pco2-set_pco2)/(current_pco2)
    print(round(factor_flow, 4))

    if abs(factor_flow) > 0.04:
        new_flow = ((factor_flow) * current_flow) + current_flow
        print(round(new_flow, 3))


if __name__ == "__main__":
    test_po2_align()
    test_pco2_align()
