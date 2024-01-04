function generateTableHead(table, data) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    for (let key of data) {
        let th = document.createElement("th");
        let text = document.createTextNode(key);
        if(key=='address'){text = document.createTextNode("Address")}
        if(key=='bookid'){text = document.createTextNode("Booking ID")}
        if(key=='date_format(checkin,\'%m-%d-%Y\')'){text = document.createTextNode("Check-in date")}
        if(key=='date_format(checkout,\'%m-%d-%Y\')'){text = document.createTextNode("Check-out date")}
        if(key=='hname'){text = document.createTextNode("Hotel Name")}
        if(key=='roomnum'){text = document.createTextNode("Room Number")}
        if(key=='gfirst'){text = document.createTextNode("First Name")}
        if(key=='glast'){text = document.createTextNode("First Name")}
        th.appendChild(text);
        row.appendChild(th);
    }
}

function generateTable(table, data) {
    for (let element of data) {
        let row = table.insertRow();
        for (key in element) {
            let cell = row.insertCell();
            let text = document.createTextNode(element[key]);
            cell.appendChild(text);
        }
    }
}