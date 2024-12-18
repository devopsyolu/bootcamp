#!/usr/bin/env bash

VAR=$VAR

# IF / ELIF / ELSE Örneği
if [[ $VAR -gt 10 ]]; then
    echo "VAR=$VAR, 10'dan daha büyük."
elif [[ $VAR -eq 10 ]]; then
    echo "VAR=$VAR, 10'a eşit."
else
    echo "VAR=$VAR, 10'dan küçük."
fi
