{% block jquery %}
var endpoint = "api/data/lang"
var ranks = [];
$.ajax({
    method :"GET",
    url : endpoint,
    success: (dataset)=>{
        console.log(dataset)
        // values = dataset.values;
        // labels = dataset.labels;

        var ctx = document.getElementById('langChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                // labels: ['Contest #1', 'Contest #2', 'Contest #3', 'Contest #4', 'Contest #5', 'Contest #6'],
                labels : dataset.labels,
                datasets: [{
                    label: 'Submissions',
                    data: dataset.values,
                    backgroundColor: [
                        'rgba(155, 255, 32, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)'
                    ],
                    borderColor: [
                        'rgba(55, 200, 0, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    },
    error:(e)=>{
        console.log("errrorr");
        console.log(e);
    }
})
{% endblock jquery %}