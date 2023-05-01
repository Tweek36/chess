$('.modal, .modal-overlay').hide()
$('.modal-overlay, .modal-close').click(function(){
    $('.modal, .modal-overlay').hide()
})



$('.add_player').click(function(){
    clone = $('.modal-field:has(.player)').last().clone()
    clone.children('.player').val('')
    clone.children('.repeat_player').val(1)
    $('.fields-list').append(clone)
})

$('#palyers').click(function(){
    $('#add_players.modal, .modal-overlay').show()
})

$('#competition').click(function(){
    $('#add_competition.modal, .modal-overlay').show()
})

$('#add_competition.modal').find('#submit').click(function(){
    let players = $(this).parent().find('#players_select').val()
    let data = {'players':JSON.stringify(players)}
    $('.modal, .modal-overlay').hide()
    $.ajaxSetup({
        headers: {
          "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    })
    $.ajax({
        method: 'GET',
        data: data,
        dataType: 'json',
        url: 'add_competition_ajax',
        success: function(response){
            location.reload();
        }
    });
})

$('#players_select').change(function(){
    let log = Math.log2($(this).val().length)
    $('#palyers_amount').text($(this).val().length).attr('acceptable', log%Math.round(log)==0)
    if(log%Math.round(log)==0){
        $(this).parent().parent().find('#submit').removeAttr('disabled')
    } else {
        $(this).parent().parent().find('#submit').attr('disabled', '')
    }
})

$('#add_players.modal').find('#submit').click(function(){
    $('.modal, .modal-overlay').hide()
    let data = {'names':[],'repeats':[]}
    let all_filds = $(this).parent().find('.modal-field')
    data['names'] = $('.modal-field .player').map(function() {return this.value}).toArray()
    data['repeats'] = $('.modal-field .repeat_player').map(function() {return this.value}).toArray()
    console.log(data)
    $.ajaxSetup({
        headers: {
          "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    })
    $.ajax({
        method: 'POST',
        data: data,
        dataType: 'json',
        url: 'add_player_ajax'
    });
})