from typing import Optional, Union, Dict, List

import numpy as np
import matplotlib.patches as patches

from quickstats.plots import AbstractPlot
from quickstats.plots.template import create_transform
from quickstats.utils.common_utils import combine_dict

class UpperLimit3DPlot(AbstractPlot):
    
    STYLES = {
        'axis':{
            'tick_bothsides': True
        },
        'errorbar': {
            "linewidth": 1,
            "markersize": 5,
            "marker": 'o',
        }        
    }
    
    COLOR_PALLETE = {
        '2sigma': '#FDC536',
        '1sigma': '#4AD9D9',
        'expected': 'k',
        'excluded': 'w',
        'observed': 'k'
    }
    
    COLOR_PALLETE_SEC = {
        '2sigma': '#FDC536',
        '1sigma': '#4AD9D9',
        'expected': 'r',
        'observed': 'r'
    }
    
    LABELS = {
        '2sigma': r'Expected limit $\pm 2\sigma$',
        '1sigma': r'Expected limit $\pm 1\sigma$',
        'expected': 'Expected limit (95% CL)',
        'observed': 'Observed limit (95% CL)'
    }
    
    LABELS_SEC = {
        '2sigma': r'Expected limit $\pm 2\sigma$',
        '1sigma': r'Expected limit $\pm 1\sigma$',
        'expected': 'Expected limit (95% CL)',
        'observed': 'Observed limit (95% CL)'
    }

    CONFIG = {
        'primary_hatch'  : '\\\\\\',
        'secondary_hatch': '///',
        'primary_alpha'  : 0.9,
        'secondary_alpha': 0.8,
        'curve_line_styles': {
            'color': 'darkred' 
        },
        'curve_fill_styles':{
            'color': 'hh:darkpink'
        },
        'highlight_styles': {
            'linewidth' : 0,
            'marker' : '*',
            'markersize' : 20,
            'color' : '#E9F1DF',
            'markeredgecolor' : 'black'
        }
    }
    
    def __init__(self, data, data_sec=None,
                 num_grid_points=None,
                 color_pallete:Optional[Dict]=None,
                 color_pallete_sec:Optional[Dict]=None,
                 labels:Optional[Dict]=None,
                 labels_sec:Optional[Dict]=None,
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Union[Dict, str]]='default',
                 config:Optional[Dict]=None):
        super().__init__(color_pallete=color_pallete,
                         color_pallete_sec=color_pallete_sec,
                         styles=styles,
                         analysis_label_options=analysis_label_options,
                         config=config)
        self.data     = data
        # secondary data
        self.data_sec = data_sec
        
        self.labels = combine_dict(self.LABELS, labels)
        self.labels_sec = combine_dict(self.LABELS_SEC, labels_sec)
        
        self.num_grid_points = num_grid_points
        self.highlight_data = None
        
    def get_default_legend_order(self):
        return ['observed', 'expected', '1sigma', '2sigma', 'curve', 'highlight']
    
    def add_highlight(self, x:float, y:float, label:str="SM prediction",
                      styles:Optional[Dict]=None):
        highlight_data = {
            'x'     : x,
            'y'     : y,
            'label' : label,
            'styles': styles
        }
        self.highlight_data = highlight_data        
    
    def draw_highlight(self, ax, data):
        styles = data['styles']
        if styles is None:
            styles = self.config['highlight_styles']
        handle = ax.plot(data['x'], data['y'], label=data['label'], **styles)
        self.update_legend_handles({'highlight': handle[0]})

    @staticmethod
    def get_grid(X_range, Y_range, num_grid_points):
        X_points = np.linspace(*X_range, num_grid_points)
        Y_points = np.linspace(*Y_range, num_grid_points)
        X_grid, Y_grid = np.meshgrid(X_points, Y_points)
        return X_grid, Y_grid

    def return_points(self, paths):
        ''' Get x-y coordinates of contour/path in order to fill color for bands '''
        uout, inn = 0, 1
        segment1_start = paths[0].vertices[0]
        segment1_end = paths[0].vertices[-1]
        try:
            if len(paths) == 2 and (segment1_start != segment1_end).all():
                segment2_start = paths[1].vertices[0]
                segment2_end = paths[1].vertices[-1]
                if np.square(segment2_start-segment2_end) > np.square(segment1_start-segment1_end):
                    out, inn = 1, 0
                return (paths[out].vertices, paths[inn].vertices)
            else:
                return (np.concatenate([i.vertices for i in paths]),)
        except Exception:
            return (np.concatenate([i.vertices for i in paths]),)

    def plot_bands(self, ax, cp, labels, cp_obs=None, domain:Optional[str]=None):
        # loop over contour curves
        # assumption: 0,4 = 2sigma outer/inner boundaries; 1,3 = 1sigma outer/inner boundaries; 2 = expectation
        inner2 = self.return_points(cp.collections[0].get_paths())
        inner1 = self.return_points(cp.collections[1].get_paths())
        center = self.return_points(cp.collections[2].get_paths())
        outer1 = self.return_points(cp.collections[3].get_paths())
        outer2 = self.return_points(cp.collections[4].get_paths())
        if cp_obs:
            observ = self.return_points(cp_obs.collections[0].get_paths())

        # fill color from outside to inside
        handle_2sigma = ax.fill(outer2[0][:,0], outer2[0][:,1],
                                self.color_pallete['2sigma'],
                                label=labels['2sigma'], zorder=1)
        handle_1sigma = ax.fill(outer1[0][:,0], outer1[0][:,1],
                                self.color_pallete['1sigma'],
                                label=labels['1sigma'], zorder=1)
        handle_expected = ax.plot(center[0][:,0], center[0][:,1],
                                  self.color_pallete['expected'], ls='--',
                                  label=labels['expected'], zorder=2)
        ax.fill(inner1[0][:,0], inner1[0][:,1], self.color_pallete['2sigma'], zorder=1)
        ax.fill(inner2[0][:,0], inner2[0][:,1], self.color_pallete['excluded'], zorder=1)
        if len(outer2) > 1:
            handle_2sigma = ax.fill(outer2[1][:,0], outer2[1][:,1], self.color_pallete['excluded'], zorder=1)
        if len(outer1) + len(center) + len(inner1) + len(inner2) > 4 :
            print('WARN', len(outer1) , len(center) , len(inner1) , len(inner2))

        if cp_obs:
            handle_observed = ax.plot(observ[0][:,0], observ[0][:,1],
                                      self.color_pallete['observed'],
                                      ls='-', label=labels['observed'], zorder=2)

        self.update_legend_handles({'2sigma': handle_2sigma[0],
                                    '1sigma': handle_1sigma[0],
                                    'expected': handle_expected[0]},
                                   domain=domain)
        if cp_obs:
            self.update_legend_handles({'observed': handle_observed[0]}, domain=domain)

    def draw_single_data(self, ax, df, x='klambda', y='k2v', scale_factor=None,
                         theory_grid=None,
                         color_pallete:Optional[Dict]=None,
                         labels:Optional[Dict]=None,
                         draw_observed:bool=False,
                         observed_marker:Optional[str]='o', 
                         alpha:float=1.,
                         domain:Optional[str]=None):
        
        assert(theory_grid.shape == (self.num_grid_points, self.num_grid_points)), '`theory_grid` in draw() fails to have shape of (`self.num_grid_points`, `self.num_grid_points`)'
        assert(not df.isnull().values.any()), 'input dataframe contains NAN'
        if color_pallete is None:
            color_pallete = self.color_pallete
        if labels is None:
            labels = self.labels
        if scale_factor is None:
            scale_factor = 1.0

        # Create 2D grid of values for a range of two coupling constant variations (e.g. a grid of k2v and kl points) by interpolating to the grid
        X_range = df[x].min(), df[x].max()
        Y_range = df[y].min(), df[y].max()
        X_grid, Y_grid = UpperLimit3DPlot.get_grid(X_range, Y_range, self.num_grid_points)

        expectation_point_list = {}
        expectation_point_list['points'] = (df[x], df[y])
        expectation_point_list['exp'] = df['0'] * scale_factor
        expectation_point_list['1sigma'] = df['1'] * scale_factor
        expectation_point_list['-1sigma'] = df['-1'] * scale_factor
        expectation_point_list['2sigma'] = df['2'] * scale_factor
        expectation_point_list['-2sigma'] = df['-2'] * scale_factor
        if draw_observed:
            expectation_point_list['obs'] = df['obs'] * scale_factor
        
        exp_grids = {}
        for i in expectation_point_list.keys():
            if i == 'points':
                continue
            from scipy import interpolate
            exp_grids[i] = interpolate.griddata(expectation_point_list['points'], 
                                                expectation_point_list[i], np.stack((X_grid, Y_grid), axis=2))
        
        # Create a 2D grid of Z-values for contour plot, arbitarily assign values of:
        #   0.5 within +1 sigma, 1.5 between +1 and +2 sigma, 2.5 outside of 2 sigma;
        #   -0.5 within -1 sigma, -1.5 between -1 and -2 sigma, -2.5 outside of -2 sigma
        Z_grid = np.zeros(theory_grid.shape)
        Z_grid[theory_grid - exp_grids['exp'] >= 0] = 0.5
        Z_grid[theory_grid - exp_grids['exp'] < 0] = -0.5
        Z_grid[theory_grid - exp_grids['1sigma'] > 0] = 1.5
        Z_grid[theory_grid - exp_grids['2sigma'] > 0] = 2.5
        Z_grid[theory_grid - exp_grids['-1sigma'] < 0] = -1.5
        Z_grid[theory_grid - exp_grids['-2sigma'] < 0] = -2.5

        contour_exp = ax.contour(X_grid, Y_grid, Z_grid, levels=[-2, -1, 0, 1, 2], linewidths=2, alpha=0, zorder=0)
        #ax.contourf(X_grid, Y_grid, Z_grid, levels=[-2, -1, 0, 1, 2], linewidths=2, alpha=1, zorder=0, cmap='GnBu')

        if draw_observed:
            Z_grid_obs = np.zeros(theory_grid.shape)
            Z_grid_obs[theory_grid - exp_grids['obs'] >= 0] = 0.5
            Z_grid_obs[theory_grid - exp_grids['obs'] < 0] = -0.5

            contour_obs = ax.contour(X_grid, Y_grid, Z_grid_obs, levels=[0], linewidths=2, alpha=0, zorder=0)

        # Plot 1 and 2 sigma bands
        self.plot_bands(ax, contour_exp, labels,
                        cp_obs=contour_obs if draw_observed else None,
                        domain=domain)


    def draw(self, x:str="", y:str="", xlabel:str="", ylabel:str="", scale_factor=None, theory_grid=None, ylim=None, xlim=None,
             draw_observed:bool=True, observed_marker:Optional[str]='o', draw_sm_line:bool=False):
        
        ax = self.draw_frame()
        
        if self.data_sec is not None:
            self.draw_single_data(ax, df=self.data_sec, x=x, y=y,
                                  scale_factor=scale_factor,
                                  theory_grid=theory_grid,
                                  draw_observed=draw_observed,
                                  color_pallete=self.color_pallete_sec,
                                  labels=self.labels_sec,
                                  observed_marker=observed_marker, 
                                  domain='extra_data_1')
            alpha = self.config['primary_alpha']
        else:
            alpha = 1.
        self.draw_single_data(ax, df=self.data, x=x, y=y,
                              scale_factor=scale_factor,
                              theory_grid=theory_grid,
                              draw_observed=draw_observed,
                              color_pallete=self.color_pallete,
                              labels=self.labels,
                              observed_marker=observed_marker, 
                              alpha=alpha)
        if self.highlight_data is not None:
            self.draw_highlight(ax, self.highlight_data)
            
        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)
        
        if ylim is not None:
            ax.set_ylim(*ylim)
        if xlim is not None:
            ax.set_xlim(*xlim)

        if draw_sm_line:
            sm_line_styles = self.config['sm_line_styles']
            sm_values = self.config['sm_values']
            transform = create_transform(transform_y="axis", transform_x="data")
            ax.vlines(sm_values[0], ymin=0, ymax=1, zorder=2, transform=transform,
                      **sm_line_styles)
            transform = create_transform(transform_x="axis", transform_y="data")
            ax.hlines(sm_values[1], xmin=0, xmax=1, zorder=2, transform=transform,
                      **sm_line_styles)

        legend_domains = self.get_legend_domains()

        # border for the legend
        border_leg = patches.Rectangle((0, 0), 1, 1, facecolor = 'none', edgecolor = 'black', linewidth = 1)
        for domain in legend_domains:
            self.add_legend_decoration(border_leg, ['1sigma', '2sigma'], domain=domain)
            
        self.draw_legend(ax, domains=legend_domains)

        return ax

