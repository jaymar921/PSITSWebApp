'use strict';

function loadAnalytic(){
    // created by Jayharron, feel free to modify this file in the future
    // getting the dataset value and attributes
    let dataset_revenue = document.getElementById('dataset_revenue').value;
    let dataset_sales = document.getElementById('dataset_sales').value;
    let dataset_courses = document.getElementById('dataset_courses').value;
    let dataset_levels = document.getElementById('dataset_levels').value;
    let monthlyChartHTML = document.getElementById('monthlySales').getContext('2d');
    let deptChartHTML = document.getElementById('deptSales').getContext('2d');
    let courseChartHTML = document.getElementById('courses').getContext('2d');
    let levelChartHTML = document.getElementById('levels').getContext('2d');
    let yearlyLabel = document.getElementById('yearlyTotal');
    let totalPopulationLabel = document.getElementById('registeredAccounts');
    let yearlyTotal = 0

    // converting the dataset value to object
    let dataset_revenue_object = JSON.parse(dataset_revenue);
    let dataset_sales_object = JSON.parse(dataset_sales);
    let dataset_courses_object = JSON.parse(dataset_courses);
    let dataset_levels_object = JSON.parse(dataset_levels);

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

    // accounts
    let coursesPopulation = new Array();
    let coursesLabel = new Array();
    let totalPopulation = 0;

    let levelPopulation = new Array();
    let levelLabel = new Array();

    // iterate through the object property
    for(let key in dataset_courses_object){
        coursesPopulation.push(parseInt(dataset_courses_object[key]))
        coursesLabel.push(key);
        totalPopulation = totalPopulation + parseInt(dataset_courses_object[key]);
        totalPopulationLabel.innerHTML = `${totalPopulation}`;
    }

    // iterate through the object property
    for(let key in dataset_levels_object){
        levelPopulation.push(parseInt(dataset_levels_object[key]));
        levelLabel.push(key);
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
                    'rgba(251, 123, 20, 1)',
                    'rgba(239, 252, 122, 1)',
                    'rgba(122, 118, 120, 1)',
                    'rgba(10, 22, 89, 1)',
                    'rgba(152, 235, 76, 1)',
                    'rgba(232, 118, 120, 1)',
                    'rgba(112, 97, 120, 1)',
                    'rgba(32, 67, 98, 1)',
                    'rgba(52, 12, 65, 1)',
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
                    'rgba(251, 123, 20, 1)',
                    'rgba(239, 252, 122, 1)',
                    'rgba(122, 118, 120, 1)',
                    'rgba(10, 22, 89, 1)',
                    'rgba(152, 235, 76, 1)',
                    'rgba(232, 118, 120, 1)',
                    'rgba(112, 97, 120, 1)',
                    'rgba(32, 67, 98, 1)',
                    'rgba(52, 12, 65, 1)',
                ],
                borderWidth: 0
            }]
        },
        options: {
    
        }
    })
    // Bar chart
    var coursesSalesChart = new Chart(courseChartHTML, {
        type: 'bar',
        data: {
            labels: coursesLabel,
            datasets: [{
                label: '# of students in course',
                data: coursesPopulation,
                backgroundColor: [
                    'rgba(238, 184, 104, 1)',
                    'rgba(75, 166, 223, 1)',
                    'rgba(239, 118, 122, 1)',
                    'rgba(251, 123, 20, 1)',
                    'rgba(239, 252, 122, 1)',
                    'rgba(122, 118, 120, 1)',
                    'rgba(10, 22, 89, 1)',
                    'rgba(152, 235, 76, 1)',
                    'rgba(232, 118, 120, 1)',
                    'rgba(112, 97, 120, 1)',
                    'rgba(32, 67, 98, 1)',
                    'rgba(52, 12, 65, 1)',
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
    var deptSalesChart = new Chart(levelChartHTML, {
        type: 'pie',
        data: {
            labels: levelLabel,
            datasets: [{
                label: '# of student levels',
                data: levelPopulation,
                backgroundColor: [
                    'rgba(238, 184, 104, 1)',
                    'rgba(75, 166, 223, 1)',
                    'rgba(239, 118, 122, 1)',
                    'rgba(251, 123, 20, 1)',
                    'rgba(239, 252, 122, 1)',
                    'rgba(122, 118, 120, 1)',
                    'rgba(10, 22, 89, 1)',
                    'rgba(152, 235, 76, 1)',
                    'rgba(232, 118, 120, 1)',
                    'rgba(112, 97, 120, 1)',
                    'rgba(32, 67, 98, 1)',
                    'rgba(52, 12, 65, 1)',
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