let currentActiveWindow = '';
const logout = () => {
    location.href = '/logout'
}
const allowReqFetch = () => {
    fetch('/api/allowadmin')
    .then(r => r.json())
    .then(data => {
        document.querySelector('#allow-reg').checked = data.allowed == 'True' ? true:false;
    })
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

    if(currentActiveWindow === 'registration' || currentActiveWindow === 'raffle')
        setSelectOptionsRegistry();
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
        case 'raffle':
            return 'raffle';
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

/*
    ADMINS PAGE
*/
let adminsCache = []
const adminsTable = document.querySelector('#admin-data');
const loadAdminsCache = async () => {
    if(getWindow() !== 'admins')
        return;
    await fetch('/api/getalladmins').then(res => res.json())
    .then(data => adminsCache=data.admins);

    updateAdminsTable();
}

function updateAdminsTable(){
    adminsTable.innerHTML = '';
    adminsCache.forEach(admin => {

        // creating each new elements for the table
        const table_row = document.createElement('tr');

        const col_id = document.createElement('td');
        col_id.innerHTML = admin.idno;

        const col_fn = document.createElement('td');
        col_fn.innerHTML = admin.lastname+", "+admin.firstname;

        const col_course = document.createElement('td');
        col_course.innerHTML = admin.course;

        const col_year = document.createElement('td');
        col_year.innerHTML = admin.year;

        const col_campus = document.createElement('td');
        col_campus.innerHTML = admin.campus;

        const col_email = document.createElement('td');
        col_email.innerHTML = admin.email;

        const col_revoke = document.createElement('td');
        const col_revokebtn = document.createElement('button');
        col_revokebtn.innerHTML = 'Revoke';
        col_revokebtn.setAttribute("class", "btn btn-outline-danger");
        col_revokebtn.addEventListener('click', (e)=> {
            deleteUser(admin.idno);
        })
        col_revoke.appendChild(col_revokebtn);


        table_row.appendChild(col_id);
        table_row.appendChild(col_fn);
        table_row.appendChild(col_course);
        table_row.appendChild(col_year);
        table_row.appendChild(col_campus);
        table_row.appendChild(col_email);
        table_row.appendChild(col_revoke);
        adminsTable.appendChild(table_row);
    })
}


setInterval(()=>{loadAdminsCache()}, 1000);
const deleteUser = async (id) =>{
    fetch('/api/register_admin', {
        method: 'DELETE',
        headers: {
            'idno':id
        }
    }).then(r => r.json())
    .then(d => alert(d.message));
}
/*
    EVENTS PAGE
*/

const registerEvents = async () => {
    const eventName = document.querySelector('#event_name').value;
    const venue = document.querySelector('#event_venue').value;
    const attendees = document.querySelector('#event_attendees').value;
    const host = document.querySelector('#event_host').value;
    const regFee = document.querySelector('#event_reg').value;
    const shirt = document.querySelector('#event_tshirt').value;

    fetch('/api/events',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {
                eventName,
                venue,
                attendees,
                host,
                regFee,
                shirt
            }
        )
    }).then(res => res.json()).then(data => {
        if(data.message === 'success'){
            document.querySelector('#event_name').value = '';
            document.querySelector('#event_venue').value = '';
            document.querySelector('#event_attendees').value = '';
            document.querySelector('#event_host').value;
            document.querySelector('#event_reg').value = '';
            document.querySelector('#event_tshirt').value = '';

        }
    })
}
let eventsCache = []
const eventsTable = document.querySelector('#events-data');
const loadEventsCache = async () => {
    if(getWindow() !== 'events')
        return;

    await fetch('/api/events')
    .then(res => res.json())
    .then(data => eventsCache=data.events);
    updateEventsTable();
}

