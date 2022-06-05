function plot_pie_chart (dom_id, ydata) {
  /*
    input:
      ydata: [{name: "", y: ""}]
  */
  Highcharts.chart(dom_id, {
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
      },
      title: {
        //text: 'Browser market shares in January, 2018'
        text: null
      },
      tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
      },
      accessibility: {
        point: {
          valueSuffix: '%'
        }
      },
      plotOptions: {
        pie: {
          allowPointSelect: false,
          cursor: 'pointer',
          dataLabels: {
            enabled: false,
            //format: '<b>{point.name}</b>: {point.percentage:.1f} %'
          },
          showInLegend: true
        }
      },
      series: [{
        name: 'Brands',
        colorByPoint: true,
        innerSize: '40%',
        data: ydata
      }]
  });
}

function plot_bar_chart(dom_id, categories, data) {
  /*
    categories: ['0~5','5~10','15~20']
    data: [12, 13, 14, 15, 16, 18, 19, 20, 30...]
  */
  Highcharts.chart(dom_id, {
    chart: {
      type: 'column'
    },
    title: {
      text: null
    },
    xAxis: {
      categories: categories,
      crosshair: false,
      title: {
        text: '時段'
      }
    },
    yAxis: {
      min: 0,
      title: {
        text: '人數'
      }
    },
    tooltip: {
      headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
      pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
        '<td style="padding:0"><b>{point.y:.1f}人</b></td></tr>',
      footerFormat: '</table>',
      shared: true,
      useHTML: true
    },
    plotOptions: {
      column: {
        //pointPadding: 0.001,
        //borderWidth: 0
      }
    },
    series: [{
      name: '電信令',
      data: data,
      showInLegend: false
    }]
  });
}

function plot_line_chart(dom_id, data, ylabel) {
  /*
    data: [1, 2, 3, 4]
  */
  Highcharts.chart(dom_id, {
    title: {
      text: null
    },

    yAxis: {
      title: {
        text: ylabel
      }
    },
  
    xAxis: {
    },
    plotOptions: {
      series: {
        label: {
          connectorAllowed: false
        },
      }
    },
    series: data
  });
}

function plot_horizontal_bar(dom_id, percent) {
  let fill_percent
  let time_interval = 1000 / percent
  if(time_interval > 60){
    time_interval = 60
  }
  if(percent == 100){
    fill_percent = 101
  }else{
    fill_percent = percent
  }
  let bar_percent = 0
  let text = 0

  var timer = setInterval(function(){
    $(`#${dom_id} > .percent_bar > .bar`).css("width", bar_percent+"%")
    $(`#${dom_id} > .right_text`).text(`${text}%`)
    bar_percent += 1
    text += 1
    if(bar_percent > fill_percent) {
      clearInterval(timer)
    }
  }, time_interval)
}

function plot_traffic_nums(dom_id, child_dom, total_nums) {
  let num = 0
  let time_interval = 1000 / total_nums 
  var timer1 = setInterval(function(){
    $(`#${dom_id} > ${child_dom}`).text(`${num}`)
    num += 1
    if(num > total_nums){
      clearInterval(timer1)
    }
  }, time_interval)
}

function plot_shop_nums(dom_id, shop_data, shop_list) {
  const shop_node = document.getElementById(dom_id)
  shop_node.innerHTML = ""
  for(let i=0; i<shop_list.length; i++){
    let shop_name = shop_list[i]
    let shop_nums = shop_data[shop_name]
    let html_tag = `<span id="shop_${i}">${shop_name}: <span class="number">0</span></span>`
    $(`#${dom_id}`).append(html_tag)

    run_number(`#${dom_id} > span#shop_${i} > span.number`, shop_nums)
  }
}

function run_number(dom, total_nums) {
  let num = 0
  let time_interval = 1000 / total_nums
  var timer = setInterval(function() {
    $(dom).text(`${num}`)
    num += 1
    if(num > total_nums){
      clearInterval(timer)
    }
  }, time_interval)
}

//TODO Here should use fetch/axio to get the data and then called plot
function plot_all(region_json, wish_info) {
  // plot explorer
    // pie chart example
  plot_pie_chart('pie_chart', region_json['land_use'])
  // bar chart example
  plot_bar_chart('bar_chart', region_json['population']['x'], region_json['population']['value'])
  // line chart example
  plot_line_chart('line_chart', region_json['shop_price'], '租金')
  plot_line_chart('line_chart2', region_json['consume_index'], '消費熱度指數')
  // year bar 
  plot_horizontal_bar('year_1', region_json['age']['0-14歲人口數'])
  plot_horizontal_bar('year_2', region_json['age']['15-24歲人口數'])
  plot_horizontal_bar('year_3', region_json['age']['25-39歲人口數'])
  plot_horizontal_bar('year_4', region_json['age']['40-64歲人口數'])
  plot_horizontal_bar('year_5', region_json['age']['65歲以上人口數'])
  // shop amount
  //plot_shop_nums("shop_num", shop_info, ['餐廳餐館', '便利商店', '美容美髮服務', '日常用品零售', '飲料店業', '其他綜合零售'])
  // 餐廳餐館', '便利商店', '美容美髮服務', '日常用品零售', '飲料店業', '其他綜合零售'
  // traffic nums
  //plot_traffic_nums('text_chart', 'i.bus.icon > .icon_text', parseInt(shop_info['Bus_within_1km']))
  //plot_traffic_nums('text_chart', 'i.subway.icon > .icon_text', parseInt(shop_info['MRT_within_1km']))
}
