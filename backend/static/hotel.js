

function generateTableHead(table, data,l) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    for (let key of data) {
        let th = document.createElement("th");
        let text = document.createTextNode(key);
        if(key=='roomid'){text = document.createTextNode("Room ID")}
        if(key=='hotelid'){text = document.createTextNode("Hotel ID")}
        if(key=='capacity'){text = document.createTextNode("Capacity")}
        if(key=='roomnum'){text = document.createTextNode("Room Number")}
        if(key=='rType'){text = document.createTextNode("Room Type")}
        if(key=='format(price,2)'){text = document.createTextNode("Price per night ($)")}
        if(key=='hname'){text = document.createTextNode("Hotel Name")}
        if(key=='address'){text = document.createTextNode("Address")}
        if(key=='phone'){text = document.createTextNode("Phone Number")}
        if(key=='xcoord'){text = document.createTextNode("X")}
        if(key=='ycoord'){text = document.createTextNode("Y")}
        th.appendChild(text);
        row.appendChild(th);
    }
    if (l==1){
        let th = document.createElement("th");
        let text = document.createTextNode('Booking Link');
        th.appendChild(text);
        row.appendChild(th);
    }
    
}

function generateTable(table, data,l) {
    for (let element of data) {
        let row = table.insertRow();
        for (key in element) {
            let cell = row.insertCell();
            let text = document.createTextNode(element[key]);
            cell.appendChild(text);
        }
        if (l==1){
            let cell = row.insertCell();
            let text = document.createTextNode("Book now!")
            let link = document.createElement('a');
            link.href = "/makebooking/" + element['roomid'];
            link.appendChild(text);
            cell.appendChild(link);
        }
    }
}
