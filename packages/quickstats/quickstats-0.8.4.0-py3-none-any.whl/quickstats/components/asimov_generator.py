from typing import Optional, Dict, List, Union
import copy

from quickstats import DescriptiveEnum, cached_import
from quickstats.components import AnalysisObject
from quickstats.utils.common_utils import parse_config
from quickstats.components.basics import WSArgument

class AsimovType(DescriptiveEnum):
    Temp                         = (-999, "do not generate any asimov")
    S_NP_Nom                     = (-2, "S + B Asimov (mu = 1) with nominal NP values")
    B_NP_Nom                     = (-1, "B only Asimov (mu = 0) with nominal NP values")
    B_NP_Fit                     = (0, "B only Asimov (mu = 0) with NP values profiled to data (fit with mu fixed at 0)")
    S_NP_Fit                     = (1, "S + B Asimov (mu = 1) with NP values profiled to data (fit with mu fixed at 1)")
    S_NP_Fit_muhat               = (2, "S + B Asimov (mu = 1) with NP values profiled to data (fit with mu floating)")
    B_unconstrained_NP_Fit       = (3, "B only Asimov (mu = 0) with unconstrained NP values profiled to data "
                                   "(fit with mu fixed at 0 and constrained NP fixed at 0)")
    S_unconstrained_NP_Fit       = (4, "S + B Asimov (mu = 1) with unconstrained NP values profiled to data "
                                   "(fit with mu fixed at 1 and constrained NP fixed at 0)")
    S_unconstrained_NP_Fit_muhat = (5, "S + B Asimov (mu = 1) with unconstrained NP values profiled to data "
                                   "(fit with mu floating and constrained NP fixed at 0)")
    
