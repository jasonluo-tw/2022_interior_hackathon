// Wish list
/*
var shop_list = [
    {name: '王大明', type: '小店面', size: '15坪', price: ['5,000', '10,000'], rate: 93, latlon: [25.09108, 121.5598], town: '信義區'},
    {name: '三重王陽明', type: '潮店', size: '25坪', price: ['15,000', '20,000'], rate: 80, latlon: [25.09800, 121.5578], town: '松山區'},
    {name: 'Hubert', type: '好店面', size: '300坪', price: ['30,000', '40,000'], rate: 70, latlon: [25.05800, 121.5460], town: '中山區'},
    {name: '湖州杰倫', type: '店面', size: '15坪', price: ['25,000', '27,000'], rate: 50, latlon: [25.055, 121.560], town: '中正區'},
]
*/
var mymap, pts_group
var vm
var card_over
var shop_list
initVue()
initMap()

// test block
fetch('http://127.0.0.1:5000/get_shop_info',  {
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
            town: ''
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
    let lat = shop_list[index]['latitude']
    let lon = shop_list[index]['longitude']
    pt_layer = matchPts(clicked_name)
    //let pts_g = pts_group

    // Test fetch
    let api_url = 'http://127.0.0.1:5000/get_region_info?town='+clicked_town
    vm['town'] = clicked_town
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