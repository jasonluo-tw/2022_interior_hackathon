var mymap 
var vm
var card_over
var shop_list
var selectedCard = null 
initVue()

//initMap()
//initial map
var mymap = new BaseMap('mapid', clat=25.09108, clon=121.5598)
mymap = mymap.addBaseMap(point_click=false).addMapboxMap()
mymap.pts_group.on("click", PtClickFunction)
// control location
L.control.zoom({
    position: 'topright'
}).addTo(mymap.basemap)

// Get shop_info mation
fetch('http://127.0.0.1:5000/api/get_shop_info',  {
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
    
    //detail & show detail
    vm.clicked_item = shop_list[index]
    console.log(vm.clicked_item)
    $("#bottom_block").css("height", 0)

    // fetch region information
    let api_url = 'http://127.0.0.1:5000/api/get_region_info?town='+clicked_town+'&second_dis='+clicked_second
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

    // print clicked name
    console.log("Click", clicked_name)
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
})
