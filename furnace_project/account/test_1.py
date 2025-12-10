import pytest
from .blast import BlastFurnaceInput, IntermediateCalculations


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
def calc(bf):
    return IntermediateCalculations(bf)


def test_values(calc):
    # Основные расчёты
    assert round(calc.Fe_content(), 3) == 94.004
    assert round(calc.C_direct_Fe(), 2) == 70.50
    assert round(calc.C_direct_impurities(), 2) == 5.69
    assert round(calc.nonvolatile_in_coke(), 0) == 87
    assert round(calc.C_from_coke(), 1) == 365.4
    assert round(calc.C_methane(), 2) == 2.92
    assert round(calc.C_in_iron(), 2) == 51.30
    assert round(calc.C_burned(), 2) == 234.98

    # Дутьё
    assert round(calc.dry_blast_per_kg_C(), 2) == 3.81
    assert round(calc.dry_blast_for_gas(), 2) == 2.04
    assert round(calc.gas_consumption_per_C(), 3) == 0.489
    assert round(calc.total_dry_blast(), 2) == 4.81
    assert round(calc.specific_blast_rate(), 1) == 1130.1

    # Состав горнового газа
    assert round(calc.CO_blast_gas(), 2) == 2.36
    assert round(calc.H2_blast_gas(), 2) == 1.02
    assert round(calc.N2_blast_gas(), 2) == 3.59

    # CO из оксидов
    assert round(calc.CO_from_oxides(), 2) == 148.07

    # Степени использования
    assert round(calc.CO_usage_degree(), 2) == 0.42
    assert round(calc.H2_usage_degree(), 2) == 0.47

    # Объёмы газов при t=1000
    assert round(calc.CO_volume_1000(), 2) == 701.71
    assert round(calc.H2_volume_1000(), 2) == 126.50
    assert round(calc.N2_volume_1000(), 2) == 844.15

    # CO₂
    assert round(calc.CO2_limestone(), 1) == 0
    assert round(calc.CO2_indirect_reduction(), 1) == 295.2

    # Колошниковый газ
    assert round(calc.top_gas_CO2(), 1) == 295.2
    assert round(calc.top_gas_CO(), 1) == 406.5
    assert round(calc.top_gas_CH4(), 1) == 5.5
    assert round(calc.top_gas_N2(), 1) == 844.1
    assert round(calc.top_gas_H2(), 1) == 126.5
    assert round(calc.top_gas_total(), 1) == 1677.8
