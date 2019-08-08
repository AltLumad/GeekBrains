#!/bin/bash


mysqldump -uroot -pQwerty123! --where="true limit 100" mysql help_keyword > dump.sql
