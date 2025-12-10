from dataclasses import dataclass
    # # Жидкие продукты доменной плавки
    # Si: float = 0.53                            #C5
    # Mn: float = 0.19                            #C6
    # S: float = 0.014                            #C7
    # P: float = 0.043                            #C8
    # Ti: float = 0.068                           #C9
    # Cr: float = 0.021                           #C10
    # V: float = 0.0                              #C11
    # C: float = 5.13                             #C12

    # T_iron: float = 1405                        #C13
    # C_iron: float = 0.9                         #C14

    # # Режим
    # rd: float = 0.35                            #C16

    # # Кокс
    # coke_rate: float = 420                      #C18
    # coke_ash: float = 11.9                      #C19
    # coke_sulfur: float = 0.5                    #C20
    # coke_volatiles: float = 0.6                 #C21
    # coke_moisture: float = 4.2                  #C22

    # # Дутьё
    # hot_blast_temp: float = 1140                #C24
    # blast_humidity: float = 6.36                #C25
    # oxygen_content: float = 24.1                #C26

    # # м3/т чугуна
    # gas_consumption: float = 115                #C27
    # gas_CH4: float = 100                        #C28
    # gas_C2H6: float = 0                         #C29
    # gas_CO2: float = 0                          #C30
    # gas_C_CH4: float = 1                        #C31
    # gas_H2_CH4: float = 2                       #C32

    # # Известняк
    # limestone_rate: float = 0                   #C34
    # limestone_moisture: float = 0               #C35
    # limestone_loss_on_ignition: float = 42      #C36

    # # Шлак
    # slag_rate: float = 260                      #C38
    # slag_sulfur: float = 1.03                   #C39
    # slag_heat_capacity: float = 1.26            #C40

    # # Колошниковый газ
    # top_gas_temp: float = 328                   #C42
    # top_CO2: float = 17.5                       #C43
    # top_CO: float = 24.1                        #C44
    # top_H2: float = 7.0                         #C45
    # top_N2: float = 51.4                        #C46

    # # ЖРМ
    # ore_rate: float = 1716                      #C48
    # pellets_rate: float = 0                     #C49
    # ore_moisture: float = 0                     #C50
@dataclass
class BlastFurnaceInput:
    Si: float
    Mn: float
    S: float
    P: float
    Ti: float
    Cr: float
    V: float
    C: float

    T_iron: float
    C_iron: float

    rd: float

    coke_rate: float
    coke_ash: float
    coke_sulfur: float
    coke_volatiles: float
    coke_moisture: float

    hot_blast_temp: float
    blast_humidity: float
    oxygen_content: float

    gas_consumption: float
    gas_CH4: float
    gas_C2H6: float
    gas_CO2: float
    gas_C_CH4: float
    gas_H2_CH4: float

    limestone_rate: float
    limestone_moisture: float
    limestone_loss_on_ignition: float

    slag_rate: float
    slag_sulfur: float
    slag_heat_capacity: float

    top_gas_temp: float
    top_CO2: float
    top_CO: float
    top_H2: float
    top_N2: float

    ore_rate: float
    pellets_rate: float
    ore_moisture: float


