#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 09:46:31 2025

@author: e158401a
"""

#TODO : make absolute path for package (init ?)
#import os
#os.chdir(/home/e158401a/Documents/mimeco)

import mimeco.utils as utils
import mimeco.enterocyte_specific_utils as enterocyte_specific_utils
import warnings
import cobra
from importlib.resources import files


def interaction_score_and_type(model1, model2, medium = None, undescribed_metabolites_constraint = None, undescribed_met_lb = -0.1, plot = False, verbose=False):
    """
    A function that, given 2 models in the same namespace and a defined medium, analyses the interaction between the two models,
    infering qualitative (interaction_type) and quantitative (interaction_score) information on their metabolic interaction. 
    
    Parameters
    ----------
    model1: cobra.Model
    model2 : cobra.Model
    medium : pandas series
        **Index** : metabolites names
        **values**  : Availability of corresponding metabolite in the medium as a positive flux value.
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
    interaction_score : float
        Predicts the nature of the interaction between model1 and model 2. 
        Score < 0 predicts a competitive interaction,
        Score = 0 predicts a neutral interaction
        Score > 0 predicts a positive interaction
    interaction_type : string
        Qualitative description of the interaction.
    """
    if medium is None:
        warnings.warn("You have not specified a medium composition. The model's bounds will be constrained based on the inputted model's exchange constraints")
    elif undescribed_metabolites_constraint == None:
        warnings.warn("You did not define a level of constraint for metabolites not described in the inputted medium. By default, the 'partially_constrained' option will be selected and a lower bound of -1 will be applied. Define the argument 'undescribed_metabolites_constraint' to chose a more suitable constraint.")
        undescribed_metabolites_constraint = "partially_constrained"
    metabolic_dict = utils.create_ecosystem_metabolic_dict(model1, model2)
        #Infers maximal objective value of both models seperately, in the given medium.
    with model1:
        model1, constrained_medium_dict1 = utils.restrain_medium(model1, medium, undescribed_metabolites_constraint, undescribed_met_lb)
        solo_growth_model1 = model1.optimize().objective_value
    with model2:
        model2, constrained_medium_dict2 = utils.restrain_medium(model2, medium, undescribed_metabolites_constraint, undescribed_met_lb)
        solo_growth_model2 = model2.optimize().objective_value
    if solo_growth_model1 == solo_growth_model2 == 0:
        raise RuntimeError("Both models had a null objective value when modeled alone in the given medium."+
                           " To enable this analysis, you need to adjust the medium or models. You can also"+
                           " try to lighten the medium constraint by using the \"partially_constrained\""+
                           " option for the undescribed_metabolites_constraint argument.") 
    elif solo_growth_model1 == 0 or solo_growth_model2 == 0:
        warnings.warn("One model had a null objective value when modeled alone in the given medium."+
                      " If this is not an expected result, you might want to use the \"partially_constrained\""+
                      " option for the undescribed_metabolites_constraint argument, or redefine your medium or model.")
    medium_dict = {**constrained_medium_dict1, **constrained_medium_dict2} #Translate medium constraint for mocba
    # mocba will create new exchange reaction exterior to both models. the original exchange reactions, if restrained, will prevent 
    #exchanges between organisms. Here we unconstrain them.
    model1 = utils.unrestrain_medium(model1)
    model2 = utils.unrestrain_medium(model2)
    sol_mofba = utils.mo_fba(model1, model2, metabolic_dict, medium_dict)[0] #get multi-objective solution (pareto front)
    xy, maxi_model1, maxi_model2 = utils.pareto_parsing(sol_mofba, solo_growth_model1, solo_growth_model2) #parse and normalize pareto front
    interaction_score = utils.infer_interaction_score(xy) #measure AUC of Pareto front, translates it in quantitative interaction prediction
    interaction_type = utils.infer_interaction_type(xy, interaction_score, maxi_model1, maxi_model2,solo_growth_model1, solo_growth_model2) #infers interaction type from pareto front's shape.
    if verbose:
        print(model1.id+" solo maximal growth is: "+str(solo_growth_model1))
        print("its maximal growth in ecosystem is: "+str(maxi_model1[0]))
        print(model2.id+" solo maximal growth is: "+str(solo_growth_model2))
        print("its maximal growth in ecosystem is: "+str(maxi_model2[1]))
    if plot:
        model1_id = model1.id
        model2_id = model2.id
        utils.pareto_plot(xy, model1_id, model2_id)
    return interaction_score, interaction_type


def crossfed_metabolites(model1, model2, solver, model1_biomass_id, model2_biomass_id, medium = None, undescribed_metabolites_constraint = None, 
                        undescribed_met_lb = -0.1, sample_size = 1000, exchange_correlation = 0.5, biomass_correlation = 0.8, lower_exchange_proportion = 0.3,
                        plot = False, retrieve_data = "no"):
    """
    A function that, given 2 models in the same namespace and a defined medium, predicts metabolic exchanges that
    are correlated with the increase of model2 objective value. Correlation options can be customized. Spearman correlation is used.
    plot and retrieve_data options enable further analysis (see documentation)

    Parameters
    ----------
    model1 : cobra.Model
    model2 : cobra.Model
    medium : pandas series
        **Index** : metabolites names
        **values**  : Availability of corresponding metabolite in the medium as a positive flux value. 
    undescribed_metabolites_constraint : string ("blocked", "partially_constrained" or "as_is"). 
        How strictly constrained are the medium metabolites for which the flux is not described in the medium dataframe.
        **"blocked"** : They are not available in the medium at all (can result in model unable to grow)
        **"partially_constrained"** : They are made available with an influx in the medium of 1 mmol.gDW^-1.h^-1
        **"as_is"** : Their availability is the same as in the original inputted model. 
    solver : string
        solver supported by the cobra toolbox. "cplex" or "gurobi" are recommended but require prior installation.
    model1_biomass_id : string
        id of the reaction used as objective in model1 (if the objective coefficient is not null for several reactions, then a new reaction must be built to constrain the model to a given objective value through its flux)
    model2_biomass_id : string
        id of the reaction used as objective in model2 (if the objective coefficient is not null for several reactions, then a new reaction must be built to constrain the model to a given objective value through its flux)
    undescribed_met_lb : negative float, optional
        Lower bound assigned to metabolites exchanges reactions that are not described in the given medium, when the "undescribed_metabolic_constraint" argument is set to "partially_constrained".
        Default is -0.1    
    sample_size : int, optional
        Number of samples sampled from the Pareto front to infer correlation between exchange reactions and biomass. The default is 1000.
    exchange_correlation : float between 0 and -1, optional
        defines the threshold for the correlation between secretion and uptake of a same metabolite by paired models for this metabolite to be considered exchanged
        default is 0.5
    biomass_correlation : float between 0 and 1, optional
        correlation threshold between the exchange of the metabolite and the biomass production of model2 for its selection as crossfed.
        default is 0.8
    lower_exchange_proportion : float between 0 and 1, optional
        proportion of the sampling solutions in which the metabolite of interest is secreted by one organism and uptaken by the other.
    plot : Boolean, optional
        Rudimentary integrated plot function to visualize Pareto front.
        default is False
    retrieve_data : str, optionnal
        Returns data that can be used for custom analysis.
        **"all"**: returns the sampling dataframe containing the fluxes of each reaction of the ecosystem in all samples. 
        "**selection"**: returns a subset of the sampling dataframe, containing the predicted crossfed metabolites exchange fluxes in all samples of the Pareto front, 
        as well as the objective value of each model in these samples.
        If retrieve_data is set on "all" or "selection", the function returns a second variable with the corresponding dataframe. 
        default is "no"

    Returns
    -------
    potential_crossfeeding : dictionnary
        **keys** : metabolites id
        **values** : [proportion of samples featuring inverse secretion/uptake for a same metabolite, 
        proportion of samples with metabolite exchange from model1 to model2, 
        proportion of samples with metabolite exchange from model2 to model1]
    sampling_data : pandas dataframe
        Dataframe based on the sampling, resulting in each row being a sample.
        **if retrieve_data == "selection"** 
        The first two columns records the objective value, in the given sample, of both models.
        Other columns are, by pairs, the flux values of the exchange reactions of a crossfed metabolite for both models.
        **if retrieve_data == "all"** 
        Columns are all reaction of the ecosystem model in the order of ecosys.reactions.
    """
    if medium is None:
        warnings.warn("You have not specified a medium composition. The model's bounds will be constrained based on the inputted model's exchange constraints")
    elif undescribed_metabolites_constraint == None:
        warnings.warn("You did not define a level of constraint for metabolites not described in the inputted medium. By default, the 'partially_constrained' option will be selected and a lower bound of -1 will be applied. Define the argument 'undescribed_metabolites_constraint' to chose a more suitable constraint.")
        undescribed_metabolites_constraint = "partially_constrained"
    metabolic_dict = utils.create_ecosystem_metabolic_dict(model1, model2)
    #Infers maximal objective value of both models seperately, in the given mdeium.
    with model1:
        model1, constrained_medium_dict1 = utils.restrain_medium(model1, medium, undescribed_metabolites_constraint, undescribed_met_lb)
        solo_growth_model1 = model1.optimize().objective_value
    with model2:
        model2, constrained_medium_dict2 = utils.restrain_medium(model2, medium, undescribed_metabolites_constraint, undescribed_met_lb)
        solo_growth_model2 = model2.optimize().objective_value
    if solo_growth_model1 == solo_growth_model2 == 0:
        raise RuntimeError("Both models had a null objective value when modeled alone in the given medium."+
                           " To enable this analysis, you need to adjust the medium or models. You can also"+
                           " try to lighten the medium constraint by using the \"partially_constrained\""+
                           " option for the undescribed_metabolites_constraint argument.") 
    elif solo_growth_model1 == 0 or solo_growth_model2 == 0:
        warnings.warn("One model had a null objective value when modeled alone in the given medium."+
                      " If this is not an expected result, you might want to use the \"partially_constrained\""+
                      " option for the undescribed_metabolites_constraint argument, or redefine your medium or model.")
    medium_dict = {**constrained_medium_dict1, **constrained_medium_dict2} #Translate medium constraint for mocba
    # mocba will create new exchange reaction exterior to both models. the original exchange reactions, if restrained, will prevent 
    #exchanges between organisms. Here we unconstrain them.
    model1 = utils.unrestrain_medium(model1)
    model2 = utils.unrestrain_medium(model2)
    sol_mofba, ecosys = utils.mo_fba(model1, model2, metabolic_dict, medium_dict) #get multi-objective solution (pareto front), and ecosystem model from mocba 
    xy, maxi_model1, maxi_model2 = utils.pareto_parsing(sol_mofba, solo_growth_model1, solo_growth_model2) #parse and normalize pareto front
    cobra_ecosys = utils.mocba_to_cobra(ecosys) #Translate mocba ecosystem into cobra.Model
    cobra_ecosys.solver = solver 
    model1_id = model1.id
    model2_id = model2.id
    sampling = utils.pareto_sampling(cobra_ecosys, xy, solo_growth_model1, solo_growth_model2, model1_id, model2_id, model1_biomass_id, model2_biomass_id, sample_size=sample_size)
    correlation_reactions = utils.correlation(sampling)
    potential_crossfeeding = utils.crossfed_mets(model1 = model1, sampling = sampling, 
                                                correlation_reactions = correlation_reactions, model1_id = model1_id, model2_id = model2_id, model1_biomass_id=model1_biomass_id,
                                                model2_biomass_id=model2_biomass_id, exchange_correlation = exchange_correlation, 
                                                biomass_correlation = biomass_correlation, lower_exchange_proportion = lower_exchange_proportion)
    if plot: #Visualize pareto front
        utils.plot_exchange(model1, sampling, potential_crossfeeding, model1_id, model2_id)
    if retrieve_data == "all":
        return potential_crossfeeding, sampling
    if retrieve_data == "selection":
        sampling_data = utils.extract_sampling_data(model1, sampling, potential_crossfeeding, model1_id, model2_id)
        return potential_crossfeeding, sampling_data
    else:
        return potential_crossfeeding


def enterocyte_interaction_score_and_type(model, solver, medium = None, undescribed_metabolites_constraint = None, 
                                          undescribed_met_lb = -0.1, plot = False):
    """
    A function infering the interaction between a given model and a small intestinal epithelial cell (sIEC) adapted from https://doi.org/10.1093/hmg/ddt119.
    Returns qualitative (interaction_type) and quantitative (interaction_score) information on their metabolic interaction.
    
    Parameters
    ----------
    model2 : cobra.Model 
    medium : pandas series
        **Index** : metabolites names
        **values**  : Availability of corresponding metabolite in the medium as a positive flux value. 
    undescribed_metabolites_constraint : string ("blocked", "partially_constrained" or "as_is"). 
        How strictly constrained are the medium metabolites for which the flux is not described in the medium dataframe.
        **"blocked"** : They are not available in the medium at all (can result in model unable to grow)
        **"partially_constrained"** : They are made available with an influx in the medium of 1 mmol.gDW^-1.h^-1
        **"as_is"** : Their availability is the same as in the original inputted model.
    solver : string
        solver supported by the cobra toolbox. "cplex" or "gurobi" are recommended but require prior installation.
    model1_biomass_id : string
    undescribed_met_lb : negative float, optional
        Lower bound assigned to metabolites exchanges reactions that are not described in the given medium, when the "undescribed_metabolic_constraint" argument is set to "partially_constrained".
        Default is -0.1
    namespace : string, optionnal
        **"bigg"** : enterocyte and medium in the BiGG namespace. Compatible with CarveMe.
        **"agora"** : enterocyte and medium in the Agora namespace: Compatible with Agora and VMH models. (Built with Model SEED / Kbase)
        default is "bigg"
    plot : Boolean, optional
        Rudimentary integrated plot function to visualize Pareto front.
        default is False

    Returns
    -------
    interaction_score : float
        Predicts the nature of the interaction between host and model 2. 
        Score < 0 predicts a competitive interaction,
        Score = 0 predicts a neutral interaction
        Score > 0 predicts a positive interaction
    interaction_type : string
        Qualitative description of the interaction.
    """
    if medium is None:
        warnings.warn("You have not specified a medium composition. The model's bounds will be constrained based on the inputted model's exchange constraints")
    elif undescribed_metabolites_constraint == None:
        warnings.warn("You did not define a level of constraint for metabolites not described in the inputted medium. By default, the 'partially_constrained' option will be selected and a lower bound of -1 will be applied. Define the argument 'undescribed_metabolites_constraint' to chose a more suitable constraint.")
        undescribed_metabolites_constraint = "partially_constrained"
    namespace, suffixe = utils.find_namespace(model)
    if namespace == "bigg":
        host = cobra.io.read_sbml_model(files("mimeco.resources").joinpath('enterocyte_BiGG.xml'))
    elif namespace == "agora":
        host = cobra.io.read_sbml_model(files("mimeco.resources").joinpath('enterocyte_VMH_v3.xml'))
    else:
        raise RuntimeError("The inputted metabolic model's namespace is not compatible with the host model. You must use a model writen in bigg or agora namespace.")
    host.solver = solver
    host.objective = host.reactions.get_by_id('biomass_reactionIEC01b')
    metabolic_dict = utils.create_ecosystem_metabolic_dict(host, model)
    #Restrain enterocyte exchanges with the blood compartment.
    host = enterocyte_specific_utils.restrain_blood_exchange_enterocyte(host, namespace = namespace)
    #Infers maximal objective value of both models seperately, in the given medium.
    with host:
        host, constrained_medium_dict1 = utils.restrain_medium(host, medium, undescribed_metabolites_constraint)
        solo_growth_host = host.optimize().objective_value
        print(solo_growth_host)
    with model:
        model, constrained_medium_dict2 = utils.restrain_medium(model, medium, undescribed_metabolites_constraint)
        solo_growth_model = model.optimize().objective_value
        print(solo_growth_model)
    if solo_growth_host == solo_growth_model == 0:
        raise RuntimeError("Both models had a null objective value when modeled alone in the given medium."+
                           " To enable this analysis, you need to adjust the medium or models. You can also"+
                           " try to lighten the medium constraint by using the \"partially_constrained\""+
                           " option for the undescribed_metabolites_constraint argument.") 
    elif solo_growth_host == 0 or solo_growth_model == 0:
        warnings.warn("One model had a null objective value when modeled alone in the given medium."+
                      " If this is not an expected result, you might want to use the \"partially_constrained\""+
                      " option for the undescribed_metabolites_constraint argument, or redefine your medium or model.")
    medium_dict = {**constrained_medium_dict1, **constrained_medium_dict2} #Translate medium constraint for mocba
    if namespace == "bigg":
        medium_dict["o2_e"] = (0, host.reactions.get_by_id("EX_o2_e").upper_bound) #O2 can only appear by enterocyte secretion.
    elif namespace == "agora":
        medium_dict["o2(e)"] = (0, host.reactions.get_by_id("EX_o2(e)").upper_bound) #O2 can only appear by enterocyte secretion.
    # mocba will create new exchange reaction exterior to both models. the original exchange reactions, if restrained, will prevent 
    #exchanges between organisms. Here we unconstrain them.
    host = utils.unrestrain_medium(host)
    model = utils.unrestrain_medium(model)
    sol_mofba = utils.mo_fba(host, model, metabolic_dict, medium_dict)[0] #get multi-objective solution (pareto front)
    xy, maxi_host, maxi_model = utils.pareto_parsing(sol_mofba, solo_growth_host, solo_growth_model) #parse and normalize pareto front
    interaction_score = utils.infer_interaction_score(xy) #measure AUC of Pareto front, translates it in quantitative interaction prediction
    interaction_type = utils.infer_interaction_type(interaction_score, maxi_host, maxi_model,solo_growth_host, solo_growth_model) #infers interaction type from pareto front's shape.
    if plot: #Visualize Pareto front
        model2_id = model.id
        utils.pareto_plot(xy, "enterocyte", model2_id)
    return interaction_score, interaction_type

def enterocyte_crossfed_metabolites(model, solver, model_biomass_id, medium = None, undescribed_metabolites_constraint = None, undescribed_met_lb = -0.1,
                                    plot = False, sample_size = 1000, exchange_correlation = 0.5, biomass_correlation = 0.8, 
                                    retrieve_data = "no"):
    """
    A function that, given 2 models in the same namespace and a defined medium, predicts metabolic exchanges that
    are correlated with the increase of model2 objective value.

    Parameters
    ----------
    model : cobra.Model
    medium : pandas series
        **Index** : metabolites names
        **values**  : Availability of corresponding metabolite in the medium as a positive flux value. 
    undescribed_metabolites_constraint : string ("blocked", "partially_constrained" or "as_is"). 
        How strictly constrained are the medium metabolites for which the flux is not described in the medium dataframe.
        **"blocked"** : They are not available in the medium at all (can result in model unable to grow)
        **"partially_constrained"** : They are made available with an influx in the medium of 1 mmol.gDW^-1.h^-1
        **"as_is"** : Their availability is the same as in the original inputted model.
    solver : string
        solver supported by the cobra toolbox. "cplex" or "gurobi" are recommended but require prior installation.
    undescribed_met_lb : negative float, optional
        Lower bound assigned to metabolites exchanges reactions that are not described in the given medium, when the "undescribed_metabolic_constraint" argument is set to "partially_constrained".
        Default is -0.1
    exchange_correlation : float between 0 and -1, optional
        defines the threshold for the correlation between secretion and uptake of a same metabolite by paired models for this metabolite to be considered exchanged
        default is 0.5
    biomass_correlation : float between 0 and 1, optional
        correlation threshold between the exchange of the metabolite and the biomass production of model2 for its selection as crossfed.
        default is 0.8
    plot : Boolean, optional
        Rudimentary integrated plot function to visualize Pareto front.
    sample_size : int, optional
        Number of samples sampled from the Pareto front to infer correlation between exchange reactions and biomass. 
        Default is 1000.
    retrieve_data : str, optional
        Returns data that can be used for custom analysis.
        **"all"**: returns the sampling dataframe containing the fluxes of each reaction of the ecosystem in all samples. 
        **"selection"**: returns a subset of the sampling dataframe, containing the predicted crossfed metabolites exchange fluxes in all samples of the Pareto front, 
        as well as the objective value of each model in these samples.
        If retrieve_data is set on "all" or "selection", the function returns a second variable with the corresponding dataframe. 
        default is "no"

    Returns
    -------
    potential_crossfeeding : dictionnary
        **keys**: metabolites id
        **values**: [proportion of samples featuring inverse secretion/uptake for a same metabolite, 
        proportion of samples with metabolite exchange from model1 to model2, 
        proportion of samples with metabolite exchange from model2 to model1]
    sampling_data : pandas dataframe
        Dataframe based on the sampling, resulting in each row being a sample.
        **if retrieve_data == "selection"**
        The first two columns records the objective value, in the given sample, of both models.
        Other columns are, by pairs, the flux values of the exchange reactions of a crossfed metabolite for both models.
        **if retrieve_data == "all"**
        Columns are all reaction of the ecosystem model in the order of ecosys.reactions.
    """
    if medium is None:
        warnings.warn("You have not specified a medium composition. The model's bounds will be constrained based on the inputted model's exchange constraints")
    elif undescribed_metabolites_constraint == None:
        warnings.warn("You did not define a level of constraint for metabolites not described in the inputted medium. By default, the 'partially_constrained' option will be selected and a lower bound of -1 will be applied. Define the argument 'undescribed_metabolites_constraint' to chose a more suitable constraint.")
        undescribed_metabolites_constraint = "partially_constrained"
    namespace, suffixe = find_namespace(model)
    if namespace == "bigg":
        host = cobra.io.read_sbml_model(files("mimeco.resources").joinpath('enterocyte_BiGG.xml'))
    elif namespace == "agora":
        host = cobra.io.read_sbml_model(files("mimeco.resources").joinpath('enterocyte_VMH_v3.xml'))
    else:
        raise RuntimeError("The inputted metabolic model's namespace is not compatible with the host model. You must use a model writen in bigg or agora namespace.")

    host.solver = solver
    host.objective = host.reactions.get_by_id('biomass_reactionIEC01b')
    host_biomass_id = 'biomass_reactionIEC01b'
    metabolic_dict = utils.create_ecosystem_metabolic_dict(host, model)
    #Restrain enterocyte exchanges with the blood compartment.
    host = enterocyte_specific_utils.restrain_blood_exchange_enterocyte(host, namespace = namespace)
    #Infers maximal objective value of both models seperately, in the given medium.
    with host:
        host, constrained_medium_dict1 = utils.restrain_medium(host, medium, undescribed_metabolites_constraint)
        solo_growth_host = host.optimize().objective_value
        print(solo_growth_host)
    with model:
        model, constrained_medium_dict2 = utils.restrain_medium(model, medium, undescribed_metabolites_constraint)
        solo_growth_model = model.optimize().objective_value
        print(solo_growth_model)
    if solo_growth_host == solo_growth_model == 0:
        raise RuntimeError("Both models had a null objective value when modeled alone in the given medium."+
                           " To enable this analysis, you need to adjust the medium or models. You can also"+
                           " try to lighten the medium constraint by using the \"partially_constrained\""+
                           " option for the undescribed_metabolites_constraint argument.") 
    elif solo_growth_host == 0 or solo_growth_model == 0:
        warnings.warn("One model had a null objective value when modeled alone in the given medium."+
                      " If this is not an expected result, you might want to use the \"partially_constrained\""+
                      " option for the undescribed_metabolites_constraint argument, or redefine your medium or model.")
    medium_dict = {**constrained_medium_dict1, **constrained_medium_dict2} #Translate medium constraint for mocba
    if namespace == "bigg":
        medium_dict["o2_e"] = (0, host.reactions.get_by_id("EX_o2_e").upper_bound) #O2 can only appear by enterocyte secretion.
    elif namespace == "agora":
        medium_dict["o2(e)"] = (0, host.reactions.get_by_id("EX_o2(e)").upper_bound) #O2 can only appear by enterocyte secretion.
    # mocba will create new exchange reaction exterior to both models. the original exchange reactions, if restrained, will prevent 
    #exchanges between organisms. Here we unconstrain them.
    host = utils.unrestrain_medium(host)
    model = utils.unrestrain_medium(model)
    sol_mofba, ecosys = utils.mo_fba(host, model, metabolic_dict, medium_dict) #get multi-objective solution (pareto front), and ecosystem model from mocba 
    xy, maxi_host, maxi_model = utils.pareto_parsing(sol_mofba, solo_growth_host, solo_growth_model) #parse and normalize pareto front
    cobra_ecosys = utils.mocba_to_cobra(ecosys) #Translate mocba ecosystem into cobra.Model
    cobra_ecosys.solver = solver 
    model_id = model.id
    sampling = utils.pareto_sampling(cobra_ecosys, xy, solo_growth_host, solo_growth_model, host.id, model_id, host_biomass_id, model_biomass_id, sample_size = sample_size)
    correlation_reactions = utils.correlation(sampling)
    potential_crossfeeding = utils.crossfed_mets(model1 = model, sampling = sampling, 
                                                correlation_reactions = correlation_reactions, model1_id = model_id, model2_id = host.id, model1_biomass_id=model_biomass_id,
                                                model2_biomass_id = host_biomass_id, exchange_correlation = exchange_correlation,
                                                biomass_correlation = biomass_correlation)
    if plot: #Visualize pareto front
        utils.plot_exchange(model1, sampling, potential_crossfeeding, host.id, model_id, namespace = namespace)
    if retrieve_data == "all":
        sampling_data = sampling
        return potential_crossfeeding, sampling_data
    if retrieve_data == "selection":
        relevant_data = utils.extract_relevant_data(sampling, potential_crossfeeding, model1_id, model2_id, namespace = namespace)
        return potential_crossfeeding, sampling_data
    else:
        return potential_crossfeeding