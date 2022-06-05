function initMap() {
    mymap = new BaseMap('mapid', clat=25.09108, clon=121.5598)
    mymap = mymap.addBaseMap(point_click=false).addMapboxMap()
    if(PtClickFunction) {
        mymap.pts_group.on("click", PtClickFunction)
    }
    // control location
    L.control.zoom({
        position: 'topright'
    }).addTo(mymap.basemap)

    // Get shop area geojson
    fetch(root + '/api/get_geojson?type=shop_area', {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'get'
    }).then(response => response.json()).then(json => {
        let shop_area = (feature, layer) => {
            layer.bindPopup(feature.properties.Name, {closeButton: false, offset: L.point(0, -10)})
            layer.on('mouseclick', function() { layer.openPopup() })
            layer.on('mouseout', function() { layer.closePopup() })
        }
        mymap.addContourf(json, '商圈', 'area', shop_area, 'geojson', 'contourf')
    }).catch(error => {
        console.log(error, 'geojson, fetch_error')
    })
    //TODO
    // Get MRT
    // Get 
}

function geojson_load(type, name, pane_name, layer_name=null) {
    fetch(root + '/api/get_geojson?type='+type+'&name='+name, {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'get'
    }).then(response => response.json()).then(json => {
        let region_area = (feature, layer) => {
            //layer.bindPopup(feature.properties.Name, {closeButton: false, offset: L.point(0, -10)})
            //layer.on('mouseclick', function() { layer.openPopup() })
            //layer.on('mouseout', function() { layer.closePopup() })
        }
        if(layer_name){
            mymap.addContourf(json, pane_name, layer_name, 
                region_area, 'geojson', "contour", 250)

        }else{
            mymap.addContourf(json, pane_name, type, 
                region_area, 'geojson', "contour", 250)
        }
    })
}