class IntermediateCalculations:
    def __init__(self, bf_input: BlastFurnaceInput):
        self.d = bf_input

    # -----------------------------
    # Основные промежуточные расчеты
    # -----------------------------

    # C5
    def Fe_content(self) -> float:
        """Содержание Fe в чугуне [%]."""
        return 100 - (self.d.Si + self.d.Mn + self.d.S + self.d.P +
                      self.d.Ti + self.d.Cr + self.d.V + self.d.C)

    # C6
    def C_direct_Fe(self) -> float:
        """Расход C на прямое восстановление Fe [кг/т чугуна]."""
        return self.Fe_content() * 10 * self.d.rd * 12 / 56

    # C7
    def C_direct_impurities(self) -> float:
        """Расход C на прямое восстановление примесей чугуна [кг/т]."""
        return 10 * (
            self.d.Mn * 12 / 55 +
            self.d.P * 60 / 62 +
            self.d.Si * 24 / 28 +
            self.d.S * 12 / 32 +
            self.d.V * 60 / 110 +
            self.d.Ti * 12 / 48 +
            self.d.Cr * 48 / 104
        )

    # C8
    def nonvolatile_in_coke(self) -> float:
        """Количество нелетучих элементов в коксе [%]."""
        return 100 - (self.d.coke_ash + self.d.coke_sulfur + self.d.coke_volatiles)


    # C9
    def C_from_coke(self) -> float:
        """Количество углерода, пришедшего в печь с коксом [кг/т]."""
        return 0.01 * self.d.coke_rate * self.nonvolatile_in_coke()

    # C10
    def C_methane(self) -> float:
        """Расход C на образование метана [кг/т]."""
        return 0.008 * self.C_from_coke()


    # C11
    def C_in_iron(self) -> float:
        """Растворяется углерода в чугуне [кг/т]."""
        return 10 * self.d.C


    # C12
    def C_burned(self) -> float:
        """Количество С, сгорающего у фурм [кг/т]."""
        return self.C_from_coke() - (self.C_in_iron() + self.C_direct_Fe() +
                                     self.C_direct_impurities() + self.C_methane())


    # C13
    def dry_blast_per_kg_C(self) -> float:
        """Расход сухого дутья на 1 кг С кокса [м3/кг Cf]."""
        return 0.9333 / (0.01 * self.d.oxygen_content + 0.00062 * self.d.blast_humidity)


    # C14
    def dry_blast_for_gas(self) -> float:
        """Расход сухого дутья для конверсии 1 м3 природного газа [м3/м3]."""
        return 0.5 / (0.01 * self.d.oxygen_content + 0.00062 * self.d.blast_humidity)


    # C15
    def gas_consumption_per_C(self) -> float:
        """Расход природного газа на 1 кг углерода кокса, сгорающего у фурм [м3/кг Cf]."""
        return self.d.gas_consumption / self.C_burned()


    # C16
    def total_dry_blast(self) -> float:
        """Суммарный расход сухого дутья [м3/кг Cf]."""
        return self.dry_blast_per_kg_C() + self.dry_blast_for_gas() * self.gas_consumption_per_C()


    # C17
    def specific_blast_rate(self) -> float:
        """Расчетный удельный расход дутья [м3/т чугуна]."""
        return self.total_dry_blast() * self.C_burned()

    # -----------------------------
    # Состав фурменного газа
    # -----------------------------


    # C18
    def CO_blast_gas(self) -> float:
        """Состав CO в горновом газе [м3/кг Cf]."""
        return 1.8667 + (self.d.gas_consumption / self.C_burned()) * self.d.gas_C_CH4


    # C19
    def H2_blast_gas(self) -> float:
        """Состав H2 в горновом газе [м3/кг Cf]."""
        tmp = 0.9333 + 0.5 * (self.d.gas_consumption / self.C_burned()) * 1
        return tmp / (0.01 * self.d.oxygen_content + 0.00124 * self.d.blast_humidity) * 0.00124 * self.d.blast_humidity + \
               (self.d.gas_consumption / self.C_burned()) * self.d.gas_H2_CH4


    # C20
    def N2_blast_gas(self) -> float:
        """Состав N2 в горновом газе [м3/кг Cf]."""
        tmp = 0.9333 + 0.5 * (self.d.gas_consumption / self.C_burned()) * 1
        return tmp / (0.01 * self.d.oxygen_content + 0.00124 * self.d.blast_humidity) * (1 - 0.01 * self.d.oxygen_content)

    # -----------------------------
    # CO при восстановлении оксидов
    # -----------------------------


    # C21
    def CO_from_oxides(self) -> float:
        """CO, образующийся при восстановлении оксидов Fe, Mn, Si, P и десульфурации [м3/т]."""

        Fe = self.Fe_content()
        rd = self.d.rd
        Mn = self.d.Mn
        slag_sulfur = self.d.slag_sulfur

        # Строим строку с формулой
        formula_str = (
            f"10 * 22.4 * ({Fe} * {rd} / 56 + {Mn} / 55 + 2 * {Fe} / 28 + {slag_sulfur} / 32)"
        )
        #print(f"Формула для CO_from_oxides: {formula_str}")

        result = 10 * 22.4 * (Fe * rd / 56 + Mn / 55 + 2 * self.d.Si / 28 + slag_sulfur / 32)
        #print(f"CO_from_oxides = {result}")

        return result




    # C22
    def CO_usage_degree(self) -> float:
        """Степень использования CO в печи."""
        return self.d.top_CO2 / (self.d.top_CO2 + self.d.top_CO)


    # C23
    def H2_usage_degree(self) -> float:
        """Степень использования H2 в печи."""
        return 0.88 * self.CO_usage_degree() + 0.1

    # -----------------------------
    # Объёмы газов при t=1000
    # -----------------------------


    # C24
    def CO_volume_1000(self) -> float:
        return self.CO_blast_gas() * self.C_burned() + self.CO_from_oxides()


    # C25
    def H2_volume_1000(self) -> float:
        return self.H2_blast_gas() * self.C_burned() * (1 - self.H2_usage_degree())


    # C26
    def N2_volume_1000(self) -> float:
        return self.N2_blast_gas() * self.C_burned()


    # C27
    def CO2_limestone(self) -> float:
        """Объём CO2 при разложении известняка [м3/т]."""
        return 0.01 * self.d.limestone_rate * 22.4 / 44 * self.d.limestone_loss_on_ignition


    # C28
    def CO2_indirect_reduction(self) -> float:
        """Объём CO2 при косвенном восстановлении оксидов железа [м3/т]."""
        return self.CO_volume_1000() * self.CO_usage_degree()

    # -----------------------------
    # Колошниковый газ
    # -----------------------------


    # C29
    def top_gas_CO2(self) -> float:
        return self.CO2_indirect_reduction() + self.CO2_limestone()


    # C30
    def top_gas_CO(self) -> float:
        return self.CO_volume_1000() - self.CO2_indirect_reduction()


    # C31
    def top_gas_CH4(self) -> float:
        return self.C_methane() * 22.4 / 12


    # C32
    def top_gas_N2(self) -> float:
        return self.N2_volume_1000()


    # C33
    def top_gas_H2(self) -> float:
        return self.H2_volume_1000()


    # C34
    def top_gas_total(self) -> float:
        return self.top_gas_CO2() + self.top_gas_CO() + self.top_gas_CH4() + self.top_gas_N2() + self.top_gas_H2()

