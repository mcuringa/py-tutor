//foo

//make underscore templates look like django templates
_.templateSettings = {
  interpolate: /\{\{(.+?)\}\}/g
};

var editors = Array();

function configureEditor(id) 
{
    // configure ace editor
    var editor = ace.edit(id);
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");
    editor.getSession().setUseWrapMode(true);
    editor.getSession().setUseSoftTabs(true);
    editor.getSession().setNewLineMode("unix");

    editors[id] = editor;
    return editor;
}


TableSorter = {}

TableSorter.init = function()
{

    var tables = $('.table-sortable');
    var sortableBtnTmpl = _.template($('#th-sort-tmpl').html());

    //go through each header and add a click event
    _.each(tables, function(t) 
    {
        var headers = $(t).find('th');
        _.each(headers, function(header, col) 
        {
            var data = {
                'col': col,
                'header': $(header).html()
            };

            $(header).data("sort", "desc");            
            $(header).html(sortableBtnTmpl(data));
            $(header).click(function(e) {
                TableSorter.sortTable(t, col); 
            });
        });
    });
}

TableSorter.sortTable = function(table, col)
{
    
    //$(header).data("sortDirection", "desc");
    var headers = $(table).find('th');
    var rows = $(table).find('tbody tr');
    var header = headers[col];
    var sortDirection = $(header).data("sort");

    $(headers).removeClass('active');
    $(header).addClass('active');
    $(headers).find('.desc').hide();
    $(headers).find('.asc').hide();


    var sorted = _.sortBy(rows, function(row) 
    {
        var cols = $(row).find('td');
        var html = $(cols[col]).html()
        var sortVal = $(cols[col]).data("sortVal");

        if(_.isUndefined(sortVal) || _.isNull(sortVal) || '' == sortVal)
            sortVal = html;
        
        var sortNum = parseFloat(sortVal);
        if(_.isNaN(sortNum))
        {
            return sortVal;
        }
        return sortNum;
    });

    if("desc" == sortDirection)
    {
        $(header).data("sort", "asc");
        $(header).find('.asc').show();
        $(header).find('.desc').hide();
    }
    else
    {
        sorted.reverse();
        $(header).data("sort", "desc");
        
        $(header).find('.desc').show();
        $(header).find('.asc').hide();
    }
    $(table).find('tbody').html(sorted);    

}


/**
 * Copy the from ace editor into a hidden filed to 
 * submit user-generated code
 */
function copyEditorCode(id)
{
    var codeField = $("#" + id).data("codeField");
    var editor = editors[id];
    var code = editor.getValue();
    $("input[name=" + codeField + "]").val(code);
}

function initEditors()
{

    $('.code-editor.lang-bash').each(function(i, editor) {
        var ace = configureEditor(editor);
        ace.renderer.setShowGutter(false); 
        ace.getSession().setMode("ace/mode/sh");
        ace.setTheme("ace/theme/chrome");
        
        ace.setOptions({
            readOnly: true,
            highlightActiveLine: false,
            highlightGutterLine: false
        });

        var code = $(editor).html()
        var linesOfCode = code.split("\n");
        $(editor).height((linesOfCode.length * 1.5 + 2) + "em");

    });

    if($("#user-code").length)
    {
        var userCodeEditor = configureEditor("user-code");
    }

    if($("#response-editor").length)
    {
        configureEditor("response-editor");
        $("#submit-user-code").click(function (event) 
        {
            copyEditorCode("response-editor");
            $("#response-form").submit();
        });
    }

    if($("#prompt-editor").length)
    {
        var prompt = configureEditor("prompt-editor");
        prompt.getSession().setMode("ace/mode/markdown");        
        
        configureEditor("solution-editor");

        $("#save-question").click(function (event) 
        {
            copyEditorCode("prompt-editor");
            copyEditorCode("solution-editor");
            $("#question-form").submit();
        });
    }
}

msg = function(msg, level)
{
    var html = $('#msg-li-tmpl').html();
    var tmpl = _.template(html);
    var li = tmpl({msg: msg, level: level});
    $( '#messages' ).append(li);
    $( '#messages' ).show();
}

function submitTestForm(e)
{
        //
    if ($( '#version' ).html() == '0')
    {
        e.preventDefault();
        msg("You must create a function name and prompt before adding unit tests.", danger);
    }
    else
    {
        // Stop form from submitting normally
        e.preventDefault();

        var $form = $( this );
        var data = $form.serialize();   
        var url = $form.attr( "action" );

        $.post( url, data ).success(function( response ) 
        {
            console.log(response['list_append']);
            if ( response.success )
            {
                $( "#test-list" ).append( response.list_append );
                msg(response.msg, response.msg_level);
            }
            else
            {
                msg(response.msg, 'danger');
            }
        });
    }

}





function fixDiff()
{
    var tables = $("table.diff");
    $(tables).removeAttr("cellpadding");
    $(tables).removeAttr("cellspacing");
    $(tables).removeAttr("rules");
    $(tables).addClass("table table-condensed table-bordered table-hover");
    $("table.diff colgroup").remove();
    $("table.diff td").removeAttr("nowrap");
    $("td.diff_next").remove();
}


$( document ).ready(function() {


    fixDiff();
    
    //question form stuff
    $( "#test-form" ).submit(submitTestForm);

    initEditors();


    $("#question-edit-tabs a").click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

    $("input, select").each(function(){
        $( this ).addClass("form-control");
    });

    $( "#id_comment").val("");


    TableSorter.init();



});
