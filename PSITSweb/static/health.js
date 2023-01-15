
async function AppendData(elementID, data){
    let element = document.getElementById(elementID)
    for(let child of element.childNodes)
        element.removeChild(child);
    
    element.innerHTML = data;
}
async function loadAccountDB(){
    fetch('/PSITS/api/health?option=accounts').then(r => r.json())
    .then((data) => {
        let color = 'red';
        if(data.result <= 30)
            color = 'yellowgreen';
        else if(data.result <= 300)
            color = 'yellow';
        else if(data.result <= 600)
            color = 'orange';

        AppendData("account",`<p style='color:${color};font-weight:900;'>${data.result}ms</p>`);
    }).catch(r => {
        AppendData("account",`<p style='color:red;font-weight:900;'>no response</p>`);
    });
}

async function loadAnnouncementDB(){
    fetch('/PSITS/api/health?option=announcements').then(r => r.json())
    .then((data) => {
        let color = 'red';
        if(data.result <= 30)
            color = 'yellowgreen';
        else if(data.result <= 300)
            color = 'yellow';
        else if(data.result <= 600)
            color = 'orange';

        AppendData("announcement",`<p style='color:${color};font-weight:900;'>${data.result}ms</p>`);
    }).catch(r => {
        AppendData("announcement",`<p style='color:red;font-weight:900;'>no response</p>`);
    });
}

async function loadMerchandiseDB(){
    fetch('/PSITS/api/health?option=merchandise').then(r => r.json())
    .then((data) => {
        let color = 'red';
        if(data.result <= 30)
            color = 'yellowgreen';
        else if(data.result <= 300)
            color = 'yellow';
        else if(data.result <= 600)
            color = 'orange';

        AppendData("merchandise",`<p style='color:${color};font-weight:900;'>${data.result}ms</p>`);
    }).catch(r => {
        AppendData("merchandise",`<p style='color:red;font-weight:900;'>no response</p>`);
    });
}

async function loadOrderDB(){
    fetch('/PSITS/api/health?option=orders').then(r => r.json())
    .then((data) => {
        let color = 'red';
        if(data.result <= 30)
            color = 'yellowgreen';
        else if(data.result <= 300)
            color = 'yellow';
        else if(data.result <= 600)
            color = 'orange';

        AppendData("order",`<p style='color:${color};font-weight:900;'>${data.result}ms</p>`);
    }).catch(r => {
        AppendData("order",`<p style='color:red;font-weight:900;'>no response</p>`);
    });
}

async function loadHandleOrder(){
    fetch('/PSITS/api/health?option=order_route').then(r => r.json())
    .then((data) => {
        let color = 'red';
        if(data.result <= 30)
            color = 'yellowgreen';
        else if(data.result <= 300)
            color = 'yellow';
        else if(data.result <= 600)
            color = 'orange';

        AppendData("order_route",`<p style='color:${color};font-weight:900;'>${data.result}ms</p>`);
    }).catch(r => {
        AppendData("order_route",`<p style='color:red;font-weight:900;'>no response</p>`);
    });
}

async function loadAccountAPI(){
    fetch('/PSITS/api/health?option=account_api').then(r => r.json())
    .then((data) => {
        let color = 'red';
        if(data.result <= 30)
            color = 'yellowgreen';
        else if(data.result <= 300)
            color = 'yellow';
        else if(data.result <= 600)
            color = 'orange';

        AppendData("account_api",`<p style='color:${color};font-weight:900;'>${data.result}ms</p>`);
    }).catch(r => {
        AppendData("account_api",`<p style='color:red;font-weight:900;'>no response</p>`);
    });
}

async function loadAccountUpdateAPI(){
    fetch('/PSITS/api/health?option=account_update_api').then(r => r.json())
    .then((data) => {
        let color = 'red';
        if(data.result <= 30)
            color = 'yellowgreen';
        else if(data.result <= 300)
            color = 'yellow';
        else if(data.result <= 600)
            color = 'orange';

        AppendData("account_update_api",`<p style='color:${color};font-weight:900;'>${data.result}ms</p>`);
    }).catch(r => {
        AppendData("account_update_api",`<p style='color:red;font-weight:900;'>no response</p>`);
    });
}


setInterval(()=>{
    loadAnnouncementDB()
    loadMerchandiseDB()
    loadOrderDB()
    loadAccountUpdateAPI()
}, 1000)
setInterval(()=>{
    loadAccountDB()
    loadHandleOrder()
    loadAccountAPI()
}, 5000)