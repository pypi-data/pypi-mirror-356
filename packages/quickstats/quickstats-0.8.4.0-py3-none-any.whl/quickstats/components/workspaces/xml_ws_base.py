from typing import Optional, Union, List, Dict
import os
import re
import time
import difflib
from functools import partial

import numpy as np

import quickstats
from quickstats import semistaticmethod, AbstractObject, GeneralEnum, PathManager
from quickstats.utils.xml_tools import TXMLTree
from quickstats.maths.numerics import to_bool
from quickstats.utils.root_utils import load_macro, get_macro_TClass, get_macro_dir
from quickstats.utils.common_utils import set_unlimited_stacksize
from quickstats.utils.string_utils import split_str

import ROOT

class WSObjectType(GeneralEnum):
    DEFINED    = 0
    FUNCTION   = 1
    VARIABLE   = 2
    CONSTRAINT = 3

class XMLAttribType(GeneralEnum):
    STR        = 0
    BOOL       = 1
    INT        = 2
    FLOAT      = 3
    STR_LIST   = 4
    INT_LIST   = 5
    FLOAT_LIST = 6

class BracketType(GeneralEnum):
    ROUND  = (1, r"(.+)\((.+)\)")
    SQUARE = (2, r"(.+)\[(.+)\]")
    CURLY  = (3, r"(.+){(.+)}")
    ANGLE  = (4, r"(.+)<(.+)>")
    
    def __new__(cls, value:int, regex:str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.regex = re.compile(regex)
        return obj
    
ConversionOperators = {
    XMLAttribType.STR: str,
    XMLAttribType.BOOL: to_bool,
    XMLAttribType.INT: int,
    XMLAttribType.FLOAT: float,
    XMLAttribType.STR_LIST  : lambda s: split_str(s, sep=',', remove_empty=True),
    XMLAttribType.INT_LIST  : lambda s: split_str(s, sep=',', remove_empty=True, cast=int),
    XMLAttribType.FLOAT_LIST: lambda s: split_str(s, sep=',', remove_empty=True, cast=float)
}

class XMLWSBase(AbstractObject):
    
    EPSILON = 1e-6
    
    def __init__(self, source:Optional[Union[str, Dict]]=None, basedir:Optional[str]=None,
                 unlimited_stack:bool=True, verbosity:Optional[Union[int, str]]="INFO"):
        super().__init__(verbosity=verbosity)
        self.source = source
        if basedir is not None:
            self.basedir = basedir
        # source is a filepath
        elif isinstance(source, str):
            self.basedir = os.path.dirname(source)
        else:
            self.basedir = os.getcwd()
        self.path_manager = PathManager(self.basedir)
        if unlimited_stack:
            set_unlimited_stacksize()
            self.stdout.info("Set stack size to unlimited")
        self.suppress_roofit_message()
        self.custom_classes = {}

    def load_extension(self):
        extensions = quickstats.get_workspace_extensions()
        for extension in extensions:
            result = load_macro(extension)
            if (result is not None) and hasattr(ROOT, extension):
                self.stdout.info(f'Loaded extension module "{extension}"')
            try:
                cls = get_macro_TClass(extension)
            except Exception:
                continue
            self.custom_classes[extension] = cls
    
    @staticmethod
    def suppress_roofit_message():
        ROOT.RooMsgService.instance().getStream(1).removeTopic(ROOT.RooFit.NumIntegration)
        ROOT.RooMsgService.instance().getStream(1).removeTopic(ROOT.RooFit.Fitting)
        ROOT.RooMsgService.instance().getStream(1).removeTopic(ROOT.RooFit.Minimization)
        ROOT.RooMsgService.instance().getStream(1).removeTopic(ROOT.RooFit.InputArguments)
        ROOT.RooMsgService.instance().getStream(1).removeTopic(ROOT.RooFit.Eval)
        ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)
        
    def get_relpath(self, filename:str):
        if filename.startswith("/") or filename.startswith("~"):
            return filename
        return os.path.join(self.basedir, filename)
    
    def check_file_exist(self, filename:str):
        return os.path.exists(self.get_relpath(filename))
    
    @staticmethod
    def _get_node_attrib(node:Dict, attrib_name:Union[str, List[str]], required:bool=True,
                         default:Optional[str]=None,
                         dtype:Union[XMLAttribType,str]='str'):
        attrib_node = node['attrib']
        if isinstance(attrib_name, str):
            attrib_name = [attrib_name]
        # aliases
        found_attribute = False
        for name in attrib_name:
            if name in attrib_node:
                if found_attribute:
                    raise RuntimeError("values defined for multiple alises of the same attribute: "
                                      f"{','.join(attrib_name)}")
                attrib_val = attrib_node[name]
                found_attribute = True
        if not found_attribute:
            if required:
                raise RuntimeError(f"attribute `{','.join(attrib_name)}` not found in the "
                                   f"node `{node['tag']}`")
            else:
                attrib_val = default
        if not isinstance(attrib_val, str):
            return attrib_val
        attrib_val = re.sub('\s+', '', attrib_val)
        dtype = XMLAttribType.parse(dtype)
        attrib_val = ConversionOperators[dtype](attrib_val)
        return attrib_val
    
    @staticmethod
    def _get_object_name_and_type_from_expr(expr:str):
        if ("::" in expr) and ("(" in expr):
            object_type = WSObjectType.FUNCTION
            object_name = expr.split("::")[1].split("(")[0]
        elif ("(" in expr):
            object_type = WSObjectType.CONSTRAINT
            object_name = expr.split("(")[0]
        elif ("[" in expr):
            object_type = WSObjectType.VARIABLE
            object_name = expr.split("[")[0]
        elif (":" in expr) and ("::" not in expr):
            raise RuntimeError(f"syntax error for the expression `{expr}`: missing colon pair")
        else:
            object_type = WSObjectType.DEFINED
            object_name = expr
        return object_name, object_type
    
    @staticmethod
    def _extract_bracket_expr(expr:str, bracket_type:Union[str, BracketType]=BracketType.ROUND,
                              match:bool=True):
        bracket_type = BracketType.parse(bracket_type)
        if match:
            result = bracket_type.regex.match(expr)
        else:
            result = bracket_type.regex.search(expr)
        if not result:
            return (None, None)
        else:
            return (result.group(1), result.group(2))
    
    def import_object(self, ws:ROOT.RooWorkspace, obj, *args, silent:bool=True):
        if silent:
            getattr(ws, "import")(obj, *args, ROOT.RooFit.Silence())        
        else:
            getattr(ws, "import")(obj, *args)    
    
    def import_expression(self, ws:ROOT.RooWorkspace, object_expr:str, check_defined:bool=False):
        object_name, object_type = self._get_object_name_and_type_from_expr(object_expr)
        # throw error when attemping to access undefined object
        if object_type == "defined":
            if (not ws.arg(object_name)):
                raise RuntimeError(f"object `{object_name}` does not exist")
            else:
                return object_name
        # throw error? when attemping to define already existing object
        if check_defined:
            if ws.arg(object_name):
                self.stdout.debug(f"object {object_name} already exists")
                return object_name
        self.stdout.debug(f"Generating {object_type} {object_expr}")
        status = ws.factory(object_expr)
        if not status:
            raise RuntimeError(f"object creation from expression `{object_expr}` had failed")
        return object_name
    
    @semistaticmethod
    def get_name_mapping_str(self, old_name:str, new_name:str, width:int=40):
        sequence = difflib.SequenceMatcher(None, old_name, new_name)
        match = sequence.find_longest_match(0, len(old_name), 0, len(new_name))
        ahead = old_name[ : match.a]
        atail = old_name[match.a + match.size : ]
        bhead = new_name[ : match.b]
        btail = new_name[match.b + match.size : ]
        common1 = old_name[match.a : match.a+match.size]
        common2 = new_name[match.b : match.b+match.size]
        result = f'{ahead}\033[91m{common1}\033[0m{atail}'.rjust(width, ' ') + ' -> ' + f'{bhead}\033[92m{common1}\033[0m{btail}'
        return result
    
    @semistaticmethod
    def get_name_mapping_str_arrays(self, rename_map:Dict):
        results = []
        if not rename_map:
            return results        
        width = max([len(i) for i in list(rename_map)]) + 20
        for old_name, new_name in rename_map.items():
            results.append(self.get_name_mapping_str(old_name, new_name, width))
        return results
    
    def get_workspace_arg(self, ws:ROOT.RooWorkspace, arg_name:str, strict:bool=True):
        obs = ws.arg(arg_name)
        if not arg_name:
            if strict:
                raise RuntimeError(f"variable {arg_name} does not exist in workspace")
            return None
        return obs
    
    def import_expressions(self, ws:ROOT.RooWorkspace, object_expr_list:List[str],
                           check_defined:bool=False):
        object_names = []
        for object_expr in object_expr_list:
            object_name = self.import_expression(ws, object_expr, check_defined=check_defined)
            object_names.append(object_name)
        return ",".join(object_names)
    
    def import_class_code(self, ws:ROOT.RooWorkspace):
        all_function_class = [i.ClassName().split("::")[-1] for i in ws.allFunctions()]
        all_pdf_class = [i.ClassName().split("::")[-1] for i in ws.allPdfs()]
        all_class = all_function_class + all_pdf_class
        for extension, cls in self.custom_classes.items():
            # the workspace does not use the extended class, no need to import
            if extension not in all_class:
                continue
            macro_dir = get_macro_dir(extension)
            ws.addClassDeclImportDir(macro_dir)
            ws.addClassImplImportDir(macro_dir)
            ws.importClassCode(cls)
            self.stdout.info(f"Imported class code for \"{cls.GetName()}\".")
        #ws.importClassCode()    
    
    def _generate_asimov(self, ws:ROOT.RooWorkspace, asimov_definitions:List, data_name:str,
                         range_name:Optional[str]=None, minimizer_config:Optional[Dict]=None,
                         title_indent_str:str="\t"):
        from quickstats.components.workspaces import AsimovHandler
        n_asimov = len(asimov_definitions)
        if n_asimov == 0:
            return None
        asimov_handler = AsimovHandler(ws, data_name=data_name, range_name=range_name,
                                       minimizer_config=minimizer_config,
                                       verbosity=self.stdout.verbosity)
        asimov_handler.title_indent_str = title_indent_str
        for attributes in asimov_definitions:
            asimov_handler.generate_single_asimov(attributes)