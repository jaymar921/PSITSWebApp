'use strict';

function loadAnalytic(){
    // created by Jayharron, feel free to modify this file in the future
    // getting the dataset value and attributes
    let dataset_revenue = document.getElementById('dataset_revenue').value;
    let dataset_sales = document.getElementById('dataset_sales').value
    let monthlyChartHTML = document.getElementById('monthlySales').getContext('2d');
    let deptChartHTML = document.getElementById('deptSales').getContext('2d');
    let yearlyLabel = document.getElementById('yearlyTotal');
    let yearlyTotal = 0

    // converting the dataset value to object
    let dataset_revenue_object = JSON.parse(dataset_revenue);
    let dataset_sales_object = JSON.parse(dataset_sales);

    // creating the array of monthly sales and label data 
    let monthlySales = new Array();
    let monthlyLabels = new Array();

    // creating the array of department sales and label
    let deptSales = new Array();
    let deptLabels = new Array()

    // currency formatter
    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'PHP',
    
        // These options are needed to round to whole numbers if that's what you want.
        //minimumFractionDigits: 0, // (this suffices for whole numbers, but will print 2500.10 as $2,500.1)
        //maximumFractionDigits: 0, // (causes 2500.99 to be printed as $2,501)
    });

    // iterate with the object properties
    for(let key in dataset_revenue_object){
        // the key format is 'YYYY MM', we will convert it into a string
        // and get only the month
        const month_string = getMonthByNumber(parseInt(key.toString().split(" ")[1]));
        monthlySales.push(parseFloat(dataset_revenue_object[key]))
        monthlyLabels.push(month_string);
        yearlyTotal = yearlyTotal + parseFloat(dataset_revenue_object[key]);
        yearlyLabel.innerHTML = `${formatter.format(yearlyTotal)}`;
    }

    // iterate through the object properties
    for(let key in dataset_sales_object){
        deptSales.push(parseInt(dataset_sales_object[key]));
        deptLabels.push(key);
    }

    // this function will convert int to string, 1 = January, I think you already know the point :>
    function getMonthByNumber(m){
        switch(m){
            case 1: return 'January';
            case 2: return 'February';
            case 3: return 'March';
            case 4: return 'April';
            case 5: return 'May';
            case 6: return 'June';
            case 7: return 'July';
            case 8: return 'August';
            case 9: return 'September';
            case 10: return 'October';
            case 11: return 'November';
            case 12: return 'December';
        }
        return "InvalidMonth";
    }


    // Bar chart
    var monthlySalesChart = new Chart(monthlyChartHTML, {
        type: 'bar',
        data: {
            labels: monthlyLabels,
            datasets: [{
                label: '# of Sales',
                data: monthlySales,
                backgroundColor: [
                    'rgba(238, 184, 104, 1)',
                    'rgba(75, 166, 223, 1)',
                    'rgba(239, 118, 122, 1)',
                ],
                borderWidth: 0
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    // Pie Chart
    var deptSalesChart = new Chart(deptChartHTML, {
        type: 'pie',
        data: {
            labels: deptLabels,
            datasets: [{
                label: '# of Sales',
                data: deptSales,
                backgroundColor: [
                    'rgba(238, 184, 104, 1)',
                    'rgba(75, 166, 223, 1)',
                    'rgba(239, 118, 122, 1)',
                ],
                borderWidth: 0
            }]
        },
        options: {
    
        }
    })
    // clear the values
    document.getElementById('dataset_revenue').value = '';
    document.getElementById('dataset_sales').value = '';
}

loadAnalytic();