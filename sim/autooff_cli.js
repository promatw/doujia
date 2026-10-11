const A=require('../app/align.js'),fs=require('fs');const notes=JSON.parse(fs.readFileSync(process.argv[2]));
const x=new Float32Array(new Uint8Array(fs.readFileSync(process.argv[3])).buffer);console.log(A.estimateOffset(x,22050,notes));
