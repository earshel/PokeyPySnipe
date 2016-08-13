//laod pokemondata

var pokemonMapping = [];

$.ajax('static/pokemondata.json')
    .then(function(data) {
        data.forEach(function(element) {
            pokemonMapping[element.Name.toLowerCase()] = parseInt(element.Number, 10);
        }, this);
    });

function loadSnipable() {
    $.ajax('http://pokesniper.org/api.php')
        .then(function(data) {
            data = $.parseJSON(data);
            var collection = $('<ul class="collection"></ul>');
            data.forEach(function(element) {
                var item = $('<li class="collection-item avatar"></li>');
                var pokeNum = pokemonMapping[element.name.toLowerCase()];
                item.append(
                    $('<img/>').attr('src', 'static/avatars/' + pokeNum + '.png')
                );
                item.append(
                    $('<span class="title"></span>').text(element.name)
                );
                item.append(
                    $('<p/>').text(element.coords + '\nIV: ' + element.iv)
                );
                item.append(
                    $('<a class="secondary-content snipe-btn" />')
                    .append($('<i class="material-icons" />').text('send'))
                    .attr('data-coords', element.coords)
                    .attr('data-name', element.name)
                );
                collection.append(item);
            }, this);
            console.log(collection);
            $('#snipable').html(collection);
            $('a.snipe-btn').click(function(e) {
                $('input#snipecoords').val($(this).attr('data-coords'));
                $('input#pokemonName').val($(this).attr('data-name'));
                updateStatus();
                $('form').submit();
            })
        });
}

loadSnipable();
setTimeout(loadSnipable(), 10000);