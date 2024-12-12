#!/bin/bash

master_prompt=$(printf "Jesteś pomocnym asystentem programistycznym. Twoim zadaniem jest odpowiadać tylko przy pomocy kodu (jeżeli nie zostaniesz o to poproszony nie dodawaj komentarzy do kodu). Chcę twoje odpowiedzi bezpośrednio przekierowywać do programów bashowych, pythonowych oraz napisanych w języku C. Odpowiedź generuj na podstawie user inputu:\n")
user_input="$@"

prompt="${master_prompt} ###user input###\n${user_input}\n###"

out=$(llm prompt -m gpt-4o-mini "${prompt}")

# Filtracja wyjścia
filtered_output=$(echo "$out" | sed -E 's/```[a-zA-Z]*//g; s/```//g')
echo "$filtered_output"
