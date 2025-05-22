import argparse
from collections import Counter
import json
from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from rich_argparse import RichHelpFormatter
from rich import print

###############################################################################

__prog__ = 'af_plotter'
__version__ = '0.1'
__author__ = 'George Young'
__maintainer__ = 'George Young'
__email__ = 'bioinformatics@lms.mrc.ac.uk'
__status__ = 'Production'
__license__ = 'MIT'

# argparse ####################################################################

parser = argparse.ArgumentParser(
    prog=__prog__,
    description='Generate pLDDT plots and PAE heatmaps from AlphaFold3 JSONs',
    epilog=f'{__prog__} processes the JSON files it finds using the `--glob` \
    search in the `target` directories and/or the `target` JSON files listed',
    formatter_class=RichHelpFormatter)
parser.add_argument(
    '-v', '--version',
    action='version', version=f'{__prog__} v{__version__} ({__status__})',
    help='show the program version and exit'
)
parser.add_argument(
    'target', type=Path, nargs='*', default=[Path()],
    help='search directory or JSON file path (default: current directory)'
)
parser.add_argument(
    '-R', '--recursive', action='store_true',
    help='recurse through directories'
)
parser.add_argument(
    '--noplddt', dest='plddt', action='store_false',
    help='don\'t produce pLDDT plots'
)
parser.add_argument(
    '--nopae', dest='pae', action='store_false',
    help='don\'t produce PAE plots'
)
parser.add_argument(
    '--glob', type=str, default='*confidences.json',
    help='JSON search glob (default: \'%(default)s\')'
)
parser.add_argument(
    '--output', type=Path,
    help='Directory to save the output plots (default: current directory)'
)

# functions ###################################################################

def plot_plddt(atom_plddts, atom_chain_ids, target, output_dir, glob_pattern):
    ''' Plot pLDDT data '''
    xlim = len(atom_plddts) + 1
    fig = plt.figure(figsize=(15, 5))
    ax = fig.gca()

    ax.add_patch(patches.Rectangle((1, 90), xlim, 10, color='green', alpha=0.2, label='Very High (90-100)'))
    ax.add_patch(patches.Rectangle((1, 70), xlim, 20, color='darkorange', alpha=0.2, label='High (70-90)'))
    ax.add_patch(patches.Rectangle((1, 50), xlim, 20, color='red', alpha=0.2, label='Low (50-70)'))
    ax.add_patch(patches.Rectangle((1, min(atom_plddts)), xlim, 50 - min(atom_plddts), color='grey', alpha=0.2, label='Very Low (<50)'))

    if len(chains := Counter(atom_chain_ids)) > 1:
        x = 1
        plt.axvline(x=x, color='grey', linestyle='--', alpha=0.5)
        ticks = []
        for chain_len in chains.values():
            ticks += [(x + chain_pos, str(chain_pos)) for chain_pos in range(chain_len) if chain_pos % 1000 == 0]
            plt.axvline(x := x + chain_len, color='grey', linestyle='--', alpha=0.5)
        plt.xticks([t[0] for t in ticks], labels=[t[1] for t in ticks])
        plt.xlabel('Atom (per chain)', fontsize=12)
    else:
        plt.xlabel('Atom', fontsize=12)

    plt.ylabel('pLDDT', fontsize=12)
    plt.title('Predicted Local Distance Difference Test (pLDDT)', fontsize=14)
    plt.grid(alpha=0.5)
    plt.plot(atom_plddts, color='black', marker='.', markersize=1, linewidth=0)

    plt.legend(
        title='Confidence Level', fontsize='small', bbox_to_anchor=(1.01, 1.0),
        loc='upper left'
    )
    plt.tight_layout()

    output_file = output_dir.joinpath(
        target.stem.rstrip(glob_pattern.replace('*', '')) + 'pLDDT.png'
    )
    plt.savefig(output_file)
    plt.close()


def plot_pae(pae, token_chain_ids, target, output_dir, glob_pattern):
    ''' Plot PAE heatmap '''
    plt.figure(figsize=(8, 8))
    plt.title('Predicted Aligned Error (PAE)', fontsize=14)
    plt.xlabel('Scored Residue', fontsize=12)
    plt.ylabel('Aligned Residue', fontsize=12)

    plt.imshow(np.array(pae), cmap='cividis', origin='lower')

    if len(chains := Counter(token_chain_ids)) > 1:
        xy = 0
        for v in list(chains.values())[:-1]:
            plt.axvline(x := xy + v, color='white', linestyle='--')
            plt.axhline(y=xy, color='white', linestyle='--')
            xy = x

    plt.colorbar(
        label='Expected Position Error (Ångströms)', orientation='horizontal',
        shrink=0.75, pad=0.075
    )
    plt.tight_layout()

    output_file = output_dir.joinpath(
        target.stem.rstrip(glob_pattern.replace('*', '')) + 'PAE.png'
    )
    plt.savefig(output_file)
    plt.close()

def process_json(target, output_dir, args):
    ''' Process and plot AlphaFold3 JSON '''
    with open(target) as f:
        data = json.load(f)

    if 'atom_chain_ids' not in data:
        return

    if args.plddt:
        plot_plddt(data['atom_plddts'], data['atom_chain_ids'], target, output_dir, args.glob)

    if args.pae:
        plot_pae(data['pae'], data['token_chain_ids'], target, output_dir, args.glob)

###############################################################################

if __name__ == '__main__':
    args = parser.parse_args()
    output_dir = args.output if args.output else Path.cwd()

    for target_path in args.target:
        if target_path.is_dir():
            paths = target_path.rglob(args.glob) if args.recursive else target_path.glob(args.glob)
            for path in paths:
                process_json(path, output_dir, args)
        else:
            process_json(target_path, output_dir, args)
