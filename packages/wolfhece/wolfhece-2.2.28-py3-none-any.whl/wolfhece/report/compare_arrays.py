import logging
import numpy as np
import numpy.ma as ma
from pathlib import Path
import matplotlib.pyplot as plt
from enum import Enum
from scipy.ndimage import label, sum_labels
import pymupdf as pdf

from .common import A4_rect, rect_cm, list_to_html, list_to_html_aligned, get_rect_from_text
from .common import inches2cm, pts2cm, cm2pts, cm2inches, DefaultLayoutA4, NamedTemporaryFile, pt2inches, TemporaryDirectory
from ..wolf_array import WolfArray, header_wolf, vector, zone, Zones, wolfvertex as wv, wolfpalette
from ..PyTranslate import _

class ArrayDifferenceLayout(DefaultLayoutA4):
    """
    Layout for comparing two arrays in a report.

    1 cadre pour la zone traitée avec photo de fond ign + contour vectoriel
    1 cadre avec zoom plus large min 250m
    1 cadre avec matrice ref + contour vectoriel
    1 cadre avec matrice à comparer + contour vectoriel
    1 cadre avec différence
    1 cadre avec valeurs de synthèse

    1 cadre avec histogramme
    1 cadre avec histogramme des différences
    """

    def __init__(self, title:str, filename = '', ox = 0, oy = 0, tx = 0, ty = 0, parent=None, is2D=True, idx = '', plotted = True, mapviewer=None, need_for_wx = False, bbox = None, find_minmax = True, shared = False, colors = None):
        super().__init__(title, filename, ox, oy, tx, ty, parent, is2D, idx, plotted, mapviewer, need_for_wx, bbox, find_minmax, shared, colors)

        useful = self.useful_part

        width = useful.xmax - useful.xmin
        height = useful.ymax - useful.ymin

        self._hitograms = self.add_element_repeated(_("Histogram"), width=width, height=2.5,
                                                    first_x=useful.xmin, first_y=useful.ymax,
                                                    count_x=1, count_y=-2, padding=0.5)

        self._arrays = self.add_element_repeated(_("Arrays"), width= (width-self.padding) / 2, height=5.5,
                                                 first_x=useful.xmin, first_y=self._hitograms.ymin - self.padding,
                                                count_x=2, count_y=-3, padding=0.5)

class CompareArraysLayout(DefaultLayoutA4):

    def __init__(self, title:str, filename = '', ox = 0, oy = 0, tx = 0, ty = 0, parent=None, is2D=True, idx = '', plotted = True, mapviewer=None, need_for_wx = False, bbox = None, find_minmax = True, shared = False, colors = None):
        super().__init__(title, filename, ox, oy, tx, ty, parent, is2D, idx, plotted, mapviewer, need_for_wx, bbox, find_minmax, shared, colors)

        useful = self.useful_part

        width = useful.xmax - useful.xmin
        height = useful.ymax - useful.ymin

        self._summary = self.add_element_repeated(_("Summary"), width=(width-self.padding) / 2, height=3, first_x=useful.xmin, first_y=useful.ymax-3, count_x=2, count_y=1)

        self._arrays = self.add_element_repeated(_("Arrays"), width= (width-self.padding) / 2, height=9., count_x=2, count_y=1, first_x=useful.xmin, first_y=14)
        self._diff_rect = self.add_element(_("Difference"), width= width, height=11.5, x=useful.xmin, y=useful.ymin)


class CompareArraysLayout2(DefaultLayoutA4):

    def __init__(self, title:str, filename = '', ox = 0, oy = 0, tx = 0, ty = 0, parent=None, is2D=True, idx = '', plotted = True, mapviewer=None, need_for_wx = False, bbox = None, find_minmax = True, shared = False, colors = None):
        super().__init__(title, filename, ox, oy, tx, ty, parent, is2D, idx, plotted, mapviewer, need_for_wx, bbox, find_minmax, shared, colors)

        useful = self.useful_part

        width = useful.xmax - useful.xmin
        height = useful.ymax - useful.ymin

        self._summary = self.add_element_repeated(_("Histogram"), width=(width-self.padding) / 2, height=6., first_x=useful.xmin, first_y=useful.ymax-6, count_x=2, count_y=1)

        self._arrays = self.add_element_repeated(_("Arrays"), width= (width-self.padding) / 2, height=6., count_x=2, count_y=1, first_x=useful.xmin, first_y=14)
        self._diff_rect = self.add_element(_("Position"), width= width, height=11.5, x=useful.xmin, y=useful.ymin)


