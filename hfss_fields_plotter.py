import matplotlib.pyplot as plt
import csv
import seaborn as sb
import pandas as pd
import matplotlib.ticker as tkr
import numpy as np
import itertools


# Create a gridpoints file for exporting field data from HFSS
def gridpoints(output_file_name = 'gridpoints_test.pts'):
    
    x = np.linspace(-2.5e-3, 2.5e-3, 2000)
    y = np.linspace(-2.5e-3, 2.5e-3, 2000)
    z = [1e-6]

    with open(output_file_name, 'w', newline='') as file_out:
            writer = csv.writer(file_out, delimiter=' ')
            for element in itertools.product(x, y, z):
                writer.writerow(element)
    
# HFSS field prepper
def process_file(input_file_name = 'H_mag_'+'310'+'_phase.fld',
                output_file_name = 'H_mag'+'310'+'_phase.txt'):

    with open(input_file_name) as file_in, open(output_file_name, 'w', newline='') as file_out:
        reader = csv.reader(file_in, delimiter=' ')
        writer = csv.writer(file_out)

        for row_num,row in enumerate(reader):
            if row_num == 0:
                writer.writerow(['X','Y','Z','Dummy','Mag'])
            else:
                writer.writerow(row)


def plot(e_file, h_file, power, unit_conversion, e_field = True, h_field = True):

    sqrt_power = (power*unit_conversion['Power'])**(-1/2)

    # E field
    if e_field is True:
        formatter = tkr.ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-2, 2))
        with open(e_file) as file:
            reader = csv.DictReader(file, delimiter=',')
            data = []

            for row in reader:
                data.append([float(row['X']), float(row['Y']),
                            float(row['Mag'])*unit_conversion['E field']*sqrt_power])
            df = pd.DataFrame(data, columns=['Y', 'X', 'Mag E'])
            df = df.pivot(index='X', columns='Y', values='Mag E')
            fig, ax = plt.subplots()
            p1 = sb.heatmap(df, xticklabels=False, yticklabels=False, 
                            cbar_kws={'label': unit_conversion['E plot'],
                                    "format": formatter, 'cmap':'viridis'},
                                    square=True)
            ax.set_ylabel('')    
            ax.set_xlabel('')
            if e_field == True and h_field == False:
                plt.show()
            
    # H field
    if h_field is True:
        formatter = tkr.ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-2, 2))
        with open(h_file) as file:
            reader = csv.DictReader(file, delimiter=',')
            data = []
            for row in reader:
                data.append([float(row['X']), float(row['Y']),
                            float(row['Mag'])*unit_conversion['H field']*sqrt_power])
            df = pd.DataFrame(data, columns=['Y', 'X', 'Mag H'])
            df = df.pivot(index='X', columns='Y', values='Mag H')
            fig, ax = plt.subplots()
            p1 = sb.heatmap(df, xticklabels=False, yticklabels=False, 
                            cbar_kws={'label': unit_conversion['H plot'],
                            "format": formatter, 'cmap':'viridis'},
                            square=True)
            ax.set_ylabel('')    
            ax.set_xlabel('')
            plt.show()         

######## Run Code ########

# gridpoints('test1.pts')

# process_file('H_mag_310_phase.fld','H_mag.txt')
# process_file('E_mag_0_phase.fld','E_mag.txt')

unit_conversion = {
    'Power': 10**(-3),          # mW -> W
    'E field': 10**(-2),        # V/m -> V/cm
    'H field': 1.25*10**(-3),   # A/m -> mT
    'N/A': 1,                   # Leave as input unit
    'E plot': r'Electric Field $\frac{V}{cm \sqrt{W}}$',
    'H plot': r'Magnetic Field $\frac{mT}{\sqrt{W}}$'
}

plot('E_mag.txt','H_mag.txt',1,unit_conversion)