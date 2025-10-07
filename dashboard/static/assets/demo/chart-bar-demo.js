// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
var ctx = document.getElementById("myBarChart");
fetch("/experiments/all_duration").then(response => {
    if (!response.ok) {
        alert("Error in console")
        throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();
}).then(data => {

    labels = []
    vals = []
    for (const [key, value] of Object.entries(data)) {
        labels.push(key)
        vals.push(value/ 60)

    }

    var myLineChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: "Recorded Minutes in day",
                backgroundColor: "rgba(2,117,216,1)",
                borderColor: "rgba(2,117,216,1)",
                data: vals,
            }],
        },
        options: {
            scales: {
                xAxes: [{
                    time: {
                        unit: 'day'
                    },
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        maxTicksLimit: 6
                    }
                }],
                yAxes: [{
                    legend: "second",
                    gridLines: {
                        display: true
                    }
                }],
            },
            legend: {
                display: true
            }
        }
    });
})

// Bar Chart Example

