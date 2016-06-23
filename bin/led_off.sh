#!/bin/bash
touch /tmp/LED_OFF.txt
mail -s "LED_OFF" "matthew.allen@fmcti.com" < /tmp/LED_OFF.txt
exit 0
