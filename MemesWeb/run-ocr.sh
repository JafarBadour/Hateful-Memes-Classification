#!/bin/bash

for i in {0..25}
do
  echo processing $i
  function ocr_i {
  python get-ocr-images.py $i;
  }
  ocr_i  &
done
