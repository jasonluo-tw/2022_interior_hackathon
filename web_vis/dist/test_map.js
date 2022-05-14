// Wish list
var wish_list = [
    {name: '王大明', type: '小店面', size: '15坪', price: ['5,000', '10,000'], rate: 93, latlon: [25.09108, 121.5598]},
    {name: '三重王陽明', type: '潮店', size: '25坪', price: ['15,000', '20,000'], rate: 80, latlon: [25.09800, 121.5578]},
    {name: 'Hubert', type: '好店面', size: '300坪', price: ['30,000', '40,000'], rate: 70, latlon: [25.05800, 121.5460]},
    {name: '湖州杰倫', type: '店面', size: '15坪', price: ['25,000', '27,000'], rate: 50, latlon: [25.055, 121.560]},
]

var vm = new Vue({
    el: "#app",
    data: {
        wish: wish_list
    },
    methods: {
        c_click: card_click,
        c_over: card_over,
        c_leave: card_leave
    }
})

// Make map
var mymap = L.map('mapid', {zoomControl: false}).setView([25.09108, 121.5598], 13)
var pts_group = L.featureGroup().addTo(mymap)

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

for(let i in wish_list) {
    let lat = wish_list[i]['latlon'][0]
    let lon = wish_list[i]['latlon'][1]
    let name = wish_list[i]['name']
    console.log(lat, lon)

    L.circleMarker([lat, lon], {
            className: 'circle_transition',
            radius: 3.5,
            color: "white",
            weight: 1,
            fillColor: "red",
            fillOpacity: 1.0,
            name: name,
            //value: value
        }
    ).bindTooltip(name, {direction: 'top'})//, {pane: tooltip_pane})
 .addTo(pts_group)
}

function match_pts (clicked_name) {
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

function card_click (index) {
    $(".info_bar").addClass('open')
    let clicked_name = wish_list[index]['name']
    let latlng = wish_list[index]['latlon']
    pt_layer = match_pts(clicked_name)
    let pts_g = pts_group

    mymap.flyTo(latlng, 14)
    // plot explorer
    //TODO Here should use fetch/axio to get the data and then called plot
    // pie chart example
    var pie_data = [
        {name: 'A', y: 10},
        {name: 'B', y: 30},
        {name: 'C', y: 50},
        {name: 'D', y: 10},
    ]
    plot_pie_chart('pie_chart', pie_data)
    // bar chart example
    var categories = ['0~5', '5~10', '10~15', '15~20', '20~25']
    var income = [300000, 400000, 500000, 300000, 200000]
    plot_bar_chart('bar_chart', categories, income)
    // line chart example
    var rental_price = [1000, 3000, 5000, 100000]
    plot_line_chart('line_chart', rental_price)
    // year bar 
    plot_horizontal_bar('year_1', 50)
    plot_horizontal_bar('year_2', 40)
    plot_horizontal_bar('year_3', 10)
    // traffic nums
    plot_traffic_chart('text_chart', 'i.bus.icon > .icon_text', 10)
    plot_traffic_chart('text_chart', 'i.subway.icon > .icon_text', 2)
    // print clicked name
    console.log(clicked_name)
}

var card_over
function card_over (index) {
    // Get index and match the exact point on the map
    let clicked_name = wish_list[index]['name']
    pt_layer = match_pts(clicked_name)
    pt_layer.openTooltip()
    card_over = pt_layer
}

function card_leave (index) {
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