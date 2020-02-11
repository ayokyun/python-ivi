from ivi.tdklambda.z60 import Z60 as PSU

psu = PSU('ASRL::COM5,57600,8n1::INSTR')
for milivolt in range(0, 60000, 100):
    psu.outputs[0].voltage_level = milivolt / 1000
    psu.outputs[0].enabled = (milivolt % 2) == 0

    voltage_measure = psu.outputs[0].measure("voltage")
    print(f'{milivolt}mV, Out={psu.outputs[0].enabled}, measureVoltage = {voltage_measure}')
psu.close()
