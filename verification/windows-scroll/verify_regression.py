#!/usr/bin/env python3
"""Isolated red/green check; run against the reviewed fix checkout."""
import os, subprocess, sys, tempfile
from pathlib import Path

RED = '332d5b66efcd0fdc622062f6370baab9d977e3d0'
GREEN = 'f1273c9ad3358181143a3e057cf126afdf7f0212'
repo = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
for revision in [RED, GREEN]:
    subprocess.run(['git', '-C', str(repo), 'cat-file', '-e', revision+'^{commit}'], check=True)
results = []
with tempfile.TemporaryDirectory(prefix='cua-scroll-repro-', dir=os.environ.get('CUA_REPRO_TMPDIR')) as folder:
    for label, revision, expected in [('red', RED, 101), ('green', GREEN, 0)]:
        tree = Path(folder)/label
        subprocess.run(['git','-C',str(repo),'worktree','add','--detach',str(tree),revision],check=True)
        try:
            command = ['cargo','test','--locked','--manifest-path',str(tree/'libs/cua-driver/rust/Cargo.toml'),'-p','platform-windows','--lib','scroll_coordinates','-j','2']
            run = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print(label.upper(), 'exit='+str(run.returncode), '\n'+run.stdout)
            assert run.returncode == expected, (label, run.returncode, expected)
            assert ('3 failed' if label == 'red' else '5 passed; 0 failed') in run.stdout
            results.append((label, run.returncode))
        finally:
            subprocess.run(['git','-C',str(repo),'worktree','remove',str(tree)],check=True)
print('PASS', results)
