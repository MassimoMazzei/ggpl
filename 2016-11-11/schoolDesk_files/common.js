function floorInteri(el){ if (!el.value.test(/^[-+]?[0-9]+$/)) { el.errors.push("Inserire un numero intero (positivo o negativo)");   return false; } else {return true;}}
function floorInteriP(el){ if (!el.value.test(/^[+]?[0-9]+$/)) { el.errors.push("Interire un numero intero positivo o zero");   return false; } else {return true;}}
function floorInteriPP(el){ if (!el.value.test(/^[1-9]{1}[0-9]*$/)) { el.errors.push("Inserire un numero intero maggiore di zero");   return false; } else {return true;}}
function floorFloat(el){ if (!el.value.test(/^[-+]?[0-9]*\.?[0-9]+$/)) { el.errors.push("Inserire un numero (positivo o negativo) (usare il carattere punto per i decimali)");   return false; } else {return true;}}
function floorFloatP(el){ if (!el.value.test(/^[+]?[0-9]*\.?[0-9]+$/)) { el.errors.push("Inserire un numero positivo o zero (usare il carattere punto per i decimali)");   return false; } else {return true;}}
function floorFloatPP(el){ if (!el.value.test(/^[+]?(([1-9]{1}[0-9]*\.?[0-9]+)|([0]{1}\.{1}[0-9]+)|([1-9]{1,}))$/)) { el.errors.push("Inserire un numero maggiore di zero (usare il carattere punto per i decimali)");   return false; } else {return true;}}
function floorBool(el){ if (!el.value.test(/^[01]{0,1}$/)) { el.errors.push("Specificare sì o no");   return false; } else {return true;}}
function floorStringhe(el){ if (!el.value.test(/^[a-z0-9èéòàùì\.\,\;\:\'-_\s]+$/)) { el.errors.push("Specificare un valore");   return false; } else {return true;}}
function floorNohtml(el){ if (!el.value.test(/^[^\<^\>]+$/)) { el.errors.push("Si prega di inserire testo senza caratteri html e usando la sintassi bbcode per grassettare e commentare.");   return false; } else {return true;}}
function floorConferma(el){ if (!el.checked) { el.errors.push("E' necessario spuntare la casella di conferma");   return false; } else {return true;}}
function floorCategoria(el){ if (parseInt(el.value)<=1) { el.errors.push("E' necessario selezionare una categoria");   return false; } else {return true;}}
	

function redirect(url) { 
	location.href = url;
} 
function preferiti(){
	if (window.sidebar) window.sidebar.addPanel(document.title, location.href,'');
	else if( window.external )   window.external.AddFavorite( location.href, document.title);
	return false;
}




function form_radio(form,name,valore,base) {
	var trovato=false;
	var radio_base=false;
	$(form).getElements('input').each(function(item, index){
		if(item.getProperty('name')==name) {
			if(item.getProperty('value')==base) radio_base=item;
			if(item.getProperty('value')==valore) {item.setProperty('checked','checked');trovato=true;}
		}
	});
	if(!trovato && radio_base) {
		radio_base.setProperty('checked','checked');
	}
}
function form_select(id,valore) {
	if($(id)) {
		$(id).getElements('option').each(function(item, index){
			if(item.getProperty('value')==valore) {
				item.setProperty('selected','selected');
			}
			
		});
	}
}

function form_check(id,valore) {
	if($(id) && valore!="") $(id).setProperty('checked','checked');
}

function form_select_multiple(id,valore) {
	if($(id) && valore!='') {
		valori=valore.split(",");
		$(id).getElements('option').each(function(item, index){
			if(valori.indexOf(item.getProperty('value'))!=-1) {
				item.setProperty('selected','selected');
			}
		});
	}
}

window.addEvent('domready', function() {

	//classe che previene il click
	$$('.noclick').addEvent('click',function(evento){evento.preventDefault();});

    //menu pagina select
	$$('.modulo_invia').addEvent('change',function() {this.form.submit();});
	$$('.modulo_invia_replica').addEvent('change',function() {
		$$('.modulo_invia').set('value',this.get('value'));
		$$('.modulo_invia').fireEvent('change');
	});
	
	//segnalazione bugs
	if($('segnala')) {
		var segnala=false;
		$('segnala').addEvent('click',function (evento) {
			if(segnala) {$('segnala_box').setStyles({'height':'24px','background':'transparent','border-bottom':'0'});segnala=false;}
			else {$('segnala_box').setStyles({'height':'200px','background':'#eaeaea','border-bottom':'1px solid #252525'});segnala=true;}
		});
		$('segnala_button').addEvent('click',function (evento) {
	
			var req = new Request.HTML({url:'http://www.pulcinodoro.it/ajax/segnala.html',
				onSuccess: function(tree,el,html) {
				    if(html=="1") alert("Segnalazione memorizzata!");
				    else ("Qualcosa non va...");
				    $('segnala').fireEvent('click');
				},
				onFailure: function(error) {
				    alert(error);
				}
			}).post({'url_s':$('segnala_url').get('value'),'testo':$('segnala_testo').get('value'),'tipo':$('segnala_tipo').get('value')});
		});
	}


    
	//CALENDARI
    var date=new Array();
    $$('.data_init').each(function(data) {
        var id=data.get('id');
        //se il value dell'input non è vuoto inizializza la data
        if($(id).get('value')) var inizia=[$(id).get('value').substr(6,4),$(id).get('value').substr(3,2)-1,$(id).get('value').substr(0,2)];
        else {
            var ora= new Date();
            var inizia=false;
        }
        //se l'imput ha la classe da_ora o a_ora cambia le date minime e massime
        var adesso= new Date();
        var ora=[adesso.getFullYear(),adesso.getMonth(),adesso.getDate()]
        if($(id).hasClass('a_ora')) var d_to=ora;
        if($(id).hasClass('da_ora')) var d_from=ora;
        var hoy = new Date();
        var salidaFrom = new Date(hoy.getFullYear(),hoy.getMonth(),hoy.getDate()+7);
        salidaFrom = [salidaFrom.getFullYear(),salidaFrom.getMonth(),salidaFrom.getDate()];
        date[id]=$(id).datePicker({
            klass: "datePicker",
            format: '%d-%m-%Y',
            from: d_from,
            to:d_to,
            setInitial: true,
            initial: inizia,
            days: ["Domenica","Lunedì","Martedì","Mercoledì","Giovedì","Venerdì","Sabato"],
            draggable: true,
            position: {x:"right",y:"top"},
            offset: {x:22,y:0},
            updateElement:true,
            firstday: 1,
            onUpdate: function(){
                if($(id).get('rel')) {
                    var legato=$(id).get('rel');
                    //$(legato).set('value')
                    //recupera la prima data
                    var valore=$(id).get('value');
                    var data_1= new Date();
                    data_1.set('date',valore.substr(0,2));
                    data_1.set('month',valore.substr(3,2)-1);
                    data_1.set('year',valore.substr(6,4));
                    //recupera la seconda data
                    var valore=$(legato).get('value');
                    var data_2= new Date();
                    data_2.set('date',valore.substr(0,2));
                    data_2.set('month',valore.substr(3,2)-1);
                    data_2.set('year',valore.substr(6,4));
                    //alert(data_1.diff(data_2));
                    var giorno_dopo=data_1.clone();
                    giorno_dopo.increment('day',1);
                    if(data_1.diff(data_2)<=0) {
                        //se il datepicker del giorno dopo è gia stato inizializzato lo modifica
                        if(date[legato]){
                            date[legato].options.from=[giorno_dopo.get('year'),giorno_dopo.get('month'),giorno_dopo.get('date')];
                            date[legato].setFullDate(giorno_dopo.get('year'),giorno_dopo.get('month'),giorno_dopo.get('date'));
                            date[legato].update();
                        }
                        //altrimenti aggiorna semplicemente il value dell'input in attesa che il datepicker venga creato
                        else {
                            var risultato=giorno_dopo.format("%d-%m-%Y");
                            $(legato).set('value',risultato);
                        }
                    }
                    //aggiorna la data minima della seconda data
                    if(date[legato]){
                        date[legato].options.from=[giorno_dopo.get('year'),giorno_dopo.get('month'),giorno_dopo.get('date')];
                        date[legato].update();
                    }
                }
            }
        },"click");
        if( $(id).getNext('img'))$(id).getNext('img .ico_calendario').addEvent('click',function(evento) {date[id].show();});
       
    });


});
