"use strict";

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function plot_pie_chart(dom_id, ydata) {
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
          enabled: false //format: '<b>{point.name}</b>: {point.percentage:.1f} %'

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
  var _Highcharts$chart;

  /*
    categories: ['0~5','5~10','15~20']
    data: [12, 13, 14, 15, 16, 18, 19, 20, 30...]
  */
  Highcharts.chart(dom_id, (_Highcharts$chart = {
    chart: {
      type: 'column'
    },
    title: {
      text: null
    },
    xAxis: {
      categories: categories,
      crosshair: false
    }
  }, _defineProperty(_Highcharts$chart, "xAxis", {
    title: {
      text: '年齡分佈'
    }
  }), _defineProperty(_Highcharts$chart, "yAxis", {
    min: 0,
    title: {
      text: '平均收入'
    }
  }), _defineProperty(_Highcharts$chart, "tooltip", {
    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
    pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' + '<td style="padding:0"><b>$NT:{point.y:.1f}</b></td></tr>',
    footerFormat: '</table>',
    shared: true,
    useHTML: true
  }), _defineProperty(_Highcharts$chart, "plotOptions", {
    column: {//pointPadding: 0.001,
      //borderWidth: 0
    }
  }), _defineProperty(_Highcharts$chart, "series", [{
    name: '收入',
    data: data,
    showInLegend: false
  }]), _Highcharts$chart));
}

function plot_line_chart(dom_id, data) {
  /*
    data: [1, 2, 3, 4]
  */
  Highcharts.chart(dom_id, {
    title: {
      text: null
    },
    yAxis: {
      title: {
        text: '租金'
      }
    },
    xAxis: {
      //TODO
      accessibility: {
        rangeDescription: 'Range: 2015 to 2019'
      }
    },
    //legend: {
    //  layout: 'vertical',
    //  align: 'right',
    //  verticalAlign: 'middle'
    //},
    plotOptions: {
      series: {
        label: {
          connectorAllowed: false
        },
        //TODO
        pointStart: 2015
      }
    },
    series: [{
      name: '店舖租金走勢',
      data: data
    }] //responsive: {
    //  rules: [{
    //    condition: {
    //      maxWidth: 500
    //    },
    //    chartOptions: {
    //      legend: {
    //        layout: 'horizontal',
    //        align: 'center',
    //        verticalAlign: 'bottom'
    //      }
    //    }
    //  }]
    //}

  });
}

function plot_horizontal_bar(dom_id, percent) {
  var fill_percent;
  var time_interval = 1000 / percent;

  if (time_interval > 60) {
    time_interval = 60;
  }

  if (percent == 100) {
    fill_percent = 101;
  } else {
    fill_percent = percent;
  }

  var bar_percent = 0;
  var text = 0;
  var timer = setInterval(function () {
    $("#".concat(dom_id, " > .percent_bar > .bar")).css("width", bar_percent + "%");
    $("#".concat(dom_id, " > .right_text")).text("".concat(text, "%"));
    bar_percent += 1;
    text += 1;

    if (bar_percent > fill_percent) {
      clearInterval(timer);
    }
  }, time_interval);
}

function plot_traffic_chart(dom_id, child_dom, total_nums) {
  var num = 0;
  var timer1 = setInterval(function () {
    $("#".concat(dom_id, " > ").concat(child_dom)).text("".concat(num));
    num += 1;

    if (num > total_nums) {
      clearInterval(timer1);
    }
  }, 30);
}