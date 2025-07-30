###############################################################################
### This is a reimplementation of workspaceCombiner library in python
### original author: Hongtao Yang, Haoshuang Ji
###############################################################################
import os
import re
import json
from typing import Optional, Union, List, Dict

try:
    from tabulate import tabulate
except Exception:
    tabulate = None
    
import numpy as np

import ROOT

import quickstats
from quickstats import semistaticmethod, AbstractObject, GeneralEnum, timer
from quickstats.components import ExtendedModel
from quickstats.utils.xml_tools import TXMLTree
from quickstats.utils.root_utils import load_macro, get_macro_dir, is_corrupt
from quickstats.utils.common_utils import format_delimiter_enclosed_text
from quickstats.maths.numerics import is_float, pretty_value
from quickstats.components.workspaces import XMLWSBase, WSObjectType, BracketType
from quickstats.interface.root import RooDataSet
from quickstats.components.discrete_nuisance import DiscreteNuisance

class XMLWSCombiner(XMLWSBase):
    
    KEYWORDS = {
        "dummy": "dummy",
        "constrterm_suffix": "_Pdf",
        "globalobs_suffix": "_In",
        "weight_name": "_weight_",
        "comb_cat_name": "combCat",
        "comb_pdf_name": "combPdf",
        "comb_ws_name": "combWS",
        "comb_data_name": "combData",
        "comb_mc_name": "ModelConfig",
        "comb_nuis_name": "nuisanceParameters",
        "comb_glob_name": "globalObservables",
        "comb_obs_name": "observables",
        "rename_save_suffix": "rename_cache",
        "rename_comb_suffix": "combine_cache"
    }
    
    def __init__(self, source:Union[str, Dict],
                 basedir:Optional[str]=None,
                 minimizer_config:Optional[Dict]=None,
                 unlimited_stack=True,
                 verbosity:Optional[Union[int, str]]="INFO",
                 use_cms_opt_pdf=False,
                 use_cms_gaussian=True,
                 use_cms_add_extraconst=False) -> None:
        super().__init__(source=source, basedir=basedir,
                         unlimited_stack=unlimited_stack,
                         verbosity=verbosity)
        self.minimizer_config = minimizer_config
        self.use_cms_opt_pdf = use_cms_opt_pdf
        self.load_extension()
        with timer() as t:
            self.initialize(source=source)
        if not hasattr(ROOT, "RooSimultaneousOpt"):
            self.use_cms_opt_pdf = False
        self.use_cms_gaussian = use_cms_gaussian and hasattr(ROOT, "SimpleGaussianConstraint") and self.use_cms_opt_pdf
        self.init_time = t.interval
        self.cms_disc_set_keyword = DiscreteNuisance._DEFAULT_CONFIG_["disc_set_keyword"]
        self.cms_nuis_pdf_keyword = "CONSTRAINTPDF"
        self.use_cms_add_extraconst = use_cms_add_extraconst and self.use_cms_opt_pdf
        self.nuis_pdf_prefix = "nuisancePdf"
        self.with_nuis_pdf_suffix = "withconstr"
        self.without_nuis_pdf_suffix = "withoutconstr"
        
    def initialize(self, source:Union[str, Dict]) -> None:
        self.combination_config = {}
        self.channel_config     = {}
        self.asimov_actions     = []
        if isinstance(source, str):
            ext = os.path.splitext(source)[-1]
            if ext == ".xml":
                self.parse_config_xml(source)
            elif ext == ".json":
                self.parse_config_json(source)
            else:
                raise ValueError(f"unsupported file format: {ext}")
        elif isinstance(source, dict):
            self.parse_config_dict(source)
        else:
            raise ValueError(f"invalid input format: {source}")
        self.reset_tmp_ws()
        self.reset_comb_ws()
 
    def parse_config_xml(self, filename:str) -> None:
        root = TXMLTree.load_as_dict(filename)
        combination_config = {
            'output_file'      : self._get_node_attrib(root, "OutputFile", required=True),
            'workspace_name'   : self._get_node_attrib(root, "WorkspaceName", required=False,
                                                       default=self.KEYWORDS["comb_ws_name"]),
            'model_config_name': self._get_node_attrib(root, "ModelConfigName", required=False,
                                                       default=self.KEYWORDS["comb_mc_name"]),
            'data_name'        : self._get_node_attrib(root, "DataName", required=False,
                                                       default=self.KEYWORDS["comb_data_name"]),
            'strict'           : self._get_node_attrib(root, "Strict", required=False, default="false", dtype="bool")
        }
        self.combination_config = combination_config
        # parse child level attributes
        nodes = root['children']
        for node in nodes:
            tag = node['tag']
            if tag == "Channel":
                self.read_channel_node(node)
            elif tag == "POIList":
                self.read_combined_poi_node(node)
            elif tag == "Asimov":
                self.read_asimov_node(node)
            else:
                raise RuntimeError(f"unknown item `{tag}`")
    
    def parse_config_dict(self, source:Dict) -> None:
        raise NotImplementedError("not implemented")
    
    def parse_config_json(self, filename:str) -> None:
        with open(filename, 'r') as f:
            source = json.load(f)
        self.parse_config_dict(source)
        
    def _get_channel_model(self, channel_config:Dict) -> ExtendedModel:
        input_file = channel_config["input_file"]
        ws_name    = channel_config["workspace_name"]
        mc_name    = channel_config["model_config_name"]
        data_name  = channel_config["data_name"]
        model = ExtendedModel(input_file, ws_name=ws_name, mc_name=mc_name,
                              data_name=data_name, verbosity="WARNING")
        return model
    
    def _exception_check(self, msg:str, strict_mode:bool=False) -> None:
        if strict_mode:
            raise RuntimeError(msg)
        else:
            msg = msg[0].capitalize() + msg[1:]
            self.stdout.warning(f"{msg}. Skipped.")
    
    def _channel_check(self, channel:str, check_poi_map:bool=False):
        if channel not in self.channel_config:
            raise RuntimeError(f"channel \"{channel}\" not initialized")
        if check_poi_map and ("poi_map" not in self.channel_config[channel]):
            raise RuntimeError(f'missing poi definition for the channel "{channel}"')
            
    def reset_tmp_ws(self):
        workspace_name = self.combination_config["workspace_name"]
        self.tmp_file = None
        self.tmp_ws   = ROOT.RooWorkspace(workspace_name, workspace_name)
        self.tmp_nuis = ROOT.RooArgSet()
        self.tmp_glob = ROOT.RooArgSet()
        
    def load_cache_ws(self, ws_type:str):
        if ws_type == "rename":
            filename = self._get_tmp_ws_path()
        elif ws_type == "combine":
            filename = self._get_comb_ws_path()
        else:
            raise ValueError(f"invalid cache workspace type: {ws_type}")
        self.stdout.info(f'Reading temporary workspace file from "{filename}"')
        if not os.path.exists(filename):
            raise FileNotFoundError(f'temporary workspace file "{filename}" does not exist')
        file = ROOT.TFile(filename)
        if is_corrupt(file):
            raise RuntimeError(f'temporary workspace file "{filename}" is corrupted')
        workspace_name = self.combination_config["workspace_name"]
        workspace = file.Get(workspace_name)
        if not workspace:
            raise RuntimeError(f'failed to load workspace "{workspace_name}"')
        nuis_set_name = self.KEYWORDS['comb_nuis_name']
        glob_set_name = self.KEYWORDS['comb_glob_name']
        nuis_set = workspace.set(nuis_set_name)
        glob_set = workspace.set(glob_set_name)
        discrete_parameters = workspace.set(self.cms_disc_set_keyword)
        constrpdf_list_all = workspace.set(self.cms_nuis_pdf_keyword)
        if not nuis_set:
            raise RuntimeError(f'failed to load nuisance parameter set "{nuis_set_name}"')
        if not glob_set:
            raise RuntimeError(f'failed to load global observable set "{glob_set_name}"')
        if ws_type == "rename":
            self.tmp_file = file
            self.tmp_ws = workspace
            self.tmp_nuis = nuis_set.snapshot()
            self.tmp_glob = glob_set.snapshot()
            if discrete_parameters:
                self.discrete_params = discrete_parameters.snapshot()
            else:
                self.discrete_params = ROOT.RooArgSet(self.cms_disc_set_keyword)
            if constrpdf_list_all:
                self.constrpdf_list_all = constrpdf_list_all.snapshot(False)
            else:
                self.constrpdf_list_all = ROOT.RooArgSet(self.cms_nuis_pdf_keyword)
        elif ws_type == "combine":
            self.comb_file = file
            self.comb_ws = workspace
            self.tmp_nuis = nuis_set.snapshot()
            self.tmp_glob = glob_set.snapshot()
            obs_set_name = self.KEYWORDS['comb_obs_name']
            obs_set = workspace.set(obs_set_name)
            if not obs_set:
                raise RuntimeError(f'failed to load observable set "{obs_set_name}"')
            self.comb_obs = obs_set
            
    def reset_comb_ws(self):
        workspace_name = self.combination_config["workspace_name"]
        self.comb_file = None
        self.comb_ws   = ROOT.RooWorkspace(workspace_name, workspace_name)
        cat_name = self.KEYWORDS['comb_cat_name']
        pdf_name = self.KEYWORDS['comb_pdf_name']
        self.comb_cat = ROOT.RooCategory(cat_name, cat_name)
        if self.use_cms_opt_pdf:
            self.stdout.info("Using CMS optimized PDF")
            self.comb_pdf = ROOT.RooSimultaneousOpt(pdf_name, pdf_name, self.comb_cat)
        else:
            self.comb_pdf = ROOT.RooSimultaneous(pdf_name, pdf_name, self.comb_cat)
        self.comb_obs = ROOT.RooArgSet()
        self.comb_data_map = {}
        
    def read_combined_poi_node(self, node:Dict) -> None:
        poi_expressions = self._get_node_attrib(node, "Combined", required=True, dtype="str_list")
        poi_definitions = {}
        for poi_expr in poi_expressions:
            poi_name, content = self._extract_bracket_expr(poi_expr, BracketType.SQUARE)
            if not poi_name:
                raise ValueError(f"invalid format for a combined POI: {poi_expr}")
            if poi_name in poi_definitions:
                raise RuntimeError(f"Combined POI \"{poi_name}\" is defined more than once.")
            tokens = content.split("~")
            tokens_float = []
            for token in tokens:
                if not is_float(token):
                    raise ValueError(f"invalid numerical value \"{token}\" from the POI "
                                     f"expression \"{poi_expr}\"")
                tokens_float.append(float(token))
            poi_info = {
                "value": None,
                "min": None,
                "max": None
            }
            # only central value provided
            if len(tokens) == 1:
                poi_info["value"] = tokens_float[0]
            # only range provided
            elif len(tokens) == 2:
                if abs(tokens_float[0] - tokens_float[1]) < self.EPSILON:
                    poi_info["value"] = tokens_float[0]
                else:
                    poi_info["min"] = tokens_float[0]
                    poi_info["max"] = tokens_float[1]
            # central value and range provided
            elif len(tokens) == 3:
                    poi_info["value"] = tokens_float[0]
                    poi_info["min"]   = tokens_float[1]
                    poi_info["max"]   = tokens_float[2]
            else:
                raise ValueError(f"too many/few values to unpack from the POI expression \"{poi_expr}\"")
            poi_definitions[poi_name] = poi_info
        self.combination_config["poi_definition"] = poi_definitions
    
    def read_asimov_node(self, node:Dict) -> None:
        asimov_action = node['attrib']
        self.asimov_actions.append(asimov_action)

    def read_channel_node(self, node:Dict) -> None:
        channel_config = {
            'channel_name'      : self._get_node_attrib(node, "Name", required=True),
            'input_file'        : self._get_node_attrib(node, "InputFile", required=True),
            'workspace_name'    : self._get_node_attrib(node, "WorkspaceName", required=False),
            'model_config_name' : self._get_node_attrib(node, "ModelConfigName", required=False),
            'data_name'         : self._get_node_attrib(node, "DataName", required=False, default="combData"),
            'simplified_import' : self._get_node_attrib(node, "SimplifiedImport", required=False,
                                                        default="false", dtype="bool"),
            'argset_list'       : [],
            'argset_strict'     : False
        }
        channel = channel_config["channel_name"]
        if channel in self.channel_config:
            raise RuntimeError(f"the channel \"{channel}\" is included more than once")
        self.channel_config[channel] = channel_config
        self.channel_config[channel]['rename_map'] = {
            "pdf"  : {},
            "var"  : {}
        }
        self.channel_config[channel]['renamed_constraint'] = {}
        self.stdout.info(f"Checking XML input for the channel \"{channel}\".")
        # walk through child nodes
        child_nodes = node["children"]
        for child_node in child_nodes:
            tag = child_node['tag']
            if tag == "RenameMap":
                self.read_channel_rename_node(channel, child_node)
            elif tag == "POIList":
                self.read_channel_poi_node(channel, child_node)
            elif tag == "ArgSetList":
                self.read_channel_argset_node(channel, child_node)
            else:
                raise RuntimeError(f"unknown item `{tag}`")
        self.stdout.info(f"Successfully validated XML input for the channel \"{channel}\".")
    
    def read_channel_rename_node(self, channel:str, node:Dict) -> None:
        ext_file = self._get_node_attrib(node, "InputFile", required=False)
        if ext_file is not None:
            node = TXMLTree.load_as_dict(ext_file)
        child_nodes = node['children']
        for child_node in child_nodes:
            tag = child_node['tag']
            if tag == "Syst":
                self.read_rename_syst_node(channel, child_node)
            else:
                raise RuntimeError(f"unknown channel item `{tag}`")
                
    def read_channel_argset_node(self, channel:str, node:Dict) -> None:
        argset_list = self._get_node_attrib(node, "Input", required=False,
                                            default=[], dtype="str_list")
        argset_strict = self._get_node_attrib(node, "Strict", required=False,
                                              default="True", dtype="bool")
        self.channel_config[channel]['argset_list'] = argset_list
        self.channel_config[channel]['argset_strict'] = argset_strict
                
    def validate_channel_input(self, channel:str):
        self._channel_check(channel)
        self.stdout.info(f"Checking input workspace for the channel \"{channel}\".")
        channel_config = self.channel_config[channel]
        model = self._get_channel_model(channel_config)
        strict_mode = self.combination_config["strict"]
        ws_filename = model.config['filename']
        renamed_pdfs = list(channel_config["rename_map"]["pdf"])
        renamed_vars = list(channel_config["rename_map"]["var"])
        renamed_pois = list(channel_config["poi_map"].values())
        renamed_constraint = channel_config["renamed_constraint"]
        missing_obj_msg = f'{{obj_type}} "{{obj_name}}" does not exist in the workspace "{ws_filename}"'
        for pdf_name in renamed_pdfs:
            nuis_name = renamed_constraint[pdf_name]["nuis"]
            glob_name = renamed_constraint[pdf_name]["glob"]
            renamed_vars.remove(nuis_name)
            renamed_vars.remove(glob_name)            
            pdf = model.workspace.pdf(pdf_name)
            if not pdf:
                msg = missing_obj_msg.format(obj_type="Constraint PDF", obj_name=pdf_name)
                self._exception_check(msg, strict_mode)
                continue
            if not isinstance(pdf, ROOT.RooGaussian):
                #msg = f"constraint PDF \"{pdf_name}\" that is not an instance of RooGaussian is not supported"
                #self._exception_check(msg, strict_mode)
                continue
            nuis = model.workspace.var(nuis_name)
            if not nuis:
                msg = missing_obj_msg.format(obj_type="Nuisance parameter", obj_name=nuis_name)
                raise RuntimeError(msg)
            glob = model.workspace.var(glob_name)
            if not glob:
                msg = missing_obj_msg.format(obj_type="Global observable", obj_name=glob_name)
                raise RuntimeError(msg)
            nuis_check, glob_check, sigma_check, glob_value = False, False, False, None
            # this part can be optimized after ROOT 6.26
            server_iter = pdf.serverIterator()
            while True:
                server = server_iter.Next()
                if not server:
                    break
                server_name = server.GetName()
                if server_name == nuis_name:
                    nuis_check = True
                elif server_name == glob_name:
                    glob_check = True
                    glob_value = server.getVal()
                elif abs(server.getVal() - 1) < self.EPSILON:
                    sigma_check = True
                server_value = server.getVal()
            if (not sigma_check) and (glob_value != 1.):
                self.stdout.warning(f"sigma of constraint pdf \"{pdf_name}\" in the workspace \"{ws_filename}\" is not unity: {server_value}")
        for var_name in renamed_vars:
            if not model.workspace.var(var_name):
                msg = missing_obj_msg.format(obj_type="variable", obj_name=var_name)
                self._exception_check(msg, strict_mode)
                continue
        for poi_name in renamed_pois:
            if poi_name == self.KEYWORDS['dummy']:
                continue
            # check poi exist in workspace
            if not model.workspace.var(poi_name):
                raise RuntimeError(f"poi \"{poi_name}\" does not exist in the channel \"{channel}\"")
        # fix unspecified names
        channel_config['workspace_name'] = model.workspace.GetName()
        channel_config['model_config_name'] = model.model_config.GetName()
        channel_config['data_name'] = model.data.GetName()
        
        argset_list = channel_config["argset_list"]
        for argset in argset_list:
            argset_obj = model.workspace.obj(argset)
            if not argset_obj:
                if channel_config["argset_strict"]:
                    raise RuntimeError(f'Argument set "{argset}" does not exist in the channel "{channel}"')
                else:
                    self.stdout.warning(f'Argument set "{argset}" does not exist in the channel "{channel}". Skipped.')
                    continue
            if not isinstance(argset_obj, ROOT.RooArgSet):
                raise RuntimeError(f'Argument set "{argset}" from the channel "{channel}" is an instance of RooArgSet object')
        self.stdout.info(f"Successfully validated input workspace for the channel \"{channel}\".")
        
    def read_rename_syst_node(self, channel:str, node:Dict) -> None:
        self._channel_check(channel)
        channel_config = self.channel_config[channel]
        old_name = self._get_node_attrib(node, "OldName", required=True)
        new_name = self._get_node_attrib(node, "NewName", required=True)
        if not old_name:
            raise ValueError(f"missing attribute \"OldName\" from the Syst node (channel = {channel}):\n"
                             f"{node}")
        if not new_name:
            raise ValueError(f"missing attribute \"NewName\" from the Syst node (channel = {channel}):\n"
                             f"{node}")
        renamed_constraint = channel_config["renamed_constraint"]
        pdf_map  = channel_config["rename_map"]["pdf"]
        var_map  = channel_config["rename_map"]["var"]
        _, object_type = self._get_object_name_and_type_from_expr(new_name)
        if object_type != WSObjectType.DEFINED:
            raise ValueError(f"the attribute \"NewName\" ({new_name}) from the Syst node should contain "
                             "only the nuisance parameter name")
        new_names = list(var_map.values())
        if new_name in new_names:
            raise ValueError(f"New nuisance parameter \"{new_name}\" is duplicated in the channel \"{channel}\"")
        _, object_type = self._get_object_name_and_type_from_expr(old_name)
        if object_type == WSObjectType.CONSTRAINT:
            pdf_name, content = self._extract_bracket_expr(old_name, BracketType.ROUND)
            components = content.split(",")
            if len(components) != 2:
                raise ValueError(f"invalid format for constraint pdf \"{old_name}\" in channel \"{channel}\"")
            nuis_name = components[0]
            glob_name = components[1]
            if nuis_name in var_map:
                raise ValueError(f"Old nuisance parameter \"{new_name}\" is duplicated in the channel \"{channel}\"")
            var_map[nuis_name] = new_name
            if glob_name in var_map:
                raise ValueError(f"Old global observable \"{glob_name}\" is duplicated in the channel \"{channel}\"")
            var_map[glob_name] = new_name + self.KEYWORDS["globalobs_suffix"]
            if pdf_name in pdf_map:
                raise ValueError(f"Old PDF \"{pdf_name}\" is duplicated in the channel \"{channel}\"")
            pdf_map[pdf_name] = new_name + self.KEYWORDS["constrterm_suffix"]
            renamed_constraint[pdf_name] = {"nuis": nuis_name, "glob": glob_name}
        elif WSObjectType.DEFINED:
            if old_name in var_map:
                raise ValueError(f"Old nuisance parameter \"{old_name}\" is duplicated in the channel \"{channel}\"")
            var_map[old_name] = new_name
                
    def read_channel_poi_node(self, channel:str, node:Dict) -> None:
        self._channel_check(channel)
        channel_config = self.channel_config[channel]
        pois = self._get_node_attrib(node, "Input", required=True, dtype="str_list")
        if "poi_definition" not in self.combination_config:
            raise RuntimeError("Combined POIs not initialized")
        comb_pois = list(self.combination_config["poi_definition"])
        if len(pois) > len(comb_pois):
            raise RuntimeError(f"channel \"{channel}\" has more POIs than the combined model")
        poi_check = {}
        for poi in pois:
            if poi == self.KEYWORDS['dummy']:
                continue
            # check for duplication
            if poi in poi_check:
                raise RuntimeError(f"POI \"{poi}\" for the channel \"{channel}\" is defined more than once.")
            poi_check[poi] = None
        dummy_pois = [self.KEYWORDS['dummy']] * (len(comb_pois) - len(pois))
        pois += dummy_pois
        poi_map = dict(zip(comb_pois, pois))
        channel_config["poi_map"] = poi_map
        
    def _append_channel_suffix_to_args(self, channel:str, args:ROOT.RooArgSet, arg_type:str,
                                       ignore_list:Optional[List[str]]=None) -> None:
        if ignore_list is None:
            ignore_list = []
        for arg in args:
            arg_name = arg.GetName()
            if arg_name in ignore_list:
                continue
            arg.SetName(f"{arg_name}_{channel}")
            self.stdout.debug(f'Appended channel suffix "{channel}" to the {arg_type} '
                              f'"{arg_name}"')
    
    def _get_tmp_ws_path(self):
        basename = os.path.splitext(self.combination_config["output_file"])[0]
        filename = f"{basename}_{self.KEYWORDS['rename_save_suffix']}.root"
        return filename
    
    def _get_comb_ws_path(self):
        basename = os.path.splitext(self.combination_config["output_file"])[0]
        filename = f"{basename}_{self.KEYWORDS['rename_comb_suffix']}.root"
        return filename    
    
    def _get_weight_var(self):
        weight_var = ROOT.RooRealVar(self.KEYWORDS['weight_name'], "", 1.)
        return weight_var
    
    def _get_obs_and_weight(self, observables:ROOT.RooArgSet):
        weight_var = self._get_weight_var()
        obs_and_weight = ROOT.RooArgSet(observables, weight_var)
        return obs_and_weight, weight_var
    
    def get_channel_summary(self, channel:str, indent:int=4) -> str:
        self._channel_check(channel)
        channel_config = self.channel_config[channel]
        summary_text = ""
        summary_text += " "*indent + f" Input File Name: {channel_config['input_file']}" + "\n"
        summary_text += " "*indent + f"  Workspace Name: {channel_config['workspace_name']}" + "\n"
        summary_text += " "*indent + f"ModelConfig Name: {channel_config['model_config_name']}" + "\n"
        summary_text += " "*indent + f"       Data Name: {channel_config['data_name']}" + "\n"
        return summary_text

    def get_poi_table(self) -> str:
        if "poi_definition" not in self.combination_config:
            raise RuntimeError("missing poi definition for the combined channel")
        poi_maps = {}
        poi_maps["Combined"] = list(self.combination_config["poi_definition"])
        for channel in self.channel_config:
            self._channel_check(channel, check_poi_map=True)
            channel_config = self.channel_config[channel]
            channel_poi_map = channel_config['poi_map']
            poi_maps[channel] = []
            for poi in poi_maps["Combined"]:
                if poi not in channel_poi_map:
                    raise RuntimeError(f'missing mapping for the poi "{poi}" from the combined channel '
                                       f'to the channel "{channel}"')
                if poi == self.KEYWORDS['dummy']:
                    poi_maps[channel].append("-")
                else:
                    poi_maps[channel].append(channel_poi_map[poi])
        import pandas as pd
        df = pd.DataFrame(poi_maps)
        if tabulate is None:
            poi_table = df.to_string(index=False)
        else:
            poi_table = tabulate(df, headers='keys', tablefmt='psql', showindex=False)
        return poi_table
    
    def get_summary_text(self, indent:int=4) -> None:
        summary_text = ""
        n_channel = len(self.channel_config)
        title = format_delimiter_enclosed_text(f"Input summary ({n_channel} channels)",
                                               delimiter="-", indent_str="")
        summary_text += title
        for channel in self.channel_config:
            title = format_delimiter_enclosed_text(f"Channel: {channel}",
                                                   delimiter="+", indent_str="")
            summary_text += title
            channel_summary_text = self.get_channel_summary(channel, indent=indent)
            summary_text += channel_summary_text
        title = format_delimiter_enclosed_text("POI map", delimiter="-", indent_str="")
        summary_text += title
        poi_table = self.get_poi_table()
        summary_text += poi_table
        return summary_text
    
    def print_input_summary(self) -> None:
        summary_text = self.get_summary_text()
        self.stdout.info(summary_text, bare=True)
        
    def rename_channel(self, channel:str) -> None:
        self._channel_check(channel, check_poi_map=True)
        channel_config = self.channel_config[channel]
        simplified_import = channel_config["simplified_import"]
        self.stdout.info(f'Renaming objects for the channel "{channel}"')
        # do not reuse model
        model = self._get_channel_model(channel_config)
        workspace = model.workspace
        variables = workspace.allVars()
        allCompConst = workspace.components()
        for comp in allCompConst:
            if comp.InheritsFrom("RooConstVar"):
                variables.add(comp)
        pdfs = workspace.allPdfs()
        functions = workspace.allFunctions()
        pdf_temp = model.pdf

        if self.use_cms_opt_pdf:
            constrpdf_list_old = model.get_all_constraints(pdf_temp)
            constrpdf_list = ROOT.RooArgSet()
            for constrpdf in constrpdf_list_old:
                pdfs.remove(constrpdf)
                constr_name = constrpdf.GetName()
                constr_class = constrpdf.ClassName()
                if constr_class == "RooGaussian" and self.use_cms_gaussian:
                    constrpdf = ROOT.SimpleGaussianConstraint(constrpdf, constrpdf.GetName())
                elif constr_class == "SimpleGaussianConstraint" and not self.use_cms_gaussian:
                    constrpdf = ROOT.RooGaussian(constrpdf, constrpdf.GetName())
                constrpdf_list.add(constrpdf)
                self.constrpdf_list_all.add(constrpdf)
                ROOT.SetOwnership(constrpdf, False) # prevent memory leak
            
            # remove the link for the constraint pdfs
            cat_pdf = pdf_temp.indexCat()
            pdf = ROOT.RooSimultaneous(pdf_temp.GetName(), pdf_temp.GetTitle(), cat_pdf)
            for i in range(cat_pdf.size()):
                cat_pdf.setBin(i)
                pdf_i = pdf_temp.getPdf(cat_pdf.getLabel())
                if isinstance(pdf_i, ROOT.RooProdPdf):
                    pdf_clean = ROOT.RooArgSet()
                    for pdf_clean_i in pdf_i.pdfList():
                        if not pdf_clean_i.dependsOnValue(constrpdf_list):
                            pdf_clean.add(pdf_clean_i)
                    pdf_i_new_name = f"{pdf_i.GetName()}_{self.without_nuis_pdf_suffix}"
                    pdf_i_new = ROOT.RooProdPdf(pdf_i_new_name, pdf_i_new_name, pdf_clean)
                else:
                    pdf_i_new = pdf_i
                pdf.addPdf(pdf_i_new, cat_pdf.getLabel())
                ROOT.SetOwnership(pdf_i_new, False) # prevent memory leak
        else:
            pdf = pdf_temp
            constrpdf_list = ROOT.RooArgSet()

        # define observables
        observables = ROOT.RooArgSet(model.observables)
        observables.remove(pdf.indexCat())
        
        ignore_list = []
        # let global observables fixed, and nuisances parameters float
        ROOT.RooStats.SetAllConstant(model.nuisance_parameters, False)
        ROOT.RooStats.SetAllConstant(model.global_observables, True)
        rename_map = channel_config["rename_map"]
        # rename pdf
        for old_name, new_name in rename_map["pdf"].items():
            old_pdf = workspace.pdf(old_name)
            if not simplified_import:
                pdfs.remove(old_pdf)
            if old_name == new_name:
                self.stdout.debug(f'Found redundant renaming of the pdf "{old_name}". Skipped.')
                continue
            old_pdf.SetName(new_name)
            self.stdout.debug(f'Renamed pdf from "{old_name}" to "{new_name}"')
        # rename variable
        for old_name, new_name in rename_map["var"].items():
            old_var = workspace.var(old_name)
            if not simplified_import:
                variables.remove(old_var)
            else:
                ignore_list.append(new_name)
            if old_name == new_name:
                self.stdout.debug(f'Found redundant renaming of the variable "{old_name}". Skipped.')
                continue
            old_var.SetName(new_name)
            self.stdout.debug(f'Renamed variable from "{old_name}" to "{new_name}"')
        # rename pois
        poi_map = channel_config['poi_map']
        for comb_poi_name, channel_poi_name in poi_map.items():
            if channel_poi_name == self.KEYWORDS['dummy']:
                continue
            poi = workspace.var(channel_poi_name)
            if not simplified_import:
                variables.remove(poi)
            else:
                ignore_list.append(comb_poi_name)
            if comb_poi_name == channel_poi_name:
                self.stdout.debug(f'Found redundant renaming of the poi "{channel_poi_name}". Skipped.')
                continue
            poi.SetName(comb_poi_name)
            self.stdout.debug(f'Renamed poi from "{channel_poi_name}" to "{comb_poi_name}"')
        if simplified_import:
            self.stdout.info(f'Simplified import requested for the channel "{channel}". '
                             'Only unspecified constraint PDFs, nuisance parameters, '
                             'global observables and POIs will be renamed.')
            global_observables = model.global_observables
            nuisance_parameters = model.nuisance_parameters
            pois = model.pois
            constr_pdfs = ROOT.RooArgSet()
            # get the relevant constraint pdfs
            for glob in global_observables:
                glob_name = glob.GetName()
                if glob_name in ignore_list:
                    continue
                client_iter = glob.clientIterator()
                constr_pdf = client_iter.Next()
                if (not constr_pdf) or (not isinstance(constr_pdf, ROOT.RooAbsPdf)):
                    raise RuntimeError(f'failed to find the constraint pdf for the global observable "{glob_name}"')
                constr_pdfs.add(constr_pdf)
                if client_iter.Next():
                    raise RuntimeError(f'global observable "{glob_name}" in channel "{channel}" '
                                       'has more than one constraint PDF')
            # add channel suffix to global observables
            self._append_channel_suffix_to_args(channel, global_observables,
                                                "global observable", ignore_list)
            # add channel suffix to constraint pdfs
            self._append_channel_suffix_to_args(channel, constr_pdfs,
                                                "constraint PDF")
            # add channel suffix to nuisance_parameters
            self._append_channel_suffix_to_args(channel, nuisance_parameters,
                                                "nuisance parameter", ignore_list)
            # add channel suffix to pois
            self._append_channel_suffix_to_args(channel, pois,
                                                "POI", ignore_list)
        else:
            variables.remove(pdf.indexCat())
            variables.remove(observables)
            
            # add channel suffix to functions
            self._append_channel_suffix_to_args(channel, functions, "function")
            self.stdout.debug(f'All functions in channel "{channel}" have been renamed')
            self._append_channel_suffix_to_args(channel, pdfs, "PDF")
            self.stdout.debug(f'All PDFs in channel "{channel}" have been renamed')
            self._append_channel_suffix_to_args(channel, variables, "variable")
            self.stdout.debug(f'All variables in channel "{channel}" have been renamed')
            if constrpdf_list.getSize() > 0:
                self._append_channel_suffix_to_args(channel, constrpdf_list, "PDF")
                self.stdout.debug(f'All extra constraint PDFs in channel "{channel}" have been renamed')
        
        # rename key objects
        if constrpdf_list.getSize() > 0 and not self.use_cms_add_extraconst:
            self.stdout.info(f"Import constraint nuis pdfs to channel {channel}")
            nuis_pdf_name = f"{self.nuis_pdf_prefix}_{channel}"
            nuis_pdf = ROOT.RooProdPdf(nuis_pdf_name, nuis_pdf_name, constrpdf_list)
            self.import_object(self.tmp_ws, nuis_pdf,
                               ROOT.RooFit.RecycleConflictNodes(), silent=True)
        
        # check if discrete parameters are present
        if workspace.genobj(self.cms_disc_set_keyword):
            discrete_parameters = workspace.genobj(self.cms_disc_set_keyword)
            self.stdout.info(f"Add discrete_params from channel {channel}")
            self.discrete_params.add(discrete_parameters)
        
        data = model.data
        if not isinstance(pdf, ROOT.RooSimultaneous):
            raise RuntimeError(f'main pdf of the channel "{channel}" does not belong to the RooSimultaneous class')
        cat = pdf.indexCat()
        old_cat_name = cat.GetName()
        new_cat_name = f"{self.KEYWORDS['comb_cat_name']}_{channel}"
        old_obs_names = [obs.GetName() for obs in observables]
        new_obs_names = [f"{obs_name}_{channel}" for obs_name in old_obs_names]
        old_name = ",".join([old_cat_name] + old_obs_names)
        new_name = ",".join([new_cat_name] + new_obs_names)
        pdf.SetName(f"{self.KEYWORDS['comb_pdf_name']}_{channel}")
        data.SetName(f"{self.KEYWORDS['comb_data_name']}_{channel}")
        self.import_object(self.tmp_ws, pdf,
                        ROOT.RooFit.RenameVariable(old_name, new_name),
                        ROOT.RooFit.RecycleConflictNodes(), silent=True)
        self.import_object(self.tmp_ws, data,
                           ROOT.RooFit.RenameVariable(old_name, new_name),
                           silent=False)
        self.update_channel_argset(channel, workspace, self.tmp_ws)
        self.tmp_nuis.add(model.nuisance_parameters.snapshot(), True)
        self.tmp_glob.add(model.global_observables.snapshot(), True)
        
    def update_channel_argset(self, channel:str, orig_ws:ROOT.RooWorkspace, new_ws:ROOT.RooWorkspace):
        channel_config = self.channel_config[channel]
        argset_map = {}
        for argset_name in channel_config["argset_list"]:
            argset_old = orig_ws.obj(argset_name)
            assert isinstance(argset_old, ROOT.RooArgSet)
            components = []
            for arg in argset_old:
                names = [arg.GetName(), f"{arg.GetName()}_{channel}"]
                for name in names:
                    obj = new_ws.obj(name)
                    if obj:
                        components.append(name)
                        break
                else:
                    raise RuntimeError(f'unable to locate the variable "{arg.GetName()}" in the renamed workspace '
                                       f'for the channel {channel}')
            new_argset_name = f"{argset_name}_{channel}"
            if (new_argset_name in self.argsets) or (new_argset_name in argset_map):
                raise RuntimeError(f'duplicated ArgSet object "{new_argset_name}"')
            argset_map[new_argset_name] = components
        self.argsets.update(argset_map)
    
    def rename(self, save_rename_ws:bool=True) -> None:
        title = format_delimiter_enclosed_text("Rename PDFs, functions and variables",
                                               delimiter="-", indent_str="")
        self.stdout.info(title, bare=True)
        self.reset_tmp_ws()
        self.discrete_params = ROOT.RooArgSet(self.cms_disc_set_keyword)
        self.constrpdf_list_all = ROOT.RooArgSet(self.cms_nuis_pdf_keyword)
        for channel in self.channel_config:
            self.rename_channel(channel)
        if save_rename_ws:
            self.tmp_ws.defineSet(self.KEYWORDS['comb_nuis_name'], self.tmp_nuis, True)
            self.tmp_ws.defineSet(self.KEYWORDS['comb_glob_name'], self.tmp_glob, True)
            if self.discrete_params.getSize() > 0:
                self.tmp_ws.defineSet(self.cms_disc_set_keyword, self.discrete_params, True)
            if self.constrpdf_list_all.getSize() > 0:
                self.tmp_ws.defineSet(self.cms_nuis_pdf_keyword, self.constrpdf_list_all, True)
            filename = self._get_tmp_ws_path()
            self.stdout.info(f'Saving temporary workspace to "{filename}"')
            self.tmp_ws.writeToFile(filename, True)
            
    def combine_channel(self, channel:str):
        title = format_delimiter_enclosed_text(f"Channel {channel}",
                                               delimiter="+", indent_str="")
        self.stdout.info(title, bare=True)
        channel_pdf_name = f"{self.KEYWORDS['comb_pdf_name']}_{channel}"
        channel_data_name = f"{self.KEYWORDS['comb_data_name']}_{channel}"
        channel_cat_name = f"{self.KEYWORDS['comb_cat_name']}_{channel}"
        channel_pdf = self.tmp_ws.pdf(channel_pdf_name)
        if not channel_pdf:
            raise RuntimeError(f'missing pdf "{channel_pdf_name}" in the channel "{channel}"')
        channel_cat = channel_pdf.indexCat()
        channel_data = self.tmp_ws.data(channel_data_name)
        if not channel_data:
            raise RuntimeError(f'missing data "{channel_data_name}" in the channel "{channel}"')
        # split the original dataset
        channel_data_list = channel_data.split(channel_cat, True)
        
        n_cat = channel_cat.size()
        for i in range(n_cat):
            channel_cat.setBin(i)
            cat_name_i = channel_cat.getLabel()
            new_cat_name_i = f"{channel_cat_name}_{cat_name_i}"
            self.stdout.info(f"Category {i+1}: {cat_name_i} --> {new_cat_name_i}", bare=True)
            pdf_i = channel_pdf.getPdf(cat_name_i)
            data_i = channel_data_list.FindObject(cat_name_i)
            observables_i = pdf_i.getObservables(data_i)
            obs_and_weight, weight_var = self._get_obs_and_weight(observables_i)
            # create new dataset
            new_data_i = ROOT.RooDataSet(f"{new_cat_name_i}_data", f"{new_cat_name_i}_data",
                                         obs_and_weight, ROOT.RooFit.WeightVar(self.KEYWORDS['weight_name']))
            for j in range(data_i.numEntries()):
                observables_i.__assign__(data_i.get(j))
                weight_val = data_i.weight()
                new_data_i.add(obs_and_weight, weight_val)
            self.comb_cat.defineType(new_cat_name_i)
            self.stdout.debug(f'Add pdf for category "{new_cat_name_i}"')
            if self.constrpdf_list_all.getSize() > 0 and self.tmp_ws.pdf(f"{self.nuis_pdf_prefix}_{channel}") and not self.use_cms_add_extraconst:
                self.stdout.info(f'Adding nuisance pdf')
                nuis_pdf = self.tmp_ws.pdf(f"{self.nuis_pdf_prefix}_{channel}")
                pdf_i_new_name = f"{pdf_i.GetName()}_{self.with_nuis_pdf_suffix}"
                pdf_i_new = ROOT.RooProdPdf(pdf_i_new_name, pdf_i_new_name, ROOT.RooArgList(nuis_pdf, pdf_i))
                self.comb_pdf.addPdf(pdf_i_new, new_cat_name_i)
                ROOT.SetOwnership(pdf_i_new, False) # prevent memory leak
            else:
                self.comb_pdf.addPdf(pdf_i, new_cat_name_i)

            self.comb_data_map[new_cat_name_i] = new_data_i
            self.comb_obs.add(observables_i.snapshot(), True)
            
    def combine(self, load_rename_ws:bool=True, save_combine_ws:bool=True) -> None:
        title = format_delimiter_enclosed_text("Create Combined Pdf and Dataset",
                                               delimiter="-", indent_str="")
        self.stdout.info(title, bare=True)
        if load_rename_ws:
            self.load_cache_ws("rename")
        
        self.reset_comb_ws()
        for channel in self.channel_config:
            self.combine_channel(channel)
        
        pdf_name  = self.KEYWORDS['comb_pdf_name']
        data_name = self.combination_config["data_name"]
        self.stdout.info(f'Generating combined pdf "{pdf_name}"')
        if self.constrpdf_list_all.getSize() > 0 and self.use_cms_add_extraconst:
            self.comb_pdf.addExtraConstraints(self.constrpdf_list_all)
        self.comb_ws.Import(self.comb_pdf)
        self.stdout.info(f'Generating combined dataset "{data_name}"')
        self.comb_obs.add(self.comb_cat)
        obs_and_weight, weight_var = self._get_obs_and_weight(self.comb_obs)
        dataset_map = RooDataSet.get_dataset_map(self.comb_data_map)
        comb_data = ROOT.RooDataSet(data_name, data_name, obs_and_weight,
                                    ROOT.RooFit.Index(self.comb_cat),
                                    ROOT.RooFit.Import(dataset_map),
                                    ROOT.RooFit.WeightVar(weight_var))
        self.comb_ws.Import(comb_data)
        self.stdout.info(f'Defining variable set "{self.KEYWORDS["comb_nuis_name"]}"')
        self.comb_ws.defineSet(self.KEYWORDS["comb_nuis_name"], self.tmp_nuis, True)
        self.stdout.info(f'Defining variable set "{self.KEYWORDS["comb_glob_name"]}"')
        self.comb_ws.defineSet(self.KEYWORDS["comb_glob_name"], self.tmp_glob, True)
        self.stdout.info(f'Defining variable set "{self.KEYWORDS["comb_obs_name"]}"')
        self.comb_ws.defineSet(self.KEYWORDS["comb_obs_name"], self.comb_obs, True)
        if self.discrete_params.getSize() > 0:
            self.stdout.info(f'Defining variable set "{self.cms_disc_set_keyword}"')
            self.comb_ws.defineSet(self.cms_disc_set_keyword, self.discrete_params, True)
        if self.constrpdf_list_all.getSize() > 0:
            self.stdout.info(f'Defining variable set "{self.cms_nuis_pdf_keyword}"')
            self.comb_ws.defineSet(self.cms_nuis_pdf_keyword, self.constrpdf_list_all, True)
        self.define_argsets(self.comb_ws)
        if save_combine_ws:
            filename = self._get_comb_ws_path()
            self.stdout.info(f'Saving temporary workspace to "{filename}"')
            self.comb_ws.writeToFile(filename, True)
            
    def define_argsets(self, ws:ROOT.RooWorkspace):
        for argset_name, arg_names in self.argsets.items():
            argset = ROOT.RooArgSet()
            for arg_name in arg_names:
                arg = ws.obj(arg_name)
                if not arg:
                    raise RuntimeError(f'failed to locate object "{arg_name}" from the combined workspace when '
                                       f'defining the ArgSet "{argset_name}"')
                argset.add(arg)
            self.stdout.info(f'Defining argument set "{argset_name}"')
            ws.Import(argset, argset_name, True)
        
    def get_combined_model_config(self) -> None:
        pois = ROOT.RooArgSet()
        if "poi_definition" not in self.combination_config:
            raise RuntimeError("Combined POIs not initialized")        
        poi_definitions = self.combination_config["poi_definition"]
        for poi_name, poi_info in poi_definitions.items():
            poi = self.comb_ws.var(poi_name)
            if poi:
                poi_min = poi_info["min"]
                poi_max = poi_info["max"]
                poi_value = poi_info["value"]
                if (poi_min is None) and (poi_max is None):
                    poi.setConstant(True)
                else:
                    poi.setRange(poi_min, poi_max)
                    if (poi_value is not None) and ((poi_value > poi_min) and (poi_value < poi_max)):
                        poi.setVal(poi_value)
                pois.add(poi)
            else:
                self.stdout.warning(f'The POI "{poi_name}" does not exist in the combined model')
        mc_name = self.combination_config["model_config_name"]
        model_config = ROOT.RooStats.ModelConfig(mc_name, self.comb_ws)
        #model_config.SetWorkspace(self.com_ws)
        pdf_name  = self.KEYWORDS['comb_pdf_name']
        data_name = self.combination_config["data_name"]
        pdf = self.comb_ws.pdf(pdf_name)
        data = self.comb_ws.data(data_name)
        
        model_config.SetPdf(pdf)
        model_config.SetProtoData(data)
        model_config.SetParametersOfInterest(pois)
        model_config.SetNuisanceParameters(self.tmp_nuis)
        model_config.SetGlobalObservables(self.tmp_glob)
        model_config.SetObservables(self.comb_obs)
        
        return model_config
    
    def get_model_config_summary(self, indent:int=0):
        mc_name = self.combination_config["model_config_name"]
        model_config = self.comb_ws.obj(mc_name)
        if not model_config:
            raise RuntimeError("combined model config not defined")
        pdf = model_config.GetPdf()
        if not pdf:
            raise RuntimeError("PDF not defined in ModelConfig")
        cat  = pdf.indexCat()
        nuis = model_config.GetNuisanceParameters()
        if not nuis:
            raise RuntimeError("Nuisance parameters not defined in ModelConfig")        
        glob = model_config.GetGlobalObservables()
        if not glob:
            raise RuntimeError("Global observables not defined in ModelConfig")        
        pois = model_config.GetParametersOfInterest()
        if not pois:
            raise RuntimeError("POIs not defined in ModelConfig")
            
        summary_text = ""
        summary_text += " " * indent + f"Number of categories: {cat.size()}\n"
        summary_text += " " * indent + f"Number of POIs: {pois.getSize()}\n"
        summary_text += " " * indent + f"Number of nuisance parameters: {nuis.getSize()}\n"
        summary_text += " " * indent + f"Number of global observables: {glob.getSize()}\n"
        
        return summary_text
    
    def generate_asimov(self):
        ws = self.comb_ws
        asimov_definitions = self.asimov_actions
        data_name = self.combination_config["data_name"]
        self._generate_asimov(ws, asimov_definitions=asimov_definitions,
                              data_name=data_name,
                              minimizer_config=self.minimizer_config,
                              title_indent_str="")    
        
    def finalize(self, load_combine_ws:bool=True, save_final_ws:bool=True,
                 import_class_code:bool=True) -> None:
        if load_combine_ws:
            self.load_cache_ws("combine")
        
        # create model config
        self.stdout.info(f'Creating ModelConfig "{self.combination_config["model_config_name"]}"')
        model_config = self.get_combined_model_config()
        self.comb_ws.Import(model_config)
        if import_class_code:
            self.import_class_code(self.comb_ws)
        
        title = format_delimiter_enclosed_text("Generate Asimov Dataset",
                                               delimiter="-", indent_str="")
        self.stdout.info(title, bare=True)
        
        # generate asimov dataset
        self.generate_asimov()
            
        title = format_delimiter_enclosed_text("Workspace Summary",
                                               delimiter="-", indent_str="")
        self.stdout.info(title, bare=True)
        
        mc_summary = self.get_model_config_summary()
        self.stdout.info(mc_summary, bare=True)
        
        if save_final_ws:
            filename = self.combination_config["output_file"]
            self.stdout.info(f'Saving final combined workspace to "{filename}"')
            self.comb_ws.writeToFile(filename, True)
            
    def reset_combination(self):
        self.argsets = {}
    
    def create_combined_workspace(self, infiles:Optional[Dict[str, str]]=None,
                                  outfile:Optional[str]=None,
                                  save_rename_ws:bool=False,
                                  save_combine_ws:bool=False,
                                  save_final_ws:bool=True,
                                  import_class_code:bool=True) -> None:
        with timer() as t:
            # override path to the input channel workspaces
            if infiles is not None:
                for channel in self.channel_config:
                    if channel not in infiles:
                        raise ValueError(f'missing input workspace path for the channel "{channel}"')
                    self.channel_config[channel]['input_file'] = infiles[channel]
            self.reset_combination()
            # override path to the combined workspace
            if outfile is not None:
                self.combination_config['output_file'] = outfile
            for channel in self.channel_config:
                self.validate_channel_input(channel)
            self.print_input_summary()
            self.rename(save_rename_ws=save_rename_ws)
            self.combine(load_rename_ws=save_rename_ws, save_combine_ws=save_combine_ws)
            self.finalize(load_combine_ws=save_combine_ws, save_final_ws=save_final_ws,
                          import_class_code=import_class_code)
        self.stdout.info(f"Total time taken: {t.interval:.3f}s")