const updateEventsTable = async () => {
    eventsTable.innerHTML = '';
    eventsCache.forEach(event => {

         // creating each new elements for the table
         const table_row = document.createElement('tr');

         const col_eventname = document.createElement('td');
         col_eventname.innerHTML = event.event_name;
 
         const col_eventvenue = document.createElement('td');
         col_eventvenue.innerHTML = event.venue;
 
         const col_eventattendees = document.createElement('td');
         col_eventattendees.innerHTML = event.attendees;
 
         const col_eventhost = document.createElement('td');
         col_eventhost.innerHTML = event.host;
 
         const col_eventprice = document.createElement('td');
         col_eventprice.innerHTML = `₱${(event.registration_price+event.tshirt_price)}`;
 
         const col_remove = document.createElement('td');
         const col_removebtn = document.createElement('button');
         col_removebtn.setAttribute("class", "btn btn-outline-danger");
         col_removebtn.addEventListener('click', (e)=> {
            if(confirm(`Delete ${event.event_name}'s data?`))
                removeEvent(event.id);
         })
         col_removebtn.innerHTML = '<i class="fa fa-trash" aria-hidden="true"></i>';
         col_remove.appendChild(col_removebtn);
 
 
         table_row.appendChild(col_eventname);
         table_row.appendChild(col_eventvenue);
         table_row.appendChild(col_eventattendees);
         table_row.appendChild(col_eventhost);
         table_row.appendChild(col_eventprice);
         table_row.appendChild(col_remove);
         eventsTable.appendChild(table_row);

    })
}

const removeEvent = (eventId) => {
    fetch('/api/events',{
        method: 'DELETE',
        headers: {
            'eventID': eventId
        }
    }).then(res=>res.json())
    .then(data => {
        if(data.message === 'success')
            loadEventsCache();
    })
}

setInterval(()=>{loadEventsCache();},1000);

/*
    REGISTRATION PAGE
*/

document.querySelector('#reg_payment').addEventListener('change', (e)=>{
    if(e.target.value === 'TICKET'){
        document.querySelector('#reg_size').disabled = true;
        document.getElementById('reg_size').value = 'NONE';
    }
    else{
        document.querySelector('#reg_size').disabled = false;
        document.getElementById('reg_size').value = 'M';
    }
})

const registerStudent = async () => {
    const idno = document.querySelector('#reg_idno').value;
    const fullname = document.querySelector('#reg_fullname').value;
    const email = document.querySelector('#reg_email').value;
    const campus = document.querySelector('#reg_campus').value;
    const payment = document.querySelector('#reg_payment').value;
    const shirtsize = document.querySelector('#reg_size').value;
    const eventID = document.querySelector('#reg_id').value;
    const reg_btn = document.querySelector('#reg_save');

    reg_btn.disabled = true;
    
    fetch('/api/registry',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            idno,
            ...ExtractFullname(fullname),
            email,
            campus,
            payment,
            shirtsize,
            eventID
        })
    }).then(res => res.json())
    .then(data => {
        if(data.message === 'success'){
            document.querySelector('#reg_idno').value = '';
            document.querySelector('#reg_fullname').value = '';
            document.querySelector('#reg_email').value = '';
            reg_btn.disabled = false;
        }
    });
}

function ExtractFullname(fullname) {
    let names = fullname.split(' ');
    
    let lastname = names[names.length-1];
    let firstname = '';
    for(let i = 0; i < names.length - 1; i++){
        if(i > 0) firstname+=' ';
        firstname += names[i]
    }
    return {firstname, lastname}
}

const setSelectOptionsRegistry = async () => {
    fetch('/api/events')
    .then(res => res.json())
    .then(data => {
        const event_options = document.querySelector('#reg_id');
        event_options.innerHTML = '';
        data.events.forEach(ev => {
            const option = document.createElement('option');
            option.innerHTML = ev.event_name;
            option.value = ev.id;
            event_options.appendChild(option);
        })
    });
    fetch('/api/events')
    .then(res => res.json())
    .then(data => {
        const event_options = document.querySelector('#metrics_id');
        event_options.innerHTML = '';
        data.events.forEach(ev => {
            const option = document.createElement('option');
            option.innerHTML = ev.event_name;
            option.value = ev.id;
            event_options.appendChild(option);
        })
    });
    fetch('/api/events')
    .then(res => res.json())
    .then(data => {
        const event_options = document.querySelector('#raffle_id');
        event_options.innerHTML = '';
        data.events.forEach(ev => {
            const option = document.createElement('option');
            option.innerHTML = ev.event_name;
            option.value = ev.id;
            event_options.appendChild(option);
        })
    });
}

