
/*
    Sending GET request to API
*/
async function search_transaction(searchData, key){

    let info_box = document.getElementById('info_box');
    let info_msg = document.getElementById('info_message');

    info_box.style.display = "block";
    
    let data;
    try{
        // searching transactions, must have a key for authentication
        const response = await fetch(`/PSITS/api/transactions/${new String(searchData)}?key=${key}`,{
            headers: {
                Authorization: key
            }
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

        // display the necessary data
        document.getElementById('display_reserve').innerHTML = data.reserve.toFixed(2);
        document.getElementById('display_paid').innerHTML = data.paid.toFixed(2);
        document.getElementById('display_total').innerHTML = data.total.toFixed(2);
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

    for(const order of data.ORDERS){

        let form_body = document.createElement('form');
        form_body.method = 'POST';
        form_body.action = '';

        let table_row = document.createElement("tr");

        // invisible name data
        let input_field = document.createElement('input');
        let table_col = document.createElement("td");

        input_field = document.createElement('input');
        input_field.setAttribute('id', order.order.uid+"idnum");
        input_field.name = 'order_ref';
        input_field.hidden = true;
        input_field.value = `${order.reference}`

        table_row.appendChild(input_field);

        // ref
        table_col = document.createElement("td");
        input_field = document.createElement('input');
        input_field.setAttribute('class', 'hide');
        input_field.setAttribute('id', order.order.uid+"ref");
        input_field.disabled = true;
        input_field.value = order.reference

        table_col.appendChild(input_field);
        table_row.appendChild(table_col);

        // name
        table_col = document.createElement("td");
        input_field = document.createElement('input');
        input_field.setAttribute('id', order.order.uid+"name");
        input_field.disabled = true;
        input_field.value = `${order.account.firstname} ${order.account.lastname}`

        table_col.appendChild(input_field);
        table_row.appendChild(table_col);

        // prod
        table_col = document.createElement("td");
        input_field = document.createElement('input');
        input_field.setAttribute('id', order.order.uid+"prod");
        input_field.disabled = true;
        input_field.value = `${order.merch.title}`

        table_col.appendChild(input_field);
        table_row.appendChild(table_col);

        // add info
        table_col = document.createElement("td");
        input_field = document.createElement('p');
        input_field.setAttribute('style', 'white-space: pre-line');
        input_field.setAttribute('class', 'information hide');
        input_field.innerHTML = `${order.order.additional_info}&#8203;&nbsp;`

        table_col.appendChild(input_field);
        table_row.appendChild(table_col);

        // quantity
        table_col = document.createElement("td");
        table_col.setAttribute('class', 'hide');
        input_field = document.createElement('input');
        input_field.setAttribute('id', order.order.uid+"qty");
        input_field.disabled = true;
        input_field.value = `${order.order.quantity}`;

        table_col.appendChild(input_field);
        table_row.appendChild(table_col);

        // amount
        table_col = document.createElement("td");
        table_col.setAttribute('class', 'hide');
        input_field = document.createElement('input');
        input_field.setAttribute('id', order.order.uid+"qty");
        input_field.disabled = true;
        input_field.value = `₱${(order.getTotal * order.order.quantity).toFixed(2)}`;

        table_col.appendChild(input_field);
        table_row.appendChild(table_col);

        // selection
        table_col = document.createElement("td");

        let selection = document.createElement('select');
        selection.name ='status'
        selection.setAttribute('id', order.order.uid+"status");
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
        
        if(order.getStatus === 'ORDERED'){
            option_ordered.selected = true;
            selection.options.add(option_ordered);
            selection.options.add(option_paid);
            selection.options.add(option_cancelled);
        }else if(order.getStatus === 'PAID'){
            option_paid.selected = true;
            selection.options.add(option_paid);
            selection.options.add(option_claimed);
        }else if(order.getStatus === 'CANCELLED'){
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
        button_edit.setAttribute('id', order.order.uid+"edit");
        button_edit.setAttribute('class', 'normalButton')
        button_edit.setAttribute('onclick',`editOrderStatus(${order.order.uid});return;`)
        button_edit.innerHTML = '✎';

        let button_save = document.createElement('button');
        button_save.setAttribute('id', order.order.uid+"button");
        button_save.setAttribute('class', 'normalButton')
        button_save.setAttribute('onclick',`update_transaction('${order.reference}','${order.order.uid+"status"}','${key}');return;`)
        button_save.hidden = true;
        button_save.innerHTML = '💾';
        button_save.type = "button";
        

        table_col.appendChild(button_edit);
        table_col.appendChild(button_save);
        table_row.appendChild(table_col);
        
        //
        form_body.appendChild(table_row);
        
        // append all the row data into the table body
        table_body.appendChild(table_row)
        
    }

    
}

async function search_individual_transaction(searchData, key){
    let info_box = document.getElementById('info_box');
    let info_msg = document.getElementById('info_message');

    info_box.style.display = "block";

    let data;

    // clear the receipt
    updateReceipt();
    
    try{
        // searching transactions, must have a key for authentication
        const response = await fetch(`/PSITS/api/transactions/${new String(searchData)}?key=${key}`);

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
            let single_order = data.ORDERS[0];

            new QRCode(document.getElementById("qrcode"), {
                text: single_order.reference,
                width: 275,
                height: 275,
                colorDark : "#000000",
                colorLight : "#ffffff",
                correctLevel : QRCode.CorrectLevel.H
            });

            
            updateReceipt(
                name=`${single_order.account.firstname} ${single_order.account.lastname}`,
                product=`${single_order.merch.title}`,
                price=`${single_order.merch.price}`,
                discounted_price=`${(single_order.getTotal)}`,
                date=`${single_order.order.order_date}`,
                quantity=`${single_order.order.quantity}`,
                total=`${(single_order.getTotal * single_order.order.quantity)}`,
                status=`${single_order.order.status}`,
                info=`${single_order.order.additional_info}`,
                ref=`${single_order.reference}`
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
    document.getElementById('info_info').value = info;
    document.getElementById('info_price').value = price?parseFloat(price).toFixed(2):'';
    document.getElementById('info_discounted_price').value = discounted_price?parseFloat(discounted_price).toFixed(2):'';
    document.getElementById('info_quantity').value = quantity;
    document.getElementById('info_status').value = status;

    if(status)
        document.getElementById('info_status').disabled = false;
    else document.getElementById('info_status').disabled = true;
    if(quantity && price){
        document.getElementById('info_quantity').disabled = false;
    }else document.getElementById('info_quantity').disabled = true;
    if(info){
        document.getElementById('info_info').disabled = false;
    }else document.getElementById('info_info').disabled = true;
        
}

function editOrderStatus(uid){
    if(document.getElementById(uid+'idnum').hidden === true){
        document.getElementById(uid+'status').disabled = false;
        document.getElementById(uid+'edit').hidden = true;
        document.getElementById(uid+'button').hidden = false;
    }
}

async function update_transaction(ref, button_id, key){
    await fetch(`/PSITS/api/transactions?key=${key}`, {
    method: "PUT",
    body: JSON.stringify({
        reference: ref,
        stat: document.getElementById(button_id).value
    }),
    headers: {"Content-type": "application/json; charset=UTF-8"}
    })
    
    search_transaction(document.getElementById('search_student').value,document.getElementById('secret_key').value);
}

function hide(element){
    element.style.display = 'none';
}

function showModal(){
    document.getElementById('order-modal').style.display = "flex";
    document.getElementById('transaction_ui').classList.add('blur');
    setTimeout(()=>{
        document.getElementById('handle_search').focus();
    }, 100);
}

function hideModal(){
    document.getElementById('order-modal').style.display = "none";
    document.getElementById('transaction_ui').classList.remove('blur');
    document.getElementById('search_student').focus();
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
    try{
        const response = await fetch(`/PSITS/api/transactions?key=${key}`, {
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

search_transaction(document.getElementById('search_student').value,document.getElementById('secret_key').value);
