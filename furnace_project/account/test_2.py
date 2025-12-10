import pytest
from .blast import BlastFurnaceInput, IntermediateCalculations, HeatBalanceFull

@pytest.fixture
def bf():
    return BlastFurnaceInput(
        Si=0.53, Mn=0.19, S=0.014, P=0.043, Ti=0.068, Cr=0.021, V=0.0, C=5.13,
        T_iron=1405, C_iron=0.9,
        rd=0.35,
        coke_rate=420, coke_ash=11.9, coke_sulfur=0.5, coke_volatiles=0.6, coke_moisture=4.2,
        hot_blast_temp=1140, blast_humidity=6.36, oxygen_content=24.1,
        gas_consumption=115, gas_CH4=100, gas_C2H6=0, gas_CO2=0,
        gas_C_CH4=1, gas_H2_CH4=2,
        limestone_rate=0, limestone_moisture=0, limestone_loss_on_ignition=42,
        slag_rate=260, slag_sulfur=1.03, slag_heat_capacity=1.26,
        top_gas_temp=328, top_CO2=17.5, top_CO=24.1, top_H2=7.0, top_N2=51.4,
        ore_rate=1716, pellets_rate=0, ore_moisture=0
    )

@pytest.fixture
def balance(bf):
    calc = IntermediateCalculations(bf)
    hb = HeatBalanceFull(bf, calc)
    return hb.get_balance()

def test_heat_balance(balance):
    v = balance

    # ---------- Incoming heat ----------
    assert round(v['C4'], 2) == 2302.81
    assert round(v['C6'], 4) == 1.4276
    assert round(v['C7'], 4) == 1.4276
    assert round(v['C8'], 4) == 1.7775
    assert round(v['C9'], 2) == 1842.79
    assert round(v['C11'], 2) == 190.56
    assert round(v['C13'], 2) == 0.0
    assert round(v['C15'], 2) == 4336.15
    assert round(v['C5'], 4) == 0.5311
    assert round(v['C10'], 4) == 0.4250
    assert round(v['C12'], 4) == 0.0439
    assert round(v['C14'], 4) == 0.0
    assert round(v['C16'], 4) == 1.0

    # ---------- Consumption ----------
    assert round(v['C19'], 2) == 893.60
    assert round(v['C21'], 2) == 160.95
    assert round(v['C23'], 2) == 4.64
    assert round(v['C25'], 2) == 19.45
    assert round(v['C27'], 2) == 1264.5
    assert round(v['C29'], 2) == 476.66
    assert round(v['C31'], 2) == 6.16
    assert round(v['C33'], 2) == 0.0
    assert round(v['C35'], 2) == 43.25
    assert round(v['C42'], 2) == 838.15
    assert round(v['C46'], 1) == 4336.2
    assert round(v['C43'], 4) == 0.1933
    assert round(v['C44'], 2) == 628.79
    assert round(v['C45'], 2) == 0.15

    # ---------- Ratios ----------
    assert round(v['C20'], 4) == 0.2061
    assert round(v['C22'], 4) == 0.0371
    assert round(v['C24'], 4) == 0.0011
    assert round(v['C26'], 4) == 0.0045
    assert round(v['C28'], 4) == 0.2916
    assert round(v['C30'], 4) == 0.1099
    assert round(v['C32'], 3) == 0.0010
    assert round(v['C34'], 4) == 0.0
    assert round(v['C36'], 4) == 0.01
    assert round(v['C47'], 4) == 1.0

    # ---------- Final ----------
    # Если нужно, сюда можно добавить C50–C81 с аналогичной таблицей
