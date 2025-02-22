let s;
let host = location.hostname;
let room;
let guest = `
<h1>log in:</h1><br>
username:<br>
<input id="name" onkeydown="
    if (event.key === 'Enter') {
        s = connect(this.value);
        document.querySelector('#fails').innerHTML = ''
    }
"><br><br>
<button onclick="
    s = connect(document.querySelector('#name').value);
    document.querySelector('#fails').innerHTML = ''
">enter as guest</button>
<button onclick="
    document.querySelector('#msgs').innerHTML = login;
    document.querySelector('#fails').innerHTML = '';
">back</button>
`;
let login = `
<h1>log in:</h1><br>
username:<br>
<input id="name" onkeydown="
    if (event.key === 'Enter') {
        s = connect(this.value, document.querySelector('#password').value);
        document.querySelector('#fails').innerHTML = ''
    }
"><br>
password:<br>
<input id="password" type="password" onkeydown="
    if (event.key === 'Enter') {
        s = connect(document.querySelector('#name').value, this.value);
        document.querySelector('#fails').innerHTML = ''
    }
">
<br><br>
<button onclick="
    s = connect(document.querySelector('#name').value, document.querySelector('#password').value);
    document.querySelector('#fails').innerHTML = ''
">login</button>
<button onclick="
    document.querySelector('#msgs').innerHTML = reg;
    document.querySelector('#fails').innerHTML = '';
">register</button>
<button onclick="
    document.querySelector('#msgs').innerHTML = guest;
    document.querySelector('#fails').innerHTML = '';
">guest</button>
`;
let reg = `
<h1>register:</h1><br>
username:<br>
    <input id="name" onkeydown="
        if (event.key === 'Enter') {
            s = connect(this.value, document.querySelector('#password').value, true);
            document.querySelector('#fails').innerHTML = ''
        }
    "><br>password:<br>
    <input id="password" type="password" onkeydown="
        if (event.key === 'Enter') {
            s = connect(document.querySelector('#name').value, this.value, true);
            document.querySelector('#fails').innerHTML = ''
        }
    "><br><br>
    <button onclick="
        s = connect(document.querySelector('#name').value, document.querySelector('#password').value, true);
        document.querySelector('#fails').innerHTML = ''
    ">register</button>
    <button onclick="
        document.querySelector('#msgs').innerHTML = login;
        document.querySelector('#fails').innerHTML = '';
    ">back</button>
    <button onclick="
    document.querySelector('#msgs').innerHTML = guest;
    document.querySelector('#fails').innerHTML = '';
">guest</button>
`;
let sen = `
        <input id="send" onkeydown="
            if (event.key === 'Enter') {
                send(s, this.value);
                this.value = '';
                document.querySelector('#fails').innerHTML = '';
            }    
        ">
        <button onclick="
            send(s, document.querySelector('#send').value);
            document.querySelector('#send').value = '';
            document.querySelector('#fails').innerHTML = '';
        ">send</button> <button onclick="
            send(s, 'room', 'leave');
            document.querySelector('#game').style = '';
            document.querySelector('#game').innerHTML = '';
            document.querySelector('#msgs').innerHTML = cr;
            document.querySelector('#fails').innerHTML = '';
            rom = false;
        ">leave room</button>
        <iframe id="msges"></iframe>
        <br>
        <button onclick="show_profile()">show profile</button>
    `;