class HeatBalanceFull:
    def __init__(self, bf_input: BlastFurnaceInput, intermediate: IntermediateCalculations):
        self.bf_input = bf_input
        self.calc = intermediate
        self.values = {}
        self._calculate_incoming()
        self._calculate_consumption()
        self._calculate_additional()
        self._calculate_final()

    def _calculate_incoming(self):
        bf_input = self.bf_input
        calc = self.calc

        # Входящие потоки
        self.values['C4'] = calc.C_burned() * 9800 * 0.001
        self.values['C6'] = 1.2897 + 0.000121 * bf_input.hot_blast_temp
        self.values['C7'] = 1.2897 + 0.000121 * bf_input.hot_blast_temp
        self.values['C8'] = 1.456 + 0.000282 * bf_input.hot_blast_temp

        self.values['C9'] = (
            0.001 * calc.specific_blast_rate() *
            ((0.01 * bf_input.oxygen_content * self.values['C6'] +
              (1 - 0.01 * bf_input.oxygen_content) * self.values['C7']) *
             (1 - 0.00124 * bf_input.blast_humidity) +
             0.00124 * bf_input.blast_humidity * self.values['C8'])
            * bf_input.hot_blast_temp
        )

        self.values['C11'] = 0.001 * bf_input.gas_consumption * (
            0.01 * (1657 * bf_input.gas_CH4 + 6046 * bf_input.gas_C2H6 - 12644 * bf_input.gas_CO2)
        )

        self.values['C13'] = 1128 * 0.00001 * bf_input.limestone_rate * bf_input.limestone_loss_on_ignition

        self.values['C15'] = self.values['C4'] + self.values['C9'] + self.values['C11'] + self.values['C13']
        self.values['C5'] = self.values['C4'] / self.values['C15']
        self.values['C10'] = self.values['C9'] / self.values['C15']
        self.values['C12'] = self.values['C11'] / self.values['C15']
        self.values['C14'] = self.values['C13'] / self.values['C15']
        self.values['C16'] = self.values['C5'] + self.values['C10'] + self.values['C12'] + self.values['C14']

    def _calculate_consumption(self):
        bf_input = self.bf_input
        calc = self.calc

        # Расход тепла
        self.values['C19'] = 0.01 * calc.Fe_content() * bf_input.rd * 2716
        self.values['C21'] = 0.01 * (
            5220 * bf_input.Mn +
            22600 * bf_input.Si +
            15490 * bf_input.P +
            36167 * bf_input.Ti +
            7982 * bf_input.V
        )
        self.values['C23'] = 1734 * 0.00001 * bf_input.slag_rate * bf_input.slag_sulfur
        self.values['C25'] = 1731 * 0.0001 * (
            0.00124 * bf_input.blast_humidity * calc.specific_blast_rate() +
            0.01 * bf_input.gas_consumption * (2 * bf_input.gas_CH4 + 3 * bf_input.gas_C2H6)
        ) * calc.H2_usage_degree()
        self.values['C27'] = 1 * bf_input.C_iron * bf_input.T_iron
        self.values['C29'] = 0.001 * bf_input.slag_rate * bf_input.slag_heat_capacity * (bf_input.T_iron + 50)
        self.values['C31'] = 1.24 * 0.0000001 * calc.specific_blast_rate() * bf_input.blast_humidity * 6912
        self.values['C33'] = 4042 * 0.000001 * bf_input.limestone_rate * bf_input.limestone_loss_on_ignition
        self.values['C35'] = 2452 * 0.00001 * (
            bf_input.ore_rate * bf_input.ore_moisture +
            bf_input.limestone_rate * bf_input.limestone_moisture +
            bf_input.coke_rate * bf_input.coke_moisture
        )

        # Газовые свойства
        self.values['C37'] = 1.2938 + 0.0000895 * bf_input.top_gas_temp
        self.values['C38'] = 1.6448 + 0.0007065 * bf_input.top_gas_temp
        self.values['C39'] = 1.3012
        self.values['C40'] = 1.4743 + 0.0002205 * bf_input.top_gas_temp
        self.values['C41'] = 1.308

        self.values['C42'] = 0.00001 * (
            (bf_input.top_CO2 * self.values['C38'] +
             bf_input.top_CO * self.values['C37'] +
             bf_input.top_N2 * self.values['C41'] +
             bf_input.top_H2 * self.values['C39']) * calc.top_gas_total() +
            (bf_input.ore_rate * bf_input.ore_moisture +
             bf_input.limestone_rate * bf_input.limestone_moisture +
             bf_input.coke_rate * bf_input.coke_moisture +
             calc.top_gas_total() * bf_input.top_H2 * calc.H2_usage_degree() / (1 - calc.H2_usage_degree())) *
            self.values['C40']
        ) * bf_input.top_gas_temp

        self.values['C44'] = self.values['C15']- (self.values['C19'] + self.values['C21'] + self.values['C23'] + self.values['C25'] + self.values['C27'] + self.values['C29'] + self.values['C31'] + self.values['C33'] + self.values['C35'] + self.values['C42'])

        self.values['C46'] = sum([
            self.values['C19'], self.values['C21'], self.values['C23'], self.values['C25'],
            self.values['C27'], self.values['C29'], self.values['C31'], self.values['C33'], self.values['C35'], self.values['C42'], self.values['C44']
        ])
        self.values['C43'] = self.values['C42'] / self.values['C46']
        
        self.values['C45'] = self.values['C44'] / self.values['C46']

    def _calculate_additional(self):
        # Относительные величины
        self.values['C20'] = self.values['C19'] / self.values['C46']
        self.values['C22'] = self.values['C21'] / self.values['C46']
        self.values['C24'] = self.values['C23'] / self.values['C46']
        self.values['C26'] = self.values['C25'] / self.values['C46']
        self.values['C28'] = self.values['C27'] / self.values['C46']
        self.values['C30'] = self.values['C29'] / self.values['C46']
        self.values['C32'] = self.values['C31'] / self.values['C46']
        self.values['C34'] = self.values['C33'] / self.values['C46']
        self.values['C36'] = self.values['C35'] / self.values['C46']
        self.values['C47'] = sum([
            self.values['C20'], self.values['C22'], self.values['C24'], self.values['C26'],
            self.values['C28'], self.values['C30'], self.values['C32'], self.values['C34'], self.values['C36'],
            self.values['C43'], self.values['C45']
        ])

    def _calculate_final(self):
        bf_input = self.bf_input
        calc = self.calc

        self.values['C50'] = self.values['C4'] + self.values['C9'] - self.values['C42']
        self.values['C51'] = self.values['C50'] / (calc.C_burned() * 0.001)
        self.values['C52'] = 100 - bf_input.rd - calc.C_direct_Fe() - bf_input.gas_consumption - bf_input.limestone_rate

        self.values['C55'] = 0.01 * self.values['C19'] / bf_input.rd
        self.values['C56'] = (self.values['C55'] * 1000) / (self.values['C51'] * 0.01 * self.values['C52'])
        self.values['C59'] = 0 if bf_input.limestone_rate == 0 else self.values['C45'] / bf_input.limestone_rate * 10
        self.values['C60'] = (self.values['C59'] * 1000) / (self.values['C51'] * 0.01 * self.values['C52'])
        self.values['C61'] = self.values['C60'] * bf_input.limestone_rate / 10
        self.values['C64'] = self.values['C9'] / bf_input.oxygen_content * 10
        self.values['C65'] = (self.values['C64'] * 1000) / (self.values['C51'] * 0.01 * self.values['C52'])
        self.values['C68'] = self.values['C11'] / bf_input.gas_consumption * 10
        self.values['C69'] = (self.values['C68'] * 1000) / (self.values['C51'] * 0.01 * self.values['C52'])
        self.values['C72'] = self.values['C31'] / bf_input.blast_humidity
        self.values['C73'] = (self.values['C72'] * 1000) / (self.values['C51'] * 0.01 * self.values['C52'])
        self.values['C76'] = self.values['C29'] / bf_input.slag_rate * 10
        self.values['C77'] = (self.values['C76'] * 1000) / (self.values['C51'] * 0.01 * self.values['C52'])
        self.values['C80'] = self.values['C15'] / 100
        self.values['C81'] = (self.values['C80'] * 1000) / (self.values['C51'] * 0.01 * self.values['C52'])

    def get_balance(self):
        """Возвращает словарь всех расчетных Cxx."""
        return self.values


