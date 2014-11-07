//foo

//make underscore templates look like django templates
_.templateSettings = {
  interpolate: /\{\{(.+?)\}\}/g
};

var editors = {};

function configureEditor(id) 
{

    console.log('configuring editor: ' + id);

    // configure ace editor
    var editor = ace.edit(id);
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");
    editor.getSession().setUseWrapMode(true);
    editor.getSession().setUseSoftTabs(true);
    editor.getSession().setNewLineMode("unix");
    editor.renderer.setShowGutter(true); 

    editors[id] = editor;

    return editor;
}



function initEditors()
{

    if($("#user-code").length)
    {
        var userCodeEditor = configureEditor("user-code");
    }

    if($("#response-editor").length)
    {
        configureEditor("response-editor");
        var mainHeight = $(window).height();
        mainHeight -= $('#top-header').height();
        mainHeight -= $('#bottom-footer').height();
        mainHeight -= 80;

        $('#response-editor').height(mainHeight);
    }

    if($("#prompt-editor").length)
    {
        var prompt = configureEditor("prompt-editor");
        console.log("configured prompt editor");
        var foo = editors["prompt-editor"];

        foo.getSession().setMode("ace/mode/markdown");   
        foo.renderer.setShowGutter(false); 

        configureEditor("solution-editor");

        $("#save-question").click(function (event) 
        {
            submitQuestion();
        });
    }
}

/**
 * Copy the from ace editor into a hidden filed to 
 * submit user-generated code
 */
function copyEditorCode(id)
{
    console.log("copying code for: " + id);
    var codeField = $("#" + id).data("codeField");
    console.log("copying into: " + codeField);
    var editor = editors[id];
    console.log("got ace editor: " + editor);
    // if(!editor)

    var code = editor.getValue();
    console.log("code: " + code);
    $("input[name=" + codeField + "]").val(code);
}


function submitQuestion(e)
{
    if(e)
        e.preventDefault();

    console.log("submitting queston");
    copyEditorCode("prompt-editor");
    copyEditorCode("solution-editor");
    $("#question-form").submit();
}

msg = function(msg, level)
{
    var html = $('#msg-li-tmpl').html();
    var tmpl = _.template(html);
    var li = tmpl({msg: msg, level: level});
    $( '#messages' ).append(li);
    $( '#messages' ).show();
}

function submitTestForm()
{
        //
    if ($( '#version' ).html() == '0')
    {
        msg("You must save your function name and prompt before adding tests.", danger);
    }
    else
    {

        var $form = $( this );
        var data = $form.serialize();   
        var url = $form.attr( "action" );

        $.post( url, data ).success(function( response ) 
        {
            if ( response.success )
            {
                $( "#test-list" ).append( response.list_append );
                msg(response.msg, response.msg_level);
                if(!response.passed)
                {
                    $('#question-panel').removeClass('panel-success').addClass('panel-danger');
                    $('#question-status-label').html('Failed')
                }
                else
                {
                    $('#question-panel').removeClass('panel-danger').addClass('panel-success');
                    $('#question-status-label').html('Passed')
                }
            }
            else
            {
                msg(response.msg, 'danger');
            }
        });
    }
}



function submitStudyCode(action)
{

    // Stop form from submitting normally
    //e.preventDefault();

    var $form = $("#response-form");
    copyEditorCode("response-editor");
    var data = $form.serialize() + "&action=" + action;   
    var url = $form.attr( "action" );

    $.post( url, data ).success(function( response ) 
    {
        $( "#test-results" ).html( response );
        editors["response-editor"].focus();
    });

}


/**
 * A client-side post-fix for the ugly diff
 * table that python provides
 */
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


function initForms()
{
    $("form").each(function()
    {
        var f = this;
        if($(f).find(".change-indicator").length > 0)
        {
            var formState = $(f).find(".change-indicator");
            var showChange = function() 
            { 
                $(formState).removeClass("label-success").addClass("label-warning");
            }
            $(f).find("select, checkbox, radio").on("change", showChange);
            $(f).find("input, select, checkbox, radio, textarea").on("input", showChange);
        }

    });

}

$( document ).ready(function() {

    var tips = $("*[data-toggle='tooltip']");
    $(tips).popover({ container: 'body', trigger: 'hover', delay: { "show": 500, "hide": 100 } });


    fixDiff();
    initEditors();
    initForms();

   //question form stuff
    $( "#test-form" ).submit(submitTestForm);
    
    if($( "#question-form" ).length)
    {

        var prompt = editors["prompt-editor"];
        var solution = editors["solution-editor"];


        _.each([prompt, solution], function(editor)
        {
            editor.commands.addCommand({
                name: "save",
                bindKey: 
                {
                    win: 'Ctrl-S',
                    mac: 'Command-S',
                    sender: 'editor|cli'
                },                
                exec: function(env, args, request) { submitQuestion(); }
            });
        });
    }


    var runUserFunction = function() {submitStudyCode("run"); return false;}
    $( "#run-code" ).click(runUserFunction);
    
    // var testUserFunction = function(e) {submitStudyCode(e, "test");}
    // $( "#test-code" ).click(testUserFunction);
    if($( "#run-code" ).length > 0)
    {
        var editor = editors["response-editor"];
        editor.focus();
        editor.gotoLine(3);

        editor.commands.addCommand({
            name: "build",
            bindKey: {win: "Ctrl-B", mac: "Command-B"},
            exec: function(editor) { runUserFunction(); }
        });

        editor.commands.addCommand({
            name: "skip",
            bindKey: {win: "Ctrl-K", mac: "Command-K"},
            exec: function(editor) { window.location = "/tutor"; }
        });

    }


    $("#question-edit-tabs a").click(function (e) {
        $(this).tab('show');
    });

    $(".form-group select, .form-group input").addClass("form-control");

    $( "#id_comment").val("");


    TableSorter.init();
    


});
