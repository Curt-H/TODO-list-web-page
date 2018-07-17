//Tool function
let log = console.log.bind(console);

let e = function (selector, parent = document) {
    return parent.querySelector(selector)
};

//Ajax function
let ajax = function (method, path, data, responseCallback) {
    let r = new XMLHttpRequest();
    r.open(method, path, true);
    r.setRequestHeader('Content-Type', 'application/json');
    r.onreadystatechange = function () {
        if (r.readyState === 4) {
            log('load ajax response type:', typeof(r.response));
            log('load ajax response:', r.response);
            let json = JSON.parse(r.response);
            log('load json type:', typeof(json));

            if (r.state_code === '1') {
                alert('ERROR')
            }
            else {
                responseCallback(json)
            }
        }
    };
    data = JSON.stringify(data);
    r.send(data)
};