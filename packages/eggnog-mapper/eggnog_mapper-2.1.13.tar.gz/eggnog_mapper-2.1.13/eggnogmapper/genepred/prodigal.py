##
## CPCantalapiedra 2020

import gzip
from os.path import isfile
from os.path import join as pjoin
from os.path import isdir as pisdir
import shutil
import subprocess
from sys import stderr as sys_stderr
from tempfile import mkdtemp, NamedTemporaryFile

from ..emapperException import EmapperException
from ..common import PRODIGAL, ITYPE_GENOME, ITYPE_META
from ..utils import colorify

# This class handles prediction of genes
# using Prodigal v2
class ProdigalPredictor:

    temp_dir = None
    pmode = None
    cpu = None

    trans_table = None
    training_genome = training_file = None
    
    outdir = None # dir with prodigal out files
    outgff = outprots = outcds = outorfs = None # prodigal out files

    PMODE_SINGLE = "single"
    PMODE_META = "meta"
    
    
    def __init__(self, args):

        if args.itype == ITYPE_GENOME:
            self.pmode = self.PMODE_SINGLE # or self.pmode = ""
        elif args.itype == ITYPE_META:
            self.pmode = self.PMODE_META
        else:
            raise EmapperException(f"Unsupported input type {args.itype} for ProdigalPredictor")
        self.cpu = args.cpu

        self.trans_table = args.trans_table
        self.training_genome = args.training_genome
        self.training_file = args.training_file
        
        self.temp_dir = args.temp_dir
        
        return

    def predict(self, in_file):
        if not PRODIGAL:
            raise EmapperException("%s command not found in path" % (PRODIGAL))

        self.outdir = mkdtemp(prefix='emappertmp_prod_', dir=self.temp_dir)
        try:
            # Training: run only if the training file does NOT exist
            if self.training_genome is not None and self.training_file is not None:
                if isfile(self.training_file):
                    print(colorify(f'Warning: --training_file {self.training_file} already exists. '
                                   f'Training will be skipped, and prediction will be run using the existing training file.', 'red'))                                    
                else:
                    cmd = self.run_training(self.training_genome, self.training_file)

            # Gene prediction
            cmd = self.run_prodigal(in_file, self.outdir)

        except Exception as e:
            raise e
        # finally:
        #     shutil.rmtree(tempdir)
        return

    def clear(self):
        if self.outdir is not None and pisdir(self.outdir):
            try:
                shutil.rmtree(self.outdir)
            except OSError as err:
                print(f"Warning: OS error while removing {self.outdir}", file = sys_stderr)
                print(f"OS error: {err}", file = sys_stderr)
        return

    def run_training(self, in_file, training_file):        
            
        cmd = (
            f'{PRODIGAL} -i \'{in_file}\' -t \'{training_file}\''
        )

        if self.trans_table is not None:
            cmd += f' -g {self.trans_table}'

        print(colorify('  '+cmd, 'yellow'))
        try:
            completed_process = subprocess.run(cmd, capture_output=True, check=True, shell=True)
        except subprocess.CalledProcessError as cpe:
            raise EmapperException("Error running prodigal: "+cpe.stderr.decode("utf-8").strip().split("\n")[-1])

        return cmd


    #
    def run_prodigal(self, in_file, outdir):

        # Prodigal doesnt handle gzipped files
        # so if the input file it is a .gz one
        # uncompress it first
        if in_file.endswith(".gz"):
            decomp_fn = pjoin(self.outdir, in_file+'.decomp')
            with gzip.open(in_file, 'rb') as f_in:
                with open(decomp_fn, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            in_file = decomp_fn
        
        self.outgff = pjoin(outdir, "output.gff")
        self.outprots = pjoin(outdir, "output.faa")
        self.outcds = pjoin(outdir, "output.fna")
        self.outorfs = pjoin(outdir, "output.orfs")
        cmd = (
            f'{PRODIGAL} -i \'{in_file}\' -p {self.pmode} '
            f'-o \'{self.outgff}\' -f gff '
            f'-a \'{self.outprots}\' -d \'{self.outcds}\' '
            f'-s \'{self.outorfs}\''
        )

        if self.trans_table is not None:
            if self.pmode == self.PMODE_META:
                print(colorify(f'Warning: --trans_table (-g Prodigal option) '
                               f'is ignored by Prodigal when using -p {self.PMODE_META}', 'red'))                
            cmd += f' -g {self.trans_table}'

        if self.training_file is not None and isfile(self.training_file):
            if self.pmode == self.PMODE_META:
                print(colorify(f'Warning: Ignoring --training_file, because Prodigal does not allow training for -p {self.PMODE_META} ', 'red'))                
            else:
                cmd += f' -t \'{self.training_file}\''

        print(colorify('  '+cmd, 'yellow'))
        try:
            completed_process = subprocess.run(cmd, capture_output=True, check=True, shell=True)
        except subprocess.CalledProcessError as cpe:
            raise EmapperException("Error running prodigal: "+cpe.stderr.decode("utf-8").strip().split("\n")[-1])

        return cmd

## END
