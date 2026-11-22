// News-image entry for make.fun — "Sum up 21 November's world news in one image".
// The entry image is entry.png beside this file: a front page drawn in this
// session by draw.py (Python/PIL, DejaVu fonts, no network), dated Saturday
// 21 November 2026, with six verified stories of that day — Iran striking
// Bahrain, Mexico capturing 'El Chapo Isidro', the Kryvyi Rih missile strike,
// COP31 running past its deadline in Antalya, the Nasdaq AI sell-off, and the
// Brazil dengue breakthrough — plus an "also on Saturday" box.
// This program simply copies that image to the grader's output path, so both
// runs write exactly the same bytes. Node 22, standard library only.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
