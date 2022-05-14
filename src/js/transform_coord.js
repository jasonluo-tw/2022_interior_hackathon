const proj4 = require('proj4')
const fs = require('fs')
// define EPSG 3821
proj4.defs("EPSG:3821", "+title=經緯度：TWD67 +proj=longlat  +towgs84=-752,-358,-179,-.0000011698,.0000018398,.0000009822,.00002329 +ellps=aust_SA +units=度 +no_defs");
proj4.defs("EPSG:3828","+proj=tmerc +lat_0=0 +lon_0=121 +k=0.9999 +x_0=250000 +y_0=0 +ellps=aust_SA +units=m +no_defs");


// read file
var data = fs.readFileSync('../../tbl/TWD67.csv', 'utf-8');

let output = ""
var rows = data.split('\n')
for(let i=1; i<rows.length-1; i++){
    let items = rows[i].split(',');
    let X   = parseFloat(items[1]);
    let Y   = parseFloat(items[2]);
    const out = proj4("EPSG:3828", "WGS84", [X, Y]); // out [lon, lat]
    let new_row = rows[i] + ',' + out[0] + ',' + out[1] + '\n';
    output += new_row
    console.log(out[0], out[1])
}

fs.writeFileSync('WGS84.csv', output)