# class HeatBalanceFull:
#     def __init__(self, bf_input: BlastFurnaceInput):
#         self.input = bf_input
#         self.calc = IntermediateCalculations(bf_input)
#         self.values = {}  # словарь для хранения всех C4–C81

#         # -----------------------------
#         # Расчеты приходной части
#         # -----------------------------

#         # C4 = Промежуточные расчёты!C12 * 9800 * 0.001
#         # Количество тепла, получающегося при горении углерода кокса
#         self.values['C4'] = self.calc.C_burned() * 9800 * 0.001

#         # C6, C7, C8 — теплоемкости O2, N2, H2O в дутье

#         # Теплоемкость O2 в дутье при температуре дутья
#         self.values['C6'] = 1.2897 + 0.000121 * bf_input.hot_blast_temp

#         #Теплоемкость N2 в дутье при температуре дутья
#         self.values['C7'] = 1.2897 + 0.000121 * bf_input.hot_blast_temp

#         #Теплоемкость H2O в дутье при температуре дутья
#         self.values['C8'] = 1.456 + 0.000282 * bf_input.hot_blast_temp

#         # C9 — тепло от горячего дутья
#         # Количество тепла от нагретого дутья
#         self.values['C9'] = 0.001 * self.calc.specific_blast_rate() * (
#             (0.01 * bf_input.oxygen_content * self.values['C6'] +
#              (1 - 0.01 * bf_input.oxygen_content) * self.values['C7']) *
#             (1 - 0.00124 * bf_input.blast_humidity) +
#             0.00124 * bf_input.blast_humidity * self.values['C8']
#         ) * bf_input.hot_blast_temp

