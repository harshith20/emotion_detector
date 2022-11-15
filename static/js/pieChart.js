$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    var actions = $("table td:last-child").html();
    $(".add-new").click(function(){
        $(this).attr("disabled", "disabled");
        var index = $("table tbody tr:last-child").index();
        var row = '<tr>' +
            '<td><input type="text" class="form-control" name="Notes" id="text"></td>' +
        '<td>' + actions + '</td>' +
        '</tr>';
        $("table").append(row);  
          $("table tbody tr").eq(index+1).find(".add, .edit").toggle();
        $('[data-toggle="tooltip"]').tooltip();
 
    });
   
    // Add row on add button click
    $(document).on("click", ".add", function(){
        var empty = false;
        var input = $(this).parents("tr").find('input[type="text"]');
        input.each(function(){
            if(!$(this).val()){
                $(this).addClass("error");
                empty = true;
            } else{
                $(this).removeClass("error");
            }
        });
        var text = $("#text").val();
        $.post("/add", { text: text}, function(data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show();
        });
        $(this).parents("tr").find(".error").first().focus();
        if(!empty){
            input.each(function(){
                $(this).parent("td").html($(this).val());
            });   
            $(this).parents("tr").find(".add, .edit").toggle();
            $(".add-new").removeAttr("disabled");
        } 
    });
    $(document).on("click", ".delete", function(){
        $(this).parents("tr").remove();
        $(".add-new").removeAttr("disabled");
        var id = $(this).attr("id");
        var string = id;
        $.post("/delete", { string: string}, function(data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show();
        });
    });
$(document).on("click", ".update", function(){
        var id = $(this).attr("id");
        var string = id;
        var txt = $("#text").val();
        if (txt == "") {
        alert("Enter something in text box");
        }
        else{
        $.post("/edit", { string: string,text: txt}, function(data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show();
           
        });}
    });
         // Edit row on edit button click
    $(document).on("click", ".edit", function(){  
        $(this).parents("tr").find("td:not(:last-child)").each(function(i){
            if (i=='0'){
                var idname = 'text';
            }else{} 
            $(this).html('<input type="text" name="Notes" id="' + idname + '" class="form-control" value="' + $(this).text() + '">');
             
        
        });  
        $(this).parents("tr").find(".add,.update, .edit").toggle();
        $(".add-new").attr("disabled", "disabled");
        $(this).parents("tr").find(".add").removeClass("add").addClass("update"); 
        
         
    });
    
});


// for save button
