$(document).ready(function() {
    $("#searchInput").keyup(function(event) {
        if (event.keyCode === 13) {
            $(".searchButton").click();
        }
    });
    $('#searchInput').on('input', function() {
        if (this.value.trim().length >= 2 || this.value.trim().length == 0) {
          $(".searchButton").click();
        }
      });
    
    $('.searchButton').on('click', function() {

        var input = $("#searchInput").val();

        req = $.ajax({
            url : '/search',
            type : 'POST',
            data : { input : input }
        });

        req.done(function(data) {
            $('#mastergrid').fadeOut(200);
            var i;
            for (i = 0; i < data.products.length; i++) { 
                if (data.category[i]=='HIDE')
                {
                    $('#search'+data.products[i]).hide();
                }
                else if (data.category[i]=='SHOW')
                {
                    $('#search'+data.products[i]).show();
                }
                
            }
            $('#mastergrid').fadeIn(200);
            console.log(data.products)

        });
    

    });

});