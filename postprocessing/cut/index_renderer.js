module.exports = {
    start: start
}
function start(ipc) {
    var added = 1
    var tabindex = 0;
    var selected;
    var filename = ""
    var cur_frame = 1
    var last_cut = 0
        
    document.querySelector('#srcbtn').addEventListener('click', function (event) {
         ipc.send('open-file-dialog2', 'src')
    });

    document.querySelector('#dstbtn').addEventListener('click', function (event) {
        ipc.send('open-file-dialog', 'dst')
    });

    ipc.on('selected-file', function (event, tag, path) {
        let id = tag + "-file"
        let txt_arr = `${path}`.split("/")
        let txt_cand = txt_arr[txt_arr.length -1]
        let len = Math.min(txt_cand.length, 20)
        let txt = txt_arr[txt_arr.length -1].substring(0, len)
        filename = path
        if(len < txt_cand.length){
            document.getElementyId(id).innerHTML = txt + "..."
        }else{

            document.getElementById(id).innerHTML = txt
        }
    });

    ipc.on('update-status', function (event, id, val) {
        let h_id = "debug"
        cur_frame = parseInt(val)
        document.getElementById(h_id).innerHTML = `${val}`
        document.getElementById(h_id).setAttribute('style', 'color:grey')
    });

    ipc.on('update-image', function (event, id, val) {
        let h_id = "cut_image"

        let img = document.getElementById(h_id)
        img.src = `${val}`
        if(selected) selected.className= '';   

    });

    ipc.on('selected-directory', function (event, tag, path) {
        let id = tag + "-directory"
        document.getElementById(id).innerHTML = `${path}`
    });

    document.querySelector('#mylist').addEventListener('click', function(e) {   
        
        if(e.target.tagName === 'LI') { 
            if(selected) selected.className= '';    
            e.target.className= 'selected';                                      
            selected= document.querySelector('li.selected');                   
            let arr = selected.innerHTML.split(" ")
            let dst = document.getElementById('dst-directory').innerHTML
            let img_txt = dst + "/cut_" + arr[arr.length -1] + ".jpg"
            
            ipc.send('change_frame', arr[arr.length -1])
            let h_id = "cut_image"
            let img = document.getElementById(h_id).src = img_txt
            
            
            let start_fr = document.getElementById("start_frame")
            start_fr.value = arr[2]
            let end_fr = document.getElementById("end_frame")
            end_fr.value = arr[4]
            
            let label = document.getElementById("editing_frame")
            label.innerHTML = "Add text: " + selected.innerHTML
        }
      });


    document.querySelector('#cut').addEventListener('click', function (event) {
        let list = document.querySelector('#mylist')
        //let btn = document.querySelector('#play')
        //btn.innerHTML="Blah"
        var entry = document.createElement('li');
        entry.tabIndex =  tabindex;
        tabindex++
        ipc.send('add_cut', 'herp')
        let start_frame = Math.min(last_cut + 1, cur_frame)
        
        entry.appendChild(document.createTextNode("Seq from " + start_frame + " to " + cur_frame));
        added ++
        last_cut = cur_frame
        list.appendChild(entry);
    });


    document.querySelector('#edit_frames').addEventListener('click', function (event) {
        if(selected){
            let start_fr = document.getElementById("start_frame").value    
            let end_fr = document.getElementById("end_frame").value

            if(start_fr >= 1 && end_fr >= start_fr){
                selected.innerHTML = "Seq from " + start_fr + " to " + end_fr
            }

        }
        });

    document.querySelector('#up').addEventListener('click', function (event) {
        let mylist = document.querySelector('#mylist')
        let list = document.querySelector('#mylist').getElementsByTagName("li")
        
        if(selected){
            //document.getElementById(h_id).innerHTML = "Selected " + list.indexOf(selected) 
            var i;
            var found = -1
            for(i = 0; i < list.length; i++){

                if(list[i].innerHTML == selected.innerHTML){

                    found = i
                }
                
                
            }
            if(found > 0){
                
                let prev = list[found -1]
                var newItem = document.createElement("LI");       // Create a <li> node
                var textnode = document.createTextNode(prev.innerHTML);  // Create a text node
                newItem.appendChild(textnode);                    // Append the text to <li>
                mylist.removeChild(prev)
                mylist.insertBefore(newItem, selected.nextSibling)
            }
        }
    });


    document.querySelector('#down').addEventListener('click', function (event) {
        let mylist = document.querySelector('#mylist')
        let list = document.querySelector('#mylist').getElementsByTagName("li")
        
        if(selected){
            //document.getElementById(h_id).innerHTML = "Selected " + list.indexOf(selected) 
            var i;
            var found = -1
            for(i = 0; i < list.length; i++){

                if(list[i].innerHTML == selected.innerHTML){

                    found = i
                }
                
                
            }
            if(found >= 0 && found < list.length -1){
                
                let next = list[found + 1]
                var newItem = document.createElement("LI");       // Create a <li> node
                var textnode = document.createTextNode(next.innerHTML);  // Create a text node
                newItem.appendChild(textnode);                    // Append the text to <li>
                mylist.removeChild(next)
                mylist.insertBefore(newItem, selected)
            }
        }
    });


    document.querySelector('#delete').addEventListener('click', function (event) {
        if(selected){
            let list = document.querySelector('#mylist')
            list.removeChild(selected)
            selected.className = ''
            
        }
        
    });

    document.querySelector('#copy').addEventListener('click', function (event) {
        if(selected){
            let list = document.querySelector('#mylist')
            let s = selected.innerHTML
            var entry = document.createElement('li');
            entry.appendChild(document.createTextNode(s))
            list.appendChild(entry);

        }
        
    });

    document.querySelector('#exclude').addEventListener('click', function (event) {
        if(selected){
            let color = selected.getAttribute("style")
            if(color == "color:grey"){

            selected.setAttribute('style', 'color:black')

            }else{

            selected.setAttribute('style', 'color:grey')

            }
        }
        
    });


    document.querySelector('#back').addEventListener('click', function (event) { 

        let pause_btn = document.querySelector('#play')
        if(pause_btn.innerHTML == "Resume"){
            ipc.send('backward_step', 'herp')
        }
    });


    document.querySelector('#forward').addEventListener('click', function (event) {
        
        let pause_btn = document.querySelector('#play')
        if(pause_btn.innerHTML == "Resume"){
            ipc.send('forward_step', 'herp')
        }
        
    });

    document.querySelector('#play').addEventListener('click', function (event) {
        
        let pause_btn = document.querySelector('#play')
        if(pause_btn.innerHTML == "Play"){
            let src = filename
            let dst = document.getElementById('dst-directory').innerHTML
            
            
            
            if(src=="Choose File"){
                alert("Add an input file")
                return
            }
            if(dst=="Choose Directory"){
                alert("Add an output directory")
                return
            }
            ipc.send('play-file', src, dst)

        }else{

            ipc.send('toggle', 'herp')
            console.log(pause_btn.value);
        }
        
        console.log('toggle');
        if(pause_btn.innerHTML == "Pause") {
            pause_btn.innerHTML = "Resume"
        } else{
            pause_btn.innerHTML = "Pause"
        }

    });

    document.querySelector('#generate').addEventListener('click', function (event) {
        let mylist = document.querySelector('#mylist')
        let list = document.querySelector('#mylist').getElementsByTagName("li")
        let arr = []
        var i
        for(i = 0; i < list.length; i++){
            let color = list[i].getAttribute("style")
            if(color == "color:grey"){
                arr.push("EX ")
            }else{
                arr.push("IN ")
            }
            arr.push(list[i].innerHTML)
        }
        let s = arr.join(' ')
        
        ipc.send('generate', s)
         
        
    });


    document.querySelector('#text_left').addEventListener('click', function (event) { 

        ipc.send('text_left', 'herp')
        
    });


    document.querySelector('#text_right').addEventListener('click', function (event) { 

        
        ipc.send('text_right', 'herp')
        
    });


    document.querySelector('#text_up').addEventListener('click', function (event) { 

        ipc.send('text_up', 'herp')
        
    });


    document.querySelector('#text_down').addEventListener('click', function (event) { 

        ipc.send('text_down', 'herp')
        
        
    });


    document.querySelector('#idT').addEventListener('click', function (event) { 

         
        ipc.send('change_up', 'herp')
        
    });

    

    document.querySelector('#text_add').addEventListener('click', function (event) {
        let src = filename
        let dst = document.getElementById('dst-directory').innerHTML
        
        if(selected){
 

        let arr = selected.innerHTML.split(" ")
        let frame_no = arr[arr.length -1]
        let text = document.getElementById('text_to_add').value
        let top = document.getElementById('idT').checked
        

        if(src=="Choose File"){
            alert("Add an input file")
            return
        }
        if(dst=="Choose Directory"){
            alert("Add an output directory")
            return
        }

        ipc.send('edit-file', src, dst, frame_no, text, top)
        ipc.send('add_text', text)

        }
    });

   



    document.querySelector('#idB').addEventListener('click', function (event) { 

        let top = document.getElementById('idT').checked
        
        ipc.send('change_down', 'herp')
    });



    return function _end() { end() }
}

function end(ipc) {
    ipc.removeListener('selected-directory')
    ipc.removeListener('selected-frile')
}

const ipc = require('electron').ipcRenderer
let end_f = start(ipc)