let cr = `<input id="cr" onkeydown="
            if (event.key === 'Enter') {
                if (this.value == '') {
                    document.querySelector('#passpan').innerHTML = \`<br>password (optional): <input type='password' id='pasi'><button id='pasb'>create</button>\`;
                    let newInput = document.querySelector(\`#pasi\`);
                    newInput.focus();
                    newInput.onkeydown = (e) => {
                        if (e.key === 'Enter') {
                            if (e.target.value === '') {
                                send(s, [null, null], 'create');
                            }
                            else {
                                send(s, [null, e.target.value], 'create');
                            }
                        }
                    }
                    newInput = document.querySelector(\`#pasb\`);
                    newInput.onclick = (e) => {
                        if (document.querySelector(\`#pasi\`).value === '') {
                            send(s, [null, null], 'create');
                        }
                        else {
                            send(s, [null, document.querySelector(\`#pasi\`).value], 'create');
                        }
                    }
                }
                else {
                    document.querySelector('#passpan').innerHTML = \`<br>password (optional): <input id='pasi' type='password'><button id='pasb'>create</button>\`;
                    let newInput = document.querySelector(\`#pasi\`);
                    newInput.focus();
                    newInput.onkeydown = (e) => {
                        if (e.key === 'Enter') {
                            if (e.target.value === '') {
                                send(s, [String(this.value), null], 'create');
                            }
                            else {
                                send(s, [String(this.value), e.target.value], 'create');
                            }
                        }
                    }
                    newInput = document.querySelector(\`#pasb\`);
                    newInput.onclick = (e) => {
                        if (document.querySelector(\`#pasi\`).value === '') {
                            send(s, [null, null], 'create');
                        }
                        else {
                            send(s, [null, document.querySelector(\`#pasi\`).value], 'create');
                        }
                    }
                }
            }
        "><span id="passpan">
        <button onclick="
            if (document.querySelector(\`#cr\`).value == '') {
                    document.querySelector('#passpan').innerHTML = \`<br>password (optional): <input id='pasi' type='password'><button id='pasb'>create</button>\`;
                    let newInput = document.querySelector(\`#pasi\`);
                    newInput.focus();
                    newInput.onkeydown = (e) => {
                        if (e.key === 'Enter') {
                            if (e.target.value === '') {
                                send(s, [null, null], 'create');
                            }
                            else {
                                send(s, [null, e.target.value], 'create');
                            }
                        }
                    }
                    newInput = document.querySelector(\`#pasb\`);
                    newInput.onclick = (e) => {
                        if (document.querySelector(\`#pasi\`).value === '') {
                            send(s, [null, null], 'create');
                        }
                        else {
                            send(s, [null, document.querySelector(\`#pasi\`).value], 'create');
                        }
                    }
                }
                else {
                    document.querySelector('#passpan').innerHTML = \`<br>password: <input id='pasi' type='password'><button id='pasb'>create</button>\`;
                    let newInput = document.querySelector(\`#pasi\`);
                    newInput.focus();
                    newInput.onkeydown = (e) => {
                        if (e.key === 'Enter') {
                            if (e.target.value === '') {
                                send(s, [String(document.querySelector(\`#cr\`).value), null], 'create');
                            }
                            else {
                                send(s, [String(document.querySelector(\`#cr\`).value), e.target.value], 'create');
                            }
                        }
                    }
                    newInput = document.querySelector(\`#pasb\`);
                    newInput.onclick = (e) => {
                        if (document.querySelector(\`#pasi\`).value === '') {
                            send(s, [null, null], 'create');
                        }
                        else {
                            send(s, [null, document.querySelector(\`#pasi\`).value], 'create');
                        }
                    }
                }
        ">create</button></span><br><br>
        <button onclick="show_profile()">show profile</button>
    `;
let pos;
let color = [];
let friends = [];
let xp = 0;
let rom;
color[0] = Math.floor(Math.random() * (255 - 0 + 1)) + 0
color[1] = Math.floor(Math.random() * (255 - 0 + 1)) + 0
color[2] = Math.floor(Math.random() * (255 - 0 + 1)) + 0
window.onload = (e) => {
    document.querySelector('#colors').style.color = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
    document.querySelector('#col').value = rgb2hex(color);
}

