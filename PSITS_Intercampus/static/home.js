let currentActiveWindow = '';
const logout = () => {
    location.href = '/logout'
}

const btnClicked = (btn) => {
    if(getWindow()){
        document.querySelector(`#${getWindow()}`).classList.remove('active');
        document.querySelector(`#${getWindow()}-container`).classList.remove('show');
        document.querySelector(`#${getWindow()}-container`).classList.add('hidden');
    }
    document.querySelector(`#${btn}`).classList.add('active');
    document.querySelector(`#${btn}-container`).classList.remove('hidden');
        document.querySelector(`#${btn}-container`).classList.add('show');
    currentActiveWindow = btn;
}

const getWindow = () => {
    switch(currentActiveWindow){
        case 'admins':
            return 'admins';
        case 'registration':
            return 'registration';
        case 'events':
            return 'events';
        case 'metrics':
            return 'metrics';
    }
    return null;
}


const loadChart = () => {
    let attendeesChart = document.getElementById('attendeesChart').getContext('2d');

    // Pie Chart
    var attendees = new Chart(attendeesChart, {
        type: 'bar',
        data: {
            labels: ['1', '2', '3', '4'],
            datasets: [{
                label: '# of attendees per year level',
                data: [86,52,32,37],
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
                borderWidth: 2
            }]
        },
        options: {
    
        }
    })
}

loadChart();

// weather api
// https://api.open-meteo.com/v1/forecast?latitude=10.32&longitude=123.85&hourly=temperature_2m,rain