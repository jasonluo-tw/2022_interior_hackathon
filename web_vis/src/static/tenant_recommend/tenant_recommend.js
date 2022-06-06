var mymap 
var vm
var card_over
var shop_list
var selectedCard = null
var root = location.protocol + '//' + location.host;

initVue()
initMap()

// Get shop_infomation
// Get query from URL
const queryString = window.location.search
const api_path = root + '/api/get_shop_info' + queryString
fetch(api_path,  {
    headers: {
        'Content-Type': 'application/json'
    },
    method: 'get'
}).then(response => response.json()).then(json => {
    vm['shop'] = json
    shop_list = json
    mymap.addPoints(json, {label: "${name}"})

}).catch(error => {
    console.log(error)
})

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

function PtClickFunction (e) {
    let card_index = e.layer.options.card_index
    document.querySelector("#card_"+card_index).scrollIntoView({
        behavior: 'smooth'
    })
    cardClick(card_index)
}


// Card reaction part
function cardClick (index) {
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
    let clicked_layer = mymap._select_change(clicked_name)
    // print clicked name
    console.log("Click", clicked_name, clicked_second, clicked_town)

    // geojson fetch
    geojson_load('district', clicked_town, pane_name='區')
    geojson_load('second_district', clicked_second, pane_name='二級')

    //detail & show detail
    vm.clicked_item = shop_list[index]
    let road_map = {0: '小巷', 1: '大路'}
    vm.clicked_item['小巷0/大路1'] = vm.clicked_item['小巷0/大路1']
    //console.log(vm.clicked_item)
    $("#bottom_block").css("height", 0)
    $("#bottom_block").css("padding-bottom", 0)
    $("#uplaod_wish").css("position", "absolute")
    $("#wish-img").css("position", "absolute")

    // fetch region information
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

    mymap.basemap.flyTo([lat, lon], 14)
    mymap._pt_click(clicked_layer, basemap_key_flag)

}

function cardOver (index) {
    // Get index and match the exact point on the map
    let clicked_name = shop_list[index]['name']
    let pt_layer = mymap._select_change(clicked_name)
    pt_layer.openTooltip()
    card_over = pt_layer
}

function cardLeave (index) {
    console.log('Card Leave', index)
    card_over.closeTooltip()
    card_over = undefined
}

// side bar
$(".close > p").click(() => {
    $(".info_bar").removeClass('open')
})

$("#close_detail").click(() => {
    $("#bottom_block").css("height", "100%")
    $("#bottom_block").css("padding-bottom", "100px")
    $("#uplaod_wish").css("position", "fixed")
    $("#wish-img").css("position", "fixed")
})