class AsimovGenerator(AnalysisObject):

    ASIMOV_SETTINGS = {
        AsimovType.Temp: None,
        AsimovType.S_NP_Nom: {
            "asimov_name": "asimovData_1_NP_Nominal",
            "asimov_snapshot": "asimovData_1_NP_Nominal",
            "poi_val": 1,
            "poi_profile": 1,
            "do_fit": False,
            "modify_globs": False
        },
        AsimovType.B_NP_Nom: {
            "asimov_name": "asimovData_0_NP_Nominal",
            "asimov_snapshot": "asimovData_0_NP_Nominal",
            "poi_val": 0,
            "poi_profile": 0,
            "do_fit": False,
            "modify_globs": False
        },
        AsimovType.B_NP_Fit: {
            "asimov_name": "asimovData_0_NP_Profile",
            "asimov_snapshot": "asimovData_0_NP_Profile",
            "poi_val": 0,
            "poi_profile": 0,
            "do_fit": True,
            "modify_globs": True
        },
        AsimovType.S_NP_Fit: {
            "asimov_name": "asimovData_1_NP_Profile",
            "asimov_snapshot": "asimovData_1_NP_Profile",
            "poi_val": 1,
            "poi_profile": 1,
            "do_fit": True,
            "modify_globs": True
        },
        AsimovType.S_NP_Fit_muhat: {
            "asimov_name": "asimovData_muhat_NP_Profile",
            "asimov_snapshot": "asimovData_muhat_NP_Profile",
            "poi_val": 1,
            "poi_profile": None,
            "do_fit": True,
            "modify_globs": True
        },
        AsimovType.B_unconstrained_NP_Fit: {
            "asimov_name": "asimovData_0_unconstrained_NP_Profile",
            "asimov_snapshot": "asimovData_0_unconstrained_NP_Profile",
            "poi_val": 0,
            "poi_profile": 0,
            "do_fit": True,
            "modify_globs": True,
            "constraint_option": 1
        },
        AsimovType.S_unconstrained_NP_Fit: {
            "asimov_name": "asimovData_1_unconstrained_NP_Profile",
            "asimov_snapshot": "asimovData_1_unconstrained_NP_Profile",
            "poi_val": 1,
            "poi_profile": 1,
            "do_fit": True,
            "modify_globs": True,
            "constraint_option": 1
        },
        AsimovType.S_unconstrained_NP_Fit_muhat: {
            "asimov_name": "asimovData_muhat_unconstrained_NP_Profile",
            "asimov_snapshot": "asimovData_muhat_unconstrained_NP_Profile",
            "poi_val": 1,
            "poi_profile": None,
            "do_fit": True,
            "modify_globs": True,
            "constraint_option": 1
        }
    }    
    
    DEFAULT_ASIMOV_TYPES = [AsimovType.B_NP_Fit, AsimovType.S_NP_Fit, AsimovType.S_NP_Fit_muhat]
    
    def __init__(self, filename:str, poi_name:str=None,
                 data_name:str='combData', 
                 config:Optional[Union[Dict, str]]=None,
                 verbosity:Optional[Union[int, str]]="INFO", **kwargs):
        config = parse_config(config)
        config['filename']  = filename
        config['poi_name']  = poi_name
        config['data_name'] = data_name
        config['verbosity'] = verbosity
        if 'preset_param' not in config:
            config['preset_param'] = True
        self._inherit_init(super(AsimovGenerator, self).__init__, **config)
        
    def generate_standard_asimov(
        self,
        asimov_types:Optional[Union[List[AsimovType], List[int], List[str]]]=None,
        asimov_names:Optional[Union[List[str], str]]=None,
        asimov_snapshots:Optional[Union[List[str], str]]=None,
        poi_scale:Optional[float]=None,
        do_import:Optional[bool]=True,
        overwrite: bool = True,
        method:Optional[str]="baseline"
    ):
        single_asimov = False
        if asimov_types is None:
            asimov_types = self.DEFAULT_ASIMOV_TYPES
        if isinstance(asimov_types, (int, str, AsimovType)):
            asimov_types = [AsimovType.parse(asimov_types)]
            single_asimov = True
        else:
            asimov_types = [AsimovType.parse(atype) for atype in asimov_types]
        if asimov_names is not None:
            if isinstance(asimov_names, str):
                asimov_names = [asimov_names]
            assert len(asimov_names) == len(asimov_types)
        if asimov_snapshots is not None:
            if isinstance(asimov_snapshots, str):
                asimov_snapshots = [asimov_snapshots]
            assert len(asimov_snapshots) == len(asimov_types)            
        if poi_scale is None:
            poi_scale = 1.0
            
        ROOT = cached_import("ROOT")
        if isinstance(self.poi, ROOT.RooArgSet):
            poi_name = [poi.GetName() for poi in self.poi]
        else:
            poi_name = self.poi.GetName()
            
        self.save_snapshot(self.kTempSnapshotName, WSArgument.MUTABLE)
        asimov_datasets = []
        for i, asimov_type in enumerate(asimov_types):
            self.load_snapshot(self.kTempSnapshotName)
            kwargs = copy.deepcopy(self.ASIMOV_SETTINGS[asimov_type])
            if kwargs is None:
                continue
            kwargs['poi_name'] = poi_name
            for key in ['poi_val', 'poi_profile']:
                if kwargs[key] is not None:
                    kwargs[key] *= poi_scale
            if asimov_names is not None:
                kwargs['asimov_name'] = asimov_names[i]
            if asimov_snapshots is not None:
                kwargs['asimov_snapshot'] = asimov_snapshots[i]
            kwargs['dataset'] = self.model.data
            kwargs['minimizer_options'] = self.default_minimizer_options
            kwargs['nll_options'] = self.default_nll_options
            kwargs['do_import'] = do_import
            kwargs['method'] = method
            kwargs['overwrite'] = overwrite
            asimov_dataset = self.model.generate_asimov(**kwargs)
            asimov_datasets.append(asimov_dataset)
        if single_asimov:
            return asimov_datasets[0]
        return asimov_datasets