let registryCache = [];
let registryMapCache = new Map();
const registryTable = document.querySelector('#registry-data');
const loadRegistryCache = async () => {
    try{
        if(getWindow() !== 'registration')
            return;
        await fetch('/api/registry',{
            headers:{
                "eventId": document.querySelector('#reg_id').value
            }
        }).then(res => res.json())
        .then(data => registryCache=data.data);

        // add the new items in map
        registryCache.forEach(registry => {
            if(!registryMapCache.has(registry.idno)){
                registryMapCache.set(registry.idno,{
                    ...registry
                })
            }
        })

        // remove item if not in cache but in map
        let ids_map = [];
        registryMapCache.forEach((v, k)=> {ids_map.push(k)});

        let ids_cache = [];
        registryCache.forEach((v)=> {ids_cache.push(v.idno)});

        ids_map.forEach(id=>{
            if(!ids_cache.includes(id))
                registryMapCache.delete(id);
        })

        // update the old data with new one
        registryCache.forEach(registry => {
            if(registryMapCache.has(registry.idno)){
                registryMapCache.set(registry.idno,{
                    ...registry
                })
            }
        })
    }catch{}
}

const updateRegistryTable = async () => {
    registryTable.innerHTML = '';

    // sort the registryCache
    const arrSorted = registryCache.sort(function(a,b){
        const nameA = a.meta_data.split('|')[0].toLowerCase();
        const nameB = b.meta_data.split('|')[0].toLowerCase();
        if(nameA < nameB)
            return -1;
        if(nameA > nameB)
            return 1;
        return 0;
    });

    const toSearch = document.querySelector('#reg_search').value;

    arrSorted.forEach(registry => {
        // creating each new elements for the table
        const table_row = document.createElement('tr');

        const idnum = document.createElement('td');
        idnum.innerHTML = registry.idno;

        const fullname = document.createElement('td');
        fullname.innerHTML = registry.meta_data.split('|')[0];

        const campus = document.createElement('td');
        campus.innerHTML = registry.meta_data.split('|')[2];

        const event = document.createElement('td');
        event.innerHTML = registry.meta_data.split('|')[1];

        const payment = document.createElement('td');
        payment.innerHTML = registry.payment;

        const shirtsize = document.createElement('td');
        shirtsize.innerHTML = registry.shirt_size;

        const claimed = document.createElement('td');
        const claimedCheckbox = document.createElement('input');
        claimedCheckbox.type = 'checkbox';
        claimedCheckbox.checked = registry.claimed.toLowerCase() === "true"? true : false;

        claimedCheckbox.addEventListener('change', (e)=>{
            if(e.target.checked)
                updateRegistryOption(registry.id, 'claimed', 'true');
            else updateRegistryOption(registry.id, 'claimed', 'false');
        })
        claimed.appendChild(claimedCheckbox);
        
        const attended  = document.createElement('td');
        const attendedCheckbox = document.createElement('input');
        attendedCheckbox.type = 'checkbox';
        attendedCheckbox.checked = registry.attended.toLowerCase() === "true"? true : false;

        attendedCheckbox.addEventListener('change', (e)=>{
            if(e.target.checked)
                updateRegistryOption(registry.id, 'attended', 'true');
            else updateRegistryOption(registry.id, 'attended', 'false');
        })
        attended.appendChild(attendedCheckbox);

        const action  = document.createElement('td');
        const deleteBtn = document.createElement('button');
        deleteBtn.innerHTML = '<i class="fa fa-trash" aria-hidden="true"></i>';
        deleteBtn.addEventListener('click', (e)=>{
            if(confirm(`Delete ${registry.meta_data.split('|')[0]}'s data?`))
                updateRegistryOption(registry.id, 'delete', 'true');
        })
        action.appendChild(deleteBtn);



        table_row.appendChild(idnum);
        table_row.appendChild(fullname);
        table_row.appendChild(campus);
        table_row.appendChild(event);
        table_row.appendChild(payment);
        table_row.appendChild(shirtsize);
        table_row.appendChild(claimed);
        table_row.appendChild(attended);
        table_row.appendChild(action);

        let found = true;
        if(toSearch !== ''){
            if(registry.meta_data.split('|')[0]){
                if(!registry.meta_data.split('|')[0].toLowerCase().startsWith(toSearch.toLowerCase()) && !registry.idno.toString().startsWith(toSearch)){
                    found = false;
                }
            }
        }
        if(found)
            registryTable.appendChild(table_row);
    })
}
setInterval(()=>{loadRegistryCache()}, 2000);
setInterval(()=>{updateRegistryTable()}, 1000);

