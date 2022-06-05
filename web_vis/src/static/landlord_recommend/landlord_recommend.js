var mymap, pts_group
var vm
var card_over
var shop_list
var root = location.protocol + '//' + location.host;
initVue()
initMap()

// Get query from URL
const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
//console.log(urlParams.get('house_index'))

const api_path = root + '/api/calculate_similar?house_index='+urlParams.get('house_index')
fetch(api_path,  {
    headers: {
        'Content-Type': 'application/json'
    },
    method: 'get'
}).then(response => response.json()).then(json => {
    vm['shop'] = json
    shop_list = json
    addPts(json)

}).catch(error => {
    console.log(error)
})
// end of test block

function initVue() {
    vm = new Vue({
        el: "#app",
        data: {
            shop: [],
            town: '',
            second_dis: '',
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
function initMap() {
    // Make map
    mymap = L.map('mapid', {zoomControl: false}).setView([25.09108, 121.5598], 13)
    pts_group = L.featureGroup().addTo(mymap)
    pts_group.on("click", function(e){
        let card_index = e.layer.options.card_index
        //location.href = "#card_"+card_index
        document.querySelector("#card_"+card_index).scrollIntoView({
            behavior: 'smooth'
        })
        cardClick(card_index)
    })

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        //id: 'mapbox/streets-v11',
        id: 'mapbox/light-v10',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiamFzb25sdW8iLCJhIjoiY2wycnAycnFyMDV2NTNkbnJiZ2s2cDZ2eCJ9.GrhXfnCmF3Mgsna8-8tBOA'
    }).addTo(mymap)

    L.control.zoom({
        position: 'topright'
    }).addTo(mymap);

}

var clicking_pts = []
function ptClick(clickedCircle) {
    //TODO: unclicked other pts
    if(clicking_pts.length > 0) {
        for(let i in clicking_pts){
            clicking_pts[i][0].setStyle({fillColor: clicking_pts[i][1]})
            clicking_pts[i][0].setRadius(6)
        }
        clicking_pts = []
    }

    //let name = clickedCircle.options.name
    let card_index  = clickedCircle.options.card_index
    clicking_pts.push([clickedCircle, clickedCircle.options.fillColor])

    // after clicking, the color and radius of the point change
    clickedCircle.setStyle({fillColor: 'red'})
    clickedCircle.setRadius(8)
    // custom clicking function
    //if(!from_card) {
    //    cardClick(card_index)
    //}
}

function addPts(pts_list) {
    for(let i in pts_list) {
        let lat = pts_list[i]['latitude']
        let lon = pts_list[i]['longitude']
        let name = pts_list[i]['name']

        L.circleMarker([lat, lon], {
                className: 'circle_transition',
                radius: 6,
                color: "white",
                weight: 1,
                fillColor: "gray",
                fillOpacity: 1.0,
                name: name,
                card_index: i
                //value: value
            }
        ).bindTooltip(name, {direction: 'top'})//, {pane: tooltip_pane})
     .addTo(pts_group)
    }
}

function matchPts(clicked_name) {
    let pts_g = pts_group
    for(i in pts_g._layers){
        if(pts_g._layers[i].options.name == clicked_name){
            let lng = pts_g._layers[i]._latlng['lng']
            let lat = pts_g._layers[i]._latlng['lat']
            //this._pt_click(pts_g._layers[i], basemap_key_flag)
            //mymap.flyTo([lat,lng], 14)
            //console.log(lng, lat)
            break
        }
    }

    return pts_g._layers[i]
}

function cardClick (index) {
    //TODO
    if(selectedCard) {
        document.getElementById(selectedCard).classList.remove("selectedCard")
    }
    document.getElementById("card_"+index).classList.add("selectedCard")
    selectedCard = "card_"+index
    
    $(".info_bar").addClass('open')
    let clicked_name = shop_list[index]['name']
    let clicked_town = shop_list[index]['town']
    let clicked_second = shop_list[index]['二級']
    let lat = shop_list[index]['latitude']
    let lon = shop_list[index]['longitude']
    pt_layer = matchPts(clicked_name)
    //let pts_g = pts_group
    
    //detail & show detail
    vm.clicked_item = shop_list[index]
    $("#bottom_block").css("height", 0)

    // Test fetch
    let api_url = root + '/api/get_region_info?town='+clicked_town+'&second_dis='+clicked_second
    vm['town'] = clicked_town
    vm['second_dis'] = clicked_second
    fetch(api_url, {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'get'
    })
    .then(response => response.json())
    .then(json => {
        // plot explorer
        plot_all(json, shop_list[index])
    })
    .catch(error => {
        console.log(error)
    })

    mymap.flyTo([lat, lon], 14)
    ptClick(pt_layer)

    // print clicked name
    console.log(clicked_name)
}

function cardOver (index) {
    // Get index and match the exact point on the map
    let clicked_name = shop_list[index]['name']
    pt_layer = matchPts(clicked_name)
    pt_layer.openTooltip()
    card_over = pt_layer
}

function cardLeave (index) {
    pt_layer.closeTooltip()
    card_over = undefined
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
})
