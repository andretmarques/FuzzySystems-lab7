import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

temp = ctrl.Antecedent(np.arange(0, 101, 1), 'temp')
clock_speed = ctrl.Antecedent(np.arange(0, 4.5, 0.5), 'clock_speed')
fan_speed = ctrl.Consequent(np.arange(0, 6001, 1), 'fan_speed')

temp['cold'] = fuzz.trimf(temp.universe, [0, 0, 50])
temp['warm'] = fuzz.trimf(temp.universe, [30, 50, 70])
temp['hot'] = fuzz.trimf(temp.universe, [50, 100, 100])

clock_speed['low'] = fuzz.trimf(clock_speed.universe, [0, 0, 1.5])
clock_speed['normal'] = fuzz.trimf(clock_speed.universe, [0.5, 2, 3.5])
clock_speed['turbo'] = fuzz.trimf(clock_speed.universe, [2.5, 4, 4])

fan_speed['slow'] = fuzz.trimf(fan_speed.universe, [0, 0, 3500])
fan_speed['fast'] = fuzz.trimf(fan_speed.universe, [2500, 6000, 6000])

temp.view()
clock_speed.view()
fan_speed.view()

rules = []
rule1 = ctrl.Rule(temp['cold'] & clock_speed['low'], fan_speed['slow'])
rule2 = ctrl.Rule(temp['cold'] & clock_speed['normal'], fan_speed['slow'])
rule3 = ctrl.Rule(temp['cold'] & clock_speed['turbo'], fan_speed['fast'])
rule4 = ctrl.Rule(temp['warm'] & clock_speed['low'], fan_speed['slow'])
rule5 = ctrl.Rule(temp['warm'] & clock_speed['normal'], fan_speed['slow'])
rule6 = ctrl.Rule(temp['warm'] & clock_speed['turbo'], fan_speed['fast'])
rule7 = ctrl.Rule(temp['hot'] & clock_speed['low'], fan_speed['fast'])
rule8 = ctrl.Rule(temp['hot'] & clock_speed['normal'], fan_speed['fast'])
rule9 = ctrl.Rule(temp['hot'] & clock_speed['turbo'], fan_speed['fast'])
rules.append(rule1)
rules.append(rule2)
rules.append(rule3)
rules.append(rule4)
rules.append(rule5)
rules.append(rule6)
rules.append(rule7)
rules.append(rule8)
rules.append(rule9)

ctrl1 = ctrl.ControlSystem(rules)
final_speed1 = ctrl.ControlSystemSimulation(ctrl1)
final_speed1.input['temp'] = 60
final_speed1.input['clock_speed'] = 2
final_speed1.compute()
print(final_speed1.output['fan_speed'])
fan_speed.view(sim=final_speed1)

fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [2000, 3000, 4000])
fan_speed.view()

rules2 = []
rule_1 = ctrl.Rule(temp['cold'] & clock_speed['low'], fan_speed['slow'])
rule_2 = ctrl.Rule(temp['cold'] & clock_speed['normal'], fan_speed['slow'])
rule_3 = ctrl.Rule(temp['cold'] & clock_speed['turbo'], fan_speed['medium'])
rule_4 = ctrl.Rule(temp['warm'] & clock_speed['low'], fan_speed['medium'])
rule_5 = ctrl.Rule(temp['warm'] & clock_speed['normal'], fan_speed['medium'])
rule_6 = ctrl.Rule(temp['warm'] & clock_speed['turbo'], fan_speed['fast'])
rule_7 = ctrl.Rule(temp['hot'] & clock_speed['low'], fan_speed['fast'])
rule_8 = ctrl.Rule(temp['hot'] & clock_speed['normal'], fan_speed['fast'])
rule_9 = ctrl.Rule(temp['hot'] & clock_speed['turbo'], fan_speed['fast'])
rules2.append(rule_1)
rules2.append(rule_2)
rules2.append(rule_3)
rules2.append(rule_4)
rules2.append(rule_5)
rules2.append(rule_6)
rules2.append(rule_7)
rules2.append(rule_8)
rules2.append(rule_9)

ctrl2 = ctrl.ControlSystem(rules2)
final_speed2 = ctrl.ControlSystemSimulation(ctrl2)
final_speed2.input['temp'] = 60
final_speed2.input['clock_speed'] = 2
final_speed2.compute()
print(final_speed2.output['fan_speed'])
fan_speed.view(sim=final_speed2)

def threeDgraph(sim):
    lin_temp = np.linspace(0, 105, 525)
    lin_clock = np.linspace(0, 5, 25)
    x, y = np.meshgrid(lin_temp, lin_clock)
    z = np.zeros_like(x)

    for i in range(25):
        for j in range(525):
            sim.input['temp'] = x[i, j]
            sim.input['clock_speed'] = y[i, j]
            sim.compute()
            z[i, j] = sim.output['fan_speed']

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
                           linewidth=0.4, antialiased=True)

    ax.contourf(x, y, z, zdir='z', offset=-1, cmap='viridis', alpha=0.5)
    ax.contourf(x, y, z, zdir='x', offset=115, cmap='viridis', alpha=0.5)
    ax.contourf(x, y, z, zdir='y', offset=5.1, cmap='viridis', alpha=0.5)

    ax.view_init(30, 200)
    plt.show()

if __name__ == '__main__':
    threeDgraph(final_speed1)
    threeDgraph(final_speed2)

    for i in range(len(rules)):
        print(rules[i])

    print("#####################################")

    for i in range(len(rules2)):
        print(rules2[i])
