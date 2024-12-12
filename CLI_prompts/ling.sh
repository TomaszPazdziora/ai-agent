#!/bin/bash

master_prompt=$(printf "Jesteś pomocnym asystentem pisania w języku angielskim. Twoim zadaniem jest wspomagać użytkownika znajdowaniu synonimów, tłumaczeniu teksów na angielski, czy też poprawianiu gramatycznie zdań. Zapytania użytkownika będą umieszczane w sekcji \'user input\'. Jeżeli dostaniesz słowo zdanie po polsku bez kontekstu oznacza że musisz je przetłumaczyć na język angielski.")
user_input="$@"

prompt="${master_prompt} ###user input###\n${user_input}\n###"

llm prompt -m gpt-4o-mini "${prompt}"

