import numpy as np
from .examples import Multinomial as multinomial

table = np.zeros((6,2,2))
table[0,0] = [825*.62,825*.38]
table[0,1] = [108*.82,108*.18]
table[1,0] = [560*.63,560*.37]
table[1,1] = [25*.68,25*.32]
table[2,0] = [325*.37,325*.63]
table[2,1] = [593*.34,593*.66]
table[3,0]= [417*.33,417*.67]
table[3,1]= [375*.35,375*.65]
table[4,0] = [191*.28,191*.72]
table[4,1] = [393*.24,393*.76]
table[5,0] = [373*.06,373*.94]
table[5,1] = [341*.07,341*.93]


UCB = multinomial(table,
                  labels=[['A','B','C','D','E','F'], 
                          ['Male','Female'], 
                          ['Accept', 'Deny']])

#UCB_female = UCB.conditional(lambda outcome: outcome[1] == 'Female',
#                             shape=(6,2))

#UCB_male = UCB.conditional(lambda outcome: outcome[1] == 'Male',
#                           shape=(6,2))
