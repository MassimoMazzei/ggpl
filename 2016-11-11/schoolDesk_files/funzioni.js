window.addEvent('domready', function() {




	//VETRINETTA PRODOTTI
	if($('vetrinetta')) {
		var vetrinetta_scroll = new Fx.Scroll('vetrinetta_overflow');
		var vetrinetta_ultimo=1;
		var timer=0;
		function vetrinetta_sposta(i) {
			var prodotto='vetrinetta_prodotto_'+i;
			vetrinetta_scroll.toElement(prodotto);
			$('vetrinetta_'+i).setStyle("background-position","top");
			$('vetrinetta_'+vetrinetta_ultimo).setStyle("background-position","bottom");
			vetrinetta_ultimo=i;

		}
		var vetrinetta_prossimo= function() {
			var i=vetrinetta_ultimo;
			i++;
			if(!$('vetrinetta_'+i)) i=1;
			vetrinetta_sposta(i);
		}
		timer= vetrinetta_prossimo.periodical(5000);

		$('vetrinetta_1').setStyle("background-position","top");

		var vetrinetta_menu=$('vetrinetta_menu').getElements('li');
		vetrinetta_menu.each(function(item) {
			item.addEvent('click',function () {
				var ids=this.get('id').split("_");
				var id=ids[1];
				$clear(timer);
				vetrinetta_sposta(id);
				timer= vetrinetta_prossimo.periodical(5000);
			});
		});

	}

	if($('ricerca_link') && $('ricerca')) {
		$('ricerca_link').addEvent('click',function(evento){
			evento.preventDefault();
			if($('testata').getStyle('height')=='500px')$('testata').setStyle('height','550px');
			$('ricerca').setStyle('opacity','0');
			$('ricerca').setStyle('display','block');
			$('ricerca').fade(1);
		});
	}

	//xxmod zebra su elenco prodotti nelle categorie
	$$('.elenco_prodotto:odd').each(function(div){div.setStyle('background','#fafafa');});
	//avviso carrello
	$$('.car_quantita').addEvent('change',function (evento) {
		$('car_avviso').setStyle('display','block');
	});

	//aggiungi ai desideri e avvisi via email
	$$('.servizio_prodotto').addEvent('click',function (evento) {

			evento.preventDefault();
			var servizio="";
			id_og=$('servizio_id').get('value');
			if(this.hasClass('desideri')) servizio='desideri';
			else if(this.hasClass('avvisi')) servizio='avvisi';
			var img=this.getElement('img');
			var img_url=img.getProperty('src');
			var classe=img.getProperty('class').split('_');
			var status=classe[1];
			img.setProperty('src','http://www.pulcinodoro.it/sito/it/img/servizio_caricamento.png');
			var req = new Request.HTML({url:'http://www.pulcinodoro.it/ajax/servizio_prodotto/'+id_og+'/'+servizio+'/'+status+'.html',

				onSuccess: function(resp,tree,html,js) {
					if(js) {
						//eval(js);
						img.setProperty('src',img_url);
					}
					else {
						img.setProperty('class','servizio_'+html);
						img.setStyle('opacity',0);
						img.setProperty('src','http://www.pulcinodoro.it/sito/it/img/servizio_'+servizio+'_'+html+'.png');
						img.fade(1);
					}
				},
				onFailure: function(error) {
				}
			}).post();
	});


	//rollover sui bottoni di submit
	var bottoni_submit=$$('.buttonSubmit');
	bottoni_submit.each(function (item, index) {
		item.addEvent('mouseover', function() {
			item.setProperty('class','buttonSubmitHovered');
		});
		item.addEvent('mouseout', function() {
			item.setProperty('class','buttonSubmit');
		});
	});



	$$('.tooltip').each(function (item, index) {
		var content = item.get('title').split('::');
		if(content[0])item.store('tip:title', content[0]);
		if(content[1])item.store('tip:text', content[1]);
	});
	var tipz = new Tips('.tooltip');

	//tooltip piccolo
	var tipmini=$$('.tipmini');
	tipmini.each(function (item, index) {
		item.store('tip:title','' );
		item.store('tip:text', item.get('title'));
	});
	var tipz2=new Tips(tipmini,{className:'tip_mini',fixed:true,offsets:{'x': 75, 'y': 30}});


	//sezione gestione account
	var account_check_user=true;
	//richiesta ajax sull'username
	if($('f_user') && $('accountGestisci')) {
		account_check_user=false;
		$('f_user').addEvent('blur',function () {
			if(this.get('value')!="") {
				var req = new Request.HTML({url:'http://www.pulcinodoro.it/ajax/account_check.html',
					onSuccess: function(tree,elements,html) {
						if(html=="1") {account_check_user=true; $('f_user_span').set('class','testo_verde'); $('f_user_span').set("html","&nbsp;&nbsp;<img src='http://www.pulcinodoro.it/sito/common/img/account_check_si.png' title='' alt='' style='vertical-align:middle' />&nbsp;Username valido!");}
						if(html=="2") {account_check_user=false; $('f_user_span').set('class','testo_rosso'); $('f_user_span').set("html","&nbsp;&nbsp;<img src='http://www.pulcinodoro.it/sito/common/img/account_check_no.png' title='' alt='' style='vertical-align:middle' />&nbsp;Questo username è gia utilizzato!");}

					},
					onFailure: function(error) {}
				}).get({'user':this.get('value')});

			}
		});
	}
	//richiesta ajax sulla email
	var account_check_email=true;
	if($('f_email') && $('accountGestisci')) {
		account_check_email=false;
		$('f_email').addEvent('blur',function () {
			if(this.get('value')!="") {
				var req = new Request.HTML({url:'http://www.pulcinodoro.it/ajax/account_check.html',
					onSuccess: function(tree,elements,html) {
						if(html=="1") {account_check_email=true; $('f_email_span').set('class','testo_verde'); $('f_email_span').set("html","&nbsp;&nbsp;<img src='http://www.pulcinodoro.it/sito/common/img/account_check_si.png' title='' alt='' style='vertical-align:middle' />&nbsp;Indirizzo email valido!");}
						if(html=="2") {account_check_email=false; $('f_email_span').set('class','testo_rosso'); $('f_email_span').set("html","&nbsp;&nbsp;<img src='http://www.pulcinodoro.it/sito/common/img/account_check_no.png' title='' alt='' style='vertical-align:middle' />&nbsp;Indirizzo email già registrato sul sito!");}

					},
					onFailure: function(error) {}
				}).get({'email':this.get('value')});

			}
		});
	}

	//fa sparire i box di suggerimento quando si invia il modulo
	if($('accountGestisci')) {
		$('accountGestisci').addEvent('submit',function (e) {
			if(!account_check_user) {alert("Attenzione, hai scelto un unsername già registrato al sito. Ti preghiamo di sceglierne un altro.");e.stop();}
			if(!account_check_email) {alert("L'indirizzo email specificato risulta già associato ad un account sul sito. Ti preghiamo di sceglierne un altro.");e.stop();}
			$$('.suggerimento').setStyle('display','none');
		});
	}


});
