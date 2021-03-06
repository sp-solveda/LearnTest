#!/bin/bash

set -v -x

printf "%04d" 12

# printf can assign value to a variable by "-v", instead of output.
printf -v NUM "%04d" 12

echo $NUM

# printf can print multiple lines, if given more input.
printf "%-6s:%4d\n" Tom 8 Jerry 16 Marry 128

printf "%-6s:%4d\n" Tom 8 Jerry 16 Marry


Fmt="
   |   |
 %1s | %1s | %1s
---+---+---
 %1s | %1s | %1s
---+---+---
   |   |
"
ttt=("" X "" "" O "" "" X "")
printf "$Fmt" "${ttt[@]}"

printf '%.0s-' {1..20}; echo
printf '%.0s=' {1..40}; echo
