Highcharts.chart('container', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Cantidad de donaciones por tipo'
    },
    xAxis: {
        categories: ['Fruta', 'Verdura', 'Otro'],
        title: {
            text: "Tipo",
          },
    },
    yAxis: {
        title: {
            text: 'Cantidad'
        }
    },

    series: [{
          name: 'Cantidad',
          data: [],
        }
      ]
});

fetch("http://localhost:5000/get-don-stats-data")
  .then((response) => response.json())
  .then((data) => {
    let parsedData = [ data["fruta"], data["verdura"], data["otro"]];

    console.log(parsedData);

    const chart = Highcharts.charts.find(
      (chart) => chart && chart.renderTo.id === "container"
    );

    chart.update({
      series: [
        {
          data: parsedData,
        },
      ],
    });
  })
  .catch((error) => console.error("Error:", error));


  Highcharts.chart('container2', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Cantidad de pedidos por tipo'
    },
    xAxis: {
        categories: ['Fruta', 'Verdura', 'Otro'],
        title: {
            text: "Tipo",
          },
    },
    yAxis: {
        title: {
            text: 'Cantidad'
        }
    },

    series: [{
          name: 'Cantidad',
          data: [],
        }
      ]
});

fetch("http://localhost:5000/get-ped-stats-data")
  .then((response) => response.json())
  .then((data) => {
    let parsedData = [ data["fruta"], data["verdura"], data["otro"]];

    console.log(parsedData);

    const chart = Highcharts.charts.find(
      (chart) => chart && chart.renderTo.id === "container2"
    );

    chart.update({
      series: [
        {
          data: parsedData,
        },
      ],
    });
  })
  .catch((error) => console.error("Error:", error));