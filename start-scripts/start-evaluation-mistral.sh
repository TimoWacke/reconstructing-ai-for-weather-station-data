#!/usr/bin/env bash

#SBATCH -J JohannesMeuer
#SBATCH -p gpu
#SBATCH -A bb1152
#SBATCH -n 1
#SBATCH --cpus-per-task=64
#SBATCH --time=12:00:00
#SBATCH --mem=256G
#SBATCH --nodelist=mg207

module load cuda/10.0.130
module load singularity/3.6.1-gcc-9.1.0
module load cdo

singularity run --bind /work/bb1152/k204233/ --nv /work/bb1152/k204233/climatereconstructionAI/torch_img_mistral.sif \
 python /work/bb1152/k204233/climatereconstructionAI/climatereconstructionAI/train_and_evaluate/evaluate.py \
 --device cuda --image-size 72 --pooling-layers 0 --encoding-layers 3 --data-types pr \
 --img-names tas_20cr_RECONSTRUCT_187001-200512.h5 --mask-names single_radar_fail.h5 \
 --data-root-dir /work/bb1152/k204233/climatereconstructionAI/data/radolan-complete-scaled/ \
 --mask-dir /work/bb1152/k204233/climatereconstructionAI/climatereconstructionAI/masks/ \
 --snapshot-dir /work/bb1152/k204233/climatereconstructionAI/climatereconstructionAI/snapshots/temperature/cmip/ckpt/1000000.pth \
 --evaluation-dirs evaluation/precipitation/radolan-single-radar-fail/ \
 --lstm-steps 0 \
 --partitions 1177 \
 --create-report \
 --eval-names Simple,Prev-Next,LSTM \
 --create-report \
 --mask-zero 0.1 \
# --infill infill \
# --create-images 2017-07-12-14:00,2017-07-12-14:00 \
# --create-video \