#         # C11 — тепло от конверсии природного газа
#         self.values['C11'] = 0.001 * bf_input.gas_consumption * (
#             0.01 * (1657 * bf_input.gas_CH4 + 6046 * bf_input.gas_C2H6 - 12644 * bf_input.gas_CO2)
#         )

#         # C13 — тепло от разложения известняка
#         self.values['C13'] = 1128 * 0.00001 * bf_input.limestone_rate * bf_input.limestone_loss_on_ignition

#         # C15 — суммарное тепло прихода
#         self.values['C15'] = self.values['C4'] + self.values['C9'] + self.values['C11'] + self.values['C13']

#         # C5 = C4 / C15 (доля прихода от горения кокса)
#         self.values['C5'] = self.values['C4'] / self.values['C15']

#         # C10 = C9 / C15 (доля прихода от горячего дутья)
#         self.values['C10'] = self.values['C9'] / self.values['C15']

#         # C12 = C11 / C15 (доля прихода от газа)
#         self.values['C12'] = self.values['C11'] / self.values['C15']

#         # C14 = C13 / C15 (доля прихода от известняка)
#         self.values['C14'] = self.values['C13'] / self.values['C15']

#         # -----------------------------
#         # Расходная часть
#         # -----------------------------
#         # Прямое восстановление
#         self.values['C19'] = 0.01 * self.calc.C_direct_Fe() * bf_input.rd * 2716
#         # Для расчета удельного расхода используем C46 позже
#         # Остальные статьи:
#         self.values['C21'] = 0.01 * (
#             5220 * bf_input.rd +
#             22600 * self.calc.C_direct_Fe() +
#             15490 * self.calc.C_direct_impurities() +
#             36167 * self.values['C9'] +
#             7982 * self.values['C11']
#         )