let connect = function(name, password = null, reg = false) {
    const s = new WebSocket(`ws://${host}:5001`);
    s.onopen = function() {
        if (password === null){
            if (name !== '') {
                send(s, [name, color], 'gue');
            }
            else{
                document.querySelector('#fails').innerHTML = 'please write a name';
            }
        }
        else if (reg) {
            if (name !== '' && password !== '') {
                send(s, [name, color, password], 'reg');
            }
            else if (name === '') {
                document.querySelector('#fails').innerHTML = 'please write a name';
            }
            else if (password === '') {
                document.querySelector('#fails').innerHTML = 'please write a password';
            }
        }
        else {
            if (name !== '' && password !== '') {
                send(s, [name, color, password], 'login');
            }
            else if (name === '') {
                document.querySelector('#fails').innerHTML = 'please write a name';
            }
            else if (password === '') {
                document.querySelector('#fails').innerHTML = 'please write a password';
            }
        }
    };
    s.onmessage = function(e) {
        let header = JSON.parse(e.data)[0];
        let msg = JSON.parse(e.data)[1];
        const response_headers = {
            1: 'success',
            2: 'fail',
            3: 'name',
            4: 'xp',
            5: 'friend',
            6: 'rm_name',
            7: 'rm_ppl',
            8: 'sys',
            9: 'uate',
            10: 'rowcount',
            11: 'sql',
            12: 'sqlerr',
            13: 'pyres',
            14: 'rooms',
            15: 'move',
            16: 'ate',
            17: 'msg'
        }
        header = response_headers[header]
        console.log(`${header}: ${msg}`);
        if (header === 'msg'){
            let mes = `<span style="color:rgb(${msg[2][0]},${msg[2][1]},${msg[2][2]});">${msg[0]}</span>: ${msg[1]}`;
            document.querySelector('#msges').contentWindow.document.body.innerHTML += `${mes}<br>`;
            document.querySelector('#msges').contentWindow.document.body.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
        else if (header === 'sys') {
            let mes = `<span style="color: #edae14;">*${msg}*</span>`;
            document.querySelector('#msges').contentWindow.document.body.innerHTML += `${mes}<br>`;
            document.querySelector('#msges').contentWindow.document.body.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
        else if (header === 'rooms') {
            let text = "";
            msg.forEach((v) => {
                if (v[2]) {
                    if (v[1].length !== 0) {
                        let friend = v[1][0];
                        v[1].slice(1, v[1].length).forEach((val) => {friend += `, ${val}`});
                        text += `${v[0]} <button onclick="
                            setpassw(\`${v[0]}\`);
                            document.querySelector('#fails').innerHTML = '';
                        ">join</button> friends in room: ${friend} <span id="passw"></span><br>`;
                    }
                    else {
                        text += `${v[0]} <button onclick="
                            setpassw(\`${v[0]}\`);
                            document.querySelector('#fails').innerHTML = '';
                        ">join</button> <span id="passw"></span><br>`;
                    }
                }
                else {
                    if (v[1].length !== 0) {
                        let friend = v[1][0];
                        v[1].slice(1, v[1].length).forEach((val) => {friend += `, ${val}`});
                        console.log(v[1])
                        text += `${v[0]} <button onclick="
                        send(s, [\`${v[0]}\`, null], 'join')
                        document.querySelector('#fails').innerHTML = '';
                    ">join</button> friends in room: ${friend}<br>`;
                    }
                    else {
                        text += `${v[0]} <button onclick="
                            send(s, [\`${v[0]}\`, null], 'join')
                            document.querySelector('#fails').innerHTML = '';
                        ">join</button><br>`;
                    }
                }
            });
            document.querySelector("#rooms").innerHTML = text;
        }
        else if (header === 'fail'){
            document.querySelector('#fails').innerHTML = msg;
        }
        else if (header === 'success') {
            if (msg === 'room') {
                rom = true;
                document.querySelector('#msgs').innerHTML = sen;
                document.querySelector('#rooms').innerHTML = '';
                document.querySelector('#fails').innerHTML = '';
                document.querySelector("#game").style.width = '430px';
                document.querySelector("#game").style.height = '400px';
                document.querySelector("#game").style.border = 'black';
                document.querySelector("#game").style.borderWidth = '1px';
                document.querySelector("#game").style.borderStyle = 'solid';
                pos = [0, 0];
                send(s, pos, 'move');
            }
            else if (msg === 'name') {
                document.querySelector('#msgs').innerHTML = cr;
                document.querySelector('#logout').innerHTML = `<button onclick="s.close(); location.reload();">log out</button>`;
            }
            else if (msg[0] === 'name' && msg[1] == true) {
                document.querySelector("#userset").innerHTML = '';
                document.querySelector('#msgs').innerHTML = cr;
                document.querySelector('#logout').innerHTML = `<button onclick="s.close(); location.reload();">log out</button>`;
            }
        }
        else if (header === 'move') {
            let mes = '';
            for (let i = 0; i < msg.length; i++) {
                let m = msg[i];
                mes += `<div class="player" style="top:${m[1][0]}px;left:${m[1][1]}px;background-color:rgb(${m[2][0]},${m[2][1]},${m[2][2]});"><div class="name">${m[0]}</div></div>`;
            }
            document.querySelector("#game").innerHTML = mes;
        }
        else if (header === 'rm_name') {
            if (msg === '') {
                document.querySelector("#name").innerHTML = msg;
            }
            else {
                document.querySelector("#name").innerHTML = `room: ${msg}`;
            }
            room = msg;
        }
        else if (header === 'rm_ppl') {
            if (msg === '') {
                document.querySelector("#ppl").innerHTML = '';
            }
            else {
                let txt = '';
                msg.forEach((v, i) => {
                    if (v[0] === document.querySelector("#usrname").innerHTML){
                        msg[i][0] = 'you';
                    }
                })
                msg.forEach((v, i) => {
                    if (i !== msg.length - 1) {
                        if (v[2]) {
                            if (v[1]) {
                                txt += `${v[0]} (host), `;
                            }
                            else {
                                txt += `${v[0]} (host)<span id="${v[0]}0"> <button onclick="send(s, '${v[0]}', 'addf'); document.querySelector('#${v[0]}0').innerHTML = '';">add</button></span>, `;
                            }
                        }
                        else {
                            if (v[1]) {
                                txt += `${v[0]}, `;
                            }
                            else {
                                txt += `${v[0]}<span id="${v[0]}0"> <button onclick="send(s, '${v[0]}', 'addf'); document.querySelector('#${v[0]}0').innerHTML = '';">add</button></span>, `;
                            }
                        }
                    }
                    else {
                        if (v[2]) {
                            if (v[1]) {
                                txt += `${v[0]} (host)`;
                            }
                            else {
                                txt += `${v[0]} (host)<span id="${v[0]}0"> <button onclick="send(s, '${v[0]}', 'addf'); document.querySelector('#${v[0]}0').innerHTML = '';">add</button></span>`;
                            }
                        }
                        else {
                            if (v[1]) {
                                txt += `${v[0]}`;
                            }
                            else {
                                txt += `${v[0]}<span id="${v[0]}0"> <button onclick="send(s, '${v[0]}', 'addf'); document.querySelector('#${v[0]}0').innerHTML = '';">add</button></span>`;
                            }
                        }
                    }
                });
                document.querySelector("#ppl").innerHTML = `participants: ${txt}`;
            }
        }
        else if (header === 'name') {
            document.querySelector('#username').innerHTML = `username:`;
            document.querySelector('#usrname').innerHTML = `${msg}`;
        }
        else if (header === 'xp') {
            xp = msg
            document.querySelector('#xp').innerHTML = xp
        }
        else if (header === 'uate') {
            pos = [0, 0];
        }
        else if (header === 'ate') {
            let mes = `<span style="color:rgb(${msg[1][0][0]},${msg[1][0][1]},${msg[1][0][2]});">${msg[0][0]}</span> ate <span style="color:rgb(${msg[1][1][0]},${msg[1][1][1]},${msg[1][1][2]});">${msg[0][1]}</span>`
            document.querySelector('#msges').contentWindow.document.body.innerHTML += `${mes}<br>`;
            document.querySelector('#msges').contentWindow.document.body.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
        else if (header === 'friend') {
            friends = msg
            document.querySelector('#friends').innerHTML = ``
            if (friends.length !== 0) {
                if (friends.length === 1) {
                    document.querySelector('#friends').innerHTML = `friends: <span id="f0">${friends[0]}<button class="remf" onclick="send(s, '${friends[0]}', 'remf'); document.querySelector('#friends').innerHTML = ''">remove</button><br></span>`;
                }
                else {
                    document.querySelector('#friends').innerHTML = `friends:`;
                    friends.forEach((v, i) => {
                        document.querySelector('#friends').innerHTML += `<span id="f${i}">${v}<button class="remf" onclick="send(s, '${v}', 'remf'); document.querySelector('#f${i}').innerHTML = ''">remove</button><br></span>`;
                    });
                }
            }
        }
    }
    return s
}


let move = function(e) {
    let focus = document.activeElement;
    if (e.key === 'Enter') {
            if (focus !== document.querySelector('input')) {
                document.querySelector('input').focus()
                focus = document.activeElement;
            }
            else {
                document.body.focus();
                document.activeElement.blur();
            }
    }
    if (focus === document.body) {
        if (e.key === 'ArrowUp') {
            if (pos[0] !== 0) {
                pos[0] -= 14;
                send(s, pos, 'move');
            }
        }
        else if (e.key === 'ArrowDown') {
            if (pos[0] + 30 < 390) {
                pos[0] += 14;
                send(s, pos, 'move');
            }
        }
        else if (e.key === 'ArrowRight') {
            if (pos[1] + 30 < 420) {
                pos[1] += 14;
                send(s, pos, 'move');
            }
        }
        else if (e.key === 'ArrowLeft') {
            if (pos[1] !== 0) {
                pos[1] -= 14;
                send(s, pos, 'move');
            }
        }
        else if (e.key === ' ') {
            send(s, pos, 'eat');
        }
    }
}


document.addEventListener('keydown', move)


let send = function(s, msg, header = 'msg') {
    const headers = {
        'login': 0,
        'reg': 1,
        'create': 2,
        'join': 3,
        'col': 4,
        'leave': 5,
        'msg': 6,
        'move': 7,
        'eat': 8,
        'del': 9, 
        'changep': 10,
        'addf': 11,
        'remf': 12,
        'sql': 13,
        'py': 14,
        'gue': 15
    }
    if (msg !== '') {
        s.send(JSON.stringify([headers[header], msg]));
    }
}

let show_profile = function() {
    document.querySelector('#xpname').innerHTML = document.querySelector('#usrname').innerHTML;
    document.querySelector('#profile').style.visibility = 'visible';
}


function setpassw(name) {
    document.querySelector('#passw').innerHTML = `<input id="passwo">`;
    let newInput = document.querySelector(`#passwo`);
    newInput.focus();
    newInput.onkeydown = (e) => {
        if (e.key === 'Enter') {
            send(s, [`${name}`, e.target.value], 'join');
            document.querySelector('#fails').innerHTML = '';
        }
    };
}

function hex2rgb(hex) {
    let r = parseInt(hex.slice(1, 3), 16);
    let g = parseInt(hex.slice(3, 5), 16);
    let b = parseInt(hex.slice(5, 7), 16);
    return [r, g, b];
}


let componentToHex = (c) => {
    let hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}


function rgb2hex(rgb) {
    return "#" + componentToHex(rgb[0]) + componentToHex(rgb[1]) + componentToHex(rgb[2]);
}
