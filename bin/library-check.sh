#!/bin/bash
for lib in lib{gmp,mpfr,mpc}.la; do
  echo $lib: $(if find /usr/lib* -name $lib|grep -q $lib;then :;else echo no;fi) found
done
unset lib
