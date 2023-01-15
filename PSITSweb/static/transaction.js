
/*
    Sending GET request to API
*/
let api_link = '';

function setAPI_LINK(link){
    api_link = link;
}

async function generateTally(searchData, key){

    let data;
    try{
        document.getElementById('display_reserve').innerHTML = '...';
        document.getElementById('display_paid').innerHTML = '...';
        document.getElementById('display_total').innerHTML = '...';
        // searching transactions, must have a key for authentication
        const response = await fetch(`${api_link}/PSITS/api/transactions_tally/${new String(searchData)}?key=${key}`,{
            headers: {
                Authorization: key,
            },
        })
        data = await response.json()

        // display the necessary data
        document.getElementById('display_reserve').innerHTML = formatToCurrency(Number.parseFloat(data.reserve));
        document.getElementById('display_paid').innerHTML = `₱${formatToCurrency(Number.parseFloat(data.paid))}`;
        document.getElementById('display_total').innerHTML = `₱${formatToCurrency(Number.parseFloat(data.total))}`;
    }catch(e){
        info_box.style.display = "none";
        return;
    }

    
}

async function search_transaction(searchData, key){
    clearMap();
    let info_box = document.getElementById('info_box');
    let info_msg = document.getElementById('info_message');

    info_msg.innerHTML = "Loading...";
    document.getElementById('info_load').style.display = 'block';

    info_box.style.display = "block";
    
    generateTally(searchData, key);
    let data;
    try{
        // searching transactions, must have a key for authentication
        const response = await fetch(`${api_link}/PSITS/api/transactions/${new String(searchData)}?key=${key}`,{
            headers: {
                Authorization: key,
            },
        })
        data = await response.json()
    }catch(e){
        info_box.style.display = "none";
        return;
    }
    

    // loop through the ORDERS list
    let table_body = document.getElementById('table_body');

    // clear all childs
    while (table_body.hasChildNodes()) {
        table_body.removeChild(table_body.firstChild);
    }

    // access denied
    if(data.status === 403){
        info_msg.innerHTML = "Access Denied";
        return;
    }else{

        document.getElementById('search_student').value = searchData;
        
        if(data.ORDERS.length > 0){
            info_box.style.display = "none";
            info_msg.innerHTML = "Loading...";
            document.getElementById('info_load').style.display = 'block';
        }
        else {
            info_msg.innerHTML = "No Records found";
            document.getElementById('info_load').style.display = 'none';
        };
    }

    let count = 1;

    /*
     V1.3 - 1.0
        ORDER = {
            'reserve': Number,
            'total': Number,
            'paid': Number,
            'ORDERS': [
                {
                    'account': {
                        'account_id': Number,
                        'fullname': String,
                        'course': String,
                        'year': Number
                    },
                    'merch': {
                        'uid': Number
                    },
                    'order': {
                        'uid': Number,
                        'order_date': Date,
                        'quantity': Number,
                        'additional_info': String
                    },
                    'reference': String,
                    'getTotal': Number,
                    'getStatus': String
                }
            ],
            'merchandise': [
                {
                    'uid': Number,
                    'title': String,
                    'price': Number,
                    'discount': Number
                },
            ],
            'search': String,
            'status': Number
        }

     V1.3 - 1.1
        ORDER = {
            'reserve': Number,
            'total': Number,
            'paid': Number,
            'ORDERS': [
                {
                    'reference': String,
                    'fullname': String,
                    'product': String,
                    'info': String,
                    'quantity': Number,
                    'amount': Number,
                    'status': String
                }
            ],
            'search': String,
            'status': Number
        }
    */

    for(const order of data.ORDERS){
        

        //const {order:_order, account, reference, getTotal, getStatus} = order;
        const {reference, fullname, product, info, quantity, status, discounted_price, size} = order

        let form_body = document.createElement('form');
        form_body.method = 'POST';
        form_body.action = '';

        let table_row = document.createElement("tr");

        let input_field = document.createElement('input');
        let table_col = document.createElement("td");

        input_field = document.createElement('input');
        input_field.setAttribute('id', reference+"idnum");
        input_field.setAttribute('class','hide');
        input_field.name = 'order_ref';
        input_field.hidden = true;
        input_field.value = `${reference}`

        table_row.appendChild(input_field);

        // number
        let num = document.createElement('p');
        num.innerHTML = count++;
        table_col.appendChild(num);
        table_row.appendChild(table_col);

        // ref
        table_col = document.createElement("td");
        input_field = document.createElement('input');
        table_col.setAttribute('class', 'hide');
        input_field.setAttribute('id', reference+"ref");
        input_field.disabled = true;
        input_field.value = reference

        table_col.appendChild(input_field);
        table_row.appendChild(table_col);

        // name
        table_col = document.createElement("td");
        input_field = document.createElement('input');
        input_field.setAttribute('id', reference+"name");
        input_field.disabled = true;
        input_field.value = `${fullname}`

        table_col.appendChild(input_field);
        table_row.appendChild(table_col);

        // prod
        table_col = document.createElement("td");
        input_field = document.createElement('input');
        input_field.setAttribute('id', reference+"prod");
        input_field.disabled = true;
        input_field.value = `${product}`

        table_col.appendChild(input_field);
        table_row.appendChild(table_col);

        // add info
        table_col = document.createElement("td");
        table_col.setAttribute('class', 'information hide');
        input_field = document.createElement('p');
        input_field.setAttribute('style', 'white-space: pre-line; padding: 5px; font-size: 70%;');
        input_field.innerHTML = `${info}`
        // filter the sizes
        if(status !== 'CANCELLED')
            filterSizesFromInfo(info)

        table_col.appendChild(input_field);
        table_row.appendChild(table_col);

        
        // size
        table_col = document.createElement("td");
        table_col.setAttribute('class', 'hide');
        input_field = document.createElement('input');
        input_field.setAttribute('id', reference+"size");
        input_field.disabled = true;
        input_field.value = `${size}`;

        table_col.appendChild(input_field);
        table_row.appendChild(table_col);

        // quantity
        table_col = document.createElement("td");
        table_col.setAttribute('class', 'hide');
        input_field = document.createElement('input');
        input_field.setAttribute('id', reference+"qty");
        input_field.disabled = true;
        input_field.value = `${quantity}`;

        table_col.appendChild(input_field);
        table_row.appendChild(table_col);

        // amount
        table_col = document.createElement("td");
        table_col.setAttribute('class', 'hide');
        input_field = document.createElement('input');
        input_field.setAttribute('id', reference+"amt");
        input_field.disabled = true;
        input_field.value = `₱${(discounted_price * quantity).toFixed(2)}`;

        table_col.appendChild(input_field);
        table_row.appendChild(table_col);

        // selection
        table_col = document.createElement("td");

        let selection = document.createElement('select');
        selection.name ='status'
        selection.setAttribute('id', reference+"status");
        selection.setAttribute('style', "width: 100%");
        selection.disabled = true;

        let option_ordered = document.createElement('option');
        option_ordered.value = 'ORDERED';
        option_ordered.innerHTML = 'ORDERED';

        let option_paid = document.createElement('option');
        option_paid.value = 'PAID';
        option_paid.innerHTML = 'PAID';

        let option_cancelled = document.createElement('option');
        option_cancelled.value = 'CANCELLED';
        option_cancelled.innerHTML = 'CANCELLED';

        let option_claimed = document.createElement('option');
        option_claimed.value = 'CLAIMED';
        option_claimed.innerHTML = 'CLAIMED';
        
        if(status === 'ORDERED'){
            option_ordered.selected = true;
            selection.options.add(option_ordered);
            selection.options.add(option_paid);
            selection.options.add(option_cancelled);
        }else if(status === 'PAID'){
            option_paid.selected = true;
            selection.options.add(option_paid);
            selection.options.add(option_claimed);
        }else if(status === 'CANCELLED'){
            option_cancelled.selected = true;
            selection.options.add(option_cancelled);
        }else{
            option_claimed.selected = true;
            selection.options.add(option_claimed);
        }


        table_col.appendChild(selection);
        table_row.appendChild(table_col);
        // end of selection
        
        // button
        table_col = document.createElement("td");
        table_col.setAttribute('class', 'hide');
        let button_edit = document.createElement('a');
        button_edit.setAttribute('id', reference+"edit");
        button_edit.setAttribute('class', 'normalButton')
        button_edit.setAttribute('onclick',`editOrderStatus('${reference}');return;`)
        button_edit.innerHTML = '✎';

        let button_save = document.createElement('button');
        button_save.setAttribute('id', reference+"button");
        button_save.setAttribute('class', 'normalButton')
        button_save.setAttribute('onclick',`update_transaction('${reference}','${reference+"status"}','${key}');return;`)
        button_save.hidden = true;
        button_save.innerHTML = '💾';
        button_save.type = "button";

        let button_delete= document.createElement('button');
        button_delete.setAttribute('id', reference+"delete");
        button_delete.setAttribute('class', 'normalButton hide')
        button_delete.setAttribute('onclick',`deleteModal('${reference}','${key}');return;`)
        button_delete.innerHTML = '❌';
        button_delete.type = "button";
        

        table_col.appendChild(button_edit);
        table_col.appendChild(button_save);
        table_row.appendChild(table_col);
        table_col = document.createElement("td");
        table_col.appendChild(button_delete);
        table_row.appendChild(table_col);
        
        //
        form_body.appendChild(table_row);
        
        // append all the row data into the table body
        table_body.appendChild(table_row)
        
        
    }
    //
    displayFilteredSizesFromInfo();
}

