# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 15:10:44 2020
ORKG PLotprogramm: reads data from ORKG comparisons and makes a simple plot 
scenario, time_end and id of comparison have to be chosen and written into the variables scenario, time_end and com_id.
@author: GanskeA
"""

import pandas as pd
import numpy as np
from orkg import ORKG

from matplotlib import pyplot as plt

# import data from ORKG comparison for Global Mean Sea Level Rise (GMSL Rise): 
# RCP8.5, 2100 compared to 2000: R48392
# RCP4.5, 2100 compared to 2000: R48401
# RCP2.6, 2100 compared to 2000: R48402
# RCP8.5, 2050 compared to 2000: R48403
# RCP4.5, 2050 compared to 2000: R48404
# RCP2.6, 2050 compared to 2000: R48405
scenario='RCP4.5'
time_end='2050'
com_id='R48404'
p_title='Projected GMSL '+time_end+ ' compared to 2000, '+scenario
pf_name='GMSL_Rise_'+time_end+'_'+scenario+'.png'

# read numbers from ORKG
orkg = ORKG(host='https://orkg.org/orkg', simcomp_host='https://orkg.org/orkg/simcomp') 
df = orkg.contributions.compare_dataframe(comparison_id=com_id)
 # Median
values = np.float32(df.loc['Has value', :])
n_elements=len(values)
# likely range between lower and upper value
lower = np.array([np.float32(x) if x else np.nan for x in df.loc['has lower limit for likely range', :]])
upper = np.array([np.float32(x) if x else np.nan for x in df.loc['has upper limit for likely range', :]])

df = pd.DataFrame(data=dict(value=values, lower=lower, upper=upper))
source = ColumnDataSource(df)
# x-axis: 
x = np.arange(0, n_elements, 1.0)
# Plot median
plt.plot(x,values,'bo',label='median')
# plot likely range
plt.errorbar(x,values,yerr=[lower,upper],fmt='.',label='likely range')

plt.xlabel("Paper No.")
plt.ylabel("Likely Range GMSL Rise [m]")
plt.title(p_title)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
# save in file pf_name
plt.savefig(pf_name)
plt.show()