const updateRegistryOption = async (id, option, checked) => {
    if(option !== 'delete'){
        fetch('/api/registry',{
            method:'PUT',
            headers: {
                'regID': id,
                'checked': checked,
                'option': option
            }
        })
    }else{
        fetch('/api/registry',{
            method:'DELETE',
            headers: {
                'eventId': id
            }
        })
    }
}

document.querySelector('#allow-reg').addEventListener('change', ({target})=> {
    if(confirm(`Set admin registration to: ${target.checked}?`)){
        fetch('/api/allowadmin',{
            method: 'PUT',
            headers:{
                "allow": target.checked
            }
        })
    }
})

document.querySelector('#reg_campus_selection').addEventListener('change', ({target})=> {
    if(target.value === 'OTHER'){
        document.querySelector('#reg_otherCampus').classList.remove('hidden');
        document.querySelector('#reg_campus').value = '';
    }else{
        document.querySelector('#reg_otherCampus').classList.add('hidden');
        document.querySelector('#reg_campus').value = target.value;
    }
})

/*
    RAFFLE
*/

document.querySelector('#use-event-toggle').addEventListener('change', ({target}) => {
    if(target.checked){
        document.querySelector('#raffle-use-event').innerHTML = 'Use Event:'
        document.querySelector('#use-custom').classList.add('hidden');
        document.querySelector('#use-event').classList.remove('hidden');

        document.querySelector('#use-custom').classList.remove('show');
        document.querySelector('#use-event').classList.add('show');

    }else{
        document.querySelector('#raffle-use-event').innerHTML = 'Custom:'
        
        document.querySelector('#use-event').classList.add('hidden');
        document.querySelector('#use-custom').classList.remove('hidden');

        document.querySelector('#use-custom').classList.add('show');
        document.querySelector('#use-event').classList.remove('show');

    }
})

document.querySelector('#attendees_only').addEventListener('change', ({target}) => {
    if(target.checked){
        document.querySelector('#raffle-att-only').innerHTML = 'Attendees only: '
    }else{
        document.querySelector('#raffle-att-only').innerHTML = 'Include everyone: '
    }
})

document.querySelector('#custom-opt').addEventListener('change', ({target}) => {
    if(target.checked){
        document.querySelector('#raffle-custom-opt').innerHTML = 'Comma Separated: '
    }else{
        document.querySelector('#raffle-custom-opt').innerHTML = 'New line Separated: '
    }
})

const submitGenerateRaffle = async () => {
    const useEvent = document.querySelector('#use-event-toggle').checked;
    const eventID = document.querySelector('#raffle_id').value;
    const attendeesOnly = document.querySelector('#attendees_only').checked;

    const commaSeparated = document.querySelector('#custom-opt').checked;
    const inputData = document.querySelector('#raffleinputData').value;
    
    const data = inputData.split(commaSeparated?",":"\n");

    fetch('/api/rafflegenerator', {
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
            useEvent,
            eventID,
            attendeesOnly,
            data
        })
    })
    .then(r => r.json())
    .then(data => location.href=`/raffle/${data.raffle_key}`)
}

// weather api
// https://api.open-meteo.com/v1/forecast?latitude=10.32&longitude=123.85&hourly=temperature_2m,rain