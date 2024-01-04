function generateTableHead(table, data) {
    let thead = table.createTHead();
    let row = thead.insertRow();
	
	
    for (let key of data) {
        let th = document.createElement("th");
        let text = document.createTextNode(key);
        if(key=='hname'){text = document.createTextNode("Hotel Name")}
        if(key=='xcoord'){text = document.createTextNode("X")}
        if(key=='ycoord'){text = document.createTextNode("Y")}
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