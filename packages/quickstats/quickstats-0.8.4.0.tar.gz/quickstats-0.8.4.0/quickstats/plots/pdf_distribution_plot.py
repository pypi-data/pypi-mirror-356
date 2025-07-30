from typing import Optional, Union, Dict, List, Tuple, Callable
import numbers

from cycler import cycler
import numpy as np

from quickstats.utils.common_utils import combine_dict

from .core import ErrorDisplayFormat
from .color_schemes import QUICKSTATS_PALETTES
from .abstract_plot import AbstractPlot
from .template import suggest_markersize, centralize_axis, create_transform

class PdfDistributionPlot(AbstractPlot):
    
    STYLES = {
        'errorbar': {
            "marker": 'o',
            "markersize": None,
            "linewidth": 0,
            "elinewidth": 1,
            "capsize": 3,
            "capthick": 1
        },
        "annotate": {
            "xy": (0.05, 0.9),
            "xycoords": "axes fraction",
            "horizontalalignment": "left",
            "verticalalignment": "top",
            "fontsize": 20
        },
        "legend": {
            "borderpad": 1
        },
        "ratio_frame": {
            "height_ratios": (4, 1)
        }
    }
    
    CONFIG = {
        "blind_linestyle": "--",
        'ratio_line_styles':{
            'color': 'gray',
            'linestyle': '--'
        }        
    }
    
    def __init__(self, collective_data:Dict,
                 plot_options:Optional[Dict]=None,
                 label_map:Optional[Dict]=None,
                 color_cycle:Optional[Dict]=None,
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Union[Dict, str]]=None,
                 figure_index:Optional[int]=None,
                 config:Optional[Dict]=None):
        super().__init__(color_cycle=color_cycle,
                         label_map=label_map,
                         styles=styles, figure_index=figure_index,
                         analysis_label_options=analysis_label_options,
                         config=config)
        self.error_options = {}
        self.set_data(collective_data)
        if plot_options is None:
            self.plot_options = {}
        else:
            self.plot_options = plot_options
        self.colors = {}
        
        self.annotation = None
        
    def set_data(self, collective_data:Dict):
        self.collective_data = collective_data
        for name in self.collective_data:
            if name not in self.error_options:
                self.set_error_options(name)

    def get_error_data(self, data):
        xerr = data.get('xerr', None)
        yerr = data.get('yerr', None)
        xerrlo = data.get('xerrlo', None)
        yerrlo = data.get('yerrlo', None)
        xerrhi = data.get('xerrhi', None)
        yerrhi = data.get('yerrhi', None)
        if all(err is None for err in [xerr, yerr, xerrlo, yerrlo, xerrhi, yerrhi]):
            return {"xerr": None, "yerr": None}
        if (xerr is not None) and ((xerrlo is not None) or (xerrhi is not None)):
            raise ValueError("invalid data: received both \"xerr\" and \"xerrlo\"/\"xerrhi\" attributes")
        if (yerr is not None) and ((yerrlo is not None) or (yerrhi is not None)):
            raise ValueError("invalid data: received both \"yerr\" and \"yerrlo\"/\"yerrhi\" attributes")
        error_data = {}
        if xerr is not None:
            error_data['xerr'] = np.array(xerr)
        elif ((xerrlo is not None) or (xerrhi is not None)):
            error_data['xerr'] = (np.array(xerrlo), np.array(xerrhi))
        else:
            error_data['xerr'] = None
        if yerr is not None:
            error_data['yerr'] = np.array(yerr)
        elif ((yerrlo is not None) or (yerrhi is not None)):
            error_data['yerr'] = (np.array(yerrlo), np.array(yerrhi))
        else:
            error_data['yerr'] = None
        return error_data
    
    def _get_selected_err(self, err, mask):     
        if err is None:
            return None
        elif isinstance(err, tuple):
            new_err = []
            for err_i in err:
                new_err.append(err_i[mask])
            return tuple(new_err)
        else:
            return err[mask]
        
    def draw_single_data(self, ax, data, label:str, label_blind:Optional[str]=None,
                         blind_range:Optional[List[float]]=None,
                         plot_options:Optional[Dict]=None, show_error:bool=True,
                         error_format:Union[ErrorDisplayFormat, str]="error_bar",
                         error_styles:Optional[Dict]=None,
                         plot_type:str="errorbar"):
        pdata = self.process_data(data, blind_range=blind_range)
        has_errorbar = not ((pdata['xerr'] is None) and (pdata['yerr'] is None))
        draw_blind = blind_range is not None
        if not has_errorbar:
            if plot_type == "errorbar":
                combined_options = combine_dict(self.styles['plot'], plot_options)
                combined_options['label'] = label
                if draw_blind:
                    # draw sideband low
                    handle_sblo = ax.plot(pdata['x'][pdata['sideband_lo']], 
                                          pdata['y'][pdata['sideband_lo']],
                                          **combined_options)
                    # avoid going through internal color cycle for the three regions
                    combined_options['color'] = handle_sblo[0].get_color()
                    # draw sideband high
                    handle_sbhi = ax.plot(pdata['x'][pdata['sideband_hi']], 
                                          pdata['y'][pdata['sideband_hi']],
                                          **combined_options)
                    combined_options['linestyle'] = self.config['blind_linestyle']
                    if label_blind is None:
                        combined_options['label'] = f"{label} (blind)"
                    else:
                        combined_options['label'] = label_blind
                    x_blind_plus_sideband_edge = [pdata['x'][pdata['sideband_lo']][-1]] + \
                                                 list(pdata['x'][pdata['blind']]) + \
                                                 [pdata['x'][pdata['sideband_hi']][0]]
                    y_blind_plus_sideband_edge = [pdata['y'][pdata['sideband_lo']][-1]] + \
                                                 list(pdata['y'][pdata['blind']]) + \
                                                 [pdata['y'][pdata['sideband_hi']][0]]                
                    handle_blind = ax.plot(x_blind_plus_sideband_edge, 
                                           y_blind_plus_sideband_edge,
                                           **combined_options)
                    handle = [handle_sblo[0], handle_blind[0]]
                else:
                    handle = ax.plot(pdata['x'], pdata['y'], **combined_options)
                    handle = handle[0]
            elif plot_type == "hist":
                pass
        else:
            if plot_type == "errorbar":
                combined_options = combine_dict(plot_options, {"label": label})
                if combined_options.get('markersize', None) is None:
                    nbins = len(pdata['x'])
                    combined_options['markersize'] = suggest_markersize(nbins)

                if draw_blind:
                    x = pdata['x'][pdata['sideband']]
                    y = pdata['y'][pdata['sideband']]
                    xerr = self._get_selected_err(pdata['xerr'], pdata['sideband'])
                    yerr = self._get_selected_err(pdata['yerr'], pdata['sideband'])
                else:
                    x = pdata['x']
                    y = pdata['y']
                    xerr = pdata['xerr']
                    yerr = pdata['yerr']
                if not show_error:
                    error_format = None
                y_nonzero = np.where(y != 0)
                x, y = x[y_nonzero], y[y_nonzero]
                if (xerr is not None):
                    if isinstance(xerr, tuple):
                        xerr = (xerr[0][y_nonzero], xerr[1][y_nonzero])
                    else:
                        xerr = xerr[y_nonzero]
                if (yerr is not None):
                    if isinstance(yerr, tuple):
                        yerr = (yerr[0][y_nonzero], yerr[1][y_nonzero])
                    else:
                        yerr = yerr[y_nonzero]
                handle = self._draw_data(ax, x, y, xerr, yerr,
                                         plot_options=combined_options,
                                         error_format=error_format,
                                         error_styles=error_styles)
            elif plot_type == "hist":
                x = pdata['x']
                y = pdata['y']
                xerr = pdata['xerr']
                yerr = pdata['yerr']
                width = np.diff(x)[0]
                combined_options = combine_dict(self.styles['bar'], plot_options)
                combined_options['label'] = label
                handle = ax.stairs(x, y, align='center', width=width, **combined_options)
        return handle
    
    def process_data(self, data, blind_range:Optional[List[float]]=None):
        processed_data = {}
        processed_data['x'] = data['x']
        processed_data['y'] = data['y']
        error_data = self.get_error_data(data)
        processed_data['xerr'] = error_data['xerr']
        processed_data['yerr'] = error_data['yerr']
        if blind_range is not None:
            x = processed_data['x']
            blind_min = blind_range[0]
            blind_max = blind_range[1]
            sideband_lo = (x <= blind_min)
            sideband_hi = (x >= blind_max)
            blind = (x > blind_min) & (x < blind_max)
            processed_data['sideband_lo'] = sideband_lo
            processed_data['sideband_hi'] = sideband_hi
            processed_data['blind'] = blind
            processed_data['sideband'] = ~blind
        return processed_data
    
    def _draw_data(self, ax, x:np.ndarray, y:np.ndarray,
                   xerr:Optional[np.ndarray]=None,
                   yerr:Optional[np.ndarray]=None,
                   plot_options:Optional[Dict]=None,
                   error_format:Optional[Union[ErrorDisplayFormat, str]]="error_bar",
                   error_styles:Optional[Dict]=None):
        combined_options = combine_dict(self.styles['errorbar'], plot_options)
        if error_format is None:
            combined_options['elinewidth'] = 0
            combined_options['capsize'] = 0
            combined_options['capthick'] = 0
            handle = ax.errorbar(x, y, xerr=xerr, yerr=yerr,
                                 **combined_options)
        elif (error_format == ErrorDisplayFormat.ERRORBAR):
            combined_options = combine_dict(combined_options, error_styles)
            handle = ax.errorbar(x, y, xerr=xerr, yerr=yerr,
                                 **combined_options)
        elif (error_format == ErrorDisplayFormat.FILL):
            combined_options['elinewidth'] = 0
            combined_options['capsize'] = 0
            combined_options['capthick'] = 0
            handle = ax.errorbar(x, y, xerr=xerr, yerr=yerr,
                                 **combined_options)
            fill_options = combine_dict(self.styles['fill_between'], error_styles)
            if "zorder" not in fill_options:
                fill_options["zorder"] = 5
            if yerr is not None:
                handle_fill = ax.fill_between(x, y - yerr[0], y + yerr[1],
                                              **fill_options)
            else:
                handle_fill = None
        else:
            raise RuntimeError(f"unkown error display format: {error_format}")
        return handle
    
    def draw_comparison(self, ax, reference_data, target_data, 
                        xlabel:str="", ylabel:str="",  mode:str="ratio",
                        plot_options:Optional[Dict]=None, show_error:bool=True, 
                        blind_range:Optional[List[float]]=None,
                        error_format:Union[ErrorDisplayFormat, str]="error_bar",
                        error_styles:Optional[Dict]=None,                        
                        draw_ratio_line:bool=True):
        pdata_ref = self.process_data(reference_data, blind_range=blind_range)
        pdata_tgt = self.process_data(target_data, blind_range=blind_range)
        if not np.allclose(pdata_tgt['x'], pdata_ref['x']):
            raise RuntimeError("cannot compare two distributions with different binnings")
        pdata_comp = {}
        pdata_comp['x'] = pdata_ref['x']
        pdata_comp['yerr'] = 0
        pdata_comp['xerr'] = pdata_ref['xerr']
        if pdata_ref['yerr'] is None:
            if isinstance(pdata_tgt['yerr'], tuple):
                yerr_ref = (np.zeros(pdata_ref['y'].shape), np.zeros(pdata_ref['y'].shape))
            else:
                yerr_ref = np.zeros(pdata_ref['y'].shape)
        else:
             yerr_ref = pdata_ref['yerr']
        if pdata_tgt['yerr'] is None:
            if isinstance(pdata_ref['yerr'], tuple):
                yerr_tgt = (np.zeros(pdata_tgt['y'].shape), np.zeros(pdata_tgt['y'].shape))
            else:
                yerr_tgt = np.zeros(pdata_tgt['y'].shape)
        else:
             yerr_tgt = pdata_tgt['yerr']
        if mode == "ratio":
            vmode = 0
        elif mode in ["diff", "difference"]:
            vmode = 1
        else:
            raise ValueError(f"unsupported mode \"{mode}\", choose between \"ratio\" and \"difference\"")
        valid_mask = (pdata_tgt['y'] > 0) & (pdata_ref['y'] > 0)
        if vmode == 0:
            pdata_comp['y'] = pdata_tgt['y'] / pdata_ref['y']
            if isinstance(yerr_ref, tuple):
                errlo = np.sqrt((yerr_ref[0]/pdata_ref['y'])**2 + (yerr_tgt[0]/pdata_tgt['y'])**2)
                errhi = np.sqrt((yerr_ref[1]/pdata_ref['y'])**2 + (yerr_tgt[1]/pdata_tgt['y'])**2)
                pdata_comp['yerr'] = (errlo, errhi)
            else:
                pdata_comp['yerr'] = np.sqrt((yerr_ref/pdata_ref['y'])**2 + (yerr_tgt/pdata_tgt['y'])**2)
        elif vmode == 1:
            pdata_comp['y'] = pdata_tgt['y'] - pdata_ref['y']
            if isinstance(yerr_ref, tuple):
                errlo = np.sqrt(yerr_ref[0]**2 + yerr_tgt[0]**2)
                errhi = np.sqrt(yerr_ref[1]**2 + yerr_tgt[1]**2)
                pdata_comp['yerr'] = (errlo, errhi)
            else:
                pdata_comp['yerr'] = np.sqrt(yerr_ref**2 + yerr_tgt**2)
            
        combined_options = combine_dict(plot_options)
        if combined_options.get('markersize', None) is None:
            nbins = len(pdata_comp['x'])
            combined_options['markersize'] = suggest_markersize(nbins)
            
        draw_blind = blind_range is not None
        if draw_blind:
            valid_mask &= pdata_ref['sideband']
        x = pdata_comp['x'][valid_mask]
        y = pdata_comp['y'][valid_mask]
        xerr = self._get_selected_err(pdata_comp['xerr'], valid_mask)
        yerr = self._get_selected_err(pdata_comp['yerr'], valid_mask)
        
        if not show_error:
            error_format = None
        handle = self._draw_data(ax, x, y, xerr, yerr,
                                 plot_options=combined_options,
                                 error_format=error_format,
                                 error_styles=error_styles)
            
        ylim = list(ax.get_ylim())
        if ylim[0] > np.min(y):
            ylim[0] = np.min(y)
        if ylim[1] < np.max(y):
            ylim[1] = np.max(y)
        ax.set_ylim(ylim)
        
        if vmode == 0:
            centralize_axis(ax, which="y", ref_value=1)
            if draw_ratio_line:
                ratio_linestyles = self.config['ratio_line_styles']
                ax.axhline(1, **ratio_linestyles)
        elif vmode == 1:
            centralize_axis(ax, which="y", ref_value=0)
            if draw_ratio_line:
                ratio_linestyles = self.config['ratio_line_styles']
                ax.axhline(0, **ratio_linestyles)
        if not ylabel:
            if vmode == 0:
                ylabel = "Fit / Data"
            elif vmode == 1:
                ylabel = "Fit - Data"
            else:
                ylabel = ""
        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)
        return handle
    
    def set_annotation(self, params:Optional[Dict]=None,
                       stats:Optional[Dict]=None,
                       val_fmt:str="{:.2f}",
                       **styles):
        text = ""
        if params:
            for param, value in params.items():
                if isinstance(value, float):
                    value = val_fmt.format(value)
                text += f"{param} = {value}\n"
            text += "\n"
        if stats:
            for stat, value in stats.items():
                if isinstance(value, float):
                    value = val_fmt.format(value)
                text += f"{stat} = {value}\n"
        self.annotation = {
            "text": text,
            **styles
        }
        
    def set_error_options(self, target:str,
                          display_format:Optional[Union[ErrorDisplayFormat, str]]="errorbar",
                          styles:Optional[Dict]=None):
        if display_format is not None:
            display_format = ErrorDisplayFormat.parse(display_format)
        self.error_options[target] = {
            "display_format": display_format,
            "styles": styles
        }

    def draw(self, xlabel:str="", ylabel:str="",
             targets:Optional[List]=None,
             logx:bool=False, logy:bool=False,
             blind_range:Optional[List[float]]=None,
             show_error:bool=True,
             plot_type:str='errorbar',
             comparison_options:Optional[Union[Dict, List[Dict]]]=None,
             xmin:Optional[float]=None, xmax:Optional[float]=None,
             ymin:Optional[float]=None, ymax:Optional[float]=None,
             ypad:Optional[float]=None):
        
        if comparison_options is not None:
            ax, ax_ratio = self.draw_frame(frametype='ratio', logx=logx, logy=logy)
        else:
            ax = self.draw_frame(frametype='single', logx=logx, logy=logy)
            ax_ratio = None
        
        if targets is None:
            targets = list(self.collective_data)
        if not self.legend_order:
            self.legend_order = list(targets)
        for target in targets:
            if target not in self.collective_data:
                raise RuntimeError(f'no input found for the target: {target}')
            data = self.collective_data[target]
            label = self.label_map.get(target, target)
            label_blind = self.label_map.get(f"{target}_blind", None)
            plot_options = self.plot_options.get(target, {})
            if (target not in self.error_options) or \
               (self.error_options[target]["display_format"] is None):
                error_format = None
                error_styles = None
            else:
                error_format = self.error_options[target]["display_format"]
                error_styles = self.error_options[target]["styles"]
            handle = self.draw_single_data(ax, data, label,
                                           label_blind=label_blind,
                                           blind_range=blind_range,
                                           plot_options=plot_options,
                                           show_error=show_error,
                                           error_format=error_format,
                                           error_styles=error_styles,
                                           plot_type=plot_type)
            if not handle.get_children():
                    self.colors[target] = handle.get_color()
            else:
                if plot_type == 'errorbar':
                    self.colors[target] = handle[0].get_color()
                elif plot_type == 'hist':
                    self.colors[target] = handle[0].get_edgecolor()
            # case draw blind
            if isinstance(handle, list) and len(handle) == 2:
                blind_target = f"{target}_blind"
                self.legend_order.append(blind_target)
                self.update_legend_handles({target: handle[0], blind_target: handle[1]})
            else:
                self.update_legend_handles({target: handle})

        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)
        self.set_axis_range(ax, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, ypad=ypad)  
        self.draw_legend(ax)
        
        if comparison_options is not None:
            if not isinstance(comparison_options, list):
                comparison_options = [comparison_options]
            for options in comparison_options:
                reference = options['reference']
                target    = options['target']
                mode      = options.get('mode', "ratio")
                ylabel    = options.get('label', "")
                labelsize = options.get('labelsize', None)
                styles    = options.get('styles', {})
                draw_ratio_line = options.get('draw_ratio_line', True)
                plot_options = self.plot_options.get(target, {})
                plot_options = combine_dict(plot_options, styles)
                if ('color' not in plot_options) and (target in self.colors):
                    plot_options['color'] = self.colors[target]
                plot_options.update(styles)
                if (reference not in self.error_options) or \
                   (self.error_options[reference]["display_format"] is None):
                    error_format = None
                    error_styles = None
                else:
                    error_format = self.error_options[reference]["display_format"]
                    error_styles = self.error_options[reference]["styles"]
                comparison_show_error = options.get('show_error', None)
                if comparison_show_error is None:
                    comparison_show_error = show_error
                self.draw_comparison(ax_ratio,
                                     self.collective_data[reference],
                                     self.collective_data[target],
                                     xlabel=ax.get_xlabel(),
                                     ylabel=ylabel, mode=mode,
                                     plot_options=plot_options,
                                     show_error=comparison_show_error,
                                     error_format=error_format,
                                     error_styles=error_styles,
                                     blind_range=blind_range,
                                     draw_ratio_line=draw_ratio_line)
                if labelsize is not None:
                    ax_ratio.yaxis.label.set_size(labelsize)                
            ax.set(xlabel=None)
            ax.tick_params(axis="x", labelbottom=False)

        if self.annotation:
            kwargs = combine_dict(self.styles['annotate'], self.annotation)
            ax.annotate(**kwargs)
            
        if comparison_options is not None:
            return ax, ax_ratio
        
        return ax

    @classmethod
    def from_roofit_data(cls, data:"ROOT.RooDataSet",
                         pdf:Optional["ROOT.RooAbsPdf"]=None,
                         observable:Optional["ROOT.RooRealVar"]=None,
                         bin_range:Optional[List]=None,
                         bin_error:bool=True,
                         nbins_data:Optional[int]=None,
                         nbins_pdf:Optional[int]=1000,
                         blind_range:Optional[List[float]]=None,
                         **kwargs):
        from quickstats.utils.roofit_utils import export_hist_data
        hist_data = export_hist_data(data, pdf,
                                     observable=observable,
                                     bin_range=bin_range,
                                     bin_error=bin_error,
                                     nbins_data=nbins_data,
                                     nbins_pdf=nbins_pdf)
        plotter = cls(hist_data, **kwargs)
        return plotter
    
    @classmethod
    def from_dataframes(cls, collective_df:Dict[str, "pandas.DataFrame"],
                        observable:str, weight:Optional[Union[float, str]]=None,
                        bin_range:Optional[Union[List, Tuple]]=None,
                        nbins:int=10, normalize:bool=True,
                        x_scale:Optional[float]=None,                        
                        error_mode:str="auto", **kwargs):
        from quickstats.maths.statistics import get_hist_data
        collective_data = {}
        for key, df in collective_df.items():
            x = df[observable].values 
            if x_scale is not None:
                x = x * x_scale
            if weight is None:
                weights = None
            elif isinstance(weight, numbers.Number):
                weights = np.full(shape=len(df.index), fill_value=weight)
            else:
                weights = df[weight].values
            hist_data = get_hist_data(x, weights, normalize=normalize,
                                      bin_range=bin_range, bins=nbins,
                                      error_mode=error_mode)
            collective_data[key] = hist_data
        plotter = cls(collective_data, **kwargs)
        return plotter