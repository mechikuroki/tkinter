#!/usr/bin/bash

while IFS= read -r line; do
	mv "$line" ~/tkinter/jugadores/
done < jugadores.txt
