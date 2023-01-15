'use strict';

async function loadData(){
    // searching transactions, must have a key for authentication
    let key = document.getElementById('key').value;
    const response = await fetch(`/PSITS/api/transactions_tally/all?key=${key}`,{
        headers: {
            Authorization: key,
        },
    })
    let data = await response.json()
    return data
}

async function loadAccounts(){
    let key = document.getElementById('key').value;
    const response = await fetch(`/PSITS/api/students_tally?key=${key}`,{
        headers: {
            Authorization: key,
        },
    })
    let data = await response.json()
    return data
}

async function loadAnalytic(){
    // created by Jayharron, feel free to modify this file in the future
    // getting the dataset value and attributes
    const {monthly_sales: dataset_revenue,merch_orders:dataset_sales,monthly_orders: dataset_monthly_orders, merch_orders_reserve: dataset_dept_orders} = await loadData()
    const {account_per_level, account_per_course} = await loadAccounts();
    let monthlyChartHTML = document.getElementById('monthlySales').getContext('2d');
    let deptChartHTML = document.getElementById('deptSales').getContext('2d');
    let courseChartHTML = document.getElementById('courses').getContext('2d');
    let levelChartHTML = document.getElementById('levels').getContext('2d');
    let mOrderChartHTML = document.getElementById('monthlyOrders').getContext('2d');
    let dOrderChartHTML = document.getElementById('deptOrders').getContext('2d');
    let yearlyLabel = document.getElementById('yearlyTotal');
    let yearlyOrder = document.getElementById('yearlyOrder');
    let totalPopulationLabel = document.getElementById('registeredAccounts');
    let yearlyTotal = 0;
    let yrlyOrder = 0;

    // converting the dataset value to object
    let dataset_revenue_object = dataset_revenue;
    let dataset_sales_object = dataset_sales;
    let dataset_courses_object = account_per_course;
    let dataset_levels_object = account_per_level;
    let dataset_monthly_orders_object = dataset_monthly_orders;
    let dataset_dept_orders_object = dataset_dept_orders;

    // creating the array of monthly sales and label data 
    let monthlySales = new Array();
    let monthlyLabels = new Array();

    // creating the array of department sales and label
    let deptSales = new Array();
    let deptLabels = new Array()

    // creating the array of monthly orders and label data
    let monthlyOrders = new Array();
    let monthlyOrderLabels = new Array();

    let deptOrders = new Array();
    let deptOrderLabels = new Array();

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

    // iterate with the object properties
    for(let key in dataset_monthly_orders_object){
        // the key format is 'YYYY MM', we will convert it into a string
        // and get only the month
        const month_string = getMonthByNumber(parseInt(key.toString().split(" ")[1]));
        monthlyOrders.push(parseFloat(dataset_monthly_orders_object[key]))
        monthlyOrderLabels.push(month_string);
        yrlyOrder = yrlyOrder + parseFloat(dataset_monthly_orders_object[key]);
        yearlyOrder.innerHTML = `${formatter.format(yrlyOrder)}`;
    }

    // iterate through the object properties
    for(let key in dataset_sales_object){
        deptSales.push(parseInt(dataset_sales_object[key]));
        deptLabels.push(key);
    }

    // iterate through the object properties
    for(let key in dataset_dept_orders_object){
        deptOrders.push(parseInt(dataset_dept_orders_object[key]));
        deptOrderLabels.push(key);
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

    // Bar chart
    var mOrders = new Chart(mOrderChartHTML, {
        type: 'line',
        data: {
            labels: monthlyOrderLabels,
            datasets: [{
                label: '# of order revenue',
                data: monthlyOrders,
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
    var dOrders = new Chart(dOrderChartHTML, {
        type: 'pie',
        data: {
            labels: deptOrderLabels,
            datasets: [{
                label: '# of product orders',
                data: deptOrders,
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
}

loadAnalytic();