async function search_individual_transaction(searchData, key){
    let info_box = document.getElementById('info_box');
    let info_msg = document.getElementById('info_message');

    document.getElementById('handle_search').value = searchData;

    info_msg.innerHTML = "Loading...";
    document.getElementById('info_load').style.display = 'block';

    info_box.style.display = "block";

    let data;

    // clear the receipt
    updateReceipt();
    
    try{
        // searching transactions, must have a key for authentication
        const response = await fetch(`${api_link}/PSITS/api/transactions/${new String(searchData)}?key=${key}`);

        data = await response.json();
    }catch(e){
        info_box.style.display = "none";
        return;
    }

    // access denied
    if(data.status === 403){
        
        return;
    }else{

        // display the necessary data
        document.getElementById("qrcode").innerHTML = '';
        if(data.ORDERS.length > 0){
            const {reference, fullname, product, info: additional_info, quantity, amount, status, discounted_price, order_date} = data.ORDERS[0]

            new QRCode(document.getElementById("qrcode"), {
                text: reference,
                width: 275,
                height: 275,
                colorDark : "#000000",
                colorLight : "#ffffff",
                correctLevel : QRCode.CorrectLevel.H
            });

            
            updateReceipt(
                name=`${fullname}`,
                product,
                price=`${amount}`,
                discounted_price,
                date=`${order_date}`,
                quantity,
                total=`${(discounted_price * quantity)}`,
                status,
                info=`${additional_info}`,
                ref=`${reference}`
            )

            info_box.style.display = "none";
            info_msg.innerHTML = "Loading...";
            document.getElementById('info_load').style.display = 'block';
        }
        else {
            info_msg.innerHTML = "No Records found";
            document.getElementById('info_load').style.display = 'none';
        };
    }
}

