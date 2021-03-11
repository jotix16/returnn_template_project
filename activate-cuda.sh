
# In case anything is missing.
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/u/zeyer/tools/glibc217

# Needed for Theano.
# Prefer CUDA 7.0 if available. Needed for new GPUs.
# If Sprint also uses CUDA in the same proc, it needs to use the same CUDA version!
# See https://groups.google.com/forum/#!topic/theano-users/Pu4YKlZKwm4
#source /u/zeyer/py-envs/py2-theano-new/bin/activate
#source /work/tools/asr/python/3.7.1_tf_1.14-generic+cuda10.1/bin/activate
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/atlas-base/

export CUDA_HOME=/usr/local/cuda-10.1
#export LD_LIBRARY_PATH=/u/kulikov/.linuxbrew/Cellar/glibc/2.19/lib64:$LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=/u/kulikov/.linuxbrew/lib64:$LD_LIBRARY_PATH
# need CUDA 6.5 in path for some old stuff. but make CUDA 8 come first in path
#export LD_LIBRARY_PATH=/usr/local/cuda-6.5.19/lib64:$LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=/usr/local/cuda-8.0/extras/CUPTI/lib64:$LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64:$LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=/usr/local/cudnn-8.0-v5.1/lib64:$LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=/usr/local/cudnn-8.0-v6.0/lib64:$LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=/usr/local/cuda-7.5/lib64:$LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=/usr/local/cuda-7.0/lib64:$LD_LIBRARY_PATH
#export PATH=/usr/local/cuda-8.0/bin:$PATH
#export PATH=/usr/local/cuda-7.5/bin:$PATH
#export PATH=/usr/local/cuda-7.0/bin:$PATH
#export PATH=/usr/local/cuda-6.5.19/bin:$PATH
export PATH=/usr/local/cuda-10.1/bin/:$PATH

# CUDA 10.1 with cudaNN 7.6
# TF also requires some 10.0 libs (libcufft, libcudart...(
# TF 1.15 is installed as pip --user
#export LD_LIBRARY_PATH=/usr/local/cuda-10.1_new/lib64/:/usr/local/cudnn-10.1-v7.6/lib64:/usr/lib/atlas-base/:/usr/local/cuda-10.0/lib64/:/usr/local/cuda-10.1_new/nsight-systems-2019.3.7.5/Target-x86_64/x86_64

# with TF 1.14
export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64/:/usr/local/cudnn-10.1-v7.6/lib64:/usr/lib/atlas-base/
#:/usr/local/cuda-10.0/lib64/
#:/usr/local/cuda-10.1_new/nsight-systems-2019.3.7.5/Target-x86_64/x86_64

# cuDNN
#CUDNN_PATH=/u/zeyer/tools/cudnn_v3
#export LD_LIBRARY_PATH=$CUDNN_PATH:$LD_LIBRARY_PATH
#export CPATH=$CUDNN_PATH:$CPATH
#export LIBRARY_PATH=$CUDNN_PATH:$LIBRARY_PATH


# For profiling:
# Debugging http://stackoverflow.com/questions/28221191/theano-cuda-error-an-illegal-memory-access-was-encountered
#export THEANO_FLAGS="$THEANO_FLAGS,profile=True,profiling.time_thunks=1"
#export CUDA_LAUNCH_BLOCKING=1 # Makes all GPU ops synchronized. They are async by default.

# Newer GCC. Old GCC is buggy and breaks Theano on new CPUs.
# https://groups.google.com/forum/#!msg/theano-users/iNNxMqDIJjY/KSbvXlGOV9AJ
# https://github.com/Theano/Theano/issues/1980
#export PATH=/work/speech/tools/gcc-4.8.0/x64/gcc-4.8.0/bin:$PATH
#export LD_LIBRARY_PATH=/work/speech/tools/gcc-4.8.0/x64/gcc-4.8.0/lib64:/work/speech/tools/gcc-4.8.0/x64/cloog-0.18.0/lib:/work/speech/tools/gcc-4.8.0/x64/gmp-5.1.2/lib:/work/speech/tools/gcc-4.8.0/x64/isl-0.11.1/lib:/work/speech/tools/gcc-4.8.0/x64/mpc-1.0.1/lib:/work/speech/tools/gcc-4.8.0/x64/mpfr-3.1.2/lib:$LD_LIBRARY_PATH
#export LIBRARY_PATH=/work/speech/tools/gcc-4.8.0/x64/gcc-4.8.0/lib/gcc/x86_64-unknown-linux-gnu/4.8.0:$LIBRARY_PATH
#export LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LIBRARY_PATH


# maybe: (http://stackoverflow.com/questions/15639779/why-does-multiprocessing-use-only-a-single-core-after-i-import-numpy)
export OPENBLAS_MAIN_FREE=1
export GOTOBLAS_MAIN_FREE=1


# using this may cause hangs (don't know why)
# maybe num_threads in SGE is not read out correctly -> interop_threads in TF not set correctly?
#export OMP_NUM_THREADS=6


# For CRNN/RETURNN, some debugging options:
#export DEBUG_SIGNAL_HANDLER=1
#export DEBUG_WARN_WITH_TRACEBACK=1
#export DEBUG_TF_BETTER_REPR=1


# not actually used but might still be imported
export THEANO_FLAGS="base_compiledir=/var/tmp/$LOGNAME/theano/,compiledir_format=compiledir_%(platform)s-%(processor)s-%(python_version)s-%(python_bitwidth)s-%(hostname)s--gpu"

# https://github.com/h5py/h5py/issues/1082
export HDF5_USE_FILE_LOCKING=FALSE
