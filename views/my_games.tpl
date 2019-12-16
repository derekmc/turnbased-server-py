<!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/basic.css">
    <script>
      window.onload = function(){
        render_list(document.getElementById("main"), game_list);
      }
      var game_list = {{!game_list}};
      //alert(game_list)
      //document.write(JSON.stringify(game_list));
      function elem(container, tag, props){
        var el = document.createElement(tag);
        for(var k in props){
          var val = props[k];
          if(k == 'style'){
            for(var k2 in val){
              el.style[k2] = val[k2]; }}
          else if(k == 'html'){
            el.innerHTML = val; }
          else if(k == 'text'){
            el.appendChild(document.createTextNode(val)); }
          else{
            el[k] = val; }}
        if(container) container.appendChild(el);
        return el;
      }
      function render_list(container, list){
        console.log('render_list', list);
        var table = elem(container, 'table');
        var tr = elem(table, 'tr');
        elem(tr, 'th', {text: 'Game Id'});
        elem(tr, 'th', {text: 'Type'});
        elem(tr, 'th', {text: 'Players'});
        for(var i=0; i<list.length; ++i){
          var game = list[i];
          var min_players = game.min_players;
          var max_players = game.max_players;
         
          var tr = elem(table, 'tr');
          var link_href = '/game/' + game.id + (game.status.is_started? '/textplay' : '/lobby');
          elem(elem(tr, 'td'), 'a', {href: link_href, text: game.id});
          elem(tr, 'td', {text: game.paradigm});
          elem(tr, 'td', {text: min_players == max_players? min_players : min_players + " - " + max_players});
        }
      }
    </script>
  </head>
  <body>
    % include('nav.tpl')
    <h1> My Games (TODO) </h1>
    <div id="main"></div>
  </body>
</html>
