// node align_cli.js notes.json lyrics.txt  -> aligned json on stdout
const A=require('../app/align.js'),fs=require('fs');
const notes=JSON.parse(fs.readFileSync(process.argv[2]));const lines=fs.readFileSync(process.argv[3],'utf8').split('\n').map(s=>s.trim()).filter(Boolean);
process.stdout.write(JSON.stringify(A.alignLyrics(lines,notes),null,1));