class ArrayDifference():
    """
    Class to manage the difference between two WolfArray objects.
    """

    def __init__(self, reference:WolfArray, to_compare:WolfArray, index:int, label:np.ndarray):

        self._dpi = 600
        self.default_size_hitograms = (12, 6)
        self.default_size_arrays = (10, 10)
        self._fontsize = 6

        self.reference = reference
        self.to_compare = to_compare

        self.reference.updatepalette()
        self.to_compare.mypal = self.reference.mypal

        self.index = index
        self.label = label

        self._background = 'IGN'

    @property
    def contour(self) -> vector:
        ret = self.reference.suxsuy_contour(abs=True)
        ret = ret[2]

        ret.myprop.color = (0, 0, 255)
        ret.myprop.width = 2

        return ret

    @property
    def external_border(self) -> vector:
        """
        Get the bounds of the reference array.
        """
        ret = vector(name=_("External border"))
        (xmin, xmax), (ymin, ymax) = self.reference.get_bounds()
        ret.add_vertex(wv(xmin, ymin))
        ret.add_vertex(wv(xmax, ymin))
        ret.add_vertex(wv(xmax, ymax))
        ret.add_vertex(wv(xmin, ymax))
        ret.force_to_close()

        ret.myprop.color = (255, 0, 0)
        ret.myprop.width = 3

        return ret

    def __str__(self):

        assert self.reference.nbnotnull == self.to_compare.nbnotnull, "The number of non-null cells in both arrays must be the same."

        ret = self.reference.__str__() + '\n'

        ret += _("Index : ") + str(self.index) + '\n'
        ret += _("Number of cells : ") + str(self.reference.nbnotnull) + '\n'

        return ret

    @property
    def _summary_text(self):
        """
        Generate a summary text for the report.
        """
        diff = self.difference.array.compressed()
        text = [
            _("Index: ") + str(self.index),
            _("Number of cells: ") + str(self.reference.nbnotnull),
            _('Resolution: ') + f"{self.reference.dx} m x {self.reference.dy} m",
            _('Extent: ') + f"({self.reference.origx}, {self.reference.origy})" + f" - ({self.reference.origx + self.reference.nbx * self.reference.dx}, {self.reference.origy + self.reference.nby * self.reference.dy})",
            _('Width x Height: ') + f"{self.reference.nbx * self.reference.dx} m x {self.reference.nby * self.reference.dy} m",
            _('Excavation: ') + f"{np.sum(diff[diff < 0.]) * self.reference.dx * self.reference.dy:.3f} m³",
            _('Deposit/Backfill: ') + f"{np.sum(diff[diff > 0.]) * self.reference.dx * self.reference.dy:.3f} m³",
            _('Net volume: ') + f"{np.sum(diff) * self.reference.dx * self.reference.dy:.3f} m³",
        ]
        return text

    def set_palette_distribute(self, minval:float, maxval:float, step:int=0):
        """
        Set the palette for both arrays.
        """
        self.reference.mypal.distribute_values(minval, maxval, step)

    def set_palette(self, values:list[float], colors:list[tuple[int, int, int]]):
        """
        Set the palette for both arrays based on specific values.
        """
        self.reference.mypal.set_values_colors(values, colors)

    def plot_position(self, figax:tuple[plt.Figure, plt.Axes]=None) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the reference array.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        old_mask = self.reference.array.mask.copy()
        self.reference.array.mask[:,:] = True

        if self._background.upper() == 'IGN' or self._background.upper() == 'NGI':
            self.reference.plot_matplotlib(figax=figax, figsize = self.default_size_arrays,
                                        first_mask_data=False, with_legend=False,
                                        update_palette= False,
                                        IGN= True,
                                        cat = 'orthoimage_coverage',
                                        )

        elif self._background.upper() == 'WALONMAP':
            self.reference.plot_matplotlib(figax=figax, figsize = self.default_size_arrays,
                                        first_mask_data=False, with_legend=False,
                                        update_palette= False,
                                        Walonmap= True,
                                        cat = 'IMAGERIE/ORTHO_2022_ETE',
                                        )

        self.reference.array.mask[:,:] = old_mask

        self.external_border.plot_matplotlib(ax=ax)
        self.contour.plot_matplotlib(ax=ax)

        return fig, ax

    def plot_position_scaled(self, scale = 4, figax:tuple[plt.Figure, plt.Axes]=None) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the reference array.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        h = self.reference.get_header()
        width = h.nbx * h.dx
        height = h.nby * h.dy

        h.origx += -width * scale / 2
        h.origy += -height *scale / 2
        h.nbx = 1
        h.nby = 1
        h.dx = width *(scale + 1)
        h.dy = height *(scale + 1)

        new = WolfArray(srcheader=h)
        new.array.mask[:,:] = True

        new.plot_matplotlib(figax=figax, figsize = self.default_size_arrays,
                                       first_mask_data=False, with_legend=False,
                                       update_palette= False,
                                       Walonmap= True,
                                       cat = 'IMAGERIE/ORTHO_2022_ETE')

        self.external_border.plot_matplotlib(ax=ax)

        return fig, ax

    def plot_reference(self, figax:tuple[plt.Figure, plt.Axes]=None) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the reference array.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        self.reference.plot_matplotlib(figax=figax, figsize = self.default_size_arrays, first_mask_data=False, with_legend=True, update_palette= False)
        return fig, ax

    def plot_to_compare(self, figax:tuple[plt.Figure, plt.Axes]=None) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the array to compare.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        self.to_compare.plot_matplotlib(figax=figax, figsize = self.default_size_arrays, first_mask_data=False, with_legend=True, update_palette= False)
        return fig, ax

    @property
    def difference(self) -> WolfArray:
        """
        Get the difference between the two arrays.
        """
        if not isinstance(self.reference, WolfArray) or not isinstance(self.to_compare, WolfArray):
            raise TypeError("Both inputs must be instances of WolfArray")

        return self.to_compare - self.reference

    def plot_difference(self, figax:tuple[plt.Figure, plt.Axes]=None) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the array to compare.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        pal = wolfpalette()
        pal.default_difference3()

        diff = self.difference
        diff.mypal = pal
        diff.plot_matplotlib(figax=figax, figsize = self.default_size_arrays, first_mask_data=False, with_legend=True, update_palette= False)
        return fig, ax

    def _plot_histogram_reference(self, figax:tuple[plt.Figure, plt.Axes]=None, density = True, alpha = 0.5, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot histogram of the reference array.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        ax.hist(self.reference.array.compressed(), density=density, alpha = alpha, **kwargs)
        # ax.set_xlabel("Value")
        # ax.set_ylabel("Frequency")
        return fig, ax

    def _plot_histogram_to_compare(self, figax:tuple[plt.Figure, plt.Axes]=None, density = True, alpha = 0.5, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot histogram of the array to compare.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        ax.hist(self.to_compare.array.compressed(), density=density, alpha = alpha, **kwargs)
        # ax.set_xlabel("Value")
        # ax.set_ylabel("Frequency")
        return fig, ax

    def plot_histograms(self, figax:tuple[plt.Figure, plt.Axes]=None, density = True, alpha = 0.5, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot histograms of both arrays.
        """
        if figax is None:
            figax = plt.subplots(1, 1, figsize=self.default_size_hitograms)

        fig, ax = figax

        self._plot_histogram_reference((fig, ax), density = density, alpha=alpha, **kwargs)
        self._plot_histogram_to_compare((fig, ax), density = density, alpha=alpha, **kwargs)

        # set font size of the labels
        ax.tick_params(axis='both', which='major', labelsize=6)
        for label in ax.get_xticklabels():
            label.set_fontsize(self._fontsize)
        for label in ax.get_yticklabels():
            label.set_fontsize(self._fontsize)
        # and gfor the label title
        ax.set_xlabel(ax.get_xlabel(), fontsize=self._fontsize)
        ax.set_ylabel(ax.get_ylabel(), fontsize=self._fontsize)

        fig.tight_layout()
        return fig, ax

    def plot_histograms_difference(self, figax:tuple[plt.Figure, plt.Axes]=None, density = True, alpha = 1.0, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot histogram of the difference between the two arrays.
        """
        if figax is None:
            figax = plt.subplots(figsize=self.default_size_hitograms)

        fig, ax = figax

        difference_data = self.difference.array.compressed()
        ax.hist(difference_data, density=density, alpha=alpha, **kwargs)

        # ax.set_xlabel("Value")
        # ax.set_ylabel("Frequency")

        # set font size of the labels
        ax.tick_params(axis='both', which='major', labelsize=6)
        for label in ax.get_xticklabels():
            label.set_fontsize(self._fontsize)
        for label in ax.get_yticklabels():
            label.set_fontsize(self._fontsize)
        # and gfor the label title
        ax.set_xlabel(ax.get_xlabel(), fontsize=self._fontsize)
        ax.set_ylabel(ax.get_ylabel(), fontsize=self._fontsize)

        return fig, ax

    def _complete_report(self, layout:ArrayDifferenceLayout):

        """
        Complete the report with the arrays and histograms.
        """
        useful = layout.useful_part

        # Plot reference array
        key_fig = [('Histogram_0-0', self.plot_histograms),
                   ('Histogram_0-1', self.plot_histograms_difference),
                   ('Arrays_0-0', self.plot_position),
                   ('Arrays_1-0', self.plot_position_scaled),
                   ('Arrays_0-1', self.plot_reference),
                   ('Arrays_1-1', self.plot_to_compare),
                   ('Arrays_0-2', self.plot_difference),]

        keys = layout.keys
        for key, fig_routine in key_fig:
            if key in keys:

                rect = layout._layout[key]

                fig, ax = fig_routine()

                # set size to fit the rectangle
                fig.set_size_inches(pt2inches(rect.width), pt2inches(rect.height))

                if 'Histogram' in key:
                    fig.tight_layout()


                # convert canvas to PNG and insert it into the PDF
                temp_file = NamedTemporaryFile(delete=False, suffix='.png')
                fig.savefig(temp_file, format='png', bbox_inches='tight', dpi=self._dpi)
                layout._page.insert_image(layout._layout[key], filename = temp_file.name)
                # delete the temporary file
                temp_file.delete = True
                temp_file.close()

                # Force to delete fig
                plt.close(fig)
            else:
                logging.warning(f"Key {key} not found in layout. Skipping plot.")

        key = 'Arrays_1-2'
        if key in keys:
            text, css = list_to_html(self._summary_text, font_size='8pt')
            layout._page.insert_htmlbox(layout._layout[key], text,
                                css=css)

    def create_report(self, output_file: str | Path = None) -> Path:
        """ Create a page report for the array difference. """

        if output_file is None:
            output_file = Path(f"array_difference_{self.index}.pdf")

        if output_file.exists():
            logging.warning(f"Output file {output_file} already exists. It will be overwritten.")

        layout = ArrayDifferenceLayout(f"Differences - Index n°{self.index}")
        layout.create_report()
        self._complete_report(layout)
        layout.save_report(output_file)

        return output_file

class CompareArrays:

    def __init__(self, reference: WolfArray | str | Path, to_compare: WolfArray | str | Path):

        self._dpi = 600
        self.default_size_arrays = (10, 10)
        self._fontsize = 6

        if isinstance(reference, (str, Path)):
            reference = WolfArray(reference)
        if isinstance(to_compare, (str, Path)):
            to_compare = WolfArray(to_compare)

        if not reference.is_like(to_compare):
            raise ValueError("Arrays are not compatible for comparison")

        self.array_reference:WolfArray
        self.array_to_compare:WolfArray
        self.array_reference = reference
        self.array_to_compare = to_compare

        self.labeled_array: np.ndarray = None
        self.num_features: int = 0
        self.nb_cells: list = []

        self.difference_parts:dict[int, ArrayDifference] = {}

    @property
    def difference(self) -> WolfArray:

        if not isinstance(self.array_reference, WolfArray) or not isinstance(self.array_to_compare, WolfArray):
            raise TypeError("Both inputs must be instances of WolfArray")

        return self.array_to_compare - self.array_reference

    def plot_position(self, figax:tuple[plt.Figure, plt.Axes]=None) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the reference array with a background.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        h = self.array_reference.get_header()
        width = h.nbx * h.dx
        height = h.nby * h.dy
        h.dx = width
        h.dy = height
        h.nbx = 1
        h.nby = 1

        new = WolfArray(srcheader=h)
        new.array.mask[:,:] = True


        new.plot_matplotlib(figax=figax, figsize = self.default_size_arrays,
                                    first_mask_data=False, with_legend=False,
                                    update_palette= False,
                                    IGN= True,
                                    cat = 'orthoimage_coverage',
                                    )

        return fig, ax

    def plot_cartoweb(self, figax:tuple[plt.Figure, plt.Axes]=None) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the reference array with a background.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        h = self.array_reference.get_header()
        width = h.nbx * h.dx
        height = h.nby * h.dy
        h.dx = width
        h.dy = height
        h.nbx = 1
        h.nby = 1

        new = WolfArray(srcheader=h)
        new.array.mask[:,:] = True


        new.plot_matplotlib(figax=figax, figsize = self.default_size_arrays,
                                    first_mask_data=False, with_legend=False,
                                    update_palette= False,
                                    Cartoweb= True,
                                    cat = 'overlay',
                                    )

        return fig, ax

    def plot_topo_grey(self, figax:tuple[plt.Figure, plt.Axes]=None) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the reference array with a background.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        h = self.array_reference.get_header()
        width = h.nbx * h.dx
        height = h.nby * h.dy
        h.dx = width
        h.dy = height
        h.nbx = 1
        h.nby = 1

        new = WolfArray(srcheader=h)
        new.array.mask[:,:] = True


        new.plot_matplotlib(figax=figax, figsize = self.default_size_arrays,
                                    first_mask_data=False, with_legend=False,
                                    update_palette= False,
                                    Cartoweb= True,
                                    cat = 'topo_grey',
                                    )

        return fig, ax

    def plot_reference(self, figax:tuple[plt.Figure, plt.Axes]=None) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the reference array.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        self.array_reference.plot_matplotlib(figax=figax, figsize = self.default_size_arrays, first_mask_data=False, with_legend=True, update_palette= False)

        for diff in self.difference_parts.values():
            diff.external_border.plot_matplotlib(ax=ax)

        return fig, ax

    def plot_to_compare(self, figax:tuple[plt.Figure, plt.Axes]=None) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the array to compare.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        self.array_to_compare.plot_matplotlib(figax=figax, figsize = self.default_size_arrays, first_mask_data=False, with_legend=True, update_palette= False)

        for diff in self.difference_parts.values():
            diff.contour.plot_matplotlib(ax=ax)

        return fig, ax

    def plot_difference(self, figax:tuple[plt.Figure, plt.Axes]=None) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the difference between the two arrays.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        pal = wolfpalette()
        pal.default_difference3()

        diff = self.difference
        diff.mypal = pal
        diff.plot_matplotlib(figax=figax, figsize = self.default_size_arrays, first_mask_data=False, with_legend=True, update_palette= False)
        return fig, ax

    def localize_differences(self, threshold: float = 0.0) -> np.ndarray:

        labeled_array = self.difference.array.data.copy()
        labeled_array[self.array_reference.array.mask] = 0

        self.labeled_array, self.num_features = label(labeled_array)

        self.nb_cells = []

        self.nb_cells = list(sum_labels(np.ones(self.labeled_array.shape, dtype=np.int32), self.labeled_array, range(1, self.num_features+1)))
        self.nb_cells = [[self.nb_cells[j], j+1] for j in range(0, self.num_features)]

        self.nb_cells.sort(key=lambda x: x[0], reverse=True)

        # find xmin, ymin, xmax, ymax for each feature
        for idx_feature in range(1, self.num_features + 1):
            mask = self.labeled_array == idx_feature
            i, j = np.where(mask)

            imin, imax = i.min(), i.max()
            jmin, jmax = j.min(), j.max()

            imin = int(max(imin - 1, 0))
            imax = int(min(imax + 1, self.labeled_array.shape[0] - 1))
            jmin = int(max(jmin - 1, 0))
            jmax = int(min(jmax + 1, self.labeled_array.shape[1] - 1))

            ref_crop = self.array_reference.crop(imin, jmin, imax-imin+1, jmax-jmin+1)
            to_compare_crop = self.array_to_compare.crop(imin, jmin, imax-imin+1, jmax-jmin+1)

            ref_crop.array.mask[:,:] = ~mask[imin:imax+1, jmin:jmax+1]
            ref_crop.set_nullvalue_in_mask()

            to_compare_crop.array.mask[:,:] = ~mask[imin:imax+1, jmin:jmax+1]
            to_compare_crop.set_nullvalue_in_mask()

            ref_crop.count()
            to_compare_crop.nbnotnull = ref_crop.nbnotnull

            self.difference_parts[idx_feature] = ArrayDifference(ref_crop, to_compare_crop, idx_feature, self.labeled_array[imin:imax+1, jmin:jmax+1].copy())

        return self.labeled_array

    @property
    def summary_text(self) -> list[str]:
        """
        Generate a summary text for the report.
        """

        diff = self.difference.array.compressed()
        text_left = [
            _("Number of features: ") + str(self.num_features),
            _('Resolution: ') + f"{self.array_reference.dx} m x {self.array_reference.dy} m",
            _('Extent: ') + f"({self.array_reference.origx}, {self.array_reference.origy})" + f" - ({self.array_reference.origx + self.array_reference.nbx * self.array_reference.dx}, {self.array_reference.origy + self.array_reference.nby * self.array_reference.dy})",
            _('Width x Height: ') + f"{self.array_reference.nbx * self.array_reference.dx} m x {self.array_reference.nby * self.array_reference.dy} m",
        ]
        text_right = [
            _('Excavation: ') + f"{np.sum(diff[diff < 0.]) * self.array_reference.dx * self.array_reference.dy:.3f} m³",
            _('Deposit/Backfill: ') + f"{np.sum(diff[diff > 0.]) * self.array_reference.dx * self.array_reference.dy:.3f} m³",
            _('Net volume: ') + f"{np.sum(diff) * self.array_reference.dx * self.array_reference.dy:.3f} m³",
        ]
        return text_left, text_right

    def _complete_report(self, layout:CompareArraysLayout):
        """ Complete the report with the global summary and individual differences. """

        key_fig = [('Arrays_0-0', self.plot_reference),
                   ('Arrays_1-0', self.plot_to_compare),
                   ('Difference', self.plot_difference),]

        keys = layout.keys
        for key, fig_routine in key_fig:
            if key in keys:

                rect = layout._layout[key]

                fig, ax = fig_routine()

                # set size to fit the rectangle
                fig.set_size_inches(pt2inches(rect.width), pt2inches(rect.height))

                # convert canvas to PNG and insert it into the PDF
                temp_file = NamedTemporaryFile(delete=False, suffix='.png')
                fig.savefig(temp_file, format='png', bbox_inches='tight', dpi=self._dpi)
                layout._page.insert_image(layout._layout[key], filename=temp_file.name)
                # delete the temporary file
                temp_file.delete = True
                temp_file.close()

                # Force to delete fig
                plt.close(fig)
            else:
                logging.warning(f"Key {key} not found in layout. Skipping plot.")

        tleft, tright = self.summary_text

        rect = layout._layout['Summary_0-0']
        text_left, css_left = list_to_html(tleft, font_size='8pt')
        layout._page.insert_htmlbox(rect, text_left, css=css_left)
        rect = layout._layout['Summary_1-0']
        text_right, css_right = list_to_html(tright, font_size='8pt')
        layout._page.insert_htmlbox(rect, text_right, css=css_right)

    def plot_histogram_features(self, figax:tuple[plt.Figure, plt.Axes]=None, density = True, alpha = 0.5, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot histogram of the number of cells in each feature.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        surf = self.array_reference.dx * self.array_reference.dy

        # Extract the number of cells for each feature
        nb_cells = [item[0] * surf for item in self.nb_cells]

        ax.hist(nb_cells, density=density, alpha=alpha, **kwargs)

        ax.set_title(_("Histogram of surface in each feature [m²]"))

        # set font size of the labels
        ax.tick_params(axis='both', which='major', labelsize=6)
        for label in ax.get_xticklabels():
            label.set_fontsize(self._fontsize)
        for label in ax.get_yticklabels():
            label.set_fontsize(self._fontsize)
        # and gfor the label title
        ax.set_xlabel(ax.get_xlabel(), fontsize=self._fontsize)
        ax.set_ylabel(ax.get_ylabel(), fontsize=self._fontsize)

        return fig, ax

    def plot_histogram_features_difference(self, figax:tuple[plt.Figure, plt.Axes]=None, density = True, alpha = 1.0, **kwargs) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot histogram of the volume in each feature for the difference.
        """
        if figax is None:
            figax = plt.subplots()

        fig, ax = figax

        # Calculate the difference between the two arrays
        diff = self.difference

        volumes = np.bincount(self.labeled_array.ravel(), weights=diff.array.ravel()) * self.array_reference.dx * self.array_reference.dy

        # Create a histogram of the differences
        ax.hist(volumes, density=density, alpha=alpha, **kwargs)

        ax.set_title(_("Histogram of net volumes [m³]"))

        # set font size of the labels
        ax.tick_params(axis='both', which='major', labelsize=6)
        for label in ax.get_xticklabels():
            label.set_fontsize(self._fontsize)
        for label in ax.get_yticklabels():
            label.set_fontsize(self._fontsize)
        # and gfor the label title
        ax.set_xlabel(ax.get_xlabel(), fontsize=self._fontsize)
        ax.set_ylabel(ax.get_ylabel(), fontsize=self._fontsize)

        fig.tight_layout()

        return fig, ax

    def _complete_report2(self, layout:CompareArraysLayout):
        """ Complete the report with the individual differences. """

        key_fig = [('Histogram_0-0', self.plot_histogram_features),
                   ('Histogram_1-0', self.plot_histogram_features_difference),
                   ('Arrays_0-0', self.plot_position),
                   ('Arrays_1-0', self.plot_cartoweb),
                   ('Position', self.plot_topo_grey),
                   ]

        keys = layout.keys
        for key, fig_routine in key_fig:
            if key in keys:

                rect = layout._layout[key]

                fig, ax = fig_routine()

                # set size to fit the rectangle
                fig.set_size_inches(pt2inches(rect.width), pt2inches(rect.height))
                fig.tight_layout()

                # convert canvas to PNG and insert it into the PDF
                temp_file = NamedTemporaryFile(delete=False, suffix='.png')
                fig.savefig(temp_file, format='png', bbox_inches='tight', dpi=self._dpi)
                layout._page.insert_image(layout._layout[key], filename=temp_file.name)
                # delete the temporary file
                temp_file.delete = True
                temp_file.close()

                # Force to delete fig
                plt.close(fig)
            else:
                logging.warning(f"Key {key} not found in layout. Skipping plot.")



    def create_report(self, output_file: str | Path = None, append_all_differences: bool = True) -> None:
        """ Create a page report for the array comparison. """

        if output_file is None:
            output_file = Path(f"compare_arrays_report.pdf")

        if output_file.exists():
            logging.warning(f"Output file {output_file} already exists. It will be overwritten.")

        layout = CompareArraysLayout("Comparison Report")
        layout.create_report()
        self._complete_report(layout)


        with TemporaryDirectory() as temp_dir:

            layout2 = CompareArraysLayout2("Distribution of Differences")
            layout2.create_report()
            self._complete_report2(layout2)
            layout2.save_report(Path(temp_dir) / "distribution_of_differences.pdf")
            all_pdfs = [Path(temp_dir) / "distribution_of_differences.pdf"]

            if append_all_differences:
                # Add each difference report to the main layout
                all_pdfs.extend([diff.create_report(Path(temp_dir) / f"array_difference_{idx}.pdf") for idx, diff in self.difference_parts.items()])

            for pdf_file in all_pdfs:
                layout._doc.insert_file(pdf_file)

        # create a TOC
        layout._doc.set_toc(layout._doc.get_toc())

        layout.save_report(output_file)