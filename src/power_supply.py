from machine import ADC

class PowerSupply:

    # ADC defines
    adc_ref_voltage = 3.3
    adc_bit_resolution = 12
    adc_voltage_resolution = adc_ref_voltage / ((2**adc_bit_resolution) - 1)

    conversion_resolution = 65535 # read_u16 scales the raw 12 bit ADC reading to 16 bit using a Taylor expansion 
    conversion_factor = adc_ref_voltage / conversion_resolution

    # Hardware defines
    vsys_conversion_factor = 3 * conversion_factor  #  VSYS is R-C filtered and divided by 3 
                                                # (by R5, R6 and C3 in the Pico schematic)

    adc0_conversion_factor = (1 / (100e3 / (100e3+100e3))) * conversion_factor
    adc1_conversion_factor = 1 / (100e3 / (100e3+330e3)) * conversion_factor

    # Battery defines
    battery_max_voltage = 4.2 # Volts
    battery_min_voltage = 2.8 # Volts

    def __init__(self):
        self.adc0 = ADC(26)
        self.adc1 = ADC(27)
        self.vsys = ADC(29)

    def read(self):

        # Reading ADCs
        adc0_raw = self.adc0.read_u16()
        adc1_raw = self.adc1.read_u16()
        vsys_raw = self.vsys.read_u16()

        # Converting to voltage values
        adc0_voltage = adc0_raw * self.adc0_conversion_factor
        adc1_voltage = adc1_raw * self.adc1_conversion_factor
        vsys_voltage = vsys_raw * self.vsys_conversion_factor

        battery_percentage = 100 * (adc0_voltage - self.battery_min_voltage) / (
            self.battery_max_voltage - self.battery_min_voltage)
        # Treating limits
        if battery_percentage > 100:
            battery_percentage = 100
        elif battery_percentage < 0:
            battery_percentage = 0

        return {
            
            'battery_voltage': { 'raw': adc0_raw, 'value': adc0_voltage, 'unit': 'V' },
            'solar_panel_voltage': { 'raw': adc1_raw, 'value': adc1_voltage, 'unit': 'V' },
            'vsys_voltage': { 'raw': vsys_raw, 'value': vsys_voltage, 'unit': 'V' },
            'battery_percentage': { 'raw': adc0_raw, 'value': battery_percentage, 'unit': '%' }
        }