function updateReceipt(name = '', product = '', price = '', discounted_price = '', date = '', quantity = '', total = '', status = '', info='', ref = ''){
    document.getElementById('fld_buyer').innerHTML = name;
    document.getElementById('fld_product').innerHTML = product;
    document.getElementById('fld_orig_price').innerHTML = price?`₱${parseFloat(price.toString()).toFixed(2)}`:'';
    document.getElementById('fld_discount_price').innerHTML = discounted_price?`₱${parseFloat(discounted_price).toFixed(2)}`:'';
    document.getElementById('fld_p_date').innerHTML = date;
    document.getElementById('fld_qty').innerHTML = quantity;
    document.getElementById('fld_total').innerHTML = total?`₱${parseFloat(total).toFixed(2)}`:'';
    document.getElementById('fld_status').innerHTML = status;
    document.getElementById('fld_reference').innerHTML = ref;

    // info
    document.getElementById('info_buyer').value = name;
    document.getElementById('info_product').value = product;
    let info_lines = info.split('\n');
    let info_new = '';
    for(let lines of info_lines){
        if(lines === ' ' || lines === '\n' || lines === '')
            continue;
        info_new += `${lines.trim()}\n`
    }
    document.getElementById('info_info').value = info_new;
    document.getElementById('info_price').value = price?parseFloat(price).toFixed(2):'';
    document.getElementById('info_discounted_price').value = discounted_price?parseFloat(discounted_price).toFixed(2):'';
    document.getElementById('info_quantity').value = quantity;
    document.getElementById('info_status').value = status;

    if(status)
        document.getElementById('info_status').disabled = false;
    else document.getElementById('info_status').disabled = true;
    if(quantity && price){
        document.getElementById('info_quantity').disabled = false;
        document.getElementById('info_info').disabled = false;
    }else {
        document.getElementById('info_quantity').disabled = true;
        document.getElementById('info_info').disabled = true;
    }
}

