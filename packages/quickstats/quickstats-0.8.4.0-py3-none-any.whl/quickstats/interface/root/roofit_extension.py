from typing import Optional, Dict, List, Union, Tuple

import numpy as np

from quickstats.interface.cppyy.vectorize import list2vec, as_np_array
from quickstats import stdout, cached_import

def unfold_constraints(constraint_pdfs:"ROOT.RooArgSet", observables:"ROOT.RooArgSet",
                       nuisance_parameters:"ROOT.RooArgSet", constraint_cls:Optional[List[str]]=None,
                       recursion_limit:int=50, strip_disconnected:bool=False):
    ROOT = cached_import("ROOT")
    result = ROOT.RooArgSet()
    if constraint_cls is None:
        constraint_cls = ROOT.RooFitExt.kConstrPdfClsList
    else:
        
        constraint_cls = list2vec(constraint_cls)
    ROOT.RooFitExt.unfoldConstraints(constraint_pdfs, observables, nuisance_parameters, result,
                                     constraint_cls, 0, recursion_limit, strip_disconnected)
    return result


def convert_argsets(*argsets, fmt:str="argset", to_str:bool=False):
    if to_str and (fmt == "argset"):
        raise ValueError("argset format does not support to_str")
    if fmt == "argset":
        ROOT = cached_import("ROOT")
        return [ROOT.RooArgSet(argset) for argset in argsets]
    elif fmt in ["list", "dict"]:
        results = []
        if to_str:
            for argset in argsets:
                results.append([i.GetName() for i in argset])
        else:
            for argset in argsets:
                results.append([i for i in argset])
        if fmt == "list":
            return tuple(results)
        elif fmt == "dict":
            dict_result = {}
            for argset, result in zip(argsets, results):
                dict_result[argset.GetName()] = result
            return dict_result
    elif fmt == "series":
        if to_str:
            result = [tuple([i.GetName() for i in items]) for items in zip(*argsets)]
        else:
            result = [tuple(items) for items in zip(*argsets)]
        return result
    else:
        raise ValueError(f"format '{fmt}' not supported")    
            
        
def pair_constraints(constraint_pdfs:"ROOT.RooArgSet", nuisance_parameters:"ROOT.RooArgSet",
                     global_observables:"ROOT.RooArgSet", fmt:str="list", to_str:bool=False, sort:bool=False):
    ROOT = cached_import("ROOT")
    if sort:
        ROOT.RooArgSet.sort(constraint_pdfs)
    paired_constraints = ROOT.RooFitExt.pairConstraints(constraint_pdfs, nuisance_parameters, global_observables)
    paired_pdfs  = paired_constraints.pdfs
    paired_nuis  = paired_constraints.nuis
    paired_globs = paired_constraints.globs
    paired_pdfs.setName("pdf")
    paired_nuis.setName("nuis")
    paired_globs.setName("globs")
    return convert_argsets(paired_pdfs, paired_nuis, paired_globs, fmt=fmt, to_str=to_str)

def pair_constraints_base_component(constraint_pdfs:"ROOT.RooArgSet", nuisance_parameters:"ROOT.RooArgSet",
                                    global_observables:"ROOT.RooArgSet", fmt:str="list", to_str:bool=False,
                                    sort:bool=False):
    ROOT = cached_import("ROOT")
    if sort:
        ROOT.RooArgSet.sort(constraint_pdfs)
    paired_pdfs      = ROOT.RooArgSet("pdf")
    paired_component = ROOT.RooArgSet("base_component")
    paired_globs     = ROOT.RooArgSet("globs")
    
    for pdf in constraint_pdfs:
        target_component   = None
        target_glob        = None
        pdf_name = pdf.GetName()
        # getting base pdf component
        components = pdf.getComponents()
        components.remove(pdf)
        if components.getSize():
            for c1 in components:
                for c2 in components:
                    if c1 == c2:
                        continue
                    if c2.dependsOn(c1):
                        components.remove(c1)
            if (components.getSize() > 1):
                raise RuntimeError("failed to isolate proper pdf base component")
            elif (components.getSize() == 1):
                target_component = components.first()
        else:
            for nuis in nuisance_parameters:
                if pdf.dependsOn(nuis):
                    target_component = nuis
                    break
        if not target_component:
            stdout.warning(f'WARNING: Could not find base component for the constraint: {pdf_name}')
            continue
        for glob in global_observables:
            if pdf.dependsOn(glob):
                target_glob = glob
                break
        if not target_glob:
            stdout.warning(f'WARNING: Could not find global observable for the constraint: {pdf_name}')
            continue
        paired_pdfs.add(pdf)
        paired_component.add(target_component)
        paired_globs.add(target_glob)
        
    return convert_argsets(paired_pdfs, paired_component, paired_globs, fmt=fmt, to_str=to_str)      
        
def get_str_data(components:"ROOT.RooArgSet", fill_classes:bool=False,
                 fill_definitions:bool=True, content:int=-1,
                 style:int=-1, indent:str="", fmt:str="dict",
                 correction:bool=True):
    ROOT = cached_import("ROOT")
    str_data = ROOT.RooFitExt.getStrData(components, fill_classes, fill_definitions,
                                         content, style, indent, correction)
    result = {
        "name" : as_np_array(str_data.names),
    }
    
    if fill_classes:
        result["class"] = as_np_array(str_data.classes)
        
    if fill_definitions:
        result["definition"] = as_np_array(str_data.definitions)
        
    if fmt == "dict":
        return result
    elif fmt == "dataframe":
        import pandas as pd
        return pd.DataFrame(result)
    else:
        raise ValueError(f"format '{fmt}' not supported")


def deduce_category_index_map(data: Dict[str, np.ndarray],
                              category_name: str,
                              observable_names: List[str]):
    if category_name not in data:
        raise ValueError(f'Data does not contain the category key "{category_name}".')
    for observable_name in observable_names:
        if observable_name not in data:
            raise ValueError(f'Data does not contain the observable key "{observable_name}".')
    category_indices = np.unique(data[category_name])
    if len(category_indices) != len(observable_names):
        raise RuntimeError('Number of category indices does not match the number of observables.')
    result = {}
    for index in category_indices:
        # NB: index here could be int32
        mask = data[category_name] == index
        obs_with_changing_values = []
        for observable_name in observable_names:
            values = data[observable_name][mask]
            if len(np.unique(values)) > 1:
                obs_with_changing_values.append(observable_name)
        if len(obs_with_changing_values) != 1:
            raise RuntimeError(f'Unable to deduce observable for the category index: {index}')
        category_observable = obs_with_changing_values[0]
        result[category_observable] = int(index)
    return result

def isolate_category_observables(argset: "ROOT.RooArgSet") -> Tuple[Optional["ROOT.RooCategory"], List["ROOT.RooRealVar"]]:
    category = None
    observables = []
    for arg in argset:
        class_name = arg.ClassName()
        if class_name == "RooCategory":
            if category is not None:
                raise RuntimeError('Found multiple RooCategory instances.')
            category = arg
        elif class_name == "RooRealVar":
            observables.append(arg)
        else:
            raise RuntimeError(f'Found argument with invalid type: {arg.GetName()}({class_name}).')
    return category, observables