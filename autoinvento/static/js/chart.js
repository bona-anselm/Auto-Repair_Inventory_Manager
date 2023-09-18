/* eslint-disable jest/require-hook */
/* eslint-disable no-undef */
const ctx = document.getElementById('myChart');

const myChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: [], // Populate this with user names
    datasets: [{
      data: [],

      // Change these colours to customize the chart
      backgroundColor: ['#ff6361', '#bc5090', '#58508d', '#ffa600', '#003f5c'],
    }],
  },
  options: {
    legend: { display: false },
    title: {
      display: true,
      text: 'Total Quantity',
    },
    scales: {
      xAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Mechanics',
        },
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Quantity',
        },
        ticks: {
          beginAtZero: true, // Ensure the scale starts from zero
          min: 0, // Set the minimum value to zero
        },
      }],
    },
  },
});

// Function to fetch data from the API and update the chart
function updateChart() {
  fetch('/api/user-inventory-usage')
    .then((response) => response.json())
    .then((data) => {
      myChart.data.labels = data.map((item) => item.username);
      myChart.data.datasets[0].data = data.map((item) => item.total_quantity);
      myChart.update();
    })
    .catch((error) => {
      console.error('Error fetching data:', error);
    });
}

// Initial chart update
updateChart();

// Script for Supply Chart

/* eslint-disable no-undef */
const ctx1 = document.getElementById('supplyChart');

const supplyChart = new Chart(ctx1, {
  type: 'bar',
  data: {
    labels: [''],
    datasets: [{
      data: [],

      // Change these colours to customize the chart
      backgroundColor: ['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600'],
    }],
  },
  options: {
    legend: { display: false },
    title: {
      display: true,
      text: 'Total Quantity',
    },
    scales: {
      xAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Supplier',
        },
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Quantity',
        },
        ticks: {
          beginAtZero: true, // Ensure the scale starts from zero
          min: 0, // Set the minimum value to zero
        },
      }],
    },
  },
});

// Function to fetch data from the API and update the chart
function updateSupplyChart() {
  // eslint-disable-next-line no-undef
  fetch('/api/inventory-data')
    .then((response) => response.json())
    .then((data) => {
      supplyChart.data.labels = data.map((item) => item.supplier);
      supplyChart.data.datasets[0].data = data.map((item) => item.total_quantity);
      supplyChart.update();
    })
    .catch((error) => {
      console.error('Error fetching data:', error);
    });
}

// Initial chart update
// eslint-disable-next-line jest/require-hook
updateSupplyChart();
