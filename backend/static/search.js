function generateTableHead(table, data) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    let counter = 0;
    for (let key of data) {
        
        let th = document.createElement("th");
        let text = document.createTextNode(key);
        if(key=='hname'){text = document.createTextNode("Hotel Name")}
        if(key=='hotelid'){text = document.createTextNode("Hotel ID")}
        if(key=='count(*)'){text = document.createTextNode("Number of available rooms")}
        if(key=='format(min(price),2)'){text = document.createTextNode("Price per night ($)")}
        th.appendChild(text);
        row.appendChild(th);
        th.style.cursor = "pointer";
        th.id = counter;
        th.onclick = function () { sortTable(this.id); };
        console.log(th.onclick);
        counter++;

    }
    let th = document.createElement("th");
    let text = document.createTextNode('Hotel Link');
    th.appendChild(text);
    row.appendChild(th);
}

function generateTable(table, data) {
    for (let element of data) {
        let row = table.insertRow();
        for (key in element) {
            let cell = row.insertCell();
            let text = document.createTextNode(element[key]);
            cell.appendChild(text);
        }
        let cell = row.insertCell();
        let text = document.createTextNode("Book now!")
        let link = document.createElement('a');
        link.href = "/hotel/" + element['hotelid'];
        link.appendChild(text);
        cell.appendChild(link);
    }
}

function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("tbl");
    switching = true;
    // Set the sorting direction to ascending:
    dir = "asc";
    /* Make a loop that will continue until
    no switching has been done: */
    while (switching) {
        // Start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /* Loop through all table rows (except the
        first, which contains table headers): */
        for (i = 1; i < (rows.length - 1); i++) {
            // Start by saying there should be no switching:
            shouldSwitch = false;
            /* Get the two elements you want to compare,
            one from current row and one from the next: */
            x = rows[i].getElementsByTagName("td")[n];
            y = rows[i + 1].getElementsByTagName("td")[n];
            console.log(document.getElementById('tbl').rows[1].getElementsByTagName('td')[n]);
            /* Check if the two rows should switch place,
            based on the direction, asc or desc: */
            if (!isNaN(x.innerText.toLowerCase())){
                if (dir == "asc") {
                    if (Number(x.innerText.toLowerCase()) > Number(y.innerText.toLowerCase())) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                } else if (dir == "desc") {
                    if (Number(x.innerText.toLowerCase()) < Number(y.innerText.toLowerCase())) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                }
            }
            if (isNaN(x.innerText.toLowerCase())){
                if (dir == "asc") {
                    if (x.innerText.toLowerCase() > y.innerText.toLowerCase()) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                } else if (dir == "desc") {
                    if (x.innerText.toLowerCase() < y.innerText.toLowerCase()) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                }
            }
        }
        if (shouldSwitch) {
            /* If a switch has been marked, make the switch
            and mark that a switch has been done: */
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            // Each time a switch is done, increase this count by 1:
            switchcount++;
        } else {
            /* If no switching has been done AND the direction is "asc",
            set the direction to "desc" and run the while loop again. */
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}
