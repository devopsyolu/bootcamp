#!/usr/bin/env bash

read -p "Bir meyve giriniz (elma, armut, muz): " FRUIT

case "$FRUIT" in
    "elma")
        echo "Elma seçtiniz."
        ;;
    "armut")
        echo "Armut seçtiniz."
        ;;
    "muz")
        echo "Muz seçtiniz."
        ;;
    *)
        echo "Bilinmeyen meyve!"
        ;;
esac
