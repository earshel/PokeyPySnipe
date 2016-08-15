//laod pokemondata

function loadSnipable() {
    $.ajax('http://pokesnipers.com/api/v1/pokemon.json')
        .then(function(data) {
            data = data.results;
            var collection = $('<ul class="collection"></ul>');
            data.forEach(function(element) {
                var item = $('<li class="collection-item avatar"></li>');
                item.append(
                    $('<img/>').attr('src', 'static/pogoico/' + element.name + '.png')
                );
                item.append(
                    $('<span class="title"></span>').text(element.name)
                );
                item.append(
                    $('<p/>').text(element.coords + '\nIV: ' + element.iv)
                );
                item.append(
                    $('<a class="secondary-content snipe-btn" />')
                    .append($('<a class="btn-floating btn-large waves-effect waves-light red"></a>').text('--GO--'))
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
            });
        });
}

loadSnipable();
setTimeout(loadSnipable(), 10000);