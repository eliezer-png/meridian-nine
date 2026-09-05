#!/bin/bash
W=/Users/matt/meridian-nine
gen(){ i=$1
  codex exec -C "$W" -s workspace-write --skip-git-repo-check \
    'Use the image generation tool ($imagegen) to generate: '"$(cat "$W/still_$i.txt")"' Wide 3:2 landscape, high resolution. Save it as ./stills/still_'"$i"'.png. Do not do anything else.' \
    > "$W/stills/log_$i.txt" 2>&1 < /dev/null
}
for b in "1 2 3" "4 5 6"; do
  for i in $b; do gen "$i" & done
  wait
done
echo DONE