function editOrderStatus(uid){
    if(document.getElementById(uid+'idnum').hidden === true){
        document.getElementById(uid+'status').disabled = false;
        document.getElementById(uid+'edit').hidden = true;
        document.getElementById(uid+'button').hidden = false;
    }
}

async function update_transaction(ref, button_id, key){
    await fetch(`${api_link}/PSITS/api/transactions?key=${key}`, {
    method: "PUT",
    body: JSON.stringify({
        reference: ref,
        stat: document.getElementById(button_id).value
    }),
    headers: {"Content-type": "application/json; charset=UTF-8"}
    })
    if(document.getElementById(ref+'idnum').hidden === true){
        document.getElementById(ref+'status').disabled = true;
        document.getElementById(ref+'edit').hidden = false;
        document.getElementById(ref+'button').hidden = true;
    }
    //search_transaction(document.getElementById('search_student').value,document.getElementById('secret_key').value);
}

function hide(element){
    element.style.display = 'none';
}

function showModal(){
    document.getElementById('order-modal').style.display = "flex";
    document.getElementById('transaction_ui').classList.add('blur');
    setTimeout(()=>{
        //document.getElementById('handle_search').focus();
    }, 100);
}

function hideModal(){
    document.getElementById('order-modal').style.display = "none";
    document.getElementById('transaction_ui').classList.remove('blur');
    //document.getElementById('search_student').focus();
}

function updateReceiptEvent(){
    const qty = document.getElementById('info_quantity').value;
    const dc_p = document.getElementById('info_discounted_price').value;
    const status = document.getElementById('info_status').value;

    // render the new data
    document.getElementById('fld_qty').innerHTML = qty;
    document.getElementById('fld_total').innerHTML = `₱${(parseFloat(dc_p).toFixed(2) * parseFloat(qty)).toFixed(2)}`;
    document.getElementById('fld_status').innerHTML = status;

}

async function updateOrder(key){
    let reference_code = document.getElementById('fld_reference').innerHTML;
    if(!reference_code)
        return;
    document.getElementById('updateMessage').style.display = 'none';
    try{
        const response = await fetch(`${api_link}/PSITS/api/transactions?key=${key}`, {
            method: "PUT",
            body: JSON.stringify({
                reference: reference_code,
                stat: document.getElementById('info_status').value,
                info: document.getElementById('info_info').value,
                qty: document.getElementById('info_quantity').value,
            }),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });

        const data = await response.json();
        document.getElementById('updateMessage').innerHTML = data.message;
    }catch(e){
        document.getElementById('updateMessage').innerHTML = 'Failed to update.';
    }
    document.getElementById('updateMessage').style.display = 'flex';

    search_individual_transaction(reference_code, key);
}

