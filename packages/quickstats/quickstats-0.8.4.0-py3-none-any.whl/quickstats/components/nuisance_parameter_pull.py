##################################################################################################
# Based on https://gitlab.cern.ch/atlas-physics/stat/tools/StatisticsTools by Stefan Gadatsch
# Author: Alkaid Cheng
# Email: chi.lung.cheng@cern.ch
##################################################################################################
import os
import sys
import time
import json
import fnmatch
from itertools import repeat
from typing import List, Optional, Union

import numpy as np

from quickstats import AbstractObject, cls_method_timer, Logger, cached_import
from quickstats.components import ExtendedModel, ExtendedMinimizer
from quickstats.utils import root_utils, common_utils, string_utils

class NuisanceParameterPull(AbstractObject):
    @property
    def model(self):
        return self._model
    
    @property
    def workspace(self):
        return self._workspace
    @property
    def model_config(self):
        return self._model_config
    @property
    def pdf(self):
        return self._pdf
    @property
    def data(self):
        return self._data
    @property
    def nuisance_parameters(self):
        return self._nuisance_parameters
    @property
    def global_observables(self):
        return self._global_observables
    @property
    def pois(self):
        return self._pois
    @property
    def observables(self):
        return self._observables  
    
    def __init__(self, verbosity:Optional[Union[int, str]]="INFO"):
        super().__init__(verbosity=verbosity)
        self._model               = None
        self._workspace           = None
        self._model_config        = None
        self._pdf                 = None
        self._data                = None
        self._nuisance_parameters = None
        self._global_observables  = None
        self._pois                = None
        self._observables         = None
    
    @staticmethod
    def evaluate_impact(model:ExtendedModel, minimizer:ExtendedMinimizer,
                        nuis, nominal_value, pois, minimizer_options, snapshot=None):
        poi_values = []
        start_time = time.time()
        if snapshot:
            model.workspace.loadSnapshot(snapshot)
        nuis.setVal(nominal_value)
        nuis.setConstant(1)   
        minimizer.minimize(**minimizer_options)
        for poi in pois:
            poi_values.append(poi.getVal())
        elapsed_time = time.time() - start_time
        return poi_values, elapsed_time

    @staticmethod
    def _run_pulls(filename:str, data_name:str, snapshot_name:str, nuis_name:str, poi_name:str, 
                   fix_param:Optional[str]=None, profile_param:Optional[str]=None,
                   binned_likelihood:bool=True, ws_name:Optional[str]=None, mc_name:Optional[str]=None,
                   minimizer_type:str='Minuit2', minimizer_algo:str='Migrad', 
                   precision:float=0.001, eps:float=1.0, retry:int=0, strategy:int=0, print_level:int=1,
                   num_cpu:int=1, offset:bool=True, optimize:int=2, eigen:bool=False,
                   fix_cache:bool=True, fix_multi:bool=True, max_calls:int=-1, 
                   max_iters:int=-1, batch_mode:bool=False, int_bin_precision:float=-1.,
                   outdir:str='pulls', cache=True, logfile_path=None,
                   minimizer_cls=None, verbosity:str="INFO", **kwargs):
        ROOT = cached_import("ROOT")
        stdout = Logger(verbosity)
        stdout.warning("The NuisanceParameterPull class is deprecated. "
                       "Please switch to the NuisanceParameterRanking class instead")
        # create output directory if not exists
        if not os.path.exists(outdir):
            os.makedirs(outdir, exist_ok=True)        
        outname_root = os.path.join(outdir, nuis_name + '.root')
        outname_json = os.path.join(outdir, nuis_name + '.json')
        #checkpointing:
        if (os.path.exists(outname_root) and os.path.exists(outname_json)) and cache:
            stdout.info('Jobs already finished for the NP: {}. Skipping.'.format(nuis_name))
            return None
        else:
            stdout.info('Evaluating pulls for the NP: {}'.format(nuis_name))
        if logfile_path is not None:
            common_utils.redirect_stdout(logfile_path)
        start_time = time.time()
        # load model
        model = ExtendedModel(filename=filename, ws_name=ws_name,
                              mc_name=mc_name, data_name=data_name, 
                              snapshot_name=snapshot_name, binned_likelihood=binned_likelihood,
                              fix_cache=fix_cache, fix_multi=fix_multi,
                              verbosity=verbosity)
        if fix_param:
            model.fix_parameters(fix_param)
            
        # by default fix all POIs before floating
        model.set_parameters_with_expression('<poi>=___0.15', mode='fix')
        for param in model.pois:
            extra_str = 'Fixing' if param.isConstant() else 'Set'
            stdout.info('{} POI {} at value {}'.format(extra_str, param.GetName(), param.getVal()))
        
        # collect pois
        rank_pois = model.profile_parameters(poi_name)
        model.set_parameters_with_expression(f'{poi_name}=___0.15', mode='unchanged')
        
        # profile pois
        if profile_param:
            stdout.info('Profiling POIs')
            profile_pois = model.profile_parameters(profile_param)
        
        buffer_time = time.time()
    
        nuip = model.workspace.var(nuis_name)
        if not nuip:
            raise ValueError(f'Nuisance parameter "{nuis_name}" does not exist')
        nuip_name = nuip.GetName()
        nuip.setConstant(0)
        stdout.info('Computing error for parameter "{}" at {}'.format(nuip.GetName(), nuip.getVal()))
        
        stdout.info('Making ExtendedMinimizer for unconditional fit')
        if minimizer_cls is None:
            minimizer_cls = ExtendedMinimizer
        minimizer = minimizer_cls("minimizer", model.pdf, model.data, workspace=model.workspace)
        stdout.info('Starting minimization')
        nll_commands = [ROOT.RooFit.NumCPU(num_cpu, 3),
                        #ROOT.RooFit.Constrain(model.nuisance_parameters),
                        ROOT.RooFit.GlobalObservables(model.global_observables), 
                        ROOT.RooFit.Offset(offset)]
        if hasattr(ROOT.RooFit, "BatchMode"):
            nll_commands.append(ROOT.RooFit.BatchMode(batch_mode))
        if hasattr(ROOT.RooFit, "IntegrateBins"):
            nll_commands.append(ROOT.RooFit.IntegrateBins(int_bin_precision))

        minimize_options = {
            'minimizer_type'   : minimizer_type,
            'minimizer_algo'   : minimizer_algo,
            'strategy' : strategy,
            'optimize'         : optimize,
            'precision'        : precision,
            'eps'              : eps,
            'retry'            : retry,
            'max_calls'        : max_calls,
            'max_iters'        : max_iters,
        }

        minimizer.minimize(nll_commands=nll_commands,
                           scan=1, scan_set=ROOT.RooArgSet(nuip),
                           **minimize_options)
        unconditional_time = time.time() - buffer_time
        stdout.info('Fitting time: {:.3f} s'.format(unconditional_time))
        pois_hat = []
        for rank_poi in rank_pois:
            name = rank_poi.GetName()
            value = rank_poi.getVal()
            pois_hat.append(value)
            print(f'\t{name} = {value}')
        
        model.workspace.saveSnapshot('tmp_snapshot', model.pdf.getParameters(model.data))
        stdout.info('Made unconditional snapshot with name tmp_snapshot')
        
        # find prefit variation
        buffer_time = time.time()
        
        nuip_hat = nuip.getVal()
        nuip_errup = nuip.getErrorHi()
        nuip_errdown = nuip.getErrorLo()

        all_constraints = model.get_all_constraints()
        prefit_variation, constraint_type, nuip_nom = model.inspect_constrained_nuisance_parameter(nuip, all_constraints)
        if not constraint_type:
            stdout.info('Not a constrained parameter. No prefit impact can be determined. Use postfit impact instead.')
        prefit_uncertainty_time = time.time() - buffer_time
        stdout.info('Time to find prefit variation: {:.3f} s'.format(prefit_uncertainty_time))
        
        if rank_pois:
            new_minimizer_options = {
                'nll_commands': nll_commands,
                'reuse_nll'   : 1,
                **minimize_options
            }
            # fix theta at the MLE value +/- postfit uncertainty and minimize again to estimate the change in the POI
            stdout.info('Evaluating effect of moving {} up by {} + {}'.format(nuip_name, nuip_hat, nuip_errup))
            pois_up, postfit_up_impact_time = NuisanceParameterPull.evaluate_impact(model, minimizer,
                                                nuip, nuip_hat + abs(nuip_errup), rank_pois,
                                                new_minimizer_options,  'tmp_snapshot')
            stdout.info('Time to find postfit up impact: {:.3f} s'.format(postfit_up_impact_time))
            
            stdout.info('Evaluating effect of moving {} down by {} - {}'.format(nuip_name, nuip_hat, nuip_errup))
            pois_down, postfit_down_impact_time = NuisanceParameterPull.evaluate_impact(model, minimizer,
                                                    nuip, nuip_hat - abs(nuip_errdown), rank_pois,
                                                    new_minimizer_options,  'tmp_snapshot')
            stdout.info('Time to find postfit down impact: {:.3f} s'.format(postfit_down_impact_time))
            
            # fix theta at the MLE value +/- prefit uncertainty and minimize again to estimate the change in the POI
            
            if constraint_type:
                stdout.info('Evaluating effect of moving {} up by {} + {}'.format(nuip_name, nuip_hat, prefit_variation))
                pois_nom_up, prefit_up_impact_time = NuisanceParameterPull.evaluate_impact(model, minimizer,
                                                        nuip, nuip_hat + prefit_variation, rank_pois,
                                                        new_minimizer_options,  'tmp_snapshot')
                stdout.info('Time to find prefit up impact: {:.3f} s'.format(prefit_up_impact_time))      
                
                stdout.info('Evaluating effect of moving {} down by {} - {}'.format(nuip_name, nuip_hat, prefit_variation))
                pois_nom_down, prefit_down_impact_time = NuisanceParameterPull.evaluate_impact(model, minimizer,
                                                            nuip, nuip_hat - prefit_variation, rank_pois,
                                                            new_minimizer_options,  'tmp_snapshot')
                stdout.info('Time to find prefit down impact: {:.3f} s'.format(prefit_up_impact_time))
            else:
                stdout.warning('Prefit impact not estimated, instead postfit impact is cloned')
                pois_nom_up = [i for i in pois_up]
                pois_nom_down = [i for i in pois_down]
        else:
            pois_up, pois_down, pois_nom_up, pois_nom_down = [], [], [], []
        
        end_time = time.time()
        stdout.info(bare=True)
        stdout.info('Time to perform all fits: {:.3f} s'.format(end_time-start_time))
        stdout.info('Unconditional minimum of NP {}: {} + {} - {}'.format(nuis_name, nuip_hat, 
              abs(nuip_errup), abs(nuip_errdown)))
        stdout.info('Prefit uncertainy of NP {}: {} +/- {}'.format(nuis_name, nuip_hat, prefit_variation))
        for i, rank_poi in enumerate(rank_pois):
            stdout.info('Unconditional minimum of POI {}: {}'.format(rank_poi.GetName(), pois_hat[i]))
            stdout.info('POI when varying NP up by 1 sigma postfit (prefit): {} ({})'.format(pois_up[i], pois_nom_up[i]))
            stdout.info('POI when varying NP down by 1 sigma postfit (prefit): {} ({})'.format(pois_down[i], pois_nom_down[i]))
            
        # store result in root file
        outname_root = os.path.join(outdir, nuis_name + '.root')
        
        result = {}
        result['nuis'] = {  'nuisance'   : nuis_name,
                            'nuis_nom'   : nuip_nom,
                            'nuis_hat'   : nuip_hat,
                            'nuis_hi'    : nuip_errup,
                            'nuis_lo'    : nuip_errdown,
                            'nuis_prefit': prefit_variation}
        result['pois'] = {}
        for i, rank_poi in enumerate(rank_pois):
            name = rank_poi.GetName()
            result['pois'][name] = { 'hat'     : pois_hat[i],
                                     'up'      : pois_up[i],
                                     'down'    : pois_down[i],
                                     'up_nom'  : pois_nom_up[i],
                                     'down_nom': pois_nom_down[i]}
            
        result_for_root = {}
        result_for_root.update(result['nuis'])
        for k,v in result['pois'].items():
            buffer = {'{}_{}'.format(k, kk): vv for kk,vv in v.items()}
            result_for_root.update(buffer)
        r_file = ROOT.TFile(outname_root, "RECREATE")
        r_tree = ROOT.TTree("result", "result")
        root_utils.fill_branch(r_tree, result_for_root)
        r_file.Write()
        r_file.Close()
        stdout.info('Saved output to {}'.format(outname_root))
        outname_json = os.path.join(outdir, nuis_name + '.json')
        json.dump(result, open(outname_json, 'w'), indent=2)
        
        if logfile_path is not None:
            common_utils.restore_stdout()

    @cls_method_timer
    def run_pulls(self, filename:str, data_name:str='combData', poi_name:str='', 
                  snapshot_name:Optional[str]=None, outdir:str='output', profile_param:Optional[str]=None,
                  fix_param:Optional[str]=None, ws_name:Optional[str]=None, mc_name:Optional[str]=None,
                  minimizer_type:str='Minuit2', minimizer_algo:str='Migrad', num_cpu:int=1, save_log:bool=True,
                  binned_likelihood:bool=True, precision:float=0.001, eps:float=1.0, retry:int=0, verbosity:str='INFO',
                  eigen:bool=False, strategy:int=0, print_level:int=1, fix_cache:bool=True, fix_multi:bool=True,
                  offset:bool=True, optimize:int=2, filter_expr:Optional[str]=None, max_calls:int=-1, max_iters:int=-1,
                  batch_mode:bool=False, int_bin_precision:float=-1.,parallel:int=0, cache:bool=True,
                  exclude_expr:Optional[str]=None, constrained_only:bool=True, minimizer_cls=None, **kwargs):
        if poi_name is None:
            poi_name = ''
        # configure default minimizer options
        ExtendedMinimizer._configure_default_minimizer_options(minimizer_type, minimizer_algo,
            strategy, debug_mode=(verbosity=="DEBUG"))
        
        model = ExtendedModel(filename, ws_name, mc_name, data_name=data_name, verbosity="WARNING")
        # include constrained NPs only
        if constrained_only:
            nuis_list = [nuis.GetName() for nuis in model.get_variables("constrained_nuisance_parameter")]
        # include all NPs
        else:
            nuis_list = [nuis.GetName() for nuis in model.get_variables("nuisance_parameter")]
        if filter_expr:
            nuis_to_include = []
            include_patterns = string_utils.split_str(filter_expr, sep=',', remove_empty=True)
            for nuis_name in nuis_list:
                # filter out nuisance parameters
                if any(fnmatch.fnmatch(nuis_name, include_pattern) for include_pattern in include_patterns):
                    nuis_to_include.append(nuis_name)
        else:
            nuis_to_include = nuis_list
        nuis_to_exclude = []
        if exclude_expr is not None:
            exclude_patterns =  string_utils.split_str(exclude_expr, sep=',', remove_empty=True)
            for nuis_name in nuis_list:
                if any(fnmatch.fnmatch(nuis_name, exclude_pattern) for exclude_pattern in exclude_patterns):
                    nuis_to_exclude.append(nuis_name)
        nuis_names = sorted(list(set(nuis_to_include) - set(nuis_to_exclude)))
        
        if save_log:
            logfile_paths = [os.path.join(outdir, '{}.log'.format(nuis_name)) for nuis_name in nuis_names]
        else:
            logfile_paths = [None]*len(nuis_names)
            

        arguments = (repeat(filename), repeat(data_name), repeat(snapshot_name), nuis_names, 
                     repeat(poi_name), repeat(fix_param), repeat(profile_param), repeat(binned_likelihood),
                     repeat(ws_name), repeat(mc_name), repeat(minimizer_type), 
                     repeat(minimizer_algo), repeat(precision), repeat(eps), repeat(retry),
                     repeat(strategy), repeat(print_level), repeat(num_cpu), repeat(offset),
                     repeat(optimize), repeat(eigen), repeat(fix_cache), repeat(fix_multi),
                     repeat(max_calls), repeat(max_iters), repeat(batch_mode),
                     repeat(int_bin_precision), repeat(outdir), repeat(cache), logfile_paths,
                     repeat(minimizer_cls), repeat(verbosity))
        common_utils.execute_multi_tasks(self._run_pulls, *arguments, parallel=parallel)

        
    @staticmethod
    def parse_root_result(filename:str):
        import uproot
        with uproot.open(filename) as file:
            result = root_utils.uproot_to_dict(file)
        return result