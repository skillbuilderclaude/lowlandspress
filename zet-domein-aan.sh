#!/bin/bash
# Koppelt lowlandspress.com aan de GitHub-Pages-site zodra de DNS bij TransIP
# naar GitHub wijst. Tot die tijd draait de site op github.io.
set -e
cd "$(dirname "$0")"
GH_IPS="185.199.108.153 185.199.109.153 185.199.110.153 185.199.111.153"

wijst_naar_github() {
  local a; a=$(dig +short lowlandspress.com A 2>/dev/null)
  [ -z "$a" ] && return 1
  for ip in $a; do
    case " $GH_IPS " in *" $ip "*) return 0;; esac
  done
  return 1
}

if ! wijst_naar_github; then
  echo "DNS wijst nog niet naar GitHub (nu: $(dig +short lowlandspress.com A | tr '\n' ' '))"
  exit 1
fi

echo "DNS staat goed. Domein aankoppelen."
[ -f CNAME.wacht-op-dns ] && mv CNAME.wacht-op-dns CNAME || echo "lowlandspress.com" > CNAME
sed -i '' '/CNAME.wacht-op-dns/d' .gitignore 2>/dev/null || true
git add -A
git commit -q -m "Custom domain lowlandspress.com weer aangekoppeld" || true
git push -q origin HEAD
gh api -X PUT repos/skillbuilderclaude/lowlandspress/pages -f 'cname=lowlandspress.com' >/dev/null
sleep 20
gh api -X PUT repos/skillbuilderclaude/lowlandspress/pages -F 'https_enforced=true' >/dev/null 2>&1 || true
echo "Klaar. https://lowlandspress.com/ wordt binnen enkele minuten actief."
