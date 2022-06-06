var mymap, pts_group, PtClickFunction
var vm
var card_over
var wish_list 
var root = location.protocol + '//' + location.host;
initVue()
initMap()

// Get query from URL
const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
let api_path
if(urlParams.get('house_index')){
    api_path = root + '/api/calculate_similar?house_index='+urlParams.get('house_index')
}else if(urlParams.get('rental_price')){
    api_path = root + '/api/calculate_similar'+queryString
}
//api_path = root + '/api/calculate_similar?house_index='+urlParams.get('house_index')

fetch(api_path,  {
    headers: {
        'Content-Type': 'application/json'
    },
    method: 'get'
}).then(response => response.json()).then(json => {
    console.log(json)
    vm['wish_list'] = json['wish']
    wish_list = json['wish']
    if(json['target_shop'][0]['lonlat'] != 0){
        mymap.addPoints(json['target_shop'], {label: "${name}"})
        mymap.basemap.flyTo([json['target_shop'][0]['latitude'], json['target_shop'][0]['longitude']], 14)
    }
    plot_district(json['town'], json['town_geojson'])

}).catch(error => {
    console.log(error, 'fetch error')
})

function plot_district(town, town_geojson) {
    geojson_pts = []
    for(let i in town) {
        let district_name = town[i]
        geojson_load('district', district_name, district_name, district_name)
    }
    //
    let Classroomsamount = new L.geoJson(town_geojson, {
        pointToLayer: function(feature, latlng) {
            let cc = new L.CircleMarker([latlng.lat, latlng.lng], {radius: feature.properties.radius});
            cc.setStyle({ fillColor: '#99fdda', fillOpacity: 0.7, color: '#99fdda'})
            return cc
        },
        onEachFeature: function(feature, layer) {
            let text = L.tooltip({
                permanent: true,
                direction: 'center',
                className: 'text'
            })
            .setContent(feature.properties.text)
            .setLatLng(layer.getLatLng());
            text.addTo(mymap.basemap);
            
            //let text2 = L.tooltip({
            //    direction: 'top',
            //    className: 'text2'
            //})
            //.setContent(feature.properties.text)
            //.setLatLng(layer.getLatLng());
            //layer.bindTooltip(text2);
        }
    }).addTo(mymap.basemap)
}

function initVue() {
    vm = new Vue({
        el: "#app",
        data: {
            wish_list: [],
            town: '',
            clicked_item: {},
        },
        methods: {
            c_click: cardClick,
            c_over: cardOver,
            c_leave: cardLeave
        }
    })
}

var selectedCard = null 
function cardClick (index) {
    //TODO
    if(selectedCard) {
        document.getElementById(selectedCard).classList.remove("selectedCard")
    }
    document.getElementById("card_"+index).classList.add("selectedCard")
    selectedCard = "card_"+index
    
    $(".info_bar").addClass('open')
    let clicked_name = wish_list[index]['name']
    let clicked_town = wish_list[index]['town']
    //let clicked_second = wish_list[index]['二級']
    //let lat = wish_list[index]['latitude']
    //let lon = wish_list[index]['longitude']
    //pt_layer = matchPts(clicked_name)
    //let pts_g = pts_group
    
    //detail & show detail
    vm.clicked_item = wish_list[index]
    console.log(wish_list[index])
    $("#bottom_block").css("height", 0)
    $("#bottom_block").css("padding-bottom", 0)

    let api_url = root + '/api/get_region_info?town='+clicked_town
    fetch(api_url, {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'get'
    })
    .then(response => response.json())
    .then(json => {
        // plot explorer
        plot_all(json, wish_list[index])
    })
    .catch(error => {
        console.log(error)
    })

    //mymap.flyTo([lat, lon], 14)
    //ptClick(pt_layer)

    // print clicked name
    console.log(clicked_name)
}

function cardOver (index) {
    // Get index and match the exact point on the map
    let clicked_name = wish_list[index]['name']
    //pt_layer = matchPts(clicked_name)
    //pt_layer.openTooltip()
    //card_over = pt_layer
}

function cardLeave (index) {
    //pt_layer.closeTooltip()
    //card_over = undefined
}

// $(".card").click(() => {
//   $(".info_bar").addClass('open')
//   console.log(this.Vue)
// })

$(".close > p").click(() => {
    $(".info_bar").removeClass('open')
})

$("#close_detail").click(() => {
    $("#bottom_block").css("height", "100%")
    $("#bottom_block").css("padding-bottom", "100px")
})

function PtClickFunction (e) {
    console.log('pt click function')
}