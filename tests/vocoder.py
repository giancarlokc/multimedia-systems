from __future__ import division, print_function
import os
import sys
from shutil import rmtree
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import soundfile as sf
import pyworld as pw
matplotlib.use('Agg')


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--frame_period", type=float, default=5.0)
parser.add_argument("-s", "--speed", type=int, default=1)
parser.add_argument("-i", "--input", type=str)


EPSILON = 1e-8


def save_image(filename, figlist, log=True):
    n = len(figlist)
    # peek into instances
    f = figlist[0]
    if len(f.shape) == 1:
        plt.figure()
        for i, f in enumerate(figlist):
            plt.subplot(n, 1, i+1)
            if len(f.shape) == 1:
                plt.plot(f)
                plt.xlim([0, len(f)])
    elif len(f.shape) == 2:
        plt.figure()
        for i, f in enumerate(figlist):
            plt.subplot(n, 1, i+1)
            if log:
                x = np.log(f + EPSILON)
            else:
                x = f + EPSILON
            plt.imshow(x.T, origin='lower', interpolation='none', aspect='auto', extent=(0, x.shape[0], 0, x.shape[1]))
    else:
        raise ValueError('Input dimension must < 3.')
    plt.savefig(filename)


def main(args):
    if os.path.isdir('test'):
        rmtree('test')
    os.mkdir('test')

    # Read speech sample
    x, fs = sf.read(args.input)

    # 1. A convenient way
    f0, sp, ap = pw.wav2world(x, fs)    # use default options
    y = pw.synthesize(f0, sp, ap, fs, pw.default_frame_period)

    # 2. Step by step
    # 2-1 Without F0 refinement
    _f0, t = pw.dio(x, fs, f0_floor=50.0, f0_ceil=600.0,
                    channels_in_octave=2,
                    frame_period=args.frame_period,
                    speed=args.speed)
    _sp = pw.cheaptrick(x, _f0, t, fs)
    _ap = pw.d4c(x, _f0, t, fs)
    _y = pw.synthesize(_f0, _sp, _ap, fs, args.frame_period)
    sf.write('test/y_without_f0_refinement.wav', _y, fs)

    # 2-2 DIO with F0 refinement (using Stonemask)
    f0 = pw.stonemask(x, _f0, t, fs)
    sp = pw.cheaptrick(x, f0, t, fs)
    ap = pw.d4c(x, f0, t, fs)
    y = pw.synthesize(f0, sp, ap, fs, args.frame_period)
    sf.write('test/y_with_f0_refinement.wav', y, fs)

    # 2-3 Harvest with F0 refinement (using Stonemask)
    _f0_h, t_h = pw.harvest(x, fs)
    f0_h = pw.stonemask(x, _f0_h, t_h, fs)
    sp_h = pw.cheaptrick(x, f0_h, t_h, fs)
    ap_h = pw.d4c(x, f0_h, t_h, fs)
    y_h = pw.synthesize(f0_h, sp_h, ap_h, fs, pw.default_frame_period)
    sf.write('test/y_harvest_with_f0_refinement.wav', y_h, fs)

    # Comparison
    save_image('test/wavform.png', [x, _y, y])
    save_image('test/sp.png', [_sp, sp])
    save_image('test/ap.png', [_ap, ap], log=False)
    save_image('test/f0.png', [_f0, f0])


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
