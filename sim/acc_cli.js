// node acc_cli.js notes.json -> ACC.arrange output + auto-intro (one 92-BPM bar of the first chord, ending exactly at the first melody note)
const ACC=require('../app/accompcore.js'),fs=require('fs');const notes=JSON.parse(fs.readFileSync(process.argv[2]));
const r=ACC.arrange(notes);const bar=4*60/ACC.BPM,first=notes[0].start;const melody_start=Math.max(0,bar-first);
process.stdout.write(JSON.stringify({bar,first,melody_start,introStart:first+melody_start-bar,firstChord:r.prog[0],acc:r.acc,shift:r.shift,keyName:r.keyName}));