function deleteModal(reference, key){
    document.getElementById('transaction_ui').classList.add('blur');
    document.getElementById('delmodalkey').value = key;
    document.getElementById('delmodalref').value = reference;
    document.getElementById('deleteModalInfo').innerHTML = `DELETE ${reference}?`;
    document.getElementById('deleteModal').style.display = 'block';
}

async function delete_transaction(){
    let key = document.getElementById('delmodalkey').value;
    let reference = document.getElementById('delmodalref').value;
    let password = document.getElementById('delmodalpass').value;
    let errMsg = document.getElementById('delModalInfoMsg');
    let user = document.getElementById('userid').value;
    
    try{
        let response = await fetch(`${api_link}/PSITS/api/transactions/${reference}?key=${key}`, {
            method: "DELETE",
            body: JSON.stringify({
                password: `${password}`,
                userid: user
            }),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });
        
        let data = await response.json();

        if(data.status === 200){
            searchString = document.getElementById('search_student').value;
            hide(document.getElementById('deleteModal'));
            document.getElementById('transaction_ui').classList.remove('blur');
            document.getElementById('delmodalpass').value = '';
            search_transaction(searchString, key);
        }else if(data.status === 403){
            errMsg.innerHTML = data.message;
        }
        
    }catch(e){
        errMsg.innerHTML = e;
    }
        
}

function formatToCurrency(amount){
    return (amount).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'); 
}



// filtering
let output_map = new Map();

function clearMap(){
    output_map.clear();
    output_map.set('14', 0);
    output_map.set('16', 0);
    output_map.set('18', 0);
    output_map.set('20', 0);
    output_map.set('S', 0);
    output_map.set('M', 0);
    output_map.set('L', 0);
    output_map.set('XL', 0);
    output_map.set('XXL', 0);
    output_map.set('XXXL', 0);
}

function filterSizesFromInfo(info){
    let fragments = info.split(/[ \n,\r]/);
    for(let index = 0; index < fragments.length; index++){
        if(fragments[index].toLowerCase().includes('size:')){
            // add to map
            let key = fragments[index+1]
            if(typeof key === 'undefined')
                continue;
            if (key === '')
                continue;
            if (key.toLowerCase().includes('color'))
                continue;
            if (key.toLowerCase() === 'large' || key.toLowerCase() === 'l')
                key = 'L';
            else if (key.toLowerCase() === 'medium' || key.toLowerCase() === 'm')
                key = 'M';
            else if (key.toLowerCase() === 'small' || key.toLowerCase() === 's')
                key = 'S';
            else if (key.toLowerCase() === 'xl')
                key = 'XL';
            else if (key.toLowerCase() === 'xxl')
                key = 'XXL';
            else if (key.toLowerCase() === 'xxxl')
                key = 'XXXL';
            if(output_map.has(key)){
                output_map.set(key,output_map.get(key)+1)
            }else output_map.set(key, 1);
        }
    }
}

function displayFilteredSizesFromInfo(){
    const info_box = document.getElementById('filter-message');
    let message ='';
    let quantity = 0;
    message =
    `14 - ${output_map.get('14')}
    16 - ${output_map.get('16')}
    18 - ${output_map.get('18')}
    20 - ${output_map.get('20')}
    S - ${output_map.get('S')}
    M - ${output_map.get('M')}
    L - ${output_map.get('L')}
    XL - ${output_map.get('XL')}
    XXL - ${output_map.get('XXL')}
    XXXL - ${output_map.get('XXXL')}
    `
    output_map.forEach((value, key) => {
        
        quantity += value;
    });
    message += `\nQTY - ${quantity}   `;
    info_box.innerHTML = message;
}


try{
    loadAPI();
}catch(e){}