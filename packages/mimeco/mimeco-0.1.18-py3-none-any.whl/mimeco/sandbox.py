reac_host = []
for reac in host.exchanges:
    reac_host.append(reac)
reac_host2 = []
for reac in host2.exchanges:
    reac_host2.append(reac)
    
for reac1, reac2 in zip(reac_host, reac_host2):
    print(reac1.reactants[0].id)
    print(reac2.reactants[0].id)
    
for reac in bact_agora2.exchanges:
    print(reac.reactants[0].id)

#check compatibility

host_ex_id = []
for ex_reac in host.exchanges:
    host_ex_id.append(ex_reac.id)

cnt = 0
for ex_reac in bact_agora2.exchanges:
    if ex_reac.id in host_ex_id:
        print(ex_reac.id)
        cnt = cnt+1

for reac in bact_agora2.reactions:
    for met in list(reac.metabolites):
        if met.compartment == "e":
            print(reac.id)
            print(reac.reaction)
            print(met.id)
            print(met.reactions)
            


Western_diet = pd.read_csv("mimeco/resources/Western_diet_BiGG.csv", index_col = 0)
int_score, int_type = mimeco.interaction_score_and_type_enterocyte(B_ado_bigg, Western_diet, undescribed_metabolites_constraint="as_is", 
                                                                   namespace="BIGG", plot=True)


Western_diet = pd.read_csv("mimeco/resources/Western_diet_VMH.csv", index_col = 0)
int_score_agora, int_type_agora = mimeco.interaction_score_and_type_enterocyte(bact_agora2, Western_diet, undescribed_metabolites_constraint="as_is", namespace="AGORA", plot=True)


model1_biomass_id = "Growth" 
model2_biomass_id = "Growth"

int_score, int_type = mimeco.interaction_score_and_type(model1, model2, Western_diet, 
                                                        undescribed_metabolites_constraint="as_is", plot=True)

potential_exchange, data = mimeco.crossfed_metabolites_plotdata(model1 = model1, model2 = model2, medium = Western_diet, undescribed_metabolites_constraint = "partially_constrained",
                               solver = "cplex", model1_biomass_id = model1_biomass_id, model2_biomass_id = model2_biomass_id, plot = True)


#potential_exchange = mimeco.crossfed_metabolites(model1 = model1, model2 = model2, medium = Western_diet, undescribed_metabolites_constraint = "partially_constrained",
#                               solver = "cplex", model1_biomass_id = model1_biomass_id, model2_biomass_id = model2_biomass_id)




potential_exchange2to1, data2 = mimeco.crossfed_metabolites_plotdata(model1 = model2, model2 = model1, medium = Western_diet, undescribed_metabolites_constraint = "partially_constrained",
                               solver = "cplex", model1_biomass_id = model1_biomass_id, model2_biomass_id = model2_biomass_id)

"""
#AAD_medium_blood = pd.read_csv("mimeco/resources/AAD_VMH.tsv", sep="\t", index_col = 0)

AAD_medium_blood = pd.read_csv("/home/e158401a/Documents/CH2_FB/AAD_adapted_VMH_namespace.csv", index_col="sIEC")
AAD_medium_blood.drop(labels = "Unnamed: 0", axis=1, inplace=True)
reac_adapted = []
for reac in AAD_medium_blood.index:
    if reac == "EX_C8CRN":
        reac_adapted.append("EX_C8CRN(b)")
    else:
        reac_adapted.append(reac[0:-2]+"(b)")
AAD_medium_blood.index = reac_adapted
AAD_medium_blood.index.names = ['reactions']

AAD_medium_blood.to_csv("mimeco/resources/AAD_VMH.tsv", sep="\t")
"""
"""
with open("/home/e158401a/Documents/MIMECO/tests/resources/Lactobacillus_plantarum_WCFS1_Akkermansia_muciniphila_ATCC_BAA_835_WD_PC_potential_exchange.pickle", "wb") as fp:
    pickle.dump(potential_exchange, fp)
    
Western_diet.to_csv("resources/Western_diet.csv", index = True)

import pandas as pd

WD = pd.read_csv("resources/Western_diet.csv", index_col = 0)
"""

host = cobra.io.read_sbml_model("mimeco/resources/enterocyte_BiGG.xml")

host.compartments
host.exchanges

import pandas as pd
blood_exchanges = pd.DataFrame(blood_exchanges, columns=['blood_exchanges'])
blood_exchanges.to_csv("/home/e158401a/Documents/mimeco/resources/blood_reactions_id_enterocyte.csv", index=False)

import csv
with open("/home/e158401a/Documents/mimeco/resources/blood_reactions_id_enterocyte.csv", 'w') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(blood_exchanges)
     
blood_exchanges = pd.read_csv("/home/e158401a/Documents/mimeco/resources/blood_reactions_id_enterocyte.csv")
for reac_id in blood_exchanges["blood_exchanges"]:
    reac = host.reactions.get_by_id(reac_id)
    print(reac_id)
    print(reac.bounds)