#         self.values['C23'] = 1734 * 0.00001 * bf_input.slag_rate * bf_input.slag_sulfur
#         self.values['C25'] = 1731 * 0.0001 * (
#             0.00124 * bf_input.blast_humidity * self.calc.specific_blast_rate() +
#             0.01 * bf_input.gas_consumption * (2 * bf_input.gas_CH4 + 3 * bf_input.gas_C2H6)
#         ) * self.calc.C_burned()

#         self.values['C27'] = 1 * bf_input.C_iron * bf_input.T_iron
#         self.values['C29'] = 0.001 * bf_input.slag_rate * bf_input.slag_heat_capacity * (bf_input.T_iron + 50)
#         self.values['C31'] = 1.24 * 0.0000001 * self.calc.specific_blast_rate() * bf_input.blast_humidity * 6912
#         self.values['C33'] = 4042 * 0.000001 * bf_input.limestone_rate * bf_input.limestone_loss_on_ignition
#         self.values['C35'] = 2452 * 0.00001 * (
#             bf_input.ore_rate * bf_input.ore_moisture +
#             bf_input.limestone_rate * bf_input.limestone_moisture +
#             bf_input.coke_rate * bf_input.coke_moisture
#         )

#         # Теплоемкость газов при колошниковом газе
#         self.values['C37'] = 1.2938 + 0.0000895 * bf_input.top_gas_temp
#         self.values['C38'] = 1.6448 + 0.0007065 * bf_input.top_gas_temp
#         self.values['C39'] = 1.3012
#         self.values['C40'] = 1.4743 + 0.0002205 * bf_input.top_gas_temp
#         self.values['C41'] = 1.308

#         # C42 — тепло, уносимое колошниковым газом
#         self.values['C42'] = 0.00001 * (
#             (bf_input.top_CO2 * self.values['C38'] +
#              bf_input.top_CO * self.values['C37'] +
#              bf_input.top_N2 * self.values['C41'] +
#              bf_input.top_H2 * self.values['C39']) * self.calc.top_gas_total() +
#             (bf_input.ore_rate * bf_input.ore_moisture +
#              bf_input.limestone_rate * bf_input.limestone_moisture +
#              bf_input.coke_rate * bf_input.coke_moisture +
#              self.calc.top_gas_total() * bf_input.top_H2 * self.calc.C_methane() / (1 - self.calc.C_methane())) *
#             self.values['C40']
#         ) * bf_input.top_gas_temp

#         # C43 = C42 / C46 (доля тепла, уносимого газом)
#         # C44 = C15 - сумма всех расходов
#         # C45 = C44 / C46 (доля остатка)
#         # C46 = сумма расходов
#         self.values['C46'] = sum([
#             self.values['C19'], self.values['C21'], self.values['C23'], self.values['C25'],
#             self.values['C27'], self.values['C29'], self.values['C31'], self.values['C33'], self.values['C35'], self.values['C42']
#         ])
#         self.values['C43'] = self.values['C42'] / self.values['C46']
#         self.values['C44'] = self.values['C15'] - self.values['C46']
#         self.values['C45'] = self.values['C44'] / self.values['C46']

#     def get_balance(self):
#         """Возвращает словарь всех расчетных Cxx."""
#         return self.values