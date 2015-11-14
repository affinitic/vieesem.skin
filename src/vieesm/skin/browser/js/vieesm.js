/*recherche sur la table periodique*/
$(document).ready(function(){

  $(function() {
    $("#periodique-titre").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "periodique-searchJSON",
                dataType: "json",
                data: {
                    featureClass: "P",
                    style: "full",
                    maxRows: 12,
                    name_startsWith: request.term
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item,
                            value: item
                        }
                    }));
                }
            });
        },
        minLength: 2,
        open: function() {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function() {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        }
    });
});
});


/*recherche sur la table livre > titre livre*/
$(document).ready(function(){

  $(function() {
    $("#livre-titre").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "livre-titre-searchJSON",
                dataType: "json",
                data: {
                    featureClass: "P",
                    style: "full",
                    maxRows: 12,
                    name_startsWith: request.term
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item,
                            value: item
                        }
                    }));
                }
            });
        },
        minLength: 2,
        open: function() {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function() {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        }
    });
});
});

/*recherche sur la table livre > mots-cles livre*/
$(document).ready(function(){

  $(function() {
    $("#mot-cle").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "livre-motcle-searchJSON",
                dataType: "json",
                data: {
                    featureClass: "P",
                    style: "full",
                    maxRows: 12,
                    name_startsWith: request.term
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item,
                            value: item
                        }
                    }));
                }
            });
        },
        minLength: 2,
        open: function() {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function() {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        }
    });
});
});



/*recherche sur la table affiche*/
$(document).ready(function(){

  $(function() {
    $("#affiche-titre").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "affiche-searchJSON",
                dataType: "json",
                data: {
                    featureClass: "P",
                    style: "full",
                    maxRows: 12,
                    name_startsWith: request.term
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item,
                            value: item
                        }
                    }));
                }
            });
        },
        minLength: 2,
        open: function() {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function() {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        }
    });
});
});


/*recherche sur la table auteur*/
$(document).ready(function(){

  $(function() {
    $(".auteur-nom").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "auteur-searchJSON",
                dataType: "json",
                data: {
                    featureClass: "P",
                    style: "full",
                    maxRows: 12,
                    name_startsWith: request.term
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item,
                            value: item
                        }
                    }));
                }
            });
        },
        minLength: 2,
        open: function() {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function() {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        }
    });
});
});


/*recherche sur la table formation*/
$(document).ready(function(){

  $(function() {
    $("#formation-titre").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "formation-searchJSON",
                dataType: "json",
                data: {
                    featureClass: "P",
                    style: "full",
                    maxRows: 12,
                    name_startsWith: request.term
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item,
                            value: item
                        }
                    }));
                }
            });
        },
        minLength: 2,
        open: function() {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function() {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        }
    });
});
});


/*recherche sur la table formation inscription*/
$(document).ready(function(){

  $(function() {
    $("#formation-nom-inscrit").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "inscription-searchJSON",
                dataType: "json",
                data: {
                    featureClass: "P",
                    style: "full",
                    maxRows: 12,
                    name_startsWith: request.term
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item,
                            value: item
                        }
                    }));
                }
            });
        },
        minLength: 2,
        open: function() {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function() {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        }
    });
});
});


/* LiveSearch filtre sur les addRemoveWidget */
$(document).ready(function(){

$('[name="add_remove_widget_input_livesearch"]').each(function() {
    var elem = $(this);

    // Save current value of element
    elem.data('oldVal', elem.val());

    // Look for changes in the value
    elem.bind("propertychange keyup input paste", function(event){
        // If value has changed...
        if (elem.data('oldVal') != elem.val()) {

            // Updated stored value
            elem.data('oldVal', elem.val());

            // Filter in the fromBox
            var originalListName = elem.attr('id') + '_original_list:list';
            var originalList = $('[name="' + originalListName + '"]');

            // Clear fromBox
            var fromBoxId = elem.attr('from_box');
            var fromBox = $('#'+fromBoxId);
            fromBox.empty();

            // Compare search filter string to each value of original list
            originalList.each(function() {
                var fromBoxId = elem.attr('from_box');
                var toBoxId = elem.attr('to_box');
                var filteredFromList = [];

                var item = $(this);
                // Check to compare the search filter to the original list
                if (item.val().toUpperCase().indexOf(elem.val().toUpperCase()) > -1
                        || elem.val() === '')
                {
                    // Check if option is not in toBox
                    if ($('#' + toBoxId + ' option[value="' + item.attr('key') +'"]').length <= 0)
                    {
                        // Add the option in fromBox
                        optionHtml = '<option value="' + item.attr('key') +'">' + item.val() + '</option>';
                        $('#'+fromBoxId).append($(optionHtml));
                    }
                }
            });

        }
    });
});
});
