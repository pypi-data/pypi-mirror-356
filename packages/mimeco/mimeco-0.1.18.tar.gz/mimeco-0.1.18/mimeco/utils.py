#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 10:37:38 2025

@author: e158401a
"""

import cobra
import pandas as pd
from sklearn import metrics
import mocbapy
from mocbapy.EcosystemModel import create_model, bensolve_default_options
import mocbapy.analysis
import math
import matplotlib.pyplot as plt
import warnings


def create_ecosystem_metabolic_dict(model1, model2):
    """
    Builds a dictionnary for how to name the metabolites of each inputted model in the ecosystem model. 
    Here, we keep the same ids. 

    Parameters
    ----------
    model1 : cobra.Model
    model2 : cobra.Model

    Returns
    -------
    metabolic_dict : dictionnary {(met_id, model): met_id}
        Dictionnary of all metabolites of the inputted models, and how to name them in the ecosystem model. 
    """

    model1_metabolites = []
    for met in model1.metabolites:
        model1_metabolites.append((met.id, model1))
    model2_metabolites = []
    for met in model2.metabolites:
        model2_metabolites.append((met.id, model2))
    all_metabolites = list(set(model1_metabolites + model2_metabolites))
    metabolic_dict = {x:x[0] for x in all_metabolites}
    return metabolic_dict

def restrain_medium(model, medium, undescribed_metabolites_constraint, undescribed_met_lb = -0.1):
    """
    Builds the dictionnary used for constraining the medium of the ecosystem model based on inputted medium data.

    Parameters
    ----------
    model : cobra.Model
    medium : pandas series
        Index : metabolites names
        values  : Availability of corresponding metabolite in the medium as a positive flux value.
    undescribed_metabolites_constraint : string ("blocked", "partially_constrained" or "as_is"). 
        How strictly constrained are the medium metabolites for which the flux is not described in the medium dataframe.
        **"blocked"** : They are not available in the medium at all (can result in model unable to grow)
        **"partially_constrained"** : They are made available with an influx in the medium of 1 mmol.gDW^-1.h^-1
        **"as_is"** : Their availability is the same as in the original inputted model.
    undescribed_met_lb : negative float, optional
        Lower bound assigned to metabolites exchanges reactions that are not described in the given medium, when the "undescribed_metabolic_constraint" argument is set to "partially_constrained".
        Default is -0.1

    Returns
    -------
    model : cobra.Model
    constrained_medium_dict : dictionnary {met_id:(lower_bound,upper_bound)}
        Defines constraint of the ecosystem medium based on inputted medium data. 
        Controls fluxes of metabolites entering the emodels external environment.
    """

    constrained_medium_dict = {}
    for reac in model.exchanges:
        old_bounds = reac.bounds
        met_ex, suffixe = no_compartment_id(list(reac.metabolites.keys())[0].id)
        if medium is None:
            constrained_medium_dict[met_ex+suffixe] = old_bounds
        elif met_ex in list(medium.index):
            constrained_medium_dict[met_ex+suffixe] = (-medium.loc[met_ex].iloc[0], reac._upper_bound)
            reac.lower_bound = -medium.loc[met_ex].iloc[0]
        elif undescribed_metabolites_constraint == "blocked":
            constrained_medium_dict[met_ex+suffixe] = (0, reac._upper_bound)
            reac.lower_bound = 0
        elif undescribed_metabolites_constraint == "partially_constrained":
            constrained_medium_dict[met_ex+suffixe] = (undescribed_met_lb, reac._upper_bound)
            reac.lower_bound = undescribed_met_lb
        elif undescribed_metabolites_constraint == "as_is":
            constrained_medium_dict[met_ex+suffixe] = (reac.lower_bound, reac._upper_bound)
    if constrained_medium_dict == {}:
        warnings.warn("The inputted medium constraint does not match the model's namespace. The medium could not be applied to the ecosystem model")
    return model, constrained_medium_dict

def unrestrain_medium(model):
    """
    Opens the exchange reaction of individual models to enable exchange with paired model. 
    Environment constraints will be reapplied at the scale of the ecosystem in the construction
    of the ecosystem model.

    Parameters
    ----------
    model : cobra.Model

    Returns
    -------
    model : cobra.Model
    """

    for reac in model.exchanges:
        reac.bounds = (-1000, 1000)
    return model

def mo_fba(model1, model2, metabolic_dict, constrained_medium_dict):
    """
    Compute multi-objective FBA between the two given models
    
    Parameters
    ----------
    model1 : cobra.Model
    model2 : cobra.Model
    metabolic_dict : dictionnary {(met_id, model): met_id}
        Dictionnary of all metabolites of the inputted models, and how to name them in the ecosystem model. 
    constrained_medium_dict : dictionnary {met_id:(lower_bound,upper_bound)}
        Guide constraint of the ecosystem medium based on inputted medium data. 
        Controls fluxes of metabolites entering the emodels external environment.

    Returns
    -------
    sol_mofba : 
        Multi-objective solution (Pareto front) of the ecosystem model
    """

    model1 = unrestrain_medium(model1)
    model2 = unrestrain_medium(model2)
    ecosys = create_model(model_array=[model1, model2], metabolic_dict=metabolic_dict, medium = constrained_medium_dict)
    bensolve_opts = bensolve_default_options()
    bensolve_opts['message_level'] = 0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sol_mofba = mocbapy.analysis.mo_fba(ecosys, options=bensolve_opts)
    return sol_mofba, ecosys

def pareto_parsing(sol_mofba, solo_growth_model1, solo_growth_model2):
    """
    Parses the Pareto front and returns its points normalized by the optimal 
    growth of each model optimized in isolation

    Parameters
    ----------
    sol_mofba : 
        Multi-objective solution (Pareto front) of the ecosystem model
    solo_growth_model1 : float
        Objective value of model1 when optimized alone in the described medium
    solo_growth_model2 : float
        Objective value of model2 when optimized alone in the described medium

    Returns
    -------
    xy : pandas dataframe
    Normalized pareto points
    maxi_model1 : numpy.ndarray
        Pareto solution in which model1 objective value is the highest. 
    maxi_model2 : numpy.ndarray
        Pareto solution in which model2 objective value is the highest. 
    """

    x = []
    y = []
    #Initialize analysis variables
    maxi_model1 = (solo_growth_model1, 0)
    maxi_model2 = (0, solo_growth_model2)
    for i in range(len(sol_mofba.Primal.vertex_value)): #Parse Pareto front points
        if sol_mofba.Primal.vertex_type[i] == 1: #Select points (vs vectors) of the Pareto front
            #Normalize points based on model solo growth
            x.append(sol_mofba.Primal.vertex_value[i][0]/solo_growth_model1)
            y.append(sol_mofba.Primal.vertex_value[i][1]/solo_growth_model2)
           
            #Evaluate if model grows better in ecosystem compared to solo model
            if sol_mofba.Primal.vertex_value[i][0] > maxi_model1[0]:
                maxi_model1 = sol_mofba.Primal.vertex_value[i]
            if sol_mofba.Primal.vertex_value[i][1] > maxi_model2[1]:
                maxi_model2 = sol_mofba.Primal.vertex_value[i]

    #Add infered ecosystem Pareto points
    xy = pd.DataFrame({'x': x, 'y': y})
    xy.sort_values('x', inplace=True)      
               
    #Add initial points, corresponding to solo models optimal objective values
    #Values added are slightly dfferent than 1 and 0 to make sure the serie of coordinate is continuous
    if not ((xy['x'] == 1) & (xy['y'] == 0)).any():
        xy = pd.concat([xy, pd.DataFrame([{'x' : 1.00001, 'y' : -0.00001}])], ignore_index=True)
        #xy = xy.append({'x' : 1.00001, 'y' : -0.00001}, ignore_index=True)
    if not ((xy['x'] == 0) & (xy['y'] == 1)).any():
        xy.reset_index(inplace = True, drop=True)
        xy.loc[-1] = [-0.00001, 1.00001]
        xy.index = xy.index + 1  # shifting index
        xy = xy.sort_index()  # sorting by index
   
    return xy, maxi_model1, maxi_model2

def infer_interaction_score(xy):
    """
    Calculates pareto front's area under the curve to determine the interaction score of the ecosystem.
    
    Parameters
    ----------
    xy : pandas dataframe
    Normalized pareto points

    Returns
    -------
    interaction_score : float
        Predicts the nature of the interaction between model1 and model 2. 
        Score < 0 predicts a competitive interaction,
        Score = 0 predicts a neutral interaction
        Score > 0 predicts a positive interaction
    """

    try:
        AUC = metrics.auc(x = xy['x'], y = xy['y'])
    except: 
    #If the growth alone is lower than with paired model, x is not monotonous since it increases and then decreases. AUC determination takes one more step.
    #We calculate the AUC where x is monotonous, the AUC of the inverted part of the Pareto, and substract the last part from the first.
        AUC1 = metrics.auc(x = xy['x'][0:-1], y = xy['y'][0:-1])
        AUC2 = metrics.auc(x = xy['x'][-2:], y = xy['y'][-2:])
        AUC = AUC1 - AUC2
    interaction_score = AUC-1
    return interaction_score
    

def infer_interaction_type(xy, interaction_score, maxi_model1, maxi_model2, solo_growth_model1, solo_growth_model2):
    """
    Infers inetraction type from the models solo maximal objective values, ecosystem maximal objective value and interaction score.

    Parameters
    ----------
    xy : pandas dataframe
    Normalized pareto points
    interaction_score : float
        Predicts the nature of the interaction between model1 and model 2. 
        Score < 0 predicts a competitive interaction,
        Score = 0 predicts a neutral interaction
        Score > 0 predicts a positive interaction
    maxi_model1 : numpy.ndarray
        Pareto solution in which model1 objective value is the highest. 
    maxi_model2 : numpy.ndarray
        Pareto solution in which model2 objective value is the highest. 
    solo_growth_model1 : float
        Objective value of model1 when optimized alone in the described medium
    solo_growth_model2 : float
        Objective value of model2 when optimized alone in the described medium

    Returns
    -------
    interaction_type : string
        Qualitative description (competition, neutrality, favors model1, favors model2,
        limited mutualism or mutualism) of the metabolic interaction between models
    """

    interaction_type_code = ["0","0","0"]
    #Evaluate parameters defining interaction category:
        #interaction_type[0] : model1 growth better in ecosystem than alone
        #interaction_type[1] : model2 growth better in ecosystem than alone
        #interaction_type[2] : A solution exists where both models have a bette objective value compared to monoculture.
        #If both models share an optimal solution, then a + is added to the code, resulting in "extreme mutualism"

    if maxi_model1[0] > solo_growth_model1+(0.001*solo_growth_model1): #solution is an approximation, so slightly varies between instances, 
                                                                      #we make sure the difference in growth is not an artefact
        interaction_type_code[0] = "1"        
    if maxi_model2[1] > solo_growth_model2+(0.001*solo_growth_model2):
        interaction_type_code[1] = "1"
    if tuple(maxi_model1) == tuple(maxi_model2) :
        interaction_type_code[2] = "1"
    if interaction_type_code == "111":
        #If both models share an optimal solution
        interaction_type_code = "111+"
    if interaction_type_code == "110":
        #If a solution exists where they both grow better than alone, Even if this is not a shared optimum
        if len(xy[(xy['x'] > 1.001) & (xy['y'] > 1.001)]) != 0: 
            interaction_type_code = "111"
    interaction_type_code=''.join(interaction_type_code)
    if interaction_score < -0.0001 and interaction_type_code == "000": #Make sure score is negative despite approximation : competition
        interaction_type_code = "-000"
    elif interaction_score >= -0.0001 and interaction_score <= 0.0001: #Make sure score is equivalent to 0 : neutrality
        interaction_type_code = "=000" 
    if interaction_type_code not in ["-000", "=000", "100","010","110", "111", "011", "101"]:
        print(interaction_type_code)
        #raise RuntimeError("There was a problem while infering interaction_type. It is probably in the definition of the model or medium.")
    interaction_type_translation = {"-000":"competition", "=000": "neutrality", 
                                    "100":"favors model1", "010":"favors model2",
                                    "110":"limited mutualism", "111":"mutualism", "111+": "extreme mutualism",
                                    "011" : "Favors model2", "101" : "favors model1",
                                    "001": "neutralism"}
    interaction_type = interaction_type_translation[interaction_type_code]
    return interaction_type

def pareto_plot(xy, model1_id, model2_id):
    plt.title("Pareto front of "+model1_id+" - "+model2_id+" metabolic interaction")
    plt.xlabel(model1_id+"'s objective value")
    plt.ylabel(model2_id+"'s objective value")
    plt.plot(xy['x'].to_numpy(), xy['y'].to_numpy(), '#ff0000', linestyle="-")
    plt.fill_between(xy['x'].to_numpy(), xy['y'].to_numpy(), color = "#f08c8c30")
    plt.axhline(y = 1, color = '#1155cc', linestyle = '--', linewidth = 1)
    plt.axvline(x = 1, color = '#1155cc', linestyle = '--', linewidth = 1)
    plt.show()

def mocba_to_cobra(ecosys):
    """
    Converts the ecosystem model built through mocbapy to a cobra.Model

    Parameters
    ----------
    ecosys : mocbapy.EcosystemModel

    Returns
    -------
    cobra_model : cobra.Model
    """

    cobra_model = cobra.Model('ecosys')
    for m in range(len(ecosys.sysmetabolites)):
        cobra_model.add_metabolites(cobra.Metabolite(ecosys.sysmetabolites[m]))
    for r in range(len(ecosys.sysreactions)):
        reaction = cobra.Reaction(ecosys.sysreactions[r])
        reaction.lower_bound = ecosys.lb[r]
        reaction.upper_bound = ecosys.ub[r]
        dict_metabolites = {}
        cobra_model.add_reactions([reaction])
        for m in range(len(ecosys.sysmetabolites)):
            if ecosys.Ssigma[m,r] != 0:
                dict_metabolites[ecosys.sysmetabolites[m]] = ecosys.Ssigma[m,r]
        reaction.add_metabolites(dict_metabolites)
    return cobra_model

def pareto_sampling(cobra_ecosys, xy, solo_growth_model1, solo_growth_model2, model1_id, model2_id, model1_biomass_id, model2_biomass_id, sample_size = 1000):
    """
    Samples the Pareto front, infering a solution for <sample_size> points on the pareto front.

    Parameters
    ----------
    cobra_ecosys : mocbapy.EcosystemModel
    xy : pandas dataframe
    Normalized pareto points
    solo_growth_model1 : float
        Objective value of model1 when optimized alone in the described medium
    solo_growth_model2 : float
        Objective value of model2 when optimized alone in the described medium
    model1_id : string
        Model denomination in the cobra.Model of model1
    model2_id : string
        Model denomination in the cobra.Model of model2
    model1_biomass_id : string
        id of the reaction used as objective in model1 (if the objective coefficient is not null for several reactions, 
        then a new reaction must be built to constrain the model to a given objective value through its flux)
    model2_biomass_id : string
        id of the reaction used as objective in model2 (if the objective coefficient is not null for several reactions, 
        hen a new reaction must be built to constrain the model to a given objective value through its flux)
    sample_size : int, optional
        Number of samples sampled from the Pareto front to infer correlation between exchange reactions and biomass. 
        Default is 1000.

    Returns
    -------
    sampling : pandas.dataframe
        **columns** : reactions_id
        **rows** : string(objective-value-model1_objective-value-model2) for a given sample
    """

    fba = cobra_ecosys.optimize() #just to get the reactions names for index of sampling
    sampling_dict = {}
    sampling_dict["reactions"] = fba.fluxes.index
    sumdist = 0    
    # Dividing pareto front into segments between two extreme points. Denormalize pareto point so that it can become objective_value constraints.
    # Measure total distance of the pareto front, to determine constant distance between samples points to represent homogeneous representation of pareto front metabolic phenotypes.
    for p in xy.index[1:]:
        x1 = xy.loc[p-1, 'x'] * solo_growth_model1
        y1 = xy.loc[p-1, 'y'] * solo_growth_model2
        x2 = xy.loc[p, 'x'] * solo_growth_model1
        y2 = xy.loc[p, 'y'] * solo_growth_model2
        dist = math.hypot(x2-x1, y2-y1)
        sumdist = sumdist + dist
    dist_1pt = sample_size/sumdist
    #Then browse the pareto again to do the sampling.
    for p in xy.index[1:]:
        x1 = xy.loc[p-1, 'x'] * solo_growth_model1
        y1 = xy.loc[p-1, 'y'] * solo_growth_model2
        x2 = xy.loc[p, 'x'] * solo_growth_model1
        y2 = xy.loc[p, 'y'] * solo_growth_model2
        dist = math.hypot(x2-x1, y2-y1)
        nbpnts_xy = round(dist*dist_1pt)
        if nbpnts_xy>0:
            dx = (x2-x1)/nbpnts_xy
            dy = (y2-y1)/nbpnts_xy
            # Sample a segment of the pareto front.
            # Constraint biomass reaction flux value based on pareto front points coordinates (pix, piy).
            for i in range (0, nbpnts_xy):
                pix = x1+dx*i
                piy = y1+dy*i
                cobra_ecosys.reactions.get_by_id(model1_biomass_id+":"+model1_id).bounds = (pix, pix)
                cobra_ecosys.reactions.get_by_id(model2_biomass_id+":"+model2_id).bounds = (piy, piy)
                fba = cobra_ecosys.optimize() #One sample
                sampling_dict[str(pix)+"_"+str(piy)] = list(fba.fluxes) #keep objective values information in sampling dataframe      
    sampling = pd.DataFrame(data=sampling_dict)
    sampling.index = sampling["reactions"]
    sampling = sampling.T
    sampling = sampling.drop("reactions")
    return sampling

def correlation(sampling):
    """
    Measures correlation between all reactions of the ecosystem model. 
    Correlation type : spearman, because we are interested in common evolution, not proportionnality.

    Parameters
    ----------
    sampling : pandas.dataframe
        **columns** : reactions_id
        **rows** : string(objective-value-model1_objective-value-model2) for a given sample

    Returns
    -------
    correlation_reactions : pandas dataframe
        a correlation matrix featuring all reactions of the ecosystem model
    """

    sampling = sampling.astype(float)
    correlation_reactions = sampling.corr(method ='spearman')
    correlation_reactions = correlation_reactions.fillna(0)
    return correlation_reactions

def oppositeSigns(x, y): #returns boolean. 1 if x y opposite sign, 0 otherwhise
    #return (y >= 0) if (x < 0) else (y < 0) 
    if x < 0:
        return (y > 0) # Because I want a net import 
    elif x > 0: # Because I want a net import 
        return (y < 0)
    else:
        return False
 
def reac_to_met_id(reac, model_id):
    """
    Returns exchanged metabolite id from an exchange reaction.

    Parameters
    ----------
    reac : cobra.Reaction.id
    model_id : string
        Model denomination in the cobra.Model

    Returns
    -------
    met : string
        metabolite id
    """
    #TODO : add a "suffixe" parameter that enable the user to use their own suffixe, to adapt to any namespace. 
    met = reac.replace("_e:"+model_id, "") #BiGG namespace
    met = met.replace("(e):"+model_id, "") #Agora namespace
    met = met.replace("_e0:"+model_id, "") #gapseq namespace
    met = met.replace("EX_", "")
    return met
    
def crossfed_mets(model1, sampling, correlation_reactions, model1_id, model2_id, model1_biomass_id, model2_biomass_id, exchange_correlation = 0.5, biomass_correlation = 0.8, lower_exchange_proportion = 0.3):
    """
    Infers metabolites that are exchanged between organisms in the ecosystem models, correlated with an increasing model1 objective value.
    In other words, crossfed metabolite benefitting model1. Correlation options can be customized. Spearman correlation is used.

    Parameters
    ----------
    model1 : cobra.Model
    sampling : pandas.dataframe
        columns : reactions_id
        rows : string(objective-value-model1_objective-value-model2) for a given sample
    correlation_reactions : pandas dataframe
        a correlation matrix featuring all reactions of the ecosystem model
    model2_id : string
        Model denomination in the cobra.Model of model2
    model2_biomass_id : string
        id of the reaction used as objective in model2 (if the objective coefficient is not null for several reactions, 
        hen a new reaction must be built to constrain the model to a given objective value through its flux)
    exchange_correlation : float between 0 and -1, optional
        defines the level correlation between secretion and uptake of a same metabolite by paired models
        default is 0.5
    biomass_correlation : float between 0 and 1, optional
        correlation between the exchange of the metabolite and the biomass production of model2 for its selection as crossfed.
    lower_exchange_proportion : float between 0 and 1, optional
        proportion of the sampling solutions in which the metabolite of interest is secreted by one organism and uptaken by the other.
    Returns
    -------
    potential_crossfeeding : dictionnary
        **keys** : metabolites id
        **values** : [proportion of samples featuring inverse secretion/uptake for a same metabolite, 
        proportion of samples with metabolite exchange from model1 to model2, 
        proportion of samples with metabolite exchange from model2 to model1]
    """

    potential_crossfeeding = {}
    metabolite_id = []
    model_benefiting = []
    proportion_exchange_list = []
    proportion_model1_to_model2 = []
    proportion_model2_to_model1 = []
    for ex_reac in model1.exchanges:     
        ecosys_reac_id_model1 = ex_reac.id+":"+model1.id
        ecosys_reac_id_model2 = ex_reac.id+":"+model2_id
        met_id = reac_to_met_id(reac = ecosys_reac_id_model1, model_id = model1.id)
        #if a metabolite has an exchange reaction in both models
        if ecosys_reac_id_model1 in correlation_reactions.index and ecosys_reac_id_model2 in correlation_reactions.index:
            #if both exchange reactions have at least one non-null flux value among all samples.
            #and if both reactions are inversely correlated (fluxes variation are going opposite ways, one toward secretion, the other toward uptake)
            if (sum(sampling[ecosys_reac_id_model1])!=0 and sum(sampling[ecosys_reac_id_model2])!=0 and 
                    correlation_reactions.loc[ecosys_reac_id_model1, ecosys_reac_id_model2] <= -exchange_correlation):
                # If the uptake / secretion of given metabolite in model1, associated with its secretion / uptake in model2, is correlated with increased model1 objective value
                if abs(correlation_reactions.loc[ecosys_reac_id_model2, model1_biomass_id+":"+model1_id]) > biomass_correlation:
                    exchange = 0
                    model1_to_model2 = 0
                    model2_to_model1 = 0
                    for s in sampling.index: #parse all solutions for metabolite of interest
                        # if metabolite is secreted in one model, and uptaken in the other
                        if (round(sampling.loc[s, ecosys_reac_id_model1], 5) != 0 and
                        	round(sampling.loc[s, ecosys_reac_id_model2], 5) != 0 and
                        	oppositeSigns(sampling.loc[s, ecosys_reac_id_model1], sampling.loc[s, ecosys_reac_id_model2])): 
                            exchange = exchange+1
                            if sampling.loc[s, ecosys_reac_id_model1] > 0 :
                                model1_to_model2 = model1_to_model2 + 1
                            elif sampling.loc[s, ecosys_reac_id_model2] > 0:
                                model2_to_model1 = model2_to_model1 + 1
                    proportion_exchange = exchange/len(sampling)
                    if proportion_exchange > lower_exchange_proportion and met_id not in potential_crossfeeding.keys():
                        #Fill lists for final dataframe, changing exchange results to proportions
                        metabolite_id.append(met_id)
                        proportion_exchange_list.append(proportion_exchange)
                        proportion_model1_to_model2.append(model1_to_model2/len(sampling))
                        proportion_model2_to_model1.append(model2_to_model1/len(sampling))
                        # Does the exchange benefit only model 1 or both models ?
                        if abs(correlation_reactions.loc[ecosys_reac_id_model1, model2_biomass_id+":"+model2_id]) > biomass_correlation:
                            model_benefiting.append("both")
                        else:
                            model_benefiting.append("model1")

                # If the uptake / secretion of given metabolite in model1, associated with its secretion / uptake in model2, is correlated with increased model2 objective value
                if abs(correlation_reactions.loc[ecosys_reac_id_model1, model2_biomass_id+":"+model2_id]) > biomass_correlation:
                    exchange = 0
                    model1_to_model2 = 0
                    model2_to_model1 = 0
                    for s in sampling.index: #parse all solutions for metabolite of interest
                        # if metabolite is secreted in one model, and uptaken in the other
                        if (round(sampling.loc[s, ecosys_reac_id_model1], 5) != 0 and
                        	round(sampling.loc[s, ecosys_reac_id_model2], 5) != 0 and
                        	oppositeSigns(sampling.loc[s, ecosys_reac_id_model1], sampling.loc[s, ecosys_reac_id_model2])): 
                            exchange = exchange+1
                            if sampling.loc[s, ecosys_reac_id_model1] > 0 :
                                model1_to_model2 = model1_to_model2 + 1
                            elif sampling.loc[s, ecosys_reac_id_model2] > 0:
                                model2_to_model1 = model2_to_model1 + 1
                    proportion_exchange = exchange/len(sampling)
                    if proportion_exchange > lower_exchange_proportion and met_id not in potential_crossfeeding.keys():
                        #Fill lists for final dataframe, changing exchange results to proportions
                        metabolite_id.append(met_id)
                        proportion_exchange_list.append(proportion_exchange)
                        proportion_model1_to_model2.append(model1_to_model2/len(sampling))
                        proportion_model2_to_model1.append(model2_to_model1/len(sampling))
                        # Cases where the exchange of a same metabolite benefit both modeled has been covered before. only exchanges benefitting model2 only are left.
                        model_benefiting.append("model2")
    potential_crossfeeding = pd.DataFrame({"metabolite_id":metabolite_id, "model_benefiting":model_benefiting, "proportion_exchange": proportion_exchange_list, 
                                            "proportion_model1_to_model2":proportion_model1_to_model2, "proportion_model2_to_model1": proportion_model2_to_model1})
    return potential_crossfeeding

def extract_sampling_data(model1, sampling, potential_crossfeeding, model1_id, model2_id):
    """
    Extracts sampling data from predicted exchanged metabolites, and models objective values for each sample.

    Parameters
    ----------
    sampling : pandas.dataframe
        **columns** : reactions_id
        **rows** : string(objective-value-model1_objective-value-model2) for a given sample
    potential_crossfeeding : dictionnary
        **keys** : metabolites id
        **values** : [proportion of samples featuring inverse secretion/uptake for a same metabolite, 
        proportion of samples with metabolite exchange from model1 to model2, 
        proportion of samples with metabolite exchange from model2 to model1]
    model1_id : string
        Model denomination in the cobra.Model of model1
    model2_id : string
        Model denomination in the cobra.Model of model1

    Returns
    -------
    sampling_data : pandas dataframe
        Dataframe based on the sampling, resulting in each rw bing a sample.
        The first two columns records the objective value, in the given sample, of both models.
        Other columns are, by pairs, the flux values of the exchange reactions of a crossfed metabolite for both models.
    """

    obj_value_model1 = []
    obj_value_model2 = []
    namespace, suffixe = find_namespace(model1)
    for i in sampling.index:      
        obj_value_model1.append(float(i.split("_", 1)[0]))
        obj_value_model2.append(float(i.split("_", 1)[1]))
    sampling_data = pd.DataFrame({"obj_value_model1" : obj_value_model1, 
                                  "obj_value_model2" : obj_value_model2})
    for metabolite in potential_crossfeeding["metabolite_id"]:
        ecosys_reac_id_model1 = "EX_"+metabolite+suffixe+":"+model1_id
        ecosys_reac_id_model2 = "EX_"+metabolite+suffixe+":"+model2_id
        sampling_data[ecosys_reac_id_model1] = sampling[ecosys_reac_id_model1].values
        sampling_data[ecosys_reac_id_model2] = sampling[ecosys_reac_id_model2].values
    return sampling_data


def plot_exchange(model1, sampling, potential_crossfeeding, model1_id, model2_id):
    """
    Visualizes crossfed metablites flux evlution on along the pareto front. This visualisation is rudimentary.

    Parameters
    ----------
    sampling : pandas.dataframe
        **columns** : reactions_id
        **rows** : string(objective-value-model1_objective-value-model2) for a given sample
    potential_crossfeeding : dictionnary
        **keys** : metabolites id
        **values** : [proportion of samples featuring inverse secretion/uptake for a same metabolite, 
        proportion of samples with metabolite exchange from model1 to model2, 
        proportion of samples with metabolite exchange from model2 to model1]
    model1_id : string
        Model denomination in the cobra.Model of model1
    model2_id : string
        Model denomination in the cobra.Model of model1
    """

    max_model1 = 0
    max_model2 = 0
    namespace, suffixe = find_namespace(model1)
    for i in sampling.index:      
        obj_value_model1 = float(i.split("_", 1)[0])
        obj_value_model2 = float(i.split("_", 1)[1])  
        if obj_value_model1 > max_model1:
            max_model1 = obj_value_model1
            max_ind_model1 = i
        if obj_value_model2 > max_model2:
            max_model2 = obj_value_model2
            max_ind_model2 = i
    for metabolite in potential_crossfeeding["metabolite_id"]:
        ecosys_reac_id_model1 = "EX_"+metabolite+suffixe+":"+model1_id
        ecosys_reac_id_model2 = "EX_"+metabolite+suffixe+":"+model2_id
        a = sampling[ecosys_reac_id_model1]
        b = sampling[ecosys_reac_id_model2]
        plt.plot(a, "#e06666", label = model1_id)
        plt.plot(b, "#3d85c6", label = model2_id)
        plt.axvline(x = max_ind_model1, color = "#e06666", linestyle=':')
        plt.axvline(x = max_ind_model2, color = "#3d85c6", linestyle=':')
        plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
        plt.title("evolution of "+metabolite+" exchanges on the pareto front")
        plt.legend()
        plt.show()
        plt.clf()

    
def no_compartment_id(metabolite):
    """
    Separates metabolic id from the compartment information. Aknowledges BiGG, AGORA and gapseq namespaces.

    Parameters
    ----------
    metabolite : cobra.Metabolite

    Returns
    -------
    metabolite : string
        metabolite_id, without its compartment information
    suffixe : string
        compartment information of the inputted metabolite
    """
    
    a = metabolite
    done = False
    if metabolite[-2:] == "_e": #to avoid deleting _e in the middle of a metabolite id
        metabolite = metabolite.replace('_e','')
        if metabolite != a:
            suffixe='_e'
            done = True
    metabolite = metabolite.replace(('(e)'),'')
    if metabolite != a and not done:
        suffixe='(e)'
        done = True
    metabolite = metabolite.replace(('_e0'),'')
    if metabolite != a and not done:
        suffixe='_e0'
        done = True
    metabolite = metabolite.replace(('_c0'),'')
    if metabolite != a and not done:
        suffixe='_c0'
        done = True
    metabolite = metabolite.replace(('_c'),'')
    if metabolite != a and not done:
        suffixe='_c'
        done = True
    metabolite = metabolite.replace(('[c]'),'')
    if metabolite != a and not done:
        suffixe='[c]'
        done = True
    metabolite = metabolite.replace(('[m]'),'')
    if metabolite != a and not done:
        suffixe='[m]'
        done = True
    metabolite = metabolite.replace(('[x]'),'')
    if metabolite != a and not done:
        suffixe='[x]'
        done = True
    metabolite = metabolite.replace(('[r]'),'')
    if metabolite != a and not done:
        suffixe='[r]'
        done = True
    metabolite = metabolite.replace(('[e]'),'')
    if metabolite != a and not done:
        suffixe='[e]'
        done = True
    metabolite = metabolite.replace(('[n]'),'')
    if metabolite != a and not done:
        suffixe='[n]'
        done = True
    metabolite = metabolite.replace(('[u]'),'')
    if metabolite != a and not done:
        suffixe='[u]'
        done = True
    metabolite = metabolite.replace(('[luC]'),'')
    if metabolite != a and not done:
        suffixe='[luC]'
        done = True
    metabolite = metabolite.replace(('[bpC]'),'')
    if metabolite != a and not done:
        suffixe='[bpC]'
        done = True
    metabolite = metabolite.replace(('[g]'),'')
    if metabolite != a and not done:
        suffixe='[g]'
        done = True
    metabolite = metabolite.replace(('[l]'),'')
    if metabolite != a and not done:
        suffixe='[l]'
        done = True
    if done == False: 
        print("no suffixe found for", metabolite)
        suffixe = ""
    return metabolite, suffixe

def find_namespace(model):
    """
    Identifies the namespace of the given model. Bigg (CarveMe), Agora (VMH) and gapseq namespace are tested and supported on mimeco. Other namespace could require adaptation.
    """
    suffixe_list = []
    for ex_reac in model.exchanges[0:3]: #check 3 suffixes to be sure
        met = list(ex_reac.metabolites.keys())[0].id
        met_id, suffixe = no_compartment_id(met)
        suffixe_list.append(suffixe)
    if len(list(set(suffixe_list))) == 1: #If the suffixe is the same for the three checked exchange reactions
        suffixe = suffixe_list[0]
    if suffixe == "_e":
        namespace = "bigg"
    elif suffixe == "(e)":
        namespace = "agora"
    elif suffixe == "_e0":
        namespace = "gapseq"
    else:
        namespace = "unkown"
        warnings.warn(f"mimeco could not identify the model's namespace. You need to instruct the suffixe for exchange reactions in the 'suffixe' argument of the reaction. If you face further problems, please open an issue on mimeco's github.")
    return namespace, suffixe