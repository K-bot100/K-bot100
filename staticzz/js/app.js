let overlay = document.getElementById('overlay');

async function farmers() {
    const response = await fetch('https://api.koafarmer.com/farmer');
    return await response.json();
}

async function new_row() {
    overlay.style.display = 'block'
    let tbody = document.getElementById('tb');
    let b = tbody.childElementCount + 1
    var nrow = document.createElement("tr");
    nrow.innerHTML = `
        <td> <select id='vc${b}' name="farmerid${b}" placeholder="farmerid" id="farmerid${b}" required ></select></td>
        <td> <input type="text" name="name${b}" placeholder="Name" id="name${b}" required readonly/></td>        
        <td><input type="text" name="number${b}" placeholder="Number" id="number${b}" required readonly /></td>
        <td> <input type="text" name="comm${b}" placeholder="Community" id="comm${b}" required readonly/></td>
                
        <td>
            <select name="ptype${b}" id="ptype${b}" required>
                <option value=""></option>
                <option value="pulp">Pulp</option>
                <option value="juice">Juice</option>
            </select>
        </td>
        <td><input type="number" min="0.5" step="0.5" name="bkt${b}" id="bkt${b}" required /></td>

        <td><input type="text" name="amt${b}" style="color:black" placeholder="Amount" id="amt${b}" required readonly /></td>
       
        <td><input type="button" id="trow${b}" class="btn btn-danger" value="Del" onclick="delrow()"></td>`;

    // <td><input type="text" name="rmk${b}" placeholder="eg: 10 bags" id="rmk${b}" required /></td>   //not needed now
    nrow.setAttribute("id", `row${b}`)
    tbody.appendChild(nrow)

    let data = await farmers();
    var options = '<option value="" selected></option>';
    for (var key in data) {
        options += `<option value='${key}'>${data[key]['farmer_id']}</option>`;
    }
    let ee = document.getElementById(`vc${b}`)
    ee.innerHTML = options



    let nptype = document.getElementById(`ptype${b}`)
    let nbkt = document.getElementById(`bkt${b}`)
        //let rmk = document.getElementById(`rmk${b}`)
    let amt = document.getElementById(`amt${b}`)



    nptype.addEventListener('change', function() {

        //nbkt.value=999;
        //amt.value=nbkt.value - 9;
        if (nptype.value === 'pulp') {
            amt.value = nbkt.value * 12;
        } else if (nptype.value === 'juice') {
            amt.value = nbkt.value * 10;
        } else {
            amt.value = ''
        }
    })


    nbkt.addEventListener('input', function() {

        //nbkt.value=999;
        //amt.value=nbkt.value - 9;
        if (nptype.value === 'pulp') {
            amt.value = nbkt.value * 12;
        } else if (nptype.value === 'juice') {
            amt.value = nbkt.value * 10;
        } else {
            amt.value = ''
        }
    })




    ee.addEventListener('change', function() {
        let vv = ee.value
        let farmer_momo_number = data[vv]['momo']
        let farmer_name = data[vv]['full_name']
        let farmer_comm = data[vv]['community']
        let nname = document.getElementById(`name${b}`)
        let nnum = document.getElementById(`number${b}`)
        let comm = document.getElementById(`comm${b}`)

        nname.value = farmer_name
        comm.value = farmer_comm
        nnum.value = farmer_momo_number

        /*
        let nptype = document.getElementById(`ptype${b}`)
        let nbkt = document.getElementById(`bkt${b}`)
        //let rmk = document.getElementById(`rmk${b}`)
        let amt = document.getElementById(`amt${b}`)
        */

        //rmk.value = '';
        amt.value = '';
        nbkt.value = '';
        nptype.value = '';
    })

    overlay.style.display = 'none'



}

let sendbtn = document.getElementById('sendbtn');
let sendbtn1 = document.getElementById('sendbtn1');

let Form = document.getElementById('form')

sendbtn.addEventListener('click', function(event) {
    let tbody = document.getElementById('tb');
    let b = tbody.childElementCount;
    if (b < 1) {

        event.preventDefault();
    } else if ((b >= 1) && (Form.checkValidity() == true)) {

        event.preventDefault();
        let smodal = document.getElementById("send-modal");
        smodal.style.zIndex = 5;
        smodal.style.opacity = 1;
        smodal.style.display = "block";
        let y = document.getElementById("y");
        let n = document.getElementById("n");
        y.addEventListener('click', function() {
            Form.submit();
            overlay.style.display = 'block';
            smodal.style.zIndex = -5;
        smodal.style.opacity = 0;
        smodal.style.display = "none";
        })
        n.addEventListener('click', function() {
            smodal.style.display = "none";
        })

    }

    //Form.preventDefault();
})




function delrow() {
    // event.target will be the input element.
    var td = event.target.parentNode;
    var tr = td.parentNode; // the row to be removed

    var delmodal = document.getElementById("delmodal");
    delmodal.style.zIndex = 5;
    delmodal.style.opacity = 1;
    delmodal.style.display = 'block';

    let yy = document.getElementById("yy");
    let nn = document.getElementById("nn");

    yy.addEventListener('click', function() {
        tr.parentNode.removeChild(tr);
        delmodal.style.zIndex = -5;
    delmodal.style.opacity = 0;
        delmodal.style.display = "none";
    });
    nn.addEventListener('click', function() {
        delmodal.style.display = "none